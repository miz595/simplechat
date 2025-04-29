# lambda/index.py
import json
import urllib.request

def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event))

        # リクエストボディの解析
        body = json.loads(event['body'])
        message = body['message']

        # FastAPIのエンドポイント
        API_URL = "https://xxxxxxx.ngrok.io/chat"  # ←あなたのURLに変えてね

        # FastAPIに送るデータ
        request_data = json.dumps({
            "message": message
        }).encode("utf-8")

        # HTTPリクエストを送信
        req = urllib.request.Request(
            API_URL,
            data=request_data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        # レスポンスを受け取る
        with urllib.request.urlopen(req) as response:
            response_data = json.loads(response.read())

        assistant_response = response_data["reply"]

        # 成功レスポンスを返す
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": True,
                "response": assistant_response,
                "conversationHistory": [
                    {"role": "user", "content": message},
                    {"role": "assistant", "content": assistant_response}
                ]
            })
        }

    except Exception as error:
        print("Error:", str(error))

        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": False,
                "error": str(error)
            })
        }

