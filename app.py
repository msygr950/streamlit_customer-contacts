import streamlit as st
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# 環境変数の読み込み
load_dotenv()

# OpenAI クライアントの初期化
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ページ設定
st.set_page_config(
    page_title="カスタマーサポート チャットボット",
    page_icon="💬",
    layout="wide"
)

# セッション状態の初期化
if "messages" not in st.session_state:
    st.session_state.messages = []

if "customers" not in st.session_state:
    st.session_state.customers = {}

if "current_customer" not in st.session_state:
    st.session_state.current_customer = None

# カスタマーデータの読み込み
def load_customers():
    """顧客データをJSONファイルから読み込む"""
    if not os.path.exists("customers.json"):
        return {}
    
    try:
        with open("customers.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"顧客データの読み込みエラー: {e}")
        return {}

# カスタマーデータの保存
def save_customers(customers):
    """顧客データをJSONファイルに保存する"""
    try:
        with open("customers.json", "w", encoding="utf-8") as f:
            json.dump(customers, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"顧客データの保存エラー: {e}")

# AIレスポンスの生成
def generate_ai_response(messages):
    """OpenAI APIを使用してAIレスポンスを生成する"""
    try:
        # システムメッセージの追加
        system_message = {
            "role": "system",
            "content": "あなたは親切で知識豊富なカスタマーサポート担当者です。丁寧な日本語で対応してください。"
        }
        
        # メッセージの整形（最新20件のみを使用してコストと性能を最適化）
        recent_messages = messages[-20:] if len(messages) > 20 else messages
        formatted_messages = [system_message] + [
            {"role": msg["role"], "content": msg["content"]}
            for msg in recent_messages
        ]
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=formatted_messages,
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

# メインアプリケーション
def main():
    st.title("💬 カスタマーサポート チャットボット")
    st.markdown("---")
    
    # サイドバー: 顧客管理
    with st.sidebar:
        st.header("👤 顧客管理")
        
        # 顧客データの読み込み
        if not st.session_state.customers:
            st.session_state.customers = load_customers()
        
        # 新規顧客登録
        with st.expander("新規顧客登録"):
            customer_name = st.text_input("顧客名")
            customer_email = st.text_input("メールアドレス")
            customer_phone = st.text_input("電話番号")
            
            if st.button("登録"):
                if customer_name and customer_email:
                    # 既存の最大IDを取得して次のIDを生成（削除による重複を防ぐ）
                    existing_ids = [int(cid[1:]) for cid in st.session_state.customers.keys()]
                    next_id = max(existing_ids, default=0) + 1
                    customer_id = f"C{next_id:04d}"
                    
                    st.session_state.customers[customer_id] = {
                        "name": customer_name,
                        "email": customer_email,
                        "phone": customer_phone,
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "conversations": []
                    }
                    save_customers(st.session_state.customers)
                    st.success(f"顧客 {customer_name} を登録しました (ID: {customer_id})")
                else:
                    st.error("顧客名とメールアドレスは必須です")
        
        # 既存顧客の選択
        st.markdown("---")
        st.subheader("顧客を選択")
        
        if st.session_state.customers:
            customer_options = {
                f"{cid}: {data['name']}": cid
                for cid, data in st.session_state.customers.items()
            }
            
            selected = st.selectbox(
                "顧客選択",
                options=["選択してください"] + list(customer_options.keys())
            )
            
            if selected != "選択してください":
                st.session_state.current_customer = customer_options[selected]
                customer_data = st.session_state.customers[st.session_state.current_customer]
                
                st.info(f"""
                **顧客情報**
                - ID: {st.session_state.current_customer}
                - 名前: {customer_data['name']}
                - メール: {customer_data['email']}
                - 電話: {customer_data.get('phone', 'N/A')}
                """)
        else:
            st.info("登録されている顧客がいません")
    
    # メインエリア: チャット
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.header("チャット")
        
        # チャット履歴の表示
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])
                    st.caption(message.get("timestamp", ""))
        
        # ユーザー入力
        if prompt := st.chat_input("メッセージを入力してください..."):
            # ユーザーメッセージの追加
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            user_message = {
                "role": "user",
                "content": prompt,
                "timestamp": timestamp
            }
            st.session_state.messages.append(user_message)
            
            # ユーザーメッセージの表示
            with st.chat_message("user"):
                st.write(prompt)
                st.caption(timestamp)
            
            # AIレスポンスの生成と表示
            with st.chat_message("assistant"):
                with st.spinner("考え中..."):
                    response = generate_ai_response(st.session_state.messages)
                    st.write(response)
                    
                    # アシスタントメッセージの追加
                    assistant_message = {
                        "role": "assistant",
                        "content": response,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    st.session_state.messages.append(assistant_message)
                    st.caption(assistant_message["timestamp"])
            
            # 顧客の会話履歴に保存（メモリ内のみ - 頻繁なディスク書き込みを避ける）
            if st.session_state.current_customer:
                customer_id = st.session_state.current_customer
                if "conversations" not in st.session_state.customers[customer_id]:
                    st.session_state.customers[customer_id]["conversations"] = []
                
                st.session_state.customers[customer_id]["conversations"].append({
                    "timestamp": timestamp,
                    "user": prompt,
                    "assistant": response
                })
                # バッチ保存のフラグを設定
                if "needs_save" not in st.session_state:
                    st.session_state.needs_save = False
                st.session_state.needs_save = True
    
    with col2:
        st.header("操作")
        
        # 会話の保存
        if st.button("会話を保存", use_container_width=True, type="primary"):
            if st.session_state.get("needs_save", False):
                save_customers(st.session_state.customers)
                st.session_state.needs_save = False
                st.success("保存しました")
            else:
                st.info("保存する変更はありません")
        
        # チャット履歴のクリア
        if st.button("チャット履歴をクリア", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        # 会話履歴のエクスポート
        if st.button("会話をエクスポート", use_container_width=True):
            if st.session_state.messages:
                conversation_text = "\n\n".join([
                    f"[{msg.get('timestamp', 'N/A')}] {msg['role'].upper()}: {msg['content']}"
                    for msg in st.session_state.messages
                ])
                st.download_button(
                    label="ダウンロード",
                    data=conversation_text,
                    file_name=f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            else:
                st.warning("エクスポートする会話がありません")
        
        # 統計情報
        st.markdown("---")
        st.subheader("統計")
        st.metric("総メッセージ数", len(st.session_state.messages))
        st.metric("登録顧客数", len(st.session_state.customers))
        
        # 未保存の変更を通知
        if st.session_state.get("needs_save", False):
            st.warning("⚠️ 未保存の会話があります")

if __name__ == "__main__":
    main()
