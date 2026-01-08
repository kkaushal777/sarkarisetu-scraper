"""Data models for SarkariSetu scraper."""
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import json


class PageType(str, Enum):
    """Enum for page types"""
    RECRUITMENT = "recruitment"
    RESULT = "result"
    ADMIT_CARD = "admit_card"
    ANSWER_KEY = "answer_key"
    EXAM_CALENDAR = "exam_calendar"
    EXAM_CITY_DETAILS = "exam_city_details"
    AGGREGATOR_JOBS = "aggregator_jobs"
    AGGREGATOR_ADMIT_CARD = "aggregator_admit_card"
    AGGREGATOR_RESULT = "aggregator_result"
    AGGREGATOR_ANSWER_KEY = "aggregator_answer_key"


@dataclass
class Link:
    """Hyperlink model"""
    label: str
    url: str
    kind: Optional[str] = None
    
    def to_dict(self):
        return asdict(self)


@dataclass
class KVDate:
    """Key-value pair with optional date parsing"""
    key: str
    value_text: str
    value_iso: Optional[str] = None
    
    def to_dict(self):
        return asdict(self)


@dataclass
class FeeLine:
    """Application fee entry"""
    category: str
    amount_text: str
    currency: Optional[str] = "INR"
    amount_value: Optional[float] = None
    notes: Optional[str] = None
    
    def to_dict(self):
        return asdict(self)


@dataclass
class Vacancy:
    """Job vacancy entry"""
    post_name: str
    count_text: str
    count: Optional[int] = None
    category: Optional[str] = None
    
    def to_dict(self):
        return asdict(self)


@dataclass
class AggregatorItem:
    """Single item from aggregator list"""
    rank: int
    title: str
    link: str
    metadata_type: Optional[str] = None
    metadata_value: Optional[str] = None
    metadata_text: Optional[str] = None
    status_text: Optional[str] = None
    
    def to_dict(self):
        return asdict(self)


@dataclass
class AggregatorRecord:
    """Aggregator listing page (jobs, results, admit cards, answer keys)"""
    page_type: str
    source_url: str
    fetched_at: str
    http_status: int
    title: Optional[str] = None
    description: Optional[str] = None
    items: List[AggregatorItem] = field(default_factory=list)
    has_pagination: bool = False
    
    def to_dict(self):
        return {
            **asdict(self),
            'items': [i.to_dict() for i in self.items]
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, default=str)


@dataclass
class RecruitmentDetail:
    """Recruitment page detail"""
    page_type: str = PageType.RECRUITMENT
    source_url: str = ""
    fetched_at: str = ""
    title: Optional[str] = None
    organization: Optional[str] = None
    advt_no: Optional[str] = None
    exam_name: Optional[str] = None
    total_posts: Optional[int] = None
    
    vacancies: List[Vacancy] = field(default_factory=list)
    important_dates: List[KVDate] = field(default_factory=list)
    application_fee: List[FeeLine] = field(default_factory=list)
    age_limits: List[Dict] = field(default_factory=list)
    eligibility: List[Dict] = field(default_factory=list)
    mode_of_selection: List[str] = field(default_factory=list)
    useful_links: List[Link] = field(default_factory=list)
    
    def to_dict(self):
        return {
            **asdict(self),
            'vacancies': [v.to_dict() for v in self.vacancies],
            'important_dates': [d.to_dict() for d in self.important_dates],
            'application_fee': [f.to_dict() for f in self.application_fee],
            'useful_links': [l.to_dict() for l in self.useful_links],
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, default=str)
