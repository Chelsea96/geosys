from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class GeoOptimizationResult:
    # 统一使用 original_content 解决 UI 报错
    original_content: str 
    optimized_text: str
    suggestions: List[str] = field(default_factory=list)
    info_density: float = 0.0
    authority_score: float = 0.0
    alignment_score: float = 0.0
    structure_score: float = 0.0
    transparency_data: Dict[str, Any] = field(default_factory=dict)
    schema_markup: Optional[str] = None
    citation_urls: List[str] = field(default_factory=list)