"""
Performance monitoring and metrics collection utilities.
"""
import time
import psutil
import functools
from typing import Dict, Any, Callable, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import json
from pathlib import Path


@dataclass
class PerformanceMetrics:
    """Container for performance metrics."""
    function_name: str
    execution_time: float
    cpu_percent: float
    memory_mb: float
    timestamp: str
    success: bool
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary."""
        return asdict(self)


class PerformanceMonitor:
    """
    Performance monitoring class for tracking application metrics.

    Usage:
        monitor = PerformanceMonitor()
        metrics = monitor.record_metrics("function_name", execution_time)
    """

    def __init__(self, metrics_file: str = "logs/performance_metrics.jsonl"):
        """
        Initialize performance monitor.

        Args:
            metrics_file: Path to store metrics (JSONL format)
        """
        self.metrics_file = Path(metrics_file)
        self.metrics_file.parent.mkdir(parents=True, exist_ok=True)
        self.process = psutil.Process()

    def record_metrics(
        self,
        function_name: str,
        execution_time: float,
        success: bool = True,
        error: Optional[str] = None
    ) -> PerformanceMetrics:
        """
        Record performance metrics for a function call.

        Args:
            function_name: Name of the function
            execution_time: Time taken to execute (seconds)
            success: Whether execution was successful
            error: Error message if any

        Returns:
            PerformanceMetrics object
        """
        metrics = PerformanceMetrics(
            function_name=function_name,
            execution_time=execution_time,
            cpu_percent=self.process.cpu_percent(),
            memory_mb=self.process.memory_info().rss / 1024 / 1024,
            timestamp=datetime.now().isoformat(),
            success=success,
            error=error
        )

        # Append to metrics file
        with open(self.metrics_file, 'a') as f:
            json.dump(metrics.to_dict(), f)
            f.write('\n')

        return metrics

    def get_system_metrics(self) -> Dict[str, Any]:
        """
        Get current system-wide metrics.

        Returns:
            Dictionary of system metrics
        """
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "memory_available_mb": psutil.virtual_memory().available / 1024 / 1024,
            "disk_usage_percent": psutil.disk_usage('/').percent,
            "timestamp": datetime.now().isoformat()
        }


# Global monitor instance
_monitor = PerformanceMonitor()


def monitor_performance(func: Callable) -> Callable:
    """
    Decorator to monitor function performance.

    Usage:
        @monitor_performance
        def my_function():
            # ... function code ...
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        error = None
        success = True

        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            success = False
            error = str(e)
            raise
        finally:
            execution_time = time.time() - start_time
            _monitor.record_metrics(
                function_name=func.__name__,
                execution_time=execution_time,
                success=success,
                error=error
            )

    return wrapper


def get_cache_stats(cache) -> Dict[str, Any]:
    """
    Get statistics for an LRU cache.

    Args:
        cache: LRUCache or functools.lru_cache instance

    Returns:
        Dictionary of cache statistics
    """
    if hasattr(cache, 'cache_info'):
        # functools.lru_cache
        info = cache.cache_info()
        return {
            "hits": info.hits,
            "misses": info.misses,
            "maxsize": info.maxsize,
            "currsize": info.currsize,
            "hit_rate": info.hits / (info.hits + info.misses) if (info.hits + info.misses) > 0 else 0
        }
    elif hasattr(cache, 'currsize'):
        # cachetools.LRUCache
        return {
            "maxsize": cache.maxsize,
            "currsize": cache.currsize,
            "hit_rate": "N/A (use functools.lru_cache for hit tracking)"
        }
    else:
        return {"error": "Unknown cache type"}


class MetricsCollector:
    """
    Collect and aggregate performance metrics.

    Usage:
        collector = MetricsCollector()
        summary = collector.get_summary()
    """

    def __init__(self, metrics_file: str = "logs/performance_metrics.jsonl"):
        """
        Initialize metrics collector.

        Args:
            metrics_file: Path to metrics file
        """
        self.metrics_file = Path(metrics_file)

    def load_metrics(self) -> list[PerformanceMetrics]:
        """
        Load all metrics from file.

        Returns:
            List of PerformanceMetrics objects
        """
        metrics = []
        if not self.metrics_file.exists():
            return metrics

        with open(self.metrics_file, 'r') as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    metrics.append(PerformanceMetrics(**data))

        return metrics

    def get_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics of all metrics.

        Returns:
            Dictionary with aggregated statistics
        """
        metrics = self.load_metrics()
        if not metrics:
            return {"error": "No metrics available"}

        execution_times = [m.execution_time for m in metrics]
        cpu_percents = [m.cpu_percent for m in metrics]
        memory_mbs = [m.memory_mb for m in metrics]
        success_count = sum(1 for m in metrics if m.success)

        return {
            "total_calls": len(metrics),
            "successful_calls": success_count,
            "failed_calls": len(metrics) - success_count,
            "success_rate": success_count / len(metrics),
            "execution_time": {
                "avg": sum(execution_times) / len(execution_times),
                "min": min(execution_times),
                "max": max(execution_times),
                "total": sum(execution_times)
            },
            "cpu_percent": {
                "avg": sum(cpu_percents) / len(cpu_percents),
                "max": max(cpu_percents)
            },
            "memory_mb": {
                "avg": sum(memory_mbs) / len(memory_mbs),
                "max": max(memory_mbs)
            }
        }

    def get_function_stats(self, function_name: str) -> Dict[str, Any]:
        """
        Get statistics for a specific function.

        Args:
            function_name: Name of the function

        Returns:
            Dictionary with function-specific statistics
        """
        metrics = [m for m in self.load_metrics() if m.function_name == function_name]
        if not metrics:
            return {"error": f"No metrics found for {function_name}"}

        execution_times = [m.execution_time for m in metrics]

        return {
            "function": function_name,
            "total_calls": len(metrics),
            "successful_calls": sum(1 for m in metrics if m.success),
            "avg_execution_time": sum(execution_times) / len(execution_times),
            "min_execution_time": min(execution_times),
            "max_execution_time": max(execution_times)
        }
