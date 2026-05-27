"""
gRPC Client Factory for AI Platform

This module provides a factory for creating gRPC clients for various AI Platform services
with built-in connection pooling, retry logic, and error handling.
"""

import grpc
from grpc import aio as grpc_aio
from typing import Optional, Dict, Any, Callable
import logging
import asyncio

from .channel import ChannelManager, ChannelConfig, create_channel

logger = logging.getLogger(__name__)


class ClientFactory:
    """
    Factory for creating gRPC clients with automatic connection management.
    
    This factory manages connection pooling and reuse across multiple client instances.
    """
    
    def __init__(self):
        """Initialize client factory."""
        self._channel_managers: Dict[str, ChannelManager] = {}
        self._lock = asyncio.Lock()
    
    async def get_channel_manager(
        self,
        service_name: str,
        target: str,
        **kwargs
    ) -> ChannelManager:
        """
        Get or create a channel manager for a service.
        
        Args:
            service_name: Name of the service
            target: Target address (e.g., "localhost:50051")
            **kwargs: Additional channel configuration
            
        Returns:
            Channel manager for the service
        """
        async with self._lock:
            if service_name not in self._channel_managers:
                config = ChannelConfig(target, **kwargs)
                self._channel_managers[service_name] = ChannelManager(config)
                logger.info(f"Created channel manager for {service_name} at {target}")
            
            return self._channel_managers[service_name]
    
    async def create_client(
        self,
        service_name: str,
        client_class: type,
        target: str,
        auth_token: Optional[str] = None,
        token_provider: Optional[Callable[[], str]] = None,
        **kwargs
    ) -> Any:
        """
        Create a gRPC client for a service.
        
        Args:
            service_name: Name of the service
            client_class: gRPC client class (generated stub)
            target: Target address (e.g., "localhost:50051")
            auth_token: Static auth token
            token_provider: Callable that returns auth token
            **kwargs: Additional channel configuration
            
        Returns:
            Configured gRPC client instance
        """
        channel_manager = await self.get_channel_manager(service_name, target, **kwargs)
        channel = await channel_manager.get_channel()
        
        # Create client with channel
        client = client_class(channel)
        
        logger.info(f"Created {service_name} client for {target}")
        return client
    
    async def close_all(self):
        """Close all managed channels."""
        async with self._lock:
            for service_name, manager in self._channel_managers.items():
                await manager.close()
                logger.info(f"Closed channel for {service_name}")
            
            self._channel_managers.clear()


# Global client factory instance
_global_factory: Optional[ClientFactory] = None
_factory_lock = asyncio.Lock()


async def get_client_factory() -> ClientFactory:
    """
    Get the global client factory instance.
    
    Returns:
        Global client factory
    """
    global _global_factory
    
    async with _factory_lock:
        if _global_factory is None:
            _global_factory = ClientFactory()
        
        return _global_factory


async def create_service_client(
    service_name: str,
    client_class: type,
    target: str,
    auth_token: Optional[str] = None,
    token_provider: Optional[Callable[[], str]] = None,
    **kwargs
) -> Any:
    """
    Convenience function to create a service client using the global factory.
    
    Args:
        service_name: Name of the service
        client_class: gRPC client class (generated stub)
        target: Target address (e.g., "localhost:50051")
        auth_token: Static auth token
        token_provider: Callable that returns auth token
        **kwargs: Additional channel configuration
        
    Returns:
        Configured gRPC client instance
    """
    factory = await get_client_factory()
    return await factory.create_client(
        service_name=service_name,
        client_class=client_class,
        target=target,
        auth_token=auth_token,
        token_provider=token_provider,
        **kwargs
    )


class ServiceConfig:
    """Configuration for AI Platform services."""
    
    # Default service addresses (can be overridden)
    SERVICES = {
        "parser": "localhost:8001",
        "gateway": "localhost:8002",
        "semantic-chunk": "localhost:8003",
        "metadata": "localhost:8004",
        "embedding": "localhost:8005",
        "retrieval": "localhost:8006",
        "generation": "localhost:8007",
        "audit": "localhost:8008",
        "moderation": "localhost:8009",
        "reranking": "localhost:8010",
        "vision": "localhost:8011",
        "monitoring": "localhost:8012",
    }
    
    @classmethod
    def get_address(cls, service_name: str, env: str = "dev") -> str:
        """
        Get the address for a service.
        
        Args:
            service_name: Name of the service
            env: Environment (dev, staging, production)
            
        Returns:
            Service address
        """
        # In production, you might want to use service discovery
        # For now, return the default address
        return cls.SERVICES.get(service_name, f"localhost:{service_name}")
    
    @classmethod
    def set_address(cls, service_name: str, address: str):
        """
        Set a custom address for a service.
        
        Args:
            service_name: Name of the service
            address: Service address
        """
        cls.SERVICES[service_name] = address


async def close_all_connections():
    """Close all gRPC connections managed by the global factory."""
    global _global_factory
    
    if _global_factory:
        await _global_factory.close_all()