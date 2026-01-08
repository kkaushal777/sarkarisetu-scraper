"""Scrapers module for SarkariSetu."""
from .base import BaseScraper
from .aggregator import AggregatorScraper
from .recruitment import RecruitmentScraper

__all__ = [
    'BaseScraper',
    'AggregatorScraper',
    'RecruitmentScraper',
]
