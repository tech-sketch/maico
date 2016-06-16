# maico documentation

## Architecture

![architecture.PNG](./images/architecture.PNG)

**Components and Role**

* sensor(Kinect)
 * 来店した顧客の動きを捉え、local terminalに転送する
* local terminal(PC)
 * 受け取ったセンサー情報をsensing protcolにまとめ、Web Systemへ転送する
* Web system(maico) 
 * 受け取ったsennsing protcolを集約し、特徴量を作成する
 * action modelは、特徴量から取るべきactionを判定する
 * state modelは、特徴量から現在のstateを判定する
 * action/stateそれぞれの情報を、action protcolにまとめる
 * action protcolの内容を基に、ダッシュボードなどの表示を行う
 * Auto modeの場合action、Manual modeの場合ユーザーからの操作を、operation protcolにまとめる
 * operation protcolを、対象の店舗・ロボットへ送信する
* Dialogue System
 * One to Oneモードの時に対話の管理を行うシステム
* Robot(Pepper)
 * operation protcolに則り、発話やジェスチャーなどの行動を行う
 * ユーザーから得られた反応などを、sensing protcolにまとめWeb systemに送信する

**Protcols**

* sensing protcol(latency: 1req/sec~, channel:web socket)
 * sensor_id: センサーのid情報。全店舗で一意のidがふられる(それがどの店舗にあるかはWeb Systemのマスタで管理)
 * sensed[]: センサーで検知した内容の配列。targetごとに格納
 * sensed/target_id: センシング対象(主に人間)を識別するためのid
 * sensed/behaviors: name/valueのdictionaryで、検知した値を格納
* action protcol
 * shop_id: お店のid
 * target_id: ターゲットのid
 * state: state modelから得られた、状態を表す離散値
 * action: action modelから得られた、行動を表す離散値
 * reward: 行動によって得られる報酬の見込み値
* operation protcol
 * sensor_id: 指示対象のsensorのid
 * operation: name/valueのdictionary
 * operation/say: 発話文
 * operation/gesture: ジェスチャー
 * operation/display: 表示画像
 * operation/move: 移動指示

stateの種類

* good: 良好な関係
* stable: 安定している
* breakdown: 破たんしている(音声認識エラーを含む)
* emergency: システムトラブルなど

actionの種類

* welcome: いらっしゃいませ
* routine: 適当な宣伝文句
* call: 声をかける(one to many)
* engage: 対話モードを開始する/維持する->以後は、フレームベースの対話管理に遷移
* terminate: 対話を打ち切る


**Models**

Estimation

* action model: featureを受け取り、target_idに対しシステムが取るべきactionを決定する
* state model: featureを受け取り、target_idとの関係状態(state)を判定する

Generation

* operation model: action/stateを元に、実際のロボットの行動を生成する

## UI

* ユーザーは、「今何をすべきか」を即時に知ることができる
 * Task Streamを左側に配置し、緊急度が高い順に並べて表示
* ユーザーは、複数の案件について並行で対応することが可能
 * Cockpitでは、自分の扱っているタスクリストを参照できる
* ユーザーは、リモートでロボットを通じた接客が可能(テレプレゼンス)
* ユーザーは、問い合わせの全体状況を認識することができる
 * Dash boardに、店舗ごとのタスク状況、オペレーターごとのタスク進捗状況を表示する

![dashboard.PNG](./images/dashboard.PNG)

![cockpit.PNG](./images/cockpit.PNG)

