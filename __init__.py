from .nodes import SiliconFlowNode, SiliconFlowVideoNode, SiliconFlowUploadNode, SiliconFlowRefreshModelsNode, SiliconFlowListModelsNode

NODE_CLASS_MAPPINGS = {
    "SiliconFlowNode": SiliconFlowNode,
    "SiliconFlowVideoNode": SiliconFlowVideoNode,
    "SiliconFlowUploadNode": SiliconFlowUploadNode,
    "SiliconFlowRefreshModelsNode": SiliconFlowRefreshModelsNode,
    "SiliconFlowListModelsNode": SiliconFlowListModelsNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SiliconFlowNode": "硅基流动2U",
    "SiliconFlowVideoNode": "硅基流动视频生成API",
    "SiliconFlowUploadNode": "硅基流动文件上传",
    "SiliconFlowRefreshModelsNode": "硅基流动刷新模型列表",
    "SiliconFlowListModelsNode": "硅基流动查看模型列表"
}

__version__ = "1.0.0"