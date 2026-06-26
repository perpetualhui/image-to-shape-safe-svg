# Image To Shape-Safe SVG

Languages: [English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

スライド画像、スクリーンショット、フローチャート、業務図、インフォグラフィックを、PowerPoint で「図形に変換」しやすい編集可能な SVG に再構成する Codex skill です。

この skill はビットマップを単純にトレースするものではありません。テキスト、パス、線、多角形、アイコン、基本図形を使ってページ構造を再構築し、Office で編集しやすい SVG を作ることを目的とします。

## できること

- スライドや業務図のスクリーンショットを構造化 SVG として再構築します。
- PowerPoint の convert-to-shapes 互換性を重視します。
- 埋め込み画像、`foreignObject`、SVG transform、marker 矢印、未展開のアイコンプレースホルダーを避けます。
- 矢印の先端を polygon として描画し、Office 変換後も残りやすくします。
- 多くのテキストを独立した SVG text ノードとして配置し、後編集しやすくします。
- 説明用の小さな複数行テキストのみ、`data-text-role="explanatory-block"` 付きの例外として扱えます。
- セマンティックな内蔵アイコンライブラリと自動キーワードマッチングツールを含みます。
- 装飾的なアイコンを減らし、番号付き円、ドット、ピル、カラーチップ、ステータスバッジに置き換える方針を既定にします。

## 出力ルール

最終 SVG は以下の検証基準を満たす必要があります。

```text
image = 0
data_icon = 0
transform = 0
marker_end = 0
marker_defs = 0
tspan = 0。ただし承認済みの説明テキストブロックは例外
foreign_object = 0
```

既定の出力フォルダー：

```text
svg_shape_safe/
```

## リポジトリ構成

```text
.
|-- SKILL.md
|-- config.yaml
|-- agents/
|-- assets/
|   `-- icons/
|-- docs/
|   |-- icon-matching.md
|   |-- map-complexity-policy.md
|   `-- troubleshooting.md
|-- examples/
|   |-- basic_usage.md
|   `-- web_usage.md
|-- references/
|   |-- local-batch-workflow.md
|   `-- web-workflow.md
|-- tests/
|   `-- test_validate_shape_safe_svg.py
`-- tools/
    |-- match_shape_safe_icon.py
    `-- validate_shape_safe_svg.py
```

## インストール

Codex の skills ディレクトリ、またはプロジェクトの `.agents/skills` に配置します。

```bash
git clone https://github.com/perpetualhui/image-to-shape-safe-svg.git
```

プロジェクト単位で使う場合の推奨パス：

```text
.agents/skills/image-to-shape-safe-svg/
```

## 使い方

Codex で skill 名を指定して呼び出します。

```text
Use $image-to-shape-safe-svg to convert these three slide screenshots into editable SVG.
Only deliver svg_shape_safe. Make sure icons and arrowheads survive PowerPoint convert-to-shapes.
```

日本語の依頼例：

```text
$image-to-shape-safe-svg を使って、この日本語の業務プロセス図を編集可能な SVG に再構築してください。
出力は svg_shape_safe に置き、矢印は marker ではなく polygon の矢印先端で描いてください。
```

アイコンが多いページ：

```text
$image-to-shape-safe-svg でこのインフォグラフィックを変換してください。
最初に preflight を作成し、アイコン数と文字密度を評価してください。アイコンが多すぎる場合は balanced 方針にして、主要モジュールのアイコンだけを残し、細かい装飾は番号付き円やバッジに置き換えてください。
```

複数ページのバッチ：

```text
$image-to-shape-safe-svg で 5 枚のダッシュボード画像を処理してください。
最初の 1 枚をスタイルアンカーにして、色、文字サイズ、角丸、余白を統一してください。最終的には検証を通過した svg_shape_safe だけを納品してください。
```

アイコン自動マッチング：

```powershell
py tools\match_shape_safe_icon.py "自動化された承認プロセス" --x 120 --y 80 --size 48 --color "#5A0FB4"
```

このコマンドは内蔵アイコンライブラリから展開済み SVG primitives を出力します。`<image>`、`transform`、`marker`、`foreignObject`、`data-icon` は使いません。

ローカルバッチ処理：

```text
references/local-batch-workflow.md
```

ブラウザーまたは Web アプリ向け処理：

```text
references/web-workflow.md
```

## 推奨ワークフロー

1. 入力画像のサイズと構成を確認します。
2. 複雑度、アイコン数、文字密度リスク、レイアウト方針、視覚モデル呼び出し予算を preflight にまとめます。
3. 大きな再設計、アイコン削減、ページ分割、構造変更が必要な場合はユーザーに確認します。
4. 編集可能な SVG primitives でページを再構築します。
5. アイコン数を抑え、意味のあるアイコンだけを残します。
6. 矢印は line/path と polygon の矢印先端で描きます。
7. 付属の検証ツールで SVG を確認します。
8. プレビューをレンダリングし、ズレ、重なり、矢印欠落、Office 変換リスクを確認します。

## 検証

ファイルまたはフォルダーを検証します。

```bash
python tools/validate_shape_safe_svg.py path/to/svg_shape_safe
```

Windows で `python` が Microsoft Store ランチャーを指す場合：

```powershell
py tools\validate_shape_safe_svg.py path\to\svg_shape_safe
```

JSON 出力：

```bash
python tools/validate_shape_safe_svg.py --json path/to/svg_shape_safe
```

`pytest` インストール後にテストを実行します。

```bash
python -m pytest tests
```

## 設計方針

目的はピクセル単位の再現ではなく、編集可能な再構築です。良い出力は、元画像の構造、階層、余白、色の意図、主要な意味を保ちながら、PowerPoint の図形変換で壊れやすい SVG 機能を避けます。

密度の高い業務スライドでは、装飾的な忠実度よりも読みやすさと編集しやすさを優先します。繰り返しの小さなアイコンや装飾マーカーは、安定した編集可能な図形に簡略化するのが基本です。

## ライセンス

MIT License。詳しくは [LICENSE](LICENSE) を参照してください。
