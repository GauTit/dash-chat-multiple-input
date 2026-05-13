# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args

ComponentSingleType = typing.Union[str, int, float, Component, None]
ComponentType = typing.Union[
    ComponentSingleType,
    typing.Sequence[ComponentSingleType],
]

NumberType = typing.Union[
    typing.SupportsFloat, typing.SupportsInt, typing.SupportsComplex
]


class ChatComponentMulti(Component):
    """A ChatComponentMulti component.
ChatComponentMulti - A React-based chat interface with customizable styles and typing indicators.
* This component provides a chat interface with support for:
- Displaying messages exchanged between 2 users typically a user and an assistant.
- Customizable themes and styles for the chat UI.
- Typing indicators for both the user and assistant.
- Integration with Dash via the `setProps` callback for state management.

Keyword arguments:

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- assistant_bubble_style (dict; optional):
    Css styles to customize the assistant message bubble.

- class_name (string; default ""):
    Name for the class attribute to be added to the chat container.

- container_style (dict; optional):
    Inline css styles to customize the chat container.

- file_attachment_button_config (dict; default {    show: True,    label: "Attach File",    icon: "paperclip",    icon_position: "only",    style: {},    className: "",}):
    Configuration for the file attachment button in the input field.
    Allows customization of appearance and behavior.

    `file_attachment_button_config` is a dict with keys:

    - show (boolean; optional)

    - label (string; optional)

    - icon (a value equal to: "paper-plane-horizontal", "paper-plane", "folder", "file", "paperclip"; optional)

    - icon_position (a value equal to: "left", "right", "only"; optional)

    - style (dict; optional)

    - className (string; optional)

- fill_height (boolean; default True):
    Whether to vertically fill the screen with the chat container. If
    False, centers and constrains container to a maximum height.

- fill_width (boolean; default True):
    Whether to horizontally fill the screen with the chat container.
    If False, centers and constrains container to a maximum width.

- input_container_style (dict; optional):
    Inline styles for the container holding the message input field.

- input_placeholder (string; default ""):
    Placeholder input to bne used in the input field.

- input_text_style (dict; optional):
    Inline styles for the message input field itself.

- messages (list of dicts; optional):
    An array of options. The list of chat messages. Each message
    object should have:    - `role` (string): The message sender,
    either \"user\" or \"assistant\".    - `content`: The content of
    the message.

    `messages` is a list of dicts with keys:

    - role (a value equal to: "user", "assistant"; required)

    - content (list of dicts; required)

        `content` is a list of dicts with keys:

        - type (a value equal to: "text", "attachment", "table", "graph"; required)

        - props (dict; optional) | dict | string | dict

- new_message (dict; optional):
    Latest chat message that was appended to messages array.

- persistence (boolean; default False):
    Whether messages should be stored for persistence.

- persistence_type (a value equal to: "local", "session"; default "local"):
    Where persisted messages will be stored.

- send_button_config (dict; default {    label: "Send",    icon: "paper-plane",    icon_position: "only",    style: {},    className: "",}):
    Configuration for the send button in the input field. Allows
    customization of appearance and behavior.

    `send_button_config` is a dict with keys:

    - label (string; optional)

    - icon (a value equal to: "paper-plane-horizontal", "paper-plane", "folder", "file", "paperclip"; optional)

    - icon_position (a value equal to: "left", "right", "only"; optional)

    - style (dict; optional)

    - className (string; optional)

- supported_input_file_types (string | list of strings; default "*/*"):
    String or array of file types to accept in the attachment file
    input.

- theme (string; default "light"):
    Theme for the chat interface. Default is \"light\". Use \"dark\"
    for a dark mode appearance.

- typing_indicator (a value equal to: "dots", "spinner"; default "dots"):
    The type of typing indicator to display. Options are:    -
    `\"dots\"`: Displays animated dots.    - `\"spinner\"`: Displays a
    spinner animation.

- user_bubble_style (dict; optional):
    Css styles to customize the user message bubble."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_chat_multi'
    _type = 'ChatComponentMulti'
    MessagesContent = TypedDict(
        "MessagesContent",
            {
            "type": Literal["text", "attachment", "table", "graph"],
            "props": NotRequired[dict]
        }
    )

    Messages = TypedDict(
        "Messages",
            {
            "role": Literal["user", "assistant"],
            "content": typing.Union[typing.Sequence[typing.Union["MessagesContent", dict]], str, dict]
        }
    )

    FileAttachmentButtonConfig = TypedDict(
        "FileAttachmentButtonConfig",
            {
            "show": NotRequired[bool],
            "label": NotRequired[str],
            "icon": NotRequired[Literal["paper-plane-horizontal", "paper-plane", "folder", "file", "paperclip"]],
            "icon_position": NotRequired[Literal["left", "right", "only"]],
            "style": NotRequired[dict],
            "className": NotRequired[str]
        }
    )

    SendButtonConfig = TypedDict(
        "SendButtonConfig",
            {
            "label": NotRequired[str],
            "icon": NotRequired[Literal["paper-plane-horizontal", "paper-plane", "folder", "file", "paperclip"]],
            "icon_position": NotRequired[Literal["left", "right", "only"]],
            "style": NotRequired[dict],
            "className": NotRequired[str]
        }
    )


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        messages: typing.Optional[typing.Sequence["Messages"]] = None,
        theme: typing.Optional[str] = None,
        container_style: typing.Optional[dict] = None,
        typing_indicator: typing.Optional[Literal["dots", "spinner"]] = None,
        new_message: typing.Optional[dict] = None,
        input_container_style: typing.Optional[dict] = None,
        input_text_style: typing.Optional[dict] = None,
        fill_height: typing.Optional[bool] = None,
        fill_width: typing.Optional[bool] = None,
        user_bubble_style: typing.Optional[dict] = None,
        assistant_bubble_style: typing.Optional[dict] = None,
        input_placeholder: typing.Optional[str] = None,
        class_name: typing.Optional[str] = None,
        persistence: typing.Optional[bool] = None,
        persistence_type: typing.Optional[Literal["local", "session"]] = None,
        supported_input_file_types: typing.Optional[typing.Union[str, typing.Sequence[str]]] = None,
        file_attachment_button_config: typing.Optional["FileAttachmentButtonConfig"] = None,
        send_button_config: typing.Optional["SendButtonConfig"] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'assistant_bubble_style', 'class_name', 'container_style', 'file_attachment_button_config', 'fill_height', 'fill_width', 'input_container_style', 'input_placeholder', 'input_text_style', 'messages', 'new_message', 'persistence', 'persistence_type', 'send_button_config', 'supported_input_file_types', 'theme', 'typing_indicator', 'user_bubble_style']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'assistant_bubble_style', 'class_name', 'container_style', 'file_attachment_button_config', 'fill_height', 'fill_width', 'input_container_style', 'input_placeholder', 'input_text_style', 'messages', 'new_message', 'persistence', 'persistence_type', 'send_button_config', 'supported_input_file_types', 'theme', 'typing_indicator', 'user_bubble_style']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(ChatComponentMulti, self).__init__(**args)

setattr(ChatComponentMulti, "__init__", _explicitize_args(ChatComponentMulti.__init__))
