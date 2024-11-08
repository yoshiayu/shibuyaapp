# 渋谷イベントアプリ

## アプリ紹介
このアプリケーションは、卒業制作として開発され、テーマは東急株式会社から提供されました。アプリの主な目的は、渋谷エリアのイベント情報を提供し、ユーザーがイベントに参加することでポイントを獲得し、渋谷への訪問を促進することです。アプリを通じて、渋谷のファンを増やし、地域活性化に貢献することを目指しています。

### プロジェクトテーマ
東急株式会社から提示されたテーマは、渋谷エリアのイベントに参加することで「渋谷のファン」を増やし、地域の活性化を図ることでした。このアプリでは、ユーザーがイベント情報を検索し、ポイントを獲得できるシステムを実装しています。

## 機能
- 渋谷エリアで開催されるイベント情報の表示
- イベント名や開催月を基にした検索機能
- ユーザー認証機能と個別イベントのおすすめ表示
- イベント参加によるポイントシステム
- イベント詳細ページに外部リンクと安全警告の表示

## アプリケーションのアーキテクチャとフロー
アプリケーションは、バックエンドにDjangoフレームワーク、フロントエンドを使用したMVC構造を採用しています。

### 画面遷移のリレーション図
以下はアプリケーションの画面遷移を示したフロー図です：
```mermaid
graph TD;
    A[ホーム画面] -->|イベントを選択| B[イベント詳細画面]
    A -->|マイページ| C[マイページ]
    A -->|イベント検索| D[イベント検索画面]
    D -->|検索結果クリック| B
    C -->|ポイント履歴確認| E[ポイント履歴画面]
    C -->|ポイント使用| F[ポイント使用確認画面]
    F -->|イベント参加| B
    B -->|イベントに参加| F
    E -->|イベント詳細を確認| B
```

## バージョン管理
- **Python**: 3.8以上
- **Django**: 4.2.16
- **PostgreSQL**: 13以上
- **HTML5**: 最新仕様
- **CSS3**: 最新仕様

## 制作工程管理

### 1. 初期設定と計画
- 東急株式会社との要件定義、アプリケーション構造の作成。
- Djangoとjsを使用したプロジェクトのセットアップ。
- データベースにはPostgreSQLを採用。

### 2. データベースおよびバックエンド実装
- ユーザー、イベント、ポイント管理を含むデータベース設計。
- Djangoを用いたイベント管理、ポイントシステム、ユーザー認証機能の実装。

### 3. フロントエンド開発
- jsとCSS Gridを用いてレスポンシブなユーザーインターフェースを構築。
- ユーザーの入力をもとにしたイベント検索機能とフィルタリングの実装。

### 4. テストとバグ修正
- バックエンドおよびフロントエンドコンポーネントの単体テストを実施。
- ユーザーフローおよび機能確認のための結合テスト。
- パフォーマンス最適化とセキュリティチェックを実施。

### 5. デプロイメント
- ローカルサーバーでのデプロイメントを行い、Dockerを用いてスケーラビリティを確保。
- GitHubでのプロジェクト管理とチームコラボレーション。

## 使用ツール
- **プロジェクト管理**: GitHubでのバージョン管理およびイシュー管理。
- **開発環境**: Visual Studio Code。
- **データベース**: PostgreSQLを使用した信頼性の高いデータ管理。
- **バージョン管理**: GitおよびGitHubを使用。
- **テスト**: バックエンドおよびフロントエンドのコンポーネントテストを実施。

## インストールと使用方法

### 1. リポジトリをクローンします：
```
git clone https://github.com/your-username/shibuya-event-app.git
```
## 2. 仮想環境を作成し、依存関係をインストールします

## 仮想環境を作成
```
python3 -m venv shibuya
```
## 仮想環境をアクティベート
```
source shibuya/bin/activate
```
## 必要なパッケージをインストール
```
pip install -r requirements.txt
```
