# PyBacklogPy

[![CircleCI](https://circleci.com/gh/kitadakyou/PyBacklogPy/tree/master.svg?style=svg)](https://circleci.com/gh/kitadakyou/PyBacklogPy/tree/master)

## これは何？

[BacklogAPI](https://developer.nulab.com/ja/docs/backlog/) を Python から簡単に呼べるようにラップしたものです。

## 必須環境

- `Python 3.5` 以上
  - `typing` モジュールを使用しているため
  - 開発およびテスト環境は `Python 3.7.3` を使用

## 使い方

詳細な仕様については[ドキュメント](https://kitadakyou.github.io/PyBacklogPy/)を参照してください

### インストール

pip からインストールします。

```bash
pip install pybacklogpy
```

### ドメインおよびシークレットキーの登録

ドメイン及びシークレットキーを登録するには以下の2種類の方法があります。

1. プログラム上で指定する
1. 設定ファイルを置く

なお、どちらも設定していた場合、 __プログラム上で指定する__ の方が優先されます。

#### プログラム上で設定する場合

Backlogのドメイン別に以下3種類のクラスを用意しています。

- BacklogComConfigure (backlog.com)
- BacklogJpConfigure (backlog.jp)
- BacklogToolConfigure (backlogtool.com)

このクラスのコンストラクタ引数として、スペースID と API のキーを渡すことで設定を行えます。

例えば、下記のような場合
- Backlogドメイン: `kitadakyou.backlog.com` 
- API キー: `qwertyuiopasdfghjklzxcvbnmqazwsxedcrfvtgbyhnujmikolp`

コードは次のようになります。

```python
from pybacklogpy.BacklogConfigure import BacklogComConfigure
from pybacklogpy.Issue import Issue

# Configure クラスのインスタンスを生成
config = BacklogComConfigure(space_key='kitadakyou',
                             api_key='qwertyuiopasdfghjklzxcvbnmqazwsxedcrfvtgbyhnujmikolp')


issue_api = Issue(config)  # API を呼ぶクラスのコンストラクタ引数として Configure クラスのインスタンスは使用可能 
response = issue_api.get_issue_list()


```

#### 設定ファイルで指定する場合

使用するプロジェクトの直下に `secrets` というファイルを作り、以下のように値を入れておいてください。
なお、当プロジェクト直下にある `secrets_sample` をコピーすると楽です。

なお、このファイルは誤ってリポジトリにあげないよう、 `.gitignore` に追加しておくことを推奨します

```ini
[backlog]
Host = kitadakyou.backlog.com
ApiKey = qwertyuiopasdfghjklzxcvbnmqazwsxedcrfvtgbyhnujmikolp
```

`secrets` を指定した場合、先ほどの例で使用した configure クラスは省略して、以下のように書くことが出来ます

```python
from pybacklogpy.Issue import Issue


issue_api_2 = Issue()  # Configure クラスを渡さなかった場合は、設定ファイルの情報を読みに行く
response_2 = issue_api_2.get_issue_list()

```

なお、 `configure` クラスを渡さず、 `secrets` も設置していない場合は実行エラーとなります。

### モジュールを読み込み、インスタンス生成

使用するモジュールをロードします。
それぞれはクラスになっているので、そのインスタンスを生成します。

例として、Wiki の API を呼びたいと考えます。

```python:sample.py
from pybacklogpy.Wiki import Wiki


wiki_api = Wiki()

```

### API を呼ぶ

どのような API があるかは [PyBacklogPy のドキュメント](https://kitadakyou.github.io/PyBacklogPy/)、もしくは [BacklogAPI のドキュメント](https://developer.nulab.com/ja/docs/backlog/)を参照してください。
また、プロジェクトID や Wiki ID 等の調べ方は…ググればすぐに出てきます

Wiki を追加するサンプル

```python:sample3.py
from pybacklogpy.Wiki import Wiki


wiki_api = Wiki()


response = wiki_api.add_wiki_page(
    project_id=1000,
    name='SampleWikiName',
    content='サンプル Wiki 本文',
    mail_notify=False,
)

```

Wiki を更新するサンプル

```python:sample3.py
from pybacklogpy.Wiki import Wiki


wiki_api = Wiki()


response = wiki_api.update_wiki_page(
    wiki_id=12345,
    name='TestWikiName',
    content='テスト 本文',
    mail_notify=False,
)

```

### 返り値を見る

全ての関数は [request](https://requests-docs-ja.readthedocs.io/en/latest/) の [レスポンスオブジェクト](https://requests-docs-ja.readthedocs.io/en/latest/user/quickstart/#id3) を返します。

リクエストが成功しているかを確認するには、 `response.ok` を見るのが１番早いです。

Wiki の更新が成功しているか確認するサンプル

```python:sample4.py
from pybacklogpy.Wiki import Wiki


wiki_api = Wiki()


response = wiki_api.update_wiki_page(
    wiki_id=12345,
    name='TestWikiName',
    content='テスト 本文',
    mail_notify=False,
)
if not response.ok:
    raise ValueError('Wiki の更新に失敗')

```

また、レスポンス本文は `response.text` の中身に生(=テキストの)の JSON が入っています。標準ライブラリ `json` を使って parse してあげれば、簡単に使えます。

Wiki の内容を取得するサンプル

```python:sample5.py
import json


from pybacklogpy.Wiki import Wiki


wiki_api = Wiki()


response = wiki_api.get_wiki_page(
    wiki_id=12345,
)

if not response.ok:
    raise ValueError('Wiki ページ情報の取得に失敗')

wiki_data = json.loads(response.text)
wiki_name = wiki_data['name']
wiki_content = wiki_data['content']

```

### ファイルの取得

ファイル取得については、特殊な返り値のため、別途こちらで説明します。

ファイルを取得する関数を使用する場合は、まずディレクトリを作成する必要があります。
デフォルトではプロジェクト直下の `/tmp` ディレクトリにファイルがダウンロードされます。(今の所、変更不可💦)

ファイルを取得する関数は「1番目がファイルのPATH」、「2番目がレスポンスオブジェクト」のタプルを返します。
そのため、一度に受け取るには、以下のように返り値を受け取る変数を2つ用意する必要があります。

```python:sample3.py
from pybacklogpy.Wiki import Wiki


wiki_api = Wiki()


downloaded_file_path, response = self.wiki_attachment.get_wiki_page_attachment(
    wiki_id=12345,
    attachment_id=987654,
)
print(downloaded_file_path)
```

## バグを見つけたら

自由にブランチを切って、 PullRequest を出してください。Issue を上げるだけでも大丈夫です。
一週間に一回くらいは見るようにするので、対応出来たら対応します。(全て対応するとは言っていない)

もし、PR出しても全くリアクションがない場合は Twitter の [kitadakyou](https://twitter.com/kitadakyou) 、若しくは<a href='mailto:kitadakyou@gmail.com'>作者のメール</a>宛にご連絡ください。

## おまけ: なんでこんな名前なの？

`PyBacklog` も `BacklogPy` も既に存在したので、苦肉の策で Py で挟みました。 
もし、`PyBacklogPy` も存在したら、 `PyBacklogXPyBacklog` という HUNTER×HUNTER 方式で行こうと考えていました。

