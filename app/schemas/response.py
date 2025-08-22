from pydantic import BaseModel
from typing import List, Optional

class TreeNode(BaseModel):
    label: str
    href: Optional[str] = None
    children: List["TreeNode"] = []

TreeNode.update_forward_refs()


class TreeResponse(BaseModel):
    url: str
    clicked: int
    tree: List[TreeNode] | TreeNode
