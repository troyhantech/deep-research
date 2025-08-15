from typing import Dict, List, Literal, Optional, TypedDict, Union


class TextContent(TypedDict):
    type: Literal["text"]
    content: str
    partial: bool


class ToolUse(TypedDict):
    type: Literal["tool_use"]
    name: str
    params: Dict[str, str]
    partial: bool  # tool name xml tag is closed


ToolContent = Union[TextContent, ToolUse]


def parse_xml_tool_content(
    tool_content: str, tool_names: List[str], tool_params_names: List[str]
) -> List[ToolContent]:
    content_blocks: List[ToolContent] = []
    current_text_content: Optional[TextContent] = None
    current_text_content_start_index = 0
    current_tool_use: Optional[ToolUse] = None
    current_tool_use_start_index = 0
    current_param_name: Optional[str] = None
    current_param_value_start_index = 0
    accumulator = ""

    for i, char in enumerate(tool_content):
        accumulator += char

        # there should be no param without tool use
        if current_tool_use and current_param_name:
            current_param_value = accumulator[current_param_value_start_index:]
            param_closing_tag = f"</{current_param_name}>"
            if current_param_value.endswith(param_closing_tag):
                # param value ends
                current_tool_use["params"][current_param_name] = current_param_value[
                    : -len(param_closing_tag)
                ]
                current_param_name = None
                continue
            else:
                # param value is accumulating
                continue

        # there is no current param name

        if current_tool_use:
            current_tool_value = accumulator[current_tool_use_start_index:]
            tool_use_closing_tag = f"</{current_tool_use['name']}>"
            if current_tool_value.endswith(tool_use_closing_tag):
                # tool use ends
                current_tool_use["partial"] = False
                content_blocks.append(current_tool_use)
                current_tool_use = None
                continue
            else:
                possible_param_opening_tags = [
                    f"<{name}>" for name in tool_params_names
                ]
                for param_opening_tag in possible_param_opening_tags:
                    if accumulator.endswith(param_opening_tag):
                        # start new param
                        current_param_name = param_opening_tag[1:-1]
                        current_param_value_start_index = len(accumulator)
                        break

                # write_to_file's special case, file content may contain end tag
                content_param_name = "content"
                if current_tool_use["name"] == "write_to_file" and accumulator.endswith(
                    f"</{content_param_name}>"
                ):
                    tool_content = accumulator[current_tool_use_start_index:]
                    content_start_tag = f"<{content_param_name}>"
                    content_end_tag = f"</{content_param_name}>"
                    content_start_index = tool_content.find(content_start_tag) + len(
                        content_start_tag
                    )
                    content_end_index = tool_content.rindex(content_end_tag)
                    if (
                        content_start_index != -1
                        and content_end_index != -1
                        and content_end_index > content_start_index
                    ):
                        current_tool_use["params"][content_param_name] = tool_content[
                            content_start_index:content_end_index
                        ]

                # tool value is accumulating
                continue

        # there is no current tool use

        did_start_tool_use = False
        possible_tool_use_opening_tags = [f"<{name}>" for name in tool_names]
        for tool_use_opening_tag in possible_tool_use_opening_tags:
            if accumulator.endswith(tool_use_opening_tag):
                # start new tool use
                current_tool_use = {
                    "type": "tool_use",
                    "name": tool_use_opening_tag[1:-1],
                    "params": {},
                    "partial": True,
                }
                current_tool_use_start_index = len(accumulator)
                # start new tool use, save current text content first
                if current_text_content:
                    # remove partial tool use tag from text content
                    current_text_content["content"] = current_text_content["content"][
                        : -len(tool_use_opening_tag[:-1])
                    ].strip()
                    if current_text_content["content"]:
                        current_text_content["partial"] = False
                        content_blocks.append(current_text_content)
                current_text_content = None

                did_start_tool_use = True
                break

        if not did_start_tool_use:
            # there is no tool use, so it must be start or text between tools
            if current_text_content is None:
                current_text_content_start_index = i
            current_text_content = {
                "type": "text",
                "content": accumulator[current_text_content_start_index:].strip(),
                "partial": False,
            }

    if current_tool_use:
        # tool call is not completed, add as partial content
        if current_param_name:
            # tool call has incomplete params
            current_tool_use["params"][current_param_name] = accumulator[
                current_param_value_start_index:
            ]
        # only add tool use when there is param or content
        if current_tool_use["params"]:
            content_blocks.append(current_tool_use)

    if current_text_content:
        # text content is not completed, add as partial content
        content_blocks.append(current_text_content)

    return content_blocks
