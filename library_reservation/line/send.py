import linebot.v3.messaging

def send_line_message(message: str, token: str, group_id: str) -> None:
    configuration = linebot.v3.messaging.Configuration(access_token=token)
    with linebot.v3.messaging.ApiClient(configuration) as api_client:
      api_instance = linebot.v3.messaging.MessagingApi(api_client)
      message_dict={
        'to': group_id,
        'messages': [{'type': 'text', 'text': message}]
      }
      push_message_request = linebot.v3.messaging.PushMessageRequest.from_dict(message_dict)
      api_instance.push_message(push_message_request)
