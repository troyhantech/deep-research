class Response:
    noToolUse = "[Error] You did not use any tool in previous response! Please retry with a tool use."

    partialToolUse = "[Error] The tool use is not complete! Please check previous response and retry with a complete tool use. Possible reasons: 1. Ensure the tool format is correct(tool_name, params, and tag close). 2. Maybe the output content too long, causing the output to be truncated."
    noMoreReasoningTimes = "[URGENT AND MANDATORY] Only one tool call opportunity remains! Must generate the report based on the available information and deliver it directly."

    @staticmethod
    def missingParam(tool_name: str, params: list[str]) -> str:
        return f"[Error] The tool {tool_name} is missing params {', '.join(params)}! Please retry with correct format."

    @staticmethod
    def failedToCallModel(err_msg: str) -> str:
        return f"[Error] Failed to call model. Please try again later. Error message: {err_msg}."
