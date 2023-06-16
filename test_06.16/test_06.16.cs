const API_TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX';
const GPT_ENDPOINT = 'https://api.openai.com/v1/chat/completions';
const MODEL_NAME = 'gpt-3.5-turbo';
const MODEL_TEMP = 0.5;
const MAX_TOKENS = 256;

function requestGpt() {
  // ChatGPTに投げるメッセージ
  const messages = [{ 'role': 'user', 'content': 'Hello!' }];
  // リクエストヘッダ
  const headers = {
    'Authorization': 'Bearer ' + API_TOKEN,
    'Content-type': 'application/json',
  };
  // リクエストオプション
  const options = {
    'method': 'POST',
    'headers': headers,
    'payload': JSON.stringify({
      'model': MODEL_NAME,        // 使用するGPTモデル
      'max_tokens': MAX_TOKENS,   // レスポンストークンの最大値(最大4,096)
      'temperature': MODEL_TEMP,  // 応答の多様性(0-1)※数値が大きいほどランダムな応答になる
      'messages': messages
    })
  };
  // HTTPリクエストでChatGPTのAPIを呼び出す
  const res = JSON.parse(UrlFetchApp.fetch(GPT_ENDPOINT, options).getContentText());
  // レスポンスから応答文を取り出す
  console.log(res.choices[0].message.content);
}
スクリプトの初回実行時のみ