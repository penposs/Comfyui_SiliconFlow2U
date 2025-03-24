from .nodes import SiliconFlowNode, SiliconFlowVideoNode

NODE_CLASS_MAPPINGS = {
    "SiliconFlowNode": SiliconFlowNode,
    "SiliconFlowVideoNode": SiliconFlowVideoNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SiliconFlowNode": "硅基流动2U",
    "SiliconFlowVideoNode": "硅基流动视频生成API"
}

__version__ = "1.0.0"