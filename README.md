# I²Cデバイスをクラス化するまで：ステップ・バイ・ステップ
## これはなに？
MicroPythonを使ってマイコンに接続したLM75B互換のI²C温度センサ（LM75B，PCT2075，P3T1085など）から値を読んでくる例を使って，オブジェクト指向でハードを抽象化する方法を段階的に説明します．  
このドキュメント自体がこのリポジトリのメイン部分で，`samples`フォルダ以下のコードは各ステップで示したコードの例です．  

最初にマイコン基板のIMXRT1050-EVKBを用いて，まず基板上のLEDの点滅を確認．そのあとMicroPythonのごく基本的な動作を確認します．  
そのあとでI²Cで接続されたデバイスのアクセス試してからコードを徐々に変更，クラス化するまでを説明します．

## 動かしてみる

### ステップ0：マイコン基板動作の確認
IMXRT1050-EVKBには"D4"ピンにLEDが接続されています．これを対話式の環境(REPL)で動かしてみます．  
サンプルコード`step00_LED_by_manual_operation.py`を手で打ってみます．  
`import machine`でMicroPythonに組み込まれたハードウェア制御用ライブラリを使用可能にします．  
`pin=machine.Pin("D4",machine.Pin.OUT)`はそのライブラリの`Pin`クラスを使って`"D4"`ピンを出力として使えるようにし，`pin`という名のインスタンスを作ります．  
`pin.value(1)`と`pin.value(0)`はpinインスタンスのメソッド（インスタンスに属する関数）を，`1`または`0`の引数を与えて呼び出しています．  
1行ごとに入力するたびにリターンキーを押して入力，`pin.value(1)`，`pin.value(0)`を実行するたびにLEDが消灯，点灯します．

_step00_LED_by_manual_operation.py_
```python
import machine
pin=machine.Pin("D4",machine.Pin.OUT)
pin.value(1)
pin.value(0)
```

> **Note**
この`machine.Pin`のようにハードウェアを使いやすく見せるのが，ここから先で説明する「デバイスのクラス化」という話です．  
コード例の中の`pin`インスタンスは`machine.Pin`クラスによって作られます．  
インスタンスが作られる時に属性が与えられ（ここでは"D4"ピン指定や出力設定），それ以降，メソッド（インスタンスに属する関数）によって操作を行えるようにします．  
I²C接続の温度センサから簡単に現在の温度を読めるように，このクラスを作る手順を示します．

### ステップ1：自動化してみる
ステップ0の作業をスクリプトとして実行します．  
上記の組み込みライブラリの他に，もう一つ`utime`を使えるようにします．
これは時間に関連したライブラリです．

`while True:`で，それ以下のインデントされた行をまとめて繰り返し実行するループを作っています．ここには必ず最後に`:`が必要です．これをつけることにより，ここから下のインデントされた部分が，ひとまとまりのコードであることを示すことができます．  
`machine.sleep( 0.1 )`で「0.1秒待ちます．`pin.value( 1 )`を実行して0.1秒待ち，`pin.value( 0 )`を実行して0.1秒待ち，そのあとはループの最初に戻ってこの動作を繰り返します．

_step01_LED_by_script.py_
```python
import machine
import utime

pin = machine.Pin( "D4", machine.Pin.OUT )

while True:
    pin.value( 1 )
    utime.sleep(0.1)

    pin.value( 0 )
    utime.sleep(0.1)
```

### ステップ2：変数を使って操作
次は変数を使ってみます．  
先頭の行は`#`で始まっています．この行は「コメント」となり，実際のプログラム実行時には無視される部分になります．  

`pin`インスタンスを作った次の行に変数があります．  
`state`という名の変数で．これに`0`が代入されています．（Pythonではあらかじめ変数を宣言する必要はありません）

ループの中では`if`が使われています．これによって`state`の値でプログラムの動作が変わります．`if state:`は`state`が「True」（ゼロではない）ことを確認した時に，次のインデントされた部分を実行します．  
`else`以下には，上記の`if`の条件に合わなかった時に実行されるコードを書いておきます．  
この例では`state`が「0」でなかった時には`state`に0を代入，`state`が「0」だった時には`state`に1を代入します．  

`pin.value( state )`では`1`や`0`を引数として与える代わりに変数を与えています．これにより変数の値によってLEDがON/OFFします．

_step02_variable.py_
```python
### this code has a bug. need to fix to run :)

import machine
import utime

pin   = machine.Pin( "D4", machine.Pin.OUT )
state = 0

while True:
    if state:
        state = 0
    else
        state = 1

    pin.value( state )
    utime.sleep(0.1)
```

> **Warning**
ちなみに，このコード例にはバグがあります．`else`は最後にコロンをつけて`else:`としておかなければ動作しません．

### ステップ3：一本締め
この解説の最後というわけではありませんが，一本締めのパターンでLEDを点滅させます．  
ここでいう一本締めは「♪♪♪・♪♪♪・♪♪♪・♪」です．

このパターンを作るのに「リスト」を使います．リストはデータを保存するための一種の配列です．
上記の音符のパターンを1と0にして，`[]`で囲って，patternという名をつけておきます．

このパターンを実行するのに`for`を使っています．  
`for v in pattern:`は`pattern`から各要素を1個ずつ取り出して`v`に代入．それに続くインデントされた部分(ブロック)ではこの`v`を使ってプログラムが実行されます．

_step03_list.py_
```python
import machine
import utime

pin     = machine.Pin( "D4", machine.Pin.OUT )
pattern = [1,1,1,0,1,1,1,0,1,1,1,0,1]

for v in pattern:
    pin.value( v )
    utime.sleep(0.1)

    pin.value( 0 )
    utime.sleep(0.1)
```

### ステップ4：`print`とリスト
変数の中身は`print()`で表示させることができます．  
リストをprintすると，その中身が表示されます．  
リストはC/C++のような単一の型の配列ではなく，様々な型（オブジェクト）を入れておくことができます．

_step04_print.py_
```python
import machine
import utime

pin     = machine.Pin( "D4", machine.Pin.OUT )
pattern = [ 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1 ]

print( "Hello, world!" )
print( pattern )

pat2    = [ 1, 2**32, 3.14, "Strawberry", "fields", True, False ]
print( pat2 )


for v in pattern:
    pin.value( v )
    utime.sleep(0.1)

    pin.value( 0 )
    utime.sleep(0.1)
```

_実行結果_
```
Hello, world!
[1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1]
[1, 4294967296, 3.14, 'Strawberry', 'fields', True, False]
```

### ステップ5：I²C
I²Cは，簡単に動作させることができます．  
IMXRT1050-EVKBにPCT2075の評価基板「PCT2075DP-ARD」を接続しておきます．  

`i2c = machine.I2C( 0 )`はmachineライブラリのI2Cクラスを使ってi2cインスタンスを作っています．引数に与えた`0`はハードウェアを指定するための数値で，これを指定することにより"A4"と"A5"ピンをI²Cとして使用できるようになります．

`i2c.scan()`はI2Cのメソッドで，このバスに接続されているデバイスのアドレスのリストを返してきます．

IMXRT1050-EVKBには基板上にあらかじめ2個のデバイスが搭載，接続されています．
このためスキャン結果には合計3個のデバイスが現れます．PCT2075のアドレスは72（16進右詰表現で0x48，左詰表現で0x90）です．

_step05_I2C.py_
```python
import machine

i2c      = machine.I2C( 0 )
dev_list = i2c.scan()
print( dev_list )
```

_実行結果_
```
[26, 31, 72]
```

### ステップ6：温度データを読む
PCT2075では電源投入後，そのままデータを読み出せば，現在温度のデータが得られます．  
温度データは2バイトのデータです．  

`value = i2c.readfrom( 72, 2 )`はI²Cの読み出しを行うメソッドです．  
2つの引数をとり，1つ目はターゲットのアドレス．2つ目はバイト数を指定します．このメソッドからの返り値をvalueに代入しています．

`print( value )`は読み出した内容を確認しています．下の例では「b'\x1a\x00'」が表示されました．このデータは実際に読めた温度によって異なります．  
「b'\x1a\x00'」は文字列「「'\x1a\x00'」」の前に「b」が付いています．これは`bytearray`と呼ばれるバイト列であることを示し，各バイトデータの値が0x1aと0x00であることを表しています．  

_step06_I2C_read_PCT2075.py_
```python
import machine

i2c   = machine.I2C( 0 )
value = i2c.readfrom( 72, 2 )
print( value )
```

_実行結果_
```
b'\x1a\x00'
```

### ステップ7：バイト列を通常のリストに
読み出したデータはバイト列のままでは扱いにくいのでリストに変換します．
（MicroPythonにはunpackのための方法も用意されていますが，邯鄲のためにこのような方法を紹介します）

`v = list( value )`はバイト列データである`value`を，通常のリストに変換して`v`に代入しています．

_step07_I2C_read_PCT2075.py_
```python
import machine

i2c   = machine.I2C( 0 )
value = i2c.readfrom( 72, 2 )
print( value )    # read value is in bytearray format

v = list( value )
print( v )
```
_実行結果_
```
b'\x1a\x00'
[26, 0]
```

### ステップ8：摂氏温度に変換
リストに変換された`v`の各要素へのアクセスは`v[0]`や`v[1]`のような添え字を使う方法で行えます．  
先頭バイトの値は`v[0]`，2番目のバイトは`v[1]`です．温度はこの2バイトを連結した16ビットに変換して256で割った値で求めることができます．  

`temp16bit = (v[ 0 ] << 8) | v[ 1 ]`は16ビット値への変換を行う式です．  
1バイト目を8ビット左シフトし，2バイト目の値とビット・オアをとっています．
この値を256で割れば，摂氏温度での値が得られます．

_step07_I2C_read_PCT2075.py_
```python
import machine

i2c   = machine.I2C( 0 )
value = i2c.readfrom( 72, 2 )
print( value )    # read value is in bytearray format

v = list( value )
print( v )

temp16bit = (v[ 0 ] << 8) | v[ 1 ]
print( temp16bit )
print( temp16bit / 256 )
```


_実行結果_
```
b'\x1a\x00'
[26, 0]
6656
26.0
```

### ステップ9：少しシンプルに書き換える
ステップ8でのコードは，計算途中の値の表示などがあり冗長です．  
これをシンプルに書き換えました．  
表示には摂氏温度の値のみが出てきます．

_step07_I2C_read_PCT2075.py_
```python
import machine

i2c   = machine.I2C( 0 )

value = i2c.readfrom( 72, 2 )
v     = list( value )
temp  = ((v[ 0 ] << 8) | v[ 1 ]) / 256
print( temp )
```

### ステップ10：毎秒の温度表示
ステップ9のコードを`While True:`を用いてループに．  
毎秒の温度を表示

_step10_I2C_read_PCT2075.py_
```python
import machine
import utime

i2c = machine.I2C( 0 )

# trying to get temp every second

while True:
    value = i2c.readfrom( 72, 2 )
    v     = list( value )
    temp  = ((v[ 0 ] << 8) | v[ 1 ]) / 256
    print( temp )
    
    utime.sleep( 1 )
```
_実行結果_
```
26.0
26.0
25.875
26.0
```


### ステップ11：温度の読み出しを関数に
デバイスからの温度の読み出しと摂氏の値に変換するところまでを，「関数」としてまとめます．　　
関数は何かの値を与えると，何かを返してくるコードのまとまりです．　　
ですが，この場合，関数に与える値は何もありません．関数を呼び出すと，デバイスからの読み出しと変換を行なって，その値を返します．

この例では`def read_temp():`という宣言で「read_temp」という関数を定義しています．コロン(:)以降の下のコードブロックにその関数の本体が記述されています．  
関数最後の`return temp`で，温度の値を返します．

MicroPythonはプログラムを先頭行から読んでいきますが，関数定義部分はその時点では実行されず，あとからその関数が呼び出された際に実行されます．  
この例ではループ内の`t = read_temp()`が関数の呼び出しで，返り値を`t`に代入しています．

実行結果はステップ9の例と同様です．

_step10_I2C_read_PCT2075.py_
```python
import machine
import utime

def read_temp():
    value = i2c.readfrom( 72, 2 )
    v     = list( value )
    temp  = ((v[ 0 ] << 8) | v[ 1 ]) / 256

    return temp    

i2c = machine.I2C( 0 )

# trying to get temp every second

while True:
    t = read_temp()
    print( t )
    utime.sleep( 1 )
```

### ステップ12：さらにシンプルに書き換え
コードを短く書き換えました．　　
各段階で一時的な変数に値を保存することなく，メソッドや関数をそのまま別の関数の引数として与えています．

_step12_function_condensed_PCT2075.py_
```python
import machine
import utime

def read_temp():
    v = list( i2c.readfrom( 72, 2 ) )
    return ((v[ 0 ] << 8) | v[ 1 ]) / 256

i2c = machine.I2C( 0 )

while True:
    print( read_temp() )
    utime.sleep( 1 )
```

### ステップ13：複数の温度センサを扱えるようにしてみる
ステップ12までの例では，アドレス=72のデバイスからの温度を読むことしかできません．  
これでは有用性が低いので，関数の引数にアドレスを与えるように書き換えました．　　
`def read_temp( address ):`の`address`が読み出し対象デバイスのターゲット・アドレスです．
関数内で`i2c.readfrom( address, 2 )`のようにターゲット・アドレス指定を`address`に書き換えました．  
関数の呼び出しでは`t = read_temp( 72 )`のようにアドレスを指定します．

_step13_function_flexible_PCT2075.py_
```python
import machine
import utime

def read_temp( address ):
    v = list( i2c.readfrom( address, 2 ) )
    return ((v[ 0 ] << 8) | v[ 1 ]) / 256

i2c = machine.I2C( 0 )

while True:
    print( read_temp( 72 ) )
    utime.sleep( 1 )
```



### ステップ14：複数の温度センサを読む
ステップ13の関数を使って，複数のセンサからの値を読んでくることができるようになります．  
具体的にはこのようなコードを書くことになります．

この例ではアドレス72，73，74のデバイスにアクセスしてみています．

_step14_multiple_dev_PCT2075.py_
```python
import machine
import utime

def read_temp( address ):
    v = list( i2c.readfrom( address, 2 ) )
    return ((v[ 0 ] << 8) | v[ 1 ]) / 256

i2c = machine.I2C( 0 )

while True:
    print( read_temp( 72 ) )
    print( read_temp( 73 ) )
    print( read_temp( 74 ) )
    utime.sleep( 1 )
```

### ステップ15：複数のバスに繋がった複数の温度センサを読む
大きなシステムの場合，マイコンに搭載された複数のI²Cバスを同時に使って，それぞれのバスに接続された複数のセンサの値を読んでくることもあります．  
関数にバスのインスタンスも渡せるようにしておけば対応することが可能です．

この例では`i2c_0`と`i2c_1`のふたつのバスに繋がった6個の温度センサを読んでみる例です．

_step15_multiple_bus_PCT2075.py_
```python
import machine
import utime

def read_temp( bus, address ):
    v = list( bus.readfrom( address, 2 ) )
    return ((v[ 0 ] << 8) | v[ 1 ]) / 256

i2c_0 = machine.I2C( 0 )
i2c_1 = machine.I2C( 1 )

while True:
    print( read_temp( i2c_0, 72 ) )
    print( read_temp( i2c_0, 73 ) )
    print( read_temp( i2c_0, 74 ) )
    print( read_temp( i2c_1, 72 ) )
    print( read_temp( i2c_1, 73 ) )
    print( read_temp( i2c_1, 74 ) )
    utime.sleep( 1 )

```

### ステップ16：クラス化
ステップ14の例では各デバイスを読む際に，「どのバス」の「どのアドレス」からという指定が必要でした．  
これをコード内で管理するのは煩雑です．  
この手間をクラス化によって省くことができます．

クラスはいくつかのデータと関数をまとめた入れ物と考えることができます．   
このクラスを作っておけば，同種の処理（この場合は温度センサ・デバイスを）単純化できます．

この例では`class temp_sensor:`によって`temp_sensor`クラスを作成しています．  
クラスの中にはふたつのメソッド（クラスで定義された関数）`__init()__`と`read()`が定義されています．  

`def __init__( self, bus, address ):`はインスタンスが作られるときに呼ばれる初期化のメソッドです．このメソッドでは与えられた`bus`と`address`をインスタンス内の変数として保存しています．  
`self`はインスタンス変数へアクセスするためのメカニズムを提供しています．メソッド定義内では必ず第一引数として指定しておき，インスタンス変数は`self.__bus`や`self.__adr`のようにアクセスします．

インスタンス変数は同クラス内の他のメソッドから参照できます．他のメソッドでも必ず第一引数`self`を用意しておき，上記と同様に`self.__adr`のようにアクセスします．

`read()`メソッド内では温度センサのアクセスに，`__init()__`で保存しておいた`self.__bus`と`self.__adr`を用いています．  
`self.__bus.readfrom( self.__adr, 2 )`のように`self.__bus`に保存されたI2Cインスタンス・メソッド`readfrom`を呼び出し，その際にアドレスを`self.__adr`で指定しています．

インスタンスの作成は`ts = temp_sensor( i2c, 72 )`で行なっています．I2Cインスタンスの`i2c`とアドレス値`72`を渡し，tsインスタンスが作られます．  
温度の読み出しはインスタンス・メソッド`read`で，インスタンス名を用いて`ts.read()`のように行います．

_step16_class_PCT2075.py_
```python
import machine
import utime

class temp_sensor:
    def __init__( self, bus, address ):
        self.__bus = bus
        self.__adr = address
    
    def read( self ):
        v = list( self.__bus.readfrom( self.__adr, 2 ) )
        return ((v[ 0 ] << 8) | v[ 1 ]) / 256
        
i2c = machine.I2C( 0 )
ts  = temp_sensor( i2c, 72 )

while True:
    print( ts.read() )
    utime.sleep( 1 )
```

### ステップ17：
ステップ15の「複数のバスに繋がった複数の温度センサを読む」は，この例のように書き換えることができます．

_step17_class_PCT2075.py_
```python
import machine
import utime

class temp_sensor:
    def __init__( self, bus, address ):
        self.__bus = bus
        self.__adr = address
    
    def read( self ):
        v = list( self.__bus.readfrom( self.__adr, 2 ) )
        return ((v[ 0 ] << 8) | v[ 1 ]) / 256

i2c_0 = machine.I2C( 0 )
i2c_1 = machine.I2C( 1 )

ts0   = temp_sensor( i2c_0, 72 )
ts1   = temp_sensor( i2c_0, 73 )
ts2   = temp_sensor( i2c_0, 74 )
ts3   = temp_sensor( i2c_1, 72 )
ts4   = temp_sensor( i2c_1, 73 )
ts5   = temp_sensor( i2c_1, 74 )

while True:
    print( ts0.read() )
    print( ts1.read() )
    print( ts2.read() )
    print( ts3.read() )
    print( ts4.read() )
    print( ts5.read() )
    utime.sleep( 1 )
```

### ステップ18：複数デバイスの管理をインスタンスのリストに
ステップ17の各インスタンスをリストとして用意しておけば，さらに管理が容易になります．  
この例の`ts_list`は温度センサのインスタンスがリストになっており，各デバイスからの読み出しは`for ts in ts_list:`のループ内で`ts.read()`を呼び出すだけで済みます．

_step18_class_PCT2075.py_
```python
import machine
import utime

class temp_sensor:
    def __init__( self, bus, address ):
        self.__bus = bus
        self.__adr = address
    
    def read( self ):
        v = list( self.__bus.readfrom( self.__adr, 2 ) )
        return ((v[ 0 ] << 8) | v[ 1 ]) / 256

i2c_0 = machine.I2C( 0 )
i2c_1 = machine.I2C( 1 )

ts_list = [ temp_sensor( i2c_0, 72 ), 
            temp_sensor( i2c_0, 73 ),
            temp_sensor( i2c_0, 74 ),
            temp_sensor( i2c_1, 72 ),
            temp_sensor( i2c_1, 73 ),
            temp_sensor( i2c_1, 74 )
            ]
              
while True:
    for ts in ts_list:
        print( ts.read() )
        utime.sleep( 1 )
```

