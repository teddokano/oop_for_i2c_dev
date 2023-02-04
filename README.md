# I²Cデバイスをクラス化するまで：ステップ・バイ・ステップ
## これはなに？
MicroPythonを使ってマイコンに接続したLM75B互換のI²C温度センサ（LM75B，PCT2075，P3T1085など）をオブジェクト指向でハードを抽象化するまでを説明します．  
このドキュメントが，この説明のメイン部分で，`samples`フォルダ以下のコードは各ステップでのコード例です．  
マイコン基板にIMXRT1050-EVKBを用いて，まずこの基板上のLEDの点滅を確認．そのあとMicroPythonの超基本的な動作を見ます．  
そのあとでI²Cで接続されたデバイスのアクセス試して，コードを徐々に変更させて，クラス化するまでを説明します．

## 動かしてみる

### ステップ0：マイコン基板動作の確認
IMXRT1050-EVKBには"D4"ピンにLEDが接続されています．これを対話式の環境(REPL)で動かしてみます．  
サンプルコード`step00_LED_by_manual_operation.py`を手で打ってみます．  
`import machine`はMicroPythonに組み込まれたハードウェア制御用ライブラリを使用可能にします．  
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

### ステップ1：自動化してみる
ステップ0の作業をスクリプトとして実行します．  
上記の組み込みライブラリの他に，もう一つ`utime`を使えるようにします．
これは時間に関連したライブラリです．

`while True:`で，それ以下のインデントされた行をまとめて繰り返し実行するループを作っています．ここには必ず最後に`:`が必要です．これをつけることにより，ここから下のインデントされた部分が，ひとまとまりのコードであることを示すことができます．  
`machine.sleep( 0.1 )`で「0.1秒待ちます．`pin.value( 1 )`を実行して0.1秒待ち，`pin.value( 0 )`を実行して0.1秒待ち，そのあとはループの最初に戻ってこの動作を繰り返します．

_step01_LED_by_script.py_
```python
import	machine
import	utime

pin	= machine.Pin( "D4", machine.Pin.OUT )

while True:
	pin.value( 1 )
	utime.sleep(0.1)

	pin.value( 0 )
	utime.sleep(0.1)
```

### ステップ2：変数を使って操作
次は変数を使ってみます．  
先頭の行は`#`で始まっています．これはコメントで実際のプログラム実行時には無視される部分です．  

`pin`インスタンスを作ったあとに，`state`という名の変数が使われています．これに`0`が代入されています．

ループの中では`if`が使われています．これによって`state`の値を確認しています．`if state:`は`state`が「ゼロではない」ことを確認した時に，次のインデントされた部分を実行します．  
`else`以下には，上記の`if`の条件に合わなかった時に実行される部分を書いておきます．  
この例では`state`が0出なかった時には`state = 0`を，`state`が0だった時には`state = 1`を実行します．  

`pin.value( state )`は`1`や`0`を引数として与える代わりに変数を与えています．これにより変数の値によってLEDがON/OFFします．

_step02_variable.py_
```python
### this code has a bug. need to fix to run :)

import	machine
import	utime

pin		= machine.Pin( "D4", machine.Pin.OUT )
state	= 0

while True:
	if state:
		state	= 0
	else
		state	= 1

	pin.value( state )
	utime.sleep(0.1)
```

ちなみに，このコード例にはバグがあります．`else`は最後にコロンをつけて`else:`としておかなければ動作しません．

### ステップ3：三本締め
この解説の最後というわけではありませんが，一本締めのパターンでLEDを点滅させます．  
ここでいう一本締めは「♪♪♪・♪♪♪・♪♪♪・♪」です．

このパターンを作るのに「リスト」を使います．リストはデータを保存するための一種の配列です．
上記の音符のパターンを1と0にして，`[]`で囲って，patternという名をつけておきます．

このパターンを実行するのに`for`を使っています．  
`for v in pattern:`は`pattern`から各要素を1個ずつ取り出して`v`に代入．それに続くインデントされた部分(ブロック)ではこの`v`を使ってプログラムが実行されます．

_step03_list.py_
```python
import	machine
import	utime

pin		= machine.Pin( "D4", machine.Pin.OUT )
pattern	= [1,1,1,0,1,1,1,0,1,1,1,0,1]

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
import	machine
import	utime

pin		= machine.Pin( "D4", machine.Pin.OUT )
pattern	= [ 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1 ]

print( "Hello, world!" )
print( pattern )

pat2	= [ 1, 2**32, 3.14, "Strawberry", "fields", True, False ]
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
I²Cは簡単に動作させることができます．  
IMXRT1050-EVKBにPCT2075の評価基板PCT2075DP-ARDを接続します．  

`i2c = machine.I2C( 0 )`はmachineライブラリのI2Cクラスを使ってi2cインスタンスを作っています．引数に与えた`0`はハードウェアを指定するための数値で，これを指定することにより"A4"と"A5"ピンをI²Cとして使用できるようになります．

`i2c.scan()`はI2Cのメソッドで，このバスに接続されているデバイスのアドレスのリストを返してきます．

IMXRT1050-EVKBには基板上にあらかじめ2個のデバイスが搭載，接続されています．
このためスキャン結果には合計3個のデバイスが現れます．PCT2075のアドレスは72（16進右詰表現で0x48，左詰表現で0x90）です．

_step05_I2C.py_
```python
import	machine

i2c			= machine.I2C( 0 )
dev_list	= i2c.scan()
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
import	machine

i2c		= machine.I2C( 0 )
value	= i2c.readfrom( 72, 2 )
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
import	machine

i2c		= machine.I2C( 0 )
value	= i2c.readfrom( 72, 2 )
print( value )	# read value is in bytearray format

v	= list( value )
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
import	machine

i2c		= machine.I2C( 0 )
value	= i2c.readfrom( 72, 2 )
print( value )	# read value is in bytearray format

v	= list( value )
print( v )


temp16bit	= (v[ 0 ] << 8) | v[ 1 ]
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
表示は摂氏温度の値のみが表示されます．

_step07_I2C_read_PCT2075.py_
```python
import	machine

i2c		= machine.I2C( 0 )

value	= i2c.readfrom( 72, 2 )
v		= list( value )
temp	= ((v[ 0 ] << 8) | v[ 1 ]) / 256
print( temp )
```

### ステップ10：毎秒の温度表示
ステップ9のコードを`While True:`を用いてループに．  
毎秒の温度を表示

_step10_I2C_read_PCT2075.py_
```python
import	machine
import	utime

i2c		= machine.I2C( 0 )

# trying to get temp every second

while True:
	value	= i2c.readfrom( 72, 2 )
	v		= list( value )
	temp	= ((v[ 0 ] << 8) | v[ 1 ]) / 256
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
