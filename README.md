# streamlit_customer-contacts
AIエージェント使用のチャットボット

## 概要
このアプリケーションは、OpenAI APIを活用したStreamlitベースのカスタマーサポートチャットボットです。顧客管理機能と自動応答機能を備えています。

## 機能
- 🤖 **AI自動応答**: OpenAI GPT-3.5を使用した自然な日本語での対応
- 👥 **顧客管理**: 顧客情報の登録・管理機能
- 💬 **チャット履歴**: 会話履歴の保存とエクスポート
- 📊 **統計表示**: メッセージ数や顧客数の可視化

## セットアップ

### 必要な環境
- Python 3.8以上
- OpenAI APIキー

### インストール手順

1. リポジトリをクローン
```bash
git clone https://github.com/msygr950/streamlit_customer-contacts.git
cd streamlit_customer-contacts
```

2. 依存パッケージをインストール
```bash
pip install -r requirements.txt
```

3. 環境変数を設定
```bash
cp .env.example .env
```
`.env`ファイルを編集し、OpenAI APIキーを設定してください。

4. アプリケーションを起動
```bash
streamlit run app.py
```

## 使い方

### 顧客登録
1. サイドバーの「新規顧客登録」を展開
2. 顧客名、メールアドレス、電話番号を入力
3. 「登録」ボタンをクリック

### チャット
1. サイドバーから対応する顧客を選択
2. チャット入力欄にメッセージを入力
3. AIが自動的に返答を生成

### 会話のエクスポート
1. 右側の「操作」パネルから「会話をエクスポート」をクリック
2. 「ダウンロード」ボタンで会話履歴をテキストファイルとして保存

## ファイル構成
```
streamlit_customer-contacts/
├── app.py                  # メインアプリケーション
├── requirements.txt        # 依存パッケージ
├── .env.example           # 環境変数テンプレート
├── .env                   # 環境変数（要作成）
├── .streamlit/
│   └── config.toml        # Streamlit設定
├── customers.json         # 顧客データ（自動生成）
└── README.md              # このファイル
```

## 技術スタック
- **Streamlit**: Webアプリケーションフレームワーク
- **OpenAI API**: AI応答生成
- **Python-dotenv**: 環境変数管理
- **Pandas**: データ処理

## ライセンス
MIT License
