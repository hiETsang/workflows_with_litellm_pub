# 声明

引入类型、运算符、变量和其他名称及构造。

*声明* 将新的名称或构造引入到你的程序中。例如,你使用声明来引入函数和方法,引入变量和常量,以及定义枚举、结构体、类和协议类型。你还可以使用声明来扩展现有命名类型的行为,并将在其他地方定义的符号导入到你的程序中。

在 Swift 中,大多数声明也同时是定义,因为它们在声明的同时就被实现或初始化了。不过,由于协议没有实现其成员,所以大多数协议成员只是声明。为方便起见,并且因为这种区别在 Swift 中并不重要,所以术语 *声明* 包括了声明和定义。

> 声明的语法:
> > *declaration* → *import-declaration* \
> > *declaration* → *constant-declaration* \
> > *declaration* → *variable-declaration* \
> > *declaration* → *typealias-declaration* \
> > *declaration* → *function-declaration* \
> > *declaration* → *enum-declaration* \
> > *declaration* → *struct-declaration* \
> > *declaration* → *class-declaration* \
> > *declaration* → *actor-declaration* \
> > *declaration* → *protocol-declaration* \
> > *declaration* → *initializer-declaration* \
> > *declaration* → *deinitializer-declaration* \
> > *declaration* → *extension-declaration* \
> > *declaration* → *subscript-declaration* \
> > *declaration* → *macro-declaration* \
> > *declaration* → *operator-declaration* \
> > *declaration* → *precedence-group-declaration* \

## 顶层代码

Swift 源文件中的顶层代码由零个或多个语句、声明和表达式组成。默认情况下,在源文件顶层定义的变量、常量和其他命名定义对同一模块中的每个源文件的代码都是可访问的。你可以通过使用访问级别修饰符来覆盖此默认行为,如 <doc:Declarations#Access-Control-Levels> 中所述。

顶层代码有两种类型:顶层声明和可执行的顶层代码。顶层声明只包含声明,在所有 Swift 源文件中都是允许的。可执行的顶层代码包含语句和表达式,而不仅仅是声明,只允许作为程序的顶层入口点。

无论你如何将代码组织到文件和模块中,你编译以生成可执行文件的 Swift 代码最多只能使用以下一种方式来标记顶层入口点: `main` 属性、`NSApplicationMain` 属性、`UIApplicationMain` 属性、一个 `main.swift` 文件或包含顶层可执行代码的文件。

> 顶层声明的语法:
> > *top-level-declaration* → *statements*_?_

## 代码块

*代码块* 由各种声明和控制结构使用,用于将语句组合在一起。它的形式如下:

```swift
{
  <#statements#>
}
```

代码块内的 *statements* 包括声明、表达式和其他类型的语句,按照它们在源代码中出现的顺序执行。

> 代码块的语法:
> > *code-block* → **`{`** *statements*_?_ **`}`**

## 导入声明

*导入声明* 允许你访问在当前文件之外定义的符号。基本形式导入整个模块;它由 `import` 关键字后跟一个模块名组成:

```swift
import <#module#>
```

提供更多细节可以限制导入哪些符号 —— 你可以指定一个特定的子模块或模块或子模块中的特定定义。当使用这种详细形式时,只有导入的符号(而不是定义它的模块)在当前作用域中可用。

```swift
import <#import kind#> <#module#>.<#symbol name#>
import <#module#>.<#submodule#>
```

以下是改进后的翻译:

> 导入声明的语法规则:
> > *导入声明* → *属性*_?_ **`import`** *导入种类*_?_ *导入路径*
> > *导入种类* → **`typealias`** | **`struct`** | **`class`** | **`enum`** | **`protocol`** | **`let`** | **`var`** | **`func`**
> > *导入路径* → *标识符* | *标识符* **`.`** *导入路径*

## 常量声明

常量声明用于在程序中引入一个命名值。常量声明使用 `let` 关键字声明,其形式如下:

```swift
let <#常量名称#>: <#类型#> = <#表达式#>
```

常量声明在常量的名称和初始化表达式的值之间建立了一个不可变的绑定关系;一旦常量的值被设置后,就不能再改变。不过,如果常量是用类对象初始化的,对象本身是可以改变的,但是常量名称和它所引用的对象之间的绑定关系是不能改变的。

当在全局作用域声明一个常量时,它必须用一个值进行初始化。当在函数或方法的上下文中声明常量时,它可以延迟初始化,只要能保证在第一次读取它的值之前已经设置了值。如果编译器能证明常量的值永远不会被读取,那么常量就不需要设置值。这种分析称为确定初始化 --- 编译器证明了在读取值之前一定会设置值。

> 注意:
> 确定初始化无法构造需要领域知识的证明,并且它跟踪条件语句中状态的能力也是有限的。如果你能确定常量总是会被设置值,但编译器无法证明这一点,请尝试简化设置值的代码路径,或使用变量声明。

当常量声明出现在类或结构体声明的上下文中时,它被视为常量属性。常量声明不是计算属性,因此没有 getter 或 setter。

如果常量使用元组模式声明,每个元组项的名称都会绑定到初始化表达式中对应的值。

```swift
let (firstNumber, secondNumber) = (10, 42)
```

在这个例子中,`firstNumber` 是值 `10` 的命名常量,`secondNumber` 是值 `42` 的命名常量。现在这两个常量都可以独立使用:

```swift
print("第一个数字是 \(firstNumber)。") // 打印 "第一个数字是 10。" 
print("第二个数字是 \(secondNumber)。") // 打印 "第二个数字是 42。"
```

当常量的类型可以被推断时,类型注解 (`:` *类型*) 在常量声明中是可选的,如 <doc:Types#Type-Inference> 中所述。

要声明常量类型属性,请使用 `static` 声明修饰符标记声明。类的常量类型属性总是隐式 final 的;你不能使用 `class` 或 `final` 声明修饰符来允许或禁止子类重写。类型属性在 <doc:Properties#Type-Properties> 中有讨论。

有关常量的更多信息以及何时使用它们的指导,请参阅 <doc:TheBasics#Constants-and-Variables> 和 <doc:Properties#Stored-Properties>。

> 常量声明的语法:
> > *常量声明* → *属性*_?_ *声明修饰符*_?_ **`let`** *模式初始化器列表*
> > *模式初始化器列表* → *模式初始化器* | *模式初始化器* **`,`** *模式初始化器列表*
> *模式初始化器* → *模式* *初始化器*_?_
> *初始化器* → **`=`** *表达式*

## 变量声明

变量声明是在程序中引入可变变量的重要方式,使用 `var` 关键字声明。

变量声明有几种形式,用于声明不同种类的命名可变值,包括存储变量和计算变量以及属性、存储变量和属性观察器,以及静态变量属性。使用哪种形式取决于变量声明的作用域以及你打算声明的变量类型。

> 注意:除了在类和结构中,还可以在协议声明的上下文中声明属性,如 <doc:Declarations#Protocol-Property-Declaration> 所述。

子类也可以通过在子类的属性声明中使用 `override` 声明修饰符来重写属性,如 <doc:Inheritance#Overriding> 所述。

### 存储变量和存储变量属性

存储变量和存储变量属性通过以下形式声明:

```swift var <#变量名称#>: <#类型#> = <#表达式#>```

存储变量和存储变量属性可以在全局作用域、函数的本地作用域或类或结构声明的上下文中定义。在全局作用域或函数的本地作用域中声明时,它被称为存储变量。在类或结构声明的上下文中声明时,它被称为存储变量属性。

在协议声明中不能出现初始化器*表达式*,但在所有其他上下文中,初始化器*表达式*是可选的。也就是说,如果没有提供初始化器*表达式*,变量声明必须包含显式类型注解(`:` *类型*)。

与常量声明一样,如果变量声明省略了初始化器表达式,则必须在第一次读取前为变量赋值。与常量声明一样,如果*变量名称*是一个元组模式,则每个元组项的名称都绑定到初始化器*表达式*中相应的值。

顾名思义,存储变量或存储变量属性的值存储在内存中。

### 计算变量和计算属性

计算变量和计算属性通过以下形式声明:

```swift var <#变量名称#>: <#类型#> { get { <#语句#> } set(<#设置值名称#>) { <#语句#> } }```

计算变量和计算属性可以在全局作用域、函数的本地作用域或类、结构、枚举或扩展声明的上下文中定义。在全局作用域或函数的本地作用域中声明时,它被称为计算变量。在类、结构或扩展声明的上下文中声明时,它被称为计算属性。

不同于存储变量和存储变量属性,计算变量或计算属性的值不存储在内存中。getter 用于读取值,setter 用于写入值。setter 子句是可选的,当只需要 getter 时,你可以省略两个子句,直接返回请求的值,如 <doc:Properties#Read-Only-Computed-Properties> 所述。但是,如果你提供了 setter 子句,你也必须提供 getter 子句。

*设置值名称*和包围的括号是可选的。如果你提供了设置值名称,它将用作 setter 的参数名称。如果你没有提供设置值名称,则 setter 的默认参数名称为 `newValue`,如 <doc:Properties#Shorthand-Setter-Declaration> 所述。

有关更多信息和计算属性示例,请参阅 <doc:Properties#Computed-Properties>。

### 存储变量观察器和属性观察器

除了上述形式,还可以通过以下方式声明存储变量或属性,使用 `willSet` 和 `didSet` 观察器:

```swift var <#变量名称#>: <#类型#> = <#表达式#> { willSet(<#设置值名称#>) { <#语句#> } didSet(<#设置值名称#>) { <#语句#> } }```

在不同作用域中,你可以使用 willSet 和 didSet 来定义变量声明。在全局作用域或函数的局部作用域中,这种观察器被称为存储变量观察器。而在类或结构体声明的上下文中,则被称为属性观察器。

你可以为任何存储属性添加属性观察器。你还可以通过在子类中重写属性(如<doc:Inheritance#Overriding-Property-Observers>中所述),为任何继承的属性(无论是存储属性还是计算属性)添加属性观察器。

在类或结构体声明的上下文中,初始化表达式是可选的,但在其他地方是必需的。当类型可以从初始化表达式推断出来时,类型注释是可选的。第一次读取属性值时,将评估此表达式。如果在读取之前对属性值进行了赋值,则在第一次写入属性之前将评估此表达式。

willSet 和 didSet 观察器提供了一种观察(并适当响应)变量或属性值被设置时的方式。在初始化上下文中不会调用这些观察器。相反,它们只在值在初始化上下文之外被设置时才会被调用。

willSet 观察器在变量或属性的值被设置之前调用。新值作为常量传递给 willSet 观察器,因此无法在 willSet 子句的实现中更改它。didSet 观察器在新值设置后立即调用。不过,didSet 观察器获取的是旧值。如果你在 didSet 观察器子句中重新为变量或属性赋值,新值将覆盖刚传递给 willSet 观察器的值。

willSet 和 didSet 子句中的 setter 名称和括号是可选的。如果你提供 setter 名称,它们将用作 willSet 和 didSet 观察器的参数名称。如果你不提供 setter 名称,则 willSet 观察器的默认参数名称为 newValue,didSet 观察器的默认参数名称为 oldValue。

当你提供 willSet 子句时,didSet 子句是可选的。同样,当你提供 didSet 子句时,willSet 子句是可选的。

如果 didSet 观察器需要访问旧值,则在观察器之前调用 getter,以使旧值可用。否则,新值将被存储而不调用超类的 getter。下面的示例显示了一个由超类定义并由其子类重写以添加观察器的计算属性。

```swift
class Superclass {
    private var xValue = 12
    var x: Int {
        get {
            print("Getter was called")
            return xValue
        }
        set {
            print("Setter was called") 
            xValue = newValue
        }
    }
}

// 这个子类在其观察器中不引用 oldValue,因此超类的 getter 只被调用一次来打印值。
class New: Superclass {
    override var x: Int {
        didSet {
            print("New value \(x)")
        }
    }
}
let new = New()
new.x = 100 // 打印 "Setter was called"
            // 打印 "Getter was called"
            // 打印 "New value 100" 

// 这个子类在其观察器中引用了 oldValue,因此在 setter 之前调用一次超类的 getter,并再次调用以打印值。
class NewAndOld: Superclass {
    override var x: Int {
        didSet {
            print("Old value \(oldValue) - new value \(x)")
        }
    }
}
let newAndOld = NewAndOld()
newAndOld.x = 200 // 打印 "Getter was called" 
                  // 打印 "Setter was called"
                  // 打印 "Getter was called"
                  // 打印 "Old value 12 - new value 200"
```

以下是改进后的翻译:

<!-- - test: `didSet-calls-superclass-getter`

  ```swifttest -> class Superclass { private var xValue = 12 var x: Int { get { print("获取器被调用"); return xValue } set { print("设置器被调用"); xValue = newValue } } } --- // 这个子类在它的观察器中没有引用 oldValue，所以父类的获取器只被调用一次来打印值。
  -> class New: Superclass { override var x: Int { didSet { print("新值 \(x)") } } } let new = New() new.x = 100 <- 设置器被调用 <- 获取器被调用 <- 新值 100 --- // 这个子类在它的观察器中引用了 oldValue，所以父类的获取器在设置器之前被调用一次，然后再次被调用来打印值。
  -> class NewAndOld: Superclass { override var x: Int { didSet { print("旧值 \(oldValue) - 新值 \(x)") } } } let newAndOld = NewAndOld() newAndOld.x = 200 <- 获取器被调用 <- 设置器被调用 <- 获取器被调用 <- 旧值 12 - 新值 200 ``` -->

有关更多信息以及如何使用属性观察器的示例，请参阅 <doc:Properties#Property-Observers>。

<!-- - test: `cant-mix-get-set-and-didSet`

  ```swifttest >> struct S { >>     var x: Int { >>         get { print("S 获取器"); return 12 } >>         set { return } >>         didSet { print("S didSet") } >>     } >> } !$ error: 'didSet' 不能与获取器一起提供 !! didSet { print("S didSet") } !! ^ ``` -->

### 类型变量属性

要声明一个类型变量属性，请使用 `static` 声明修饰符标记声明。
类可以使用 `class` 声明修饰符而不是 `static` 来标记类型计算属性，以允许子类重写超类的实现。
类型属性在 <doc:Properties#Type-Properties> 中有讨论。

变量声明的语法:

> *variable-declaration* → *variable-declaration-head* *pattern-initializer-list* \
*variable-declaration* → *variable-declaration-head* *variable-name* *type-annotation* *code-block* \
*variable-declaration* → *variable-declaration-head* *variable-name* *type-annotation* *getter-setter-block* \  
*variable-declaration* → *variable-declaration-head* *variable-name* *type-annotation* *getter-setter-keyword-block* \
*variable-declaration* → *variable-declaration-head* *variable-name* *initializer* *willSet-didSet-block* \
*variable-declaration* → *variable-declaration-head* *variable-name* *type-annotation* *initializer*? *willSet-didSet-block*

*variable-declaration-head* → *attributes*? *declaration-modifiers*? **`var`** \
*variable-name* → *identifier*

*getter-setter-block* → *code-block* \
*getter-setter-block* → **`{`** *getter-clause* *setter-clause*? **`}`** \
*getter-setter-block* → **`{`** *setter-clause* *getter-clause* **`}`** \
*getter-clause* → *attributes*? *mutation-modifier*? **`get`** *code-block* \
*setter-clause* → *attributes*? *mutation-modifier*? **`set`** *setter-name*? *code-block* \
*setter-name* → **`(`** *identifier* **`)`**

*getter-setter-keyword-block* → **`{`** *getter-keyword-clause* *setter-keyword-clause*? **`}`** \
*getter-setter-keyword-block* → **`{`** *setter-keyword-clause* *getter-keyword-clause* **`}`** \
*getter-keyword-clause* → *attributes*? *mutation-modifier*? **`get`** \
*setter-keyword-clause* → *attributes*? *mutation-modifier*? **`set`**

*willSet-didSet-block* → **`{`** *willSet-clause* *didSet-clause*? **`}`** \
*willSet-didSet-block* → **`{`** *didSet-clause* *willSet-clause*? **`}`** \
*willSet-clause* → *attributes*? **`willSet`** *setter-name*? *code-block* \
*didSet-clause* → *attributes*? **`didSet`** *setter-name*? *code-block*

<!-- 注意:计算属性需要类型注解 - 这些属性的类型不是计算/推断的。 -->

## 类型别名声明

*类型别名声明* 将一个现有类型的命名别名引入你的程序。
类型别名声明使用 `typealias` 关键字声明,格式如下:

```swift typealias <#name#> = <#existing type#> ```

在声明类型别名后,可以在程序中任何地方使用别名 *name* 代替 *existing type*。
*existing type* 可以是命名类型或复合类型。
类型别名不会创建新类型;它们只是允许一个名称引用现有类型。

类型别名声明可以使用泛型参数为现有泛型类型提供一个名称。类型别名可以为现有类型的某些或全部泛型参数提供具体类型。
例如:

```swift typealias StringDictionary<Value> = Dictionary<String, Value>

// 以下字典具有相同的类型。
var dictionary1: StringDictionary<Int> = [:] 
var dictionary2: Dictionary<String, Int> = [:]
```

<!-- - test: `typealias-with-generic`

  ```swifttest 
  -> typealias StringDictionary<Value> = Dictionary<String, Value>
  ---
  // 以下字典具有相同的类型。
  -> var dictionary1: StringDictionary<Int> = [:] 
  -> var dictionary2: Dictionary<String, Int> = [:]
  ```
-->

当使用泛型参数声明类型别名时,这些参数的约束必须与现有类型的泛型参数的约束完全匹配。
例如:

```swift
typealias DictionaryOfInts<Key: Hashable> = Dictionary<Key, Int>
```

<!-- - test: `typealias-with-generic-constraint`

由于类型别名和现有类型可以互换使用,因此类型别名不能引入额外的泛型约束。

类型别名可以通过省略声明中的所有泛型参数来转发现有类型的泛型参数。例如,这里声明的 `Diccionario` 类型别名具有与 `Dictionary` 相同的泛型参数和约束。

```swift
typealias Diccionario = Dictionary
```

在协议声明中,类型别名可以为经常使用的类型提供一个更短、更方便的名称。例如:

```swift
protocol Sequence {
    associatedtype Iterator: IteratorProtocol
    typealias Element = Iterator.Element
}

func sum<T: Sequence>(_ sequence: T) -> Int where T.Element == Int {
    // ...
}
```

如果没有这个类型别名,`sum` 函数会将关联类型称为 `T.Iterator.Element` 而不是 `T.Element`。

请参阅 <doc:Declarations#Protocol-Associated-Type-Declaration>。

> 类型别名声明的语法:
>
> *typealias-declaration* → *attributes*_?_ *access-level-modifier*_?_ **`typealias`** *typealias-name* *generic-parameter-clause*_?_ *typealias-assignment*
>
> *typealias-name* → *identifier*
>
> *typealias-assignment* → **`=`** *type*

## 函数声明

*函数声明* 将函数或方法引入到你的程序中。在类、结构体、枚举或协议上下文中声明的函数被称为 *方法*。函数声明使用 `func` 关键字,形式如下:

```swift
func <#函数名称#>(<#参数#>) -> <#返回类型#> {
    <#语句#>
}
```

如果函数的返回类型是 `Void`,可以省略返回类型,如下所示:

```swift
func <#函数名称#>(<#参数#>) {
    <#语句#>
}
```

每个参数的类型都必须显式声明,不能被推断出来。如果在参数类型前面写 `inout`,该参数可以在函数作用域内被修改。In-out 参数将在下面的 <doc:Declarations#In-Out-Parameters> 中详细讨论。

如果 *语句* 只包含单个表达式,该函数声明会返回该表达式的值。只有当表达式的类型和函数的返回类型都不是 `Void` 且不是没有任何案例的枚举(如 `Never`)时,才考虑使用这种隐式返回语法。

函数可以使用元组类型作为函数的返回类型来返回多个值。

函数定义可以出现在另一个函数声明中。这种函数被称为 *嵌套函数*。

如果嵌套函数捕获了一个永远不会逃逸的值(例如 in-out 参数)或作为非逃逸函数参数传递的值,则该嵌套函数是非逃逸的。否则,嵌套函数是一个逃逸函数。

有关嵌套函数的讨论,请参阅 <doc:Functions#Nested-Functions>。

### 参数名称

### 参数名称

函数参数是由逗号分隔的列表组成,每个参数可以采用以下几种形式之一。在函数调用中,参数的顺序必须与函数声明中参数的顺序相匹配。参数列表中最简单的形式如下:

```swift <#参数名称#>: <#参数类型#>```

参数有一个名称,在函数体内使用,以及一个参数标签,在调用函数或方法时使用。默认情况下,参数名称也用作参数标签。例如:

```swift func f(x: Int, y: Int) -> Int { return x + y } f(x: 1, y: 2) // x 和 y 都有标签```

我们可以使用以下其中一种形式覆盖参数标签的默认行为:

```swift <#参数标签#> <#参数名称#>: <#参数类型#> _ <#参数名称#>: <#参数类型#>```

在参数名称之前的名称为参数提供了一个显式的参数标签,可以与参数名称不同。相应的参数必须在函数或方法调用中使用给定的参数标签。

参数名称前的下划线(`_`)会抑制参数标签。相应的参数在函数或方法调用中必须没有标签。

```swift func repeatGreeting(_ greeting: String, count n: Int) { /* 重复问候 n 次 */ } repeatGreeting("你好,世界!",count: 2) // count 有标签,greeting 没有```

### 参数修饰符

*参数修饰符*改变了参数传递给函数的方式。

```swift <#参数标签#> <#参数名称#>: <#参数修饰符#> <#参数类型#>```

要使用参数修饰符,请在参数类型之前写入 `inout`、`borrowing` 或 `consuming`。

```swift func someFunction(a: inout A, b: consuming B, c: C) { ... }```

#### 输入输出参数

默认情况下,Swift 中的函数参数是按值传递的:函数内部对参数所做的修改,在调用者那里是不可见的。要使参数成为输入输出参数,请应用 `inout` 参数修饰符。

```swift func someFunction(a: inout Int) { a += 1 }```

调用包含输入输出参数的函数时,输入输出参数必须加上前缀 `&` 以标记该函数调用可以更改参数的值。

```swift var x = 7 someFunction(&x) print(x) // 打印 "8"```

输入输出参数的传递方式如下:

1. 调用函数时,参数值被复制。
2. 在函数体内,复制的值被修改。
3. 函数返回时,复制值被赋给原始参数。

这种行为称为*复制输入复制输出*或*按值结果调用*。例如,当计算属性或具有观察器的属性作为输入输出参数传递时,它的 getter 会在函数调用时被调用,它的 setter 会在函数返回时被调用。

作为一种优化,当存储在内存中的值作为参数传递时,函数体内外使用相同的内存位置。这种优化行为称为*按引用调用*;它满足复制输入复制输出模型的所有要求,同时消除了复制的开销。编写代码时应使用复制输入复制输出模型,不要依赖于按引用调用优化,这样无论是否进行优化,代码都能正确运行。

在函数内部,不要访问作为输入输出参数传递的值,即使原始值在当前作用域中可用,因为这会违反内存独占性。访问原始值会同时访问该值,这违反了内存独占性。

```swift var someValue: Int func someFunction(a: inout Int) { a += someValue }

在 Swift 中,当你试图同时访问和修改同一个内存位置时,就会发生"独占性违规"错误。这通常发生在将同一个 inout 参数传递给多个函数或闭包时。例如:

```swift
var someValue = 42
someFunction(&someValue)  // 错误: 这会导致运行时独占性违规
```

你不能将同一个值传递给多个 inout 参数,因为这样做会违反内存独占性规则。

```swift  
var someValue = 0
func someFunction(a: inout Int, b: inout Int) {
    a += b
    b += 1
}

someFunction(&someValue, &someValue) // 错误: 不能将同一个值传递给多个 inout 参数
```

有关内存安全和内存独占性的更多信息,请参阅 <doc:MemorySafety>。

捕获 inout 参数的闭包或嵌套函数必须是非逃逸的。如果你需要捕获一个 inout 参数而不改变它,请使用捕获列表来显式地不可变捕获该参数。

```swift
func someFunction(a: inout Int) -> () -> Int {
    return { [a] in
        return a + 1
    }
}
```

如果你需要捕获和改变一个 inout 参数,请使用一个显式的本地副本,例如在多线程代码中,确保在函数返回之前所有的变异都已完成。

```swift
func multithreadedFunction(queue: DispatchQueue, x: inout Int) {
    // 创建一个本地副本,并在返回前手动复制回去
    var localX = x
    defer { x = localX }

    // 异步操作 localX,然后等待完成后再返回
    queue.async { someMutatingOperation(&localX) }
    queue.sync {}
}
```

有关 inout 参数的更多讨论和示例,请参阅 <doc:Functions#In-Out-Parameters>。

#### 借用和消费参数

默认情况下,Swift 使用一组规则自动管理跨函数调用的对象生命周期,在需要时复制值。默认规则旨在最小化大多数情况下的开销 - 如果你需要更具体的控制,可以应用 `borrowing` 或 `consuming` 参数修饰符。在这种情况下,使用 `copy` 来显式标记复制操作。

无论你是否使用默认规则,Swift 都能保证在所有情况下正确管理对象生命周期和所有权。这些参数修饰符只影响特定用法模式的相对效率,而不影响正确性。

`borrowing` 修饰符表示函数不会保留参数的值,只是临时借用。在这种情况下,调用者保留对象的所有权和对象生命周期的责任。当函数只是短暂使用对象时,使用 `borrowing` 可以最小化开销,避免不必要的复制。例如,你可以将 `borrowing` 应用于只读取但不修改参数值的函数。

在 Swift 中，`isLessThan` 不会保留任何一个参数的值。

```swift
func isLessThan(lhs: borrowing A, rhs: borrowing A) -> Bool {
    ...
}
```

如果函数需要保留参数的值，例如将其存储在全局变量中，你需要使用 `copy` 来显式复制该值。

```swift 
// 与上面相同, 但这个 `isLessThan` 也想记录最小值
func isLessThan(lhs: borrowing A, rhs: borrowing A) -> Bool {
    if lhs < storedValue {
        storedValue = copy lhs
    } else if rhs < storedValue {
        storedValue = copy rhs
    }
    return lhs < rhs
}
```

相反，`consuming` 参数修饰符表示函数获取该值的所有权，并负责在函数返回之前存储或销毁它。

```swift
// `store` 保留其参数, 因此将其标记为 `consuming` 
func store(a: consuming A) {
    someGlobalVariable = a
}
```

使用 `consuming` 可以在调用者不再需要在函数调用后使用该对象时最小化开销。

```swift
// 通常, 这是你对一个值做的最后一件事
store(a: value)
```

如果你在函数调用后继续使用一个可复制的对象，编译器会在函数调用之前自动复制该对象。

```swift
// 编译器在这里插入了一个隐式复制
store(a: someValue)  // 此函数消费 someValue
print(someValue)  // 这使用了 someValue 的副本
```

与 `inout` 不同，`borrowing` 和 `consuming` 参数在调用函数时不需要任何特殊标记:

```swift
func someFunction(a: borrowing A, b: consuming B) {
    ...
}

someFunction(a: someA, b: someB)
```

显式使用 `borrowing` 或 `consuming` 表明你打算更严格地控制运行时所有权管理的开销。因此，使用这些修饰符标记的参数不能被复制，除非你使用显式的 `copy` 关键字:

```swift
func borrowingFunction1(a: borrowing A) {
    // 错误: 不能隐式复制 a
    // 此赋值需要复制, 因为 `a` 只是从调用者那里借用的
    someGlobalVariable = a
}

func borrowingFunction2(a: borrowing A) {
    // 正确: 显式复制可以工作
    someGlobalVariable = copy a
}

func consumingFunction1(a: consuming A) {
    // 错误: 不能隐式复制 a
    // 此赋值需要复制, 因为下面的 `print`
    someGlobalVariable = a
    print(a)
}

func consumingFunction2(a: consuming A) {
    // 正确: 无论如何显式复制都可以工作
    someGlobalVariable = copy a
    print(a)
}

func consumingFunction3(a: consuming A) {
    // 正确: 这里不需要复制, 因为这是对该值的最后使用
    someGlobalVariable = a
}
```

使用以下形式可以忽略参数、接受可变数量的值以及提供默认值:

```swift
_: <#参数类型#>
<#参数名称#>: <#参数类型#>...
<#参数名称#>: <#参数类型#> = <#默认参数值#>
```

下划线 (`_`) 参数被显式忽略，无法在函数体内访问。

紧跟基本类型名称后面的三个点 (`...`) 表示这是一个可变参数。紧跟在可变参数后面的参数必须有一个参数标签。一个函数可以有多个可变参数。可变参数被视为包含基本类型元素的数组。例如，可变参数 `Int...` 被视为 `[Int]`。有关使用可变参数的示例，请参阅 <doc:Functions#Variadic-Parameters>。

在类型后面带有等号 (`=`) 和表达式的参数被理解为具有给定表达式的默认值。给定的表达式在调用函数时求值。如果在调用函数时省略了该参数，则使用默认值。

```swift
func f(x: Int = 42) -> Int { return x }
f()       // 有效, 使用默认值  
f(x: 7)   // 有效, 使用提供的值
f(7)      // 无效, 缺少参数标签
```

枚举或结构体上修改 `self` 的方法必须使用 `mutating` 声明修饰符标记。

重写超类方法的方法必须使用 `override` 声明修饰符标记。如果没有 `override` 修饰符重写方法或在不重写超类方法的方法上使用 `override` 修饰符,都会导致编译时错误。

对于枚举和结构体,与类型相关而不是与类型实例相关的方法必须使用 `static` 声明修饰符标记。对于类,则必须使用 `static` 或 `class` 声明修饰符标记。使用 `class` 声明修饰符标记的类型方法可以被子类实现重写;使用 `class final` 或 `static` 标记的类型方法则不能被重写。

有几种特殊名称的方法可以启用函数调用语法的语法糖。如果一个类型定义了这些方法中的一个,该类型的实例就可以使用函数调用语法。函数调用被理解为对该实例上的特殊命名方法之一的调用。

类、结构体或枚举类型可以通过定义 `dynamicallyCall(withArguments:)` 方法或 `dynamicallyCall(withKeywordArguments:)` 方法来支持函数调用语法,如 <doc:Attributes#dynamicCallable> 所述。或者通过定义一个 call-as-function 方法,如下所述。

如果类型同时定义了 call-as-function 方法和 `dynamicCallable` 属性使用的其中一个方法,编译器在任何一个方法都可以使用的情况下会优先选择 call-as-function 方法。

call-as-function 方法的名称是 `callAsFunction()`。或者以 `callAsFunction(` 开头并添加带标签或不带标签的参数的其他名称 —— 例如,`callAsFunction(_:_:)` 和 `callAsFunction(something:)` 也是有效的 call-as-function 方法名称。

以下函数调用是等价的:

call-as-function 方法和 `dynamicCallable` 属性的方法在将信息编码到类型系统以及运行时可能的动态行为之间做出了不同的权衡。call-as-function 方法需要指定参数的数量、每个参数的类型和标签。而 `dynamicCallable` 属性的方法只需指定用于保存参数数组的类型。

以下函数调用是等价的:

```swift
struct CallableStruct {
    var value: Int
    func callAsFunction(_ number: Int, scale: Int) {
        print(scale * (number + value))
    }
}

let callable = CallableStruct(value: 100)
callable(4, scale: 2)
callable.callAsFunction(4, scale: 2) // 两个函数调用都会打印 208。
```

定义一个 call-as-function 方法或 `dynamicCallable` 属性的方法并不会让你在除函数调用表达式之外的任何上下文中将该类型的实例当作函数使用。例如:

```swift
let someFunction1: (Int, Int) -> Void = callable(_:scale:)  // 错误
let someFunction2: (Int, Int) -> Void = callable.callAsFunction(_:scale:)
```

`subscript(dynamicMember:)` 下标运算符启用了成员查找的语法糖，如 <doc:Attributes#dynamicMemberLookup> 中所述。

可以抛出错误的函数和方法必须用 `throws` 关键字标记。这些函数和方法被称为*抛出函数*和*抛出方法*。它们的形式如下:

```swift
func <#函数名称#>(<#参数#>) throws -> <#返回类型#> {
    <#语句#>
}
```

抛出特定错误类型的函数的形式如下:

```swift
func <#函数名称#>(<#参数#>) throws(<#错误类型#>) -> <#返回类型#> {
    <#语句#>
}
```

对抛出函数或方法的调用必须包裹在 `try` 或 `try!` 表达式中(即在 `try` 或 `try!` 运算符的作用域内)。

函数的类型包括它是否可以抛出错误以及抛出什么类型的错误。这种子类型关系意味着，例如，你可以在期望抛出函数的上下文中使用非抛出函数。有关抛出函数类型的更多信息，请参阅 <doc:Types#Function-Type>。有关使用具有显式类型的错误的示例，请参阅 <doc:ErrorHandling#Specifying-the-Error-Type>。

你不能仅基于函数是否可以抛出错误来重载函数。不过，你可以基于函数*参数*是否可以抛出错误来重载函数。

抛出方法不能重写非抛出方法，抛出方法也不能满足非抛出方法的协议要求。但是，非抛出方法可以重写抛出方法，非抛出方法可以满足抛出方法的协议要求。

可以使用 `rethrows` 关键字声明一个函数或方法，以指示它只在其函数参数之一抛出错误时才抛出错误。这些函数和方法被称为*重新抛出函数*和*重新抛出方法*。重新抛出函数和方法必须至少有一个抛出函数参数。

一个重新抛出的函数或方法只能在 `catch` 子句内包含 `throw` 语句。这让你可以在 `do`-`catch` 语句中调用抛出函数,并在 `catch` 子句中通过抛出不同的错误来处理错误。此外,`catch` 子句必须只处理由重新抛出函数的抛出参数之一抛出的错误。例如,以下代码无效,因为 `catch` 子句将处理由 `alwaysThrows()` 抛出的错误。

```swift
func alwaysThrows() throws { throw SomeError.error }
func someFunction(callback: () throws -> Void) rethrows {
    do {
        try callback()
        try alwaysThrows()  // 无效,alwaysThrows() 不是抛出参数
    } catch {
        throw AnotherError.error
    }
}
```

抛出方法不能重写重新抛出方法,抛出方法也不能满足重新抛出方法的协议要求。相反,重新抛出方法可以重写抛出方法,重新抛出方法可以满足抛出方法的协议要求。

重新抛出的替代方案是在泛型代码中抛出特定的错误类型。例如:

```swift
func someFunction<E: Error>(callback: () throws(E) -> Void) throws(E) {
    try callback()
}
```

这种传播错误的方法保留了有关错误的类型信息。但是,与标记函数 `rethrows` 不同,这种方法不会阻止函数抛出同一类型的错误。

### 异步函数和方法

运行异步的函数和方法必须用 `async` 关键字标记。这些函数和方法被称为*异步函数*和*异步方法*。它们的形式如下:

```swift
func <#函数名称#>(<#参数#>) async -> <#返回类型#> {
    <#语句#>
}
```

对异步函数或方法的调用必须包裹在 `await` 表达式中 --- 也就是说,它们必须在 `await` 运算符的作用域内。

`async` 关键字是函数类型的一部分,同步函数是异步函数的子类型。因此,你可以在需要异步函数的上下文中使用同步函数。例如,你可以用同步方法重写异步方法,同步方法可以满足需要异步方法的协议要求。

你可以根据函数是否异步来重载函数。在调用站点,上下文决定使用哪个重载:在异步上下文中使用异步函数,在同步上下文中使用同步函数。

异步方法不能重写同步方法,异步方法也不能满足同步方法的协议要求。相反,同步方法可以重写异步方法,同步方法可以满足异步方法的协议要求。

### 永不返回的函数及其用途

Swift 定义了 [`Never`][] 类型,表示一个函数或方法不会返回到它的调用者。
具有 `Never` 返回类型的函数和方法被称为*永不返回*。
永不返回的函数和方法要么会导致不可恢复的错误,要么开始一个无限继续的工作序列。
这意味着本来会在调用之后立即执行的代码永远不会被执行。
即使是永不返回的函数,抛出和重新抛出的函数也可以将程序控制权转移到适当的 `catch` 块。

[`Never`]: https://developer.apple.com/documentation/swift/never

永不返回的函数或方法可以被调用来结束 guard 语句的 `else` 子句,如 <doc:Statements#Guard-Statement> 中所讨论的。

你可以重写一个永不返回的方法,但新方法必须保留其返回类型和永不返回的行为。

> 函数声明的语法:
> > *function-declaration* → *function-head* *function-name* *generic-parameter-clause*_?_ *function-signature* *generic-where-clause*_?_ *function-body*_?_ > > *function-head* → *attributes*_?_ *declaration-modifiers*_?_ **`func`** \ > *function-name* → *identifier* | *operator* > > *function-signature* → *parameter-clause* **`async`**_?_ *throws-clause*_?_ *function-result*_?_ \ > *function-signature* → *parameter-clause* **`async`**_?_ **`rethrows`** *function-result*_?_ \ > *function-result* → **`->`** *attributes*_?_ *type* \ > *function-body* → *code-block* > > *parameter-clause* → **`(`** **`)`** | **`(`** *parameter-list* **`)`** \ > *parameter-list* → *parameter* | *parameter* **`,`** *parameter-list* \ > *parameter* → *external-parameter-name*_?_ *local-parameter-name* *parameter-type-annotation* *default-argument-clause*_?_ \ > *parameter* → *external-parameter-name*_?_ *local-parameter-name* *parameter-type-annotation* \ > *parameter* → *external-parameter-name*_?_ *local-parameter-name* *parameter-type-annotation* **`...`** > > *external-parameter-name* → *identifier* \ > *local-parameter-name* → *identifier* \ > *parameter-type-annotation* → **`:`** *attributes*_?_ *parameter-modifier*_?_ *type* \ > *parameter-modifier* → **`inout`** | **`borrowing`** | **`consuming`** > *default-argument-clause* → **`=`** *expression*

<!-- 注意:在协议的上下文中,代码块是可选的。
  在其他地方,它是必需的。
  我们可以重构,将函数定义/声明分开。
  还有一种低级的 "asm name" FFI,它是一种定义和声明的边角情况。
  让我们在文字中处理这种差异。
-->

## 枚举声明

*枚举声明*将一个命名的枚举类型引入到你的程序中。

枚举声明有两种基本形式,使用 `enum` 关键字声明。
使用任一形式声明的枚举的主体包含零个或多个值 --- 称为*枚举案例* --- 以及任意数量的声明,包括计算属性、实例方法、类型方法、初始化器、类型别名,甚至其他枚举、结构体、类和 actor 声明。
枚举声明不能包含析构器或协议声明。

枚举类型可以采纳任意数量的协议,但不能继承自类、结构体或其他枚举。

与类和结构体不同,枚举类型没有隐式提供的默认初始化器;
所有初始化器都必须显式声明。初始化器可以委托给枚举中的其他初始化器,但只有在初始化器将枚举案例之一赋值给 `self` 后,初始化过程才算完成。

与类不同,枚举是值类型,但与结构体相似,当赋值给变量或常量时,或作为参数传递给函数调用时,枚举的实例会被复制。有关值类型的信息,请参阅<doc:ClassesAndStructures#Structures-and-Enumerations-Are-Value-Types>。

您可以使用扩展声明来扩展枚举类型的行为,如<doc:Declarations#Extension-Declaration>中所讨论的。

### 任意类型的枚举案例

以下形式声明了一个包含任意类型枚举案例的枚举类型:

```swift
enum <#枚举名称#>: <#采用的协议#> {
    case <#枚举案例1#>
    case <#枚举案例2#>(<#关联值类型#>)
}
```

用这种形式声明的枚举在其他编程语言中有时被称为*discriminated unions*。

在这种形式中,每个 case 块由`case`关键字后跟一个或多个由逗号分隔的枚举案例组成。每个案例的名称必须是唯一的。每个案例也可以指定它存储给定类型的值。这些类型在*关联值类型*元组中指定,紧跟在案例名称之后。

存储关联值的枚举案例可以用作创建具有指定关联值的枚举实例的函数。就像函数一样,您可以获取对枚举案例的引用,并在代码中稍后应用它。

```swift
enum Number {
    case integer(Int)
    case real(Double)
}
let f = Number.integer // f 是类型为 (Int) -> Number 的函数

// 应用 f 创建一个包含整数值的 Number 实例数组
let evenInts: [Number] = [0, 2, 4, 6].map(f)
```

有关带关联值类型的案例的更多信息和示例,请参阅<doc:Enumerations#Associated-Values>。

#### 带间接引用的枚举

枚举可以具有递归结构,也就是说,它们可以有关联值为枚举类型自身实例的案例。然而,枚举类型的实例具有值语义,这意味着它们在内存中有固定的布局。为了支持递归,编译器必须插入一层间接引用。

要为特定的枚举案例启用间接引用,请使用`indirect`声明修饰符对其进行标记。一个间接案例必须有一个关联值。

```swift
enum Tree<T> {
    case empty
    indirect case node(value: T, left: Tree, right: Tree)
}
```

要为具有关联值的枚举的所有案例启用间接引用,请使用`indirect`修饰符标记整个枚举——当枚举包含许多需要用`indirect`修饰符标记的案例时,这很方便。

用`indirect`修饰符标记的枚举可以包含具有关联值的案例和不具有关联值的案例的混合。也就是说,它不能包含任何也标记有`indirect`修饰符的案例。

下面是改进后的翻译:

Swift 中枚举有两种基本形式,一种是不带原始值的简单枚举,另一种是带有原始值类型的枚举。

### 带有原始值类型的枚举案例

以下形式声明了一个枚举类型,其枚举案例具有相同的基本类型:

```swift
enum <#枚举名称#>: <#原始值类型#>, <#采用的协议#> {
    case <#枚举案例1#> = <#原始值1#>
    case <#枚举案例2#> = <#原始值2#>
}
```

在这种形式中,每个 case 块由关键字 `case` 开头,后跟一个或多个由逗号分隔的枚举案例。与简单枚举不同,这里每个案例都有一个相同基本类型的底层值,称为*原始值*。

这些原始值的类型在*原始值类型*中指定,必须表示整数、浮点数、字符串或单个字符。具体来说,*原始值类型*必须符合 `Equatable` 协议,同时符合以下协议之一: `ExpressibleByIntegerLiteral`(用于整数字面量)、`ExpressibleByFloatLiteral`(用于浮点数字面量)、`ExpressibleByStringLiteral`(用于包含任意数量字符的字符串字面量)、`ExpressibleByUnicodeScalarLiteral` 或 `ExpressibleByExtendedGraphemeClusterLiteral`(用于只包含单个字符的字符串字面量)。每个案例必须具有唯一的名称并被分配一个唯一的原始值。

如果原始值类型指定为 `Int`,且你没有显式分配值给案例,它们将被隐式分配值 `0`、`1`、`2` 等等。如果没有显式指定值,每个 `Int` 类型的案例都会被隐式分配一个从前一个案例的原始值自动递增的原始值。

```swift
enum ExampleEnum: Int {
    case a, b, c = 5, d 
}
```

在上面的示例中, `ExampleEnum.a` 的原始值是 `0`, `ExampleEnum.b` 的值是 `1`。由于 `ExampleEnum.c` 的值被显式设置为 `5`, 因此 `ExampleEnum.d` 的值会从 `5` 自动递增,因此是 `6`。

如果原始值类型指定为 `String`,且你没有显式指定值,每个案例都会被隐式分配一个与该案例名称相同的字符串作为原始值。

```swift
enum GamePlayMode: String {
    case cooperative, individual, competitive
}
```

在上面的示例中, `GamePlayMode.cooperative` 的原始值是 `"cooperative"`、`GamePlayMode.individual` 的原始值是 `"individual"`、`GamePlayMode.competitive` 的原始值是 `"competitive"`。

如果枚举的 case 具有原始值类型,它们会隐式遵守 Swift 标准库中定义的 RawRepresentable 协议。这意味着它们拥有一个 rawValue 属性和一个签名为 init?(rawValue: RawValue) 的失败构造器。您可以使用 rawValue 属性访问枚举 case 的原始值,如 ExampleEnum.b.rawValue。您还可以通过调用枚举的可失败初始化器来查找对应的 case(如果存在),如 ExampleEnum(rawValue: 5),它返回一个可选的 case。有关更多信息和查看具有原始值类型的 case 示例,请参阅<doc:Enumerations#Raw-Values>。

### 访问枚举 case

要引用枚举类型的 case,可使用点号(.)语法,如 EnumerationType.enumerationCase。当枚举类型可以从上下文推断时,您可以省略它(但点号仍然需要),如<doc:Enumerations#Enumeration-Syntax>和<doc:Expressions#Implicit-Member-Expression>中所述。

要获取枚举 case 的值,可使用 switch 语句,如<doc:Enumerations#Matching-Enumeration-Values-with-a-Switch-Statement>所示。枚举类型会与 switch 语句 case 块中的枚举 case 模式进行模式匹配,如<doc:Patterns#Enumeration-Case-Pattern>中所述。

枚举声明的语法规则如下:

> *enum-declaration* → *attributes*_?_ *access-level-modifier*_?_ *联合体式枚举* \
> *enum-declaration* → *attributes*_?_ *access-level-modifier*_?_ *原始值式枚举*
>
> *联合体式枚举* → **`indirect`**_?_ **`enum`** *enum-name* *generic-parameter-clause*_?_ *type-inheritance-clause*_?_ *generic-where-clause*_?_ **`{`** *union-style-enum-members*_?_ **`}`** \
> *union-style-enum-members* → *union-style-enum-member* *union-style-enum-members*_?_ \
> *union-style-enum-member* → *declaration* | *union-style-enum-case-clause* | *compiler-control-statement* \
> *union-style-enum-case-clause* → *attributes*_?_ **`indirect`**_?_ **`case`** *union-style-enum-case-list* \
> *union-style-enum-case-list* → *union-style-enum-case* | *union-style-enum-case* **`,`** *union-style-enum-case-list* \
> *union-style-enum-case* → *enum-case-name* *tuple-type*_?_ \
> *enum-name* → *identifier* \
> *enum-case-name* → *identifier*
>
> *原始值式枚举* → **`enum`** *enum-name* *generic-parameter-clause*_?_ *type-inheritance-clause* *generic-where-clause*_?_ **`{`** *raw-value-style-enum-members* **`}`** \
> *raw-value-style-enum-members* → *raw-value-style-enum-member* *raw-value-style-enum-members*_?_ \
> *raw-value-style-enum-member* → *declaration* | *raw-value-style-enum-case-clause* | *compiler-control-statement* \
> *raw-value-style-enum-case-clause* → *attributes*_?_ **`case`** *raw-value-style-enum-case-list* \
> *raw-value-style-enum-case-list* → *raw-value-style-enum-case* | *raw-value-style-enum-case* **`,`** *raw-value-style-enum-case-list* \
> *raw-value-style-enum-case* → *enum-case-name* *raw-value-assignment*_?_ \
> *raw-value-assignment* → **`=`** *raw-value-literal* \
> *raw-value-literal* → *numeric-literal* | *static-string-literal* | *boolean-literal*

## 结构体声明

在你的程序中定义了一个命名的结构体类型。
结构体声明使用 `struct` 关键字声明,形式如下:

```swift struct <#结构体名称#>: <#采纳的协议#> { <#声明#> }```

结构体的主体包含零个或多个*声明*。
这些*声明*可以包括存储属性和计算属性、类型属性、实例方法、类型方法、构造器、下标、类型别名,甚至其他结构体、类、actor 和枚举声明。
结构体声明不能包含析构器或协议声明。
关于包含各种声明的结构体的讨论和示例,请参阅<doc:ClassesAndStructures>。

结构体类型可以采纳任意数量的协议,但不能继承自类、枚举或其他结构体。

有三种方式可以创建之前声明过的结构体的实例:

以下是根据您的要求和反馈进行改进后的翻译:

创建之前声明的结构体实例有三种方式:

- 调用结构体内声明的初始化方法之一,如<doc:Initialization#Initializers>中所述。
- 如果没有声明任何初始化方法,则调用结构体的成员构造初始化方法,如<doc:Initialization#Memberwise-Initializers-for-Structure-Types>中所述。
- 如果没有声明任何初始化方法,并且结构体声明中的所有属性都被赋予了初始值,则调用结构体的默认初始化方法,如<doc:Initialization#Default-Initializers>中所述。

初始化结构体声明的属性的过程在<doc:Initialization>中有描述。

你可以使用点(.)语法访问结构体实例的属性,如<doc:ClassesAndStructures#Accessing-Properties>中所述。

结构体是值类型,因此当将结构体实例赋值给变量或常量,或作为参数传递给函数调用时,都会进行复制。有关值类型的信息,请参阅<doc:ClassesAndStructures#Structures-and-Enumerations-Are-Value-Types>。

你可以使用扩展声明来扩展结构体类型的行为,如<doc:Declarations#Extension-Declaration>中所讨论的。

> 结构体声明的语法:
> > *struct-declaration* → *attributes*_?_ *access-level-modifier*_?_ **`struct`** *struct-name* *generic-parameter-clause*_?_ *type-inheritance-clause*_?_ *generic-where-clause*_?_ *struct-body* \ > *struct-name* → *identifier* \ > *struct-body* → **`{`** *struct-members*_?_ **`}`** > > *struct-members* → *struct-member* *struct-members*_?_ \ > *struct-member* → *declaration* | *compiler-control-statement*

## 类声明

*类声明*将一个命名的类类型引入到你的程序中。
类声明使用`class`关键字声明,格式如下:

```swift class <#类名#>: <#超类#>, <#采纳的协议#> { <#声明#> } ```

类体中包含零个或多个*声明*。这些*声明*可以包括存储属性和计算属性、实例方法、类型方法、初始化方法、单个析构方法、下标、类型别名,甚至其他类、结构体、actor 和枚举声明。类声明不能包含协议声明。有关包含各种声明的类的讨论和几个示例,请参阅<doc:ClassesAndStructures>。

一个类类型只能继承自一个父类,即它的*超类*,但可以采纳任意数量的协议。*超类*在*类名*和冒号之后出现,然后是任何*采纳的协议*。泛型类可以继承自其他泛型和非泛型类,但非泛型类只能继承自其他非泛型类。当你在冒号后写泛型超类类的名称时,你必须包括该泛型类的完整名称,包括其泛型参数子句。

如<doc:Declarations#Initializer-Declaration>中所讨论的,类可以有指定构造器和便利构造器。类的指定构造器必须初始化该类声明的所有属性,并且必须在调用任何超类的指定构造器之前完成初始化。

类可以覆盖其超类的属性、方法、下标和初始化方法。被覆盖的属性、方法、下标和指定构造器必须使用`override`声明修饰符标记。

<!-- - test: `designatedInitializersRequireOverride`

  ```swifttest -> class C { init() {} } -> class D: C { override init() { super.init() } } ``` -->

要确保子类实现超类的初始化方法,可以在超类的初始化方法上使用`required`声明修饰符。子类对该初始化方法的实现也必须使用`required`声明修饰符标记。

尽管*超类*中声明的属性和方法会被当前类继承,但*超类*中声明的指定构造器只有在子类满足<doc:Initialization#Automatic-Initializer-Inheritance>中描述的条件时才会被继承。Swift 类没有继承自通用基类。

创建之前声明的类实例有两种方式:

- 调用类中声明的初始化方法之一,如<doc:Initialization#Initializers>中所述。
- 如果没有声明任何初始化方法,并且类声明中的所有属性都被赋予了初始值,则调用类的默认初始化方法,如<doc:Initialization#Default-Initializers>中所述。

使用点(`.`)语法访问类实例的属性,如<doc:ClassesAndStructures#Accessing-Properties>中所述。

类是引用类型;当实例被赋值给变量或常量,或作为参数传递给函数调用时,它们是被引用而不是被复制的。有关引用类型的信息,请参阅<doc:ClassesAndStructures#Classes-Are-Reference-Types>。

你可以使用扩展声明来扩展类型的行为,如<doc:Declarations#Extension-Declaration>中所讨论的。

> 类声明的语法:
> > *class-declaration* → *attributes*_?_ *access-level-modifier*_?_ **`final`**_?_ **`class`** *class-name* *generic-parameter-clause*_?_ *type-inheritance-clause*_?_ *generic-where-clause*_?_ *class-body* \ > *class-declaration* → *attributes*_?_ **`final`** *access-level-modifier*_?_ **`class`** *class-name* *generic-parameter-clause*_?_ *type-inheritance-clause*_?_ *generic-where-clause*_?_ *class-body* \ > *class-name* → *identifier* \ > *class-body* → **`{`** *class-members*_?_ **`}`** > > *class-members* → *class-member* *class-members*_?_ \ > *class-member* → *declaration* | *compiler-control-statement*

## Actor 声明

*actor 声明*将一个命名的 actor 类型引入到你的程序中。
actor 声明使用`actor`关键字声明,格式如下:

```swift actor <#actor名称#>: <#采纳的协议#> { <#声明#> } ```

actor 所包含的主体包含零个或多个*声明*。
这些*声明*可以包括存储属性和计算属性、实例方法、类型方法、初始化器、单个析构器、下标、类型别名,甚至其他类、结构体和枚举声明。
有关包含各种声明的 actor 的讨论和几个示例,请参阅<doc:Concurrency#Actors>。

actor 类型可以采纳任意数量的协议,但不能继承自类、枚举、结构体或其他 actor。
但是,标记有`@objc`属性的 actor 隐式符合`NSObjectProtocol`协议,并在 Objective-C 运行时作为`NSObject`的子类型公开。

有两种方式可以创建先前声明的 actor 的实例:

- 调用 actor 中声明的初始化器之一,如<doc:Initialization#Initializers>中所述。
- 如果没有声明任何初始化器,并且 actor 声明中的所有属性都被赋予了初始值,则调用 actor 的默认初始化器,如<doc:Initialization#Default-Initializers>中所述。

默认情况下,actor 的成员是隔离在该 actor 中的。
代码(如方法体或属性的 getter)在该 actor 上执行。
actor 内部的代码可以同步与它们交互,因为该代码已经在同一 actor 上运行,但 actor 外部的代码必须使用`await`标记它们,以指示这是在另一个 actor 上异步运行的代码。
关键路径不能引用 actor 的隔离成员。
actor 隔离的存储属性可以作为同步函数的输入输出参数传递,但不能作为异步函数的参数。

actor 也可以有非隔离成员,其声明使用`nonisolated`关键字标记。
非隔离成员的执行方式类似于 actor 外部的代码:
它不能与 actor 的任何隔离状态交互,并且调用者在使用它时不需要标记`await`。

只有当 actor 的成员是非隔离的或异步的时候,才能使用`@objc`属性标记。

actor 声明的属性的初始化过程在<doc:Initialization>中有描述。

可以使用点(`.`)语法访问 actor 实例的属性,如<doc:ClassesAndStructures#Accessing-Properties>中所述。

actor 是引用类型;当实例被赋值给变量或常量,或作为参数传递给函数调用时,它们是被引用而不是被复制的。
有关引用类型的信息,请参阅<doc:ClassesAndStructures#Classes-Are-Reference-Types>。

你可以使用扩展声明来扩展 actor 类型的行为,如<doc:Declarations#Extension-Declaration>中所讨论的。

下面是 actor 声明的语法规则:

> *actor-declaration* → *attributes*_?_ *access-level-modifier*_?_ **`actor`** *actor-name* *generic-parameter-clause*_?_ *type-inheritance-clause*_?_ *generic-where-clause*_?_ *actor-body* \
> *actor-name* → *identifier* \
> *actor-body* → **`{`** *actor-members*_?_ **`}`**
>
> *actor-members* → *actor-member* *actor-members*_?_ \
> *actor-member* → *declaration* | *compiler-control-statement*

## 协议声明

*协议声明*将一个命名的协议类型引入到你的程序中。
协议声明的语法规则如下:

```swift
protocol <#协议名称#>: <#继承的协议#> { <#协议成员声明#> }
```

协议声明可以出现在全局作用域,也可以嵌套在非泛型类型或非泛型函数中。

协议的主体包含零个或多个*协议成员声明*(星号表示该部分是可选的),描述了任何采用该协议的类型必须满足的一致性要求。
特别是,协议可以声明符合该协议的类型必须实现某些属性、方法、初始化器和下标。
协议还可以声明一种特殊的类型别名,称为*关联类型*,可以指定协议中各种声明之间的关系。
协议声明不能包含类、结构体、枚举或其他协议声明。
*协议成员声明*将在下面详细讨论。

协议类型可以继承任意数量的其他协议。
当一个协议类型继承自其他协议时,来自那些其他协议的要求集会被聚合,任何继承当前协议的类型都必须符合所有这些要求。
有关如何使用协议继承的示例,请参阅<doc:Protocols#Protocol-Inheritance>。

注意: 你也可以使用协议组合类型来聚合多个协议的一致性要求,如<doc:Types#Protocol-Composition-Type>和<doc:Protocols#Protocol-Composition>中所述。

你可以通过在该类型的扩展声明中采用协议,为先前声明的类型添加协议一致性。
在扩展中,你必须实现所采用协议的所有要求。如果该类型已经实现了所有要求,则可以将扩展声明的主体留空。

默认情况下,符合协议的类型必须实现协议中声明的所有属性、方法和下标。
不过,你可以使用 `optional` 声明修饰符标记这些协议成员声明,以指定它们在符合类型中的实现是可选的。
`optional` 修饰符只能应用于标记有 `objc` 属性的成员,并且只能应用于标记有 `objc` 属性的协议的成员。因此,只有类类型才能采用和符合包含可选成员要求的协议。
有关如何使用 `optional` 声明修饰符以及如何访问可选协议成员的指导(例如,当你不确定符合类型是否实现它们时),请参阅<doc:Protocols#Optional-Protocol-Requirements>。

<!-- TODO: 目前,你无法检查可选初始化器,因此我们将其从文档中删除,即使你可以使用 @optional 属性标记初始化器。编译器团队仍在讨论这个问题。如果他们决定使一切正常工作于可选初始化器要求,请更新此部分。
-->

枚举的情况可以满足类型成员的协议要求。
具体来说,没有任何关联值的枚举情况满足类型 `Self` 的只读类型变量的协议要求,带有关联值的枚举情况满足返回 `Self` 的函数的协议要求,其参数及其参数标签与该情况的关联值匹配。
例如:

```swift
protocol SomeProtocol {
    static var someValue: Self { get }
    static func someFunction(x: Int) -> Self
}
enum MyEnum: SomeProtocol {
    case someValue
    case someFunction(x: Int)
}
```

<!-- - test: `enum-case-satisfy-protocol-requirement`

  ```swifttest
  -> protocol SomeProtocol {
       static var someValue: Self { get }
       static func someFunction(x: Int) -> Self
     }
  -> enum MyEnum: SomeProtocol {
       case someValue
       case someFunction(x: Int)
     }
  ```
-->

要将协议的采用限制为仅适用于类类型,请在冒号之后的*继承的协议*列表中包含 `AnyObject` 协议。
例如,以下协议只能被类类型采用:

```swift
protocol SomeProtocol: AnyObject {
    /* 协议成员在这里 */
}
```

<!-- - test: `protocol-declaration` -->

任何继承自标注了 `AnyObject` 限制的协议的协议，只能被类类型实现。

> 注意: 如果一个协议被标注了 `objc` 属性，那么 `AnyObject` 限制会被自动添加到该协议上；不需要显式地用 `AnyObject` 限制标注该协议。

协议是有名类型，因此它们可以出现在你代码中与其他有名类型相同的所有位置，如 <doc:Protocols#Protocols-as-Types> 中所讨论的。然而，你不能实例化一个协议，因为协议实际上并没有提供它们定义的要求的实现。

你可以使用协议来声明一个类或结构体的委托应该实现哪些方法，如 <doc:Protocols#Delegation> 中所描述的。

> 协议声明的语法:
> > *协议声明* → *属性*_?_ *访问级别修饰符*_?_ **`protocol`** *协议名称* *类型继承子句*_?_ *泛型 where 子句*_?_ *协议主体* \ > *协议名称* → *标识符* \ > *协议主体* → **`{`** *协议成员*_?_ **`}`** > > *协议成员* → *协议成员声明* *协议成员*_?_ \ > *协议成员* → *编译器控制语句* > > *协议成员声明* → *协议属性声明* \ > *协议成员声明* → *协议方法声明* \ > *协议成员声明* → *协议初始化器声明* \ > *协议成员声明* → *协议下标声明* \ > *协议成员声明* → *协议关联类型声明* \ > *协议成员声明* → *类型别名声明*

### 协议属性声明

协议通过在协议声明主体中包含一个 *协议属性声明* 来声明遵循该协议的类型必须实现一个属性。协议属性声明有一种特殊形式的变量声明:

```swift var <#属性名称#>: <#类型#> { get set } ```

与其他协议成员声明一样，这些属性声明只声明了实现该协议的类型的 getter 和 setter 要求。因此，你不会在声明该协议的协议中直接实现 getter 或 setter。

实现类型可以通过多种方式满足 getter 和 setter 要求。如果一个属性声明包含 `get` 和 `set` 关键字，实现类型可以用一个存储型变量属性或一个可读可写的计算型属性(即实现了 getter 和 setter)来实现它。但是，该属性声明不能被实现为一个常量属性或只读计算型属性。如果一个属性声明只包含 `get` 关键字，它可以被实现为任何类型的属性。

有关实现类型如何实现协议的属性要求的示例，请参阅 <doc:Protocols#Property-Requirements>。

要在协议声明中声明一个类型属性要求，请在属性声明前标记 `static` 关键字。符合该协议的结构体和枚举声明该属性时使用 `static` 关键字，而符合该协议的类则使用 `static` 或 `class` 关键字声明该属性。为结构体、枚举或类添加协议符合性的扩展使用与它们扩展的类型相同的关键字。为类型属性要求提供默认实现的扩展使用 `static` 关键字。

<!-- - test: `protocols-with-type-property-requirements`

  ```swifttest -> protocol P { static var x: Int { get } } -> protocol P2 { class var x: Int { get } } !$ error: class properties are only allowed within classes; use 'static' to declare a requirement fulfilled by either a static or class property !! protocol P2 { class var x: Int { get } } !!              ~~~~~ ^ !!              static -> struct S: P { static var x = 10 } -> class C1: P { static var x = 20 } -> class C2: P { class var x = 30 } !$ error: class stored properties not supported in classes; did you mean 'static'?
  !! class C2: P { class var x = 30 } !!               ~~~~~     ^ ``` -->

<!-- - test: `protocol-type-property-default-implementation`

  ```swifttest
  -> protocol P {
         static var x: Int { get set }
     }
  -> extension P {
         static var x: Int {
             get { return 42 }
             set { }
         }
     }
  -> struct S: P { }
  -> S.x
  <- 42
  ```
-->

以下是根据您的反馈和建议改进后的翻译:

<!-- - test: `protocol-type-property-default-implementation`

  ```swifttest -> protocol P { static var x: Int { get } } -> extension P { static var x: Int { return 100 } } -> struct S1: P { } -> print(S1.x) <- 100 -> struct S2: P { static var x = 10 } -> print(S2.x) <- 10 ``` -->

参见 <doc:Declarations#Variable-Declaration>。

> 协议属性声明的语法:
> > *protocol-property-declaration* → *variable-declaration-head* *variable-name* *type-annotation* *getter-setter-keyword-block*

### 协议方法声明

协议可以通过包含方法声明来要求符合类型实现该方法。协议方法声明的形式与函数声明相同,但不包含函数体,也不能提供默认参数值。有关符合类型实现协议方法要求的示例,请参阅 <doc:Protocols#Method-Requirements>。

要在协议声明中声明类或静态方法要求,请在方法声明前标记 `static` 声明修饰符。符合协议的结构体和枚举使用 `static` 关键字声明该方法,而符合协议的类使用 `static` 或 `class` 关键字声明该方法。为结构体、枚举或类添加协议一致性的扩展,使用与被扩展类型相同的关键字。为类型方法要求提供默认实现的扩展使用 `static` 关键字。

另请参阅 <doc:Declarations#Function-Declaration>。

<!-- TODO: Talk about using ``Self`` in parameters and return types.
-->

> 协议方法声明的语法:
> > *protocol-method-declaration* → *function-head* *function-name* *generic-parameter-clause*_?_ *function-signature* *generic-where-clause*_?_

### 协议构造器声明  

协议可以通过包含构造器声明来要求符合类型实现该构造器。协议构造器声明的形式与构造器声明相同,只是它们不包含构造器的主体。

符合类型可以通过实现一个不可失败的构造器或 `init!` 可失败构造器来满足不可失败的协议构造器要求。符合类型可以通过实现任何类型的构造器来满足可失败的协议构造器要求。

当类实现一个构造器来满足协议的构造器要求时,如果该类没有标记为 `final` 声明修饰符,则该构造器必须标记为 `required` 声明修饰符。

另请参阅 <doc:Declarations#Initializer-Declaration>。

> 协议构造器声明的语法:
> > *protocol-initializer-declaration* → *initializer-head* *generic-parameter-clause*_?_ *parameter-clause* *throws-clause*_?_ *generic-where-clause*_?_ \ > *protocol-initializer-declaration* → *initializer-head* *generic-parameter-clause*_?_ *parameter-clause* **`rethrows`** *generic-where-clause*_?_

### 协议下标声明

协议可以通过包含下标声明来要求符合类型实现该下标。协议下标声明具有下标声明的特殊形式:

```swift subscript (<#parameters#>) -> <#return type#> { get set } ```

下标声明只声明了符合协议的类型的最小 getter 和 setter 实现要求。如果下标声明包含 `get` 和 `set` 关键字,则符合类型必须实现 getter 和 setter 子句。如果下标声明只包含 `get` 关键字,则符合类型必须至少实现一个 getter 子句,并且可以选择实现一个 setter 子句。

要在协议声明中声明静态下标要求,请在下标声明前标记 `static` 声明修饰符。符合协议的结构体和枚举使用 `static` 关键字声明下标,而符合协议的类使用 `static` 或 `class` 关键字声明下标。为静态下标要求提供默认实现的扩展使用 `static` 关键字。

另请参阅 <doc:Declarations#Subscript-Declaration>。

> 协议下标声明的语法:
> > *protocol-subscript-declaration* → *subscript-head* *subscript-result* *generic-where-clause*_?_ *getter-setter-keyword-block*

### 协议关联类型声明

协议使用 `associatedtype` 关键字声明关联类型。关联类型为协议声明中使用的类型提供了一个别名。关联类型与泛型参数子句中的类型参数相似,但它们与声明它们的协议中的 `Self` 相关联。在这种情况下,`Self` 指的是最终符合该协议的类型。欲了解更多信息和示例,请参见 <doc:Generics#Associated-Types>。

在协议声明中,您可以使用泛型 `where` 子句为从另一个协议继承的关联类型添加约束,而无需重新声明这些关联类型。例如,下面的 `SubProtocol` 声明是等价的:

```swift
protocol SomeProtocol { 
    associatedtype SomeType
}

protocol SubProtocolA: SomeProtocol { // 这种语法会产生警告
    associatedtype SomeType: Equatable 
}

// 这种语法更可取
protocol SubProtocolB: SomeProtocol where SomeType: Equatable { }
```

<!-- - test: `protocol-associatedtype`

  ```swifttest 
-> protocol SomeProtocol { 
    associatedtype SomeType
} 
--- 
-> protocol SubProtocolA: SomeProtocol { // 这种语法会产生警告
    associatedtype SomeType: Equatable 
} 
!$ warning: 重新声明从协议 'SomeProtocol' 继承的关联类型 'SomeType' 最好使用协议上的 'where' 子句表达
!! associatedtype SomeType: Equatable
!! ~~~~~~~~~~~~~~~^~~~~~~~~~~~~~~~~~~ 
!!- 
!$ note: 'SomeType' 在这里声明
!! associatedtype SomeType
!! ^
---
// 这种语法更可取 
-> protocol SubProtocolB: SomeProtocol where SomeType: Equatable { }
```-->

<!-- TODO: 完成这一部分的撰写,等待 WWDC 后。
-->

有关类型别名声明的更多信息,另请参阅 <doc:Declarations#Type-Alias-Declaration>。

如文档所述,另请参阅<doc:Declarations#Type-Alias-Declaration>。

> 协议关联类型声明的语法:
> > *协议关联类型声明* → *属性*_?_ *访问级别修饰符*_?_ **`associatedtype`** *类型别名名称* *类型继承子句*_?_ *类型别名赋值*_?_ *泛型 where 子句*_?_

## 构造器声明

*构造器声明*将一个类、结构体或枚举的构造器引入到你的程序中。
构造器声明使用 `init` 关键字声明,有两种基本形式。

对于结构体、枚举和类,它们可以有任意数量的构造器,但类构造器的规则和相关行为与之不同。
与结构体和枚举不同,类有两种构造器:指定构造器和便利构造器,如<doc:Initialization>中所述。

以下形式声明结构体、枚举和类的指定构造器:

```swift init(<#参数#>) { <#语句#> } ```

指定构造器直接初始化该类的所有属性。它不能调用同一类的任何其他构造器,如果该类有超类,则必须调用超类的一个指定构造器。
如果该类从其超类继承了任何属性,则在当前类中设置或修改这些属性之前,必须调用超类的一个指定构造器。

指定构造器只能在类声明的上下文中声明,因此不能使用扩展声明将其添加到类中。

结构体和枚举中的构造器可以调用其他已声明的构造器,以委托部分或全部初始化过程。

要为类声明便利构造器,请在构造器声明上使用 `convenience` 声明修饰符。

```swift convenience init(<#参数#>) { <#语句#> } ```

便利构造器可以将初始化过程委托给另一个便利构造器或该类的一个指定构造器。
也就是说,初始化过程必须以调用一个指定构造器结束,该构造器最终初始化类的属性。
便利构造器不能调用超类的构造器。

您可以使用 `required` 声明修饰符标记指定和便利构造器,以要求每个子类实现该构造器。
子类对该构造器的实现也必须标记有 `required` 声明修饰符。

默认情况下,在超类中声明的构造器不会被子类继承。
也就是说,如果子类使用默认值初始化了所有存储属性,并且没有定义任何自己的构造器,它将继承超类的所有构造器。
如果子类重写了超类的所有指定构造器,它将继承超类的便利构造器。

与方法、属性和下标一样,您需要使用 `override` 声明修饰符标记重写的指定构造器。

> 注意:如果您使用 `required` 声明修饰符标记了一个构造器,
> 在子类中重写该必需构造器时,您不需要再使用 `override` 修饰符标记。

就像函数和方法一样,构造器可以抛出或重新抛出错误。
同样,您使用 `throws` 或 `rethrows` 关键字在构造器的参数之后指示相应的行为。
同样,构造器也可以是异步的,您使用 `async` 关键字来指示这一点。

要查看各种类型声明中构造器的示例,请参阅<doc:Initialization>。

### 可失败构造器

*可失败构造器*是一种构造器,它生成所声明类型的可选实例或隐式解包可选实例。
因此,可失败构造器可以返回 `nil` 以指示初始化失败。

要声明生成可选实例的可失败构造器,请在构造器声明中将问号附加到 `init` 关键字后面(`init?`)。
要声明生成隐式解包可选实例的可失败构造器,请改为附加一个感叹号(`init!`)。下面的示例显示了一个 `init?` 可失败构造器,它生成一个结构体的可选实例。

```swift struct SomeStruct { let property: String // 生成 'SomeStruct' 的可选实例 init?(input: String) { if input.isEmpty { // 丢弃 'self' 并返回 'nil' return nil } property = input } } ```

<!-- - test: `failable`

  ```swifttest -> struct SomeStruct { let property: String // 生成 'SomeStruct' 的可选实例 init?(input: String) { if input.isEmpty { // 丢弃 'self' 并返回 'nil' return nil } property = input } } ``` -->

调用 `init?` 可失败初始化器的方式与调用不会失败的初始化器相同,只是你必须处理结果的可选性。

```swift
if let actualInstance = SomeStruct(input: "Hello") {
    // 使用 'SomeStruct' 的实例
} else {
    // 'SomeStruct' 的初始化失败,初始化器返回了 'nil'
}
```

可以失败的初始化器在初始化器主体实现的任何位置都可以返回 `nil`。

可以失败的初始化器可以委托给任何类型的初始化器。
不会失败的初始化器可以委托给另一个不会失败的初始化器或 `init!` 可失败初始化器。
不会失败的初始化器可以通过强制解包超类初始化器的结果来委托给 `init?` 可失败初始化器 —— 例如,写成 `super.init()!`。

初始化失败会通过初始化器委托传播。也就是说,如果一个可以失败的初始化器委托给失败并返回 `nil` 的初始化器,那么委托的初始化器也会失败并隐式返回 `nil`。
如果一个不会失败的初始化器委托给失败并返回 `nil` 的 `init!` 可失败初始化器,那么会引发运行时错误(就像你使用 `!` 运算符解包一个 `nil` 值的可选值一样)。

能够失败的指定初始化器在子类中可以被任何类型的指定初始化器重写。
不会失败的指定初始化器在子类中只能被不会失败的指定初始化器重写。

想了解更多并查看可失败初始化器的示例,请参阅 <doc:Initialization#Failable-Initializers>。

> *initializer-declaration* → *initializer-head* *generic-parameter-clause*_?_ *parameter-clause* **`async`**_?_ *throws-clause*_?_ *generic-where-clause*_?_ *initializer-body* \
> *initializer-declaration* → *initializer-head* *generic-parameter-clause*_?_ *parameter-clause* **`async`**_?_ **`rethrows`** *generic-where-clause*_?_ *initializer-body* \
> *initializer-head* → *attributes*_?_ *declaration-modifiers*_?_ **`init`** \
> *initializer-head* → *attributes*_?_ *declaration-modifiers*_?_ **`init`** **`?`** \
> *initializer-head* → *attributes*_?_ *declaration-modifiers*_?_ **`init`** **`!`** \
> *initializer-body* → *code-block*

## 析构器声明

*析构器声明*为类类型声明一个析构器。
析构器不带参数,形式如下:

```swift 
deinit { <#statements#> }
```

当不再有对类对象的引用时,在类对象被释放之前,析构器会自动被调用。
析构器只能在类声明的主体中声明 —— 而不能在类的扩展中声明 —— 并且每个类最多只能有一个。

子类继承其超类的析构器,在子类对象被释放之前,超类的析构器会被隐式调用。
子类对象在其继承链中所有析构器执行完毕之前不会被释放。

析构器不能直接被调用。

有关如何在类声明中使用析构器的示例,请参阅 <doc:Deinitialization>。

> *deinitializer-declaration* → *attributes*_?_ **`deinit`** *code-block*

## 扩展声明  

*扩展声明*允许你扩展现有类型的行为。
扩展声明使用 `extension` 关键字声明,形式如下:

```swift
extension <#type name#> where <#requirements#> { <#declarations#> }
```

扩展声明的主体包含零个或多个*声明*。
这些*声明*可以包括计算属性、计算类型属性、实例方法、类型方法、初始化器、下标声明,甚至类、结构体和枚举声明。
扩展声明不能包含析构器或协议声明、存储属性、属性观察器或其他扩展声明。
协议扩展中的声明不能被标记为 `final`。
有关包含各种声明的扩展的讨论和几个示例,请参阅 <doc:Extensions>。

如果 *类型名称* 是类、结构体或枚举类型,扩展就会扩展该类型。
如果 *类型名称* 是协议类型,扩展就会扩展所有符合该协议的类型。

扩展声明如果扩展了泛型类型或包含关联类型的协议,可以包含 *要求*。如果扩展类型的实例或符合扩展协议的类型的实例满足 *要求*,该实例就会获得声明中指定的行为。

扩展声明可以包含构造器声明。但是,如果你要扩展的类型是在另一个模块中定义的,构造器声明必须委托给该模块中已经定义的构造器。这样可以确保该类型的成员被正确初始化。

现有类型的属性、方法和构造器不能在该类型的扩展中被重写。

扩展声明可以通过指定 *遵循的协议* 来为现有的类、结构体或枚举类型添加协议一致性:

```swift extension <#类型名称#>: <#遵循的协议#> where <#要求#> { <#声明#> } ```

扩展声明不能为现有类添加类继承,因此在 *类型名称* 和冒号之后只能指定协议列表。

### 条件一致性

你可以扩展泛型类型以有条件地符合协议,这样该类型的实例只有在满足某些要求时才符合该协议。你可以在扩展声明中包含 *要求* 来为协议添加条件一致性。

#### 在某些泛型上下文中不使用重写的要求

在某些泛型上下文中,通过条件一致性获得协议行为的类型并不总是使用该协议要求的特殊实现。为了说明这种行为,下面的示例定义了两个协议和一个有条件地符合这两个协议的泛型类型。

```swift 
protocol Loggable { func log() } 
extension Loggable { func log() { print(self) } }

protocol TitledLoggable: Loggable { static var logTitle: String { get } } 
extension TitledLoggable { func log() { print("\(Self.logTitle): \(self)") } }

struct Pair<T>: CustomStringConvertible { 
    let first: T
    let second: T
    var description: String { return "(\(first), \(second))" }
}

extension Pair: Loggable where T: Loggable { }
extension Pair: TitledLoggable where T: TitledLoggable {
    static var logTitle: String { return "Pair of '\(T.logTitle)'" }
}

extension String: TitledLoggable {
    static var logTitle: String { return "String" }
} 
```

`Pair` 结构体在其泛型类型符合 `Loggable` 或 `TitledLoggable` 时分别符合 `Loggable` 和 `TitledLoggable`。在下面的示例中,`oneAndTwo` 是 `Pair<String>` 的实例,因为 `String` 符合 `TitledLoggable`,所以 `Pair<String>` 也符合 `TitledLoggable`。当直接在 `oneAndTwo` 上调用 `log()` 方法时,会使用包含标题字符串的特殊版本。

```swift
let oneAndTwo = Pair(first: "one", second: "two")
oneAndTwo.log() // 打印 "Pair of 'String': (one, two)"
```

当 `oneAndTwo` 在泛型上下文中使用或作为 `Loggable` 协议的实例时,它的专用版本不会被调用。Swift 会根据 `Pair` 需要遵守 `Loggable` 的最低要求来选择调用哪个 `log()` 实现。因此,由 `Loggable` 协议提供的默认实现会被使用。

```swift
func doSomething<T: Loggable>(with x: T) { x.log() } 
doSomething(with: oneAndTwo) // 打印 "(one, two)"
```

<!-- - test: `conditional-conformance`

  ```swifttest -> func doSomething<T: Loggable>(with x: T) { x.log() } doSomething(with: oneAndTwo) <- (one, two) ``` -->

当在传递给 `doSomething(_:)` 的实例上调用 `log()` 时,记录的字符串中会省略自定义标题。

### 协议遵从性不能冗余

具体类型只能对特定协议遵从一次。Swift 会将冗余的协议遵从标记为错误,这种错误可能出现在以下两种情况:

第一种情况是,你显式地多次遵从同一协议,但要求不同。第二种情况是,你隐式地从同一协议继承多次。下面将讨论这些情况。

#### 解决显式冗余

在具体类型上的多个扩展不能添加对同一协议的遵从,即使扩展的要求是互斥的。下面的示例演示了这种限制情况。两个扩展声明试图为 `Serializable` 协议添加条件遵从,一个用于 `Int` 元素的数组,另一个用于 `String` 元素的数组。

```swift
protocol Serializable { func serialize() -> Any }

extension Array: Serializable where Element == Int { func serialize() -> Any { // 实现 } } 
extension Array: Serializable where Element == String { func serialize() -> Any { // 实现 } }
// 错误: Array<Element> 对协议 Serializable 的重复遵从
```

<!-- - test: `multiple-conformances`

  ```swifttest -> protocol Serializable { func serialize() -> Any } --- extension Array: Serializable where Element == Int { func serialize() -> Any { // implementation >>         return 0 ->     } } extension Array: Serializable where Element == String { func serialize() -> Any { // implementation >>         return 0 ->     } } // Error: redundant conformance of 'Array<Element>' to protocol 'Serializable' !$ error: conflicting conformance of 'Array<Element>' to protocol 'Serializable'; there cannot be more than one conformance, even with different conditional bounds !! extension Array: Serializable where Element == String { !! ^ !$ note: 'Array<Element>' declares conformance to protocol 'Serializable' here !! extension Array: Serializable where Element == Int { !! ^ ``` -->

如果你需要根据多个具体类型添加条件遵从,请创建一个新协议,每个类型都可以遵从该协议,并在声明条件遵从时使用该协议作为要求。

```swift
protocol SerializableInArray { }
extension Int: SerializableInArray { }
extension String: SerializableInArray { }

extension Array: Serializable where Element: SerializableInArray { func serialize() -> Any { // 实现 } }
```

<!-- - test: `multiple-conformances-success`

  ```swifttest >> protocol Serializable { } -> protocol SerializableInArray { } extension Int: SerializableInArray { } extension String: SerializableInArray { } --- -> extension Array: Serializable where Element: SerializableInArray { func serialize() -> Any { // implementation >>         return 0 ->     } } ``` -->

#### 解决隐式冗余

当具体类型有条件地遵从某个协议时,该类型隐式地遵从任何具有相同要求的父协议。

如果需要一个类型有条件地遵从两个继承自同一父协议的协议,请显式地声明对父协议的遵从,这样可以避免隐式地以不同要求两次遵从父协议。

下面的示例显式地声明了 `Array` 对 `Loggable` 的条件遵从,以避免在声明它对新的 `MarkedLoggable` 协议和 `TitledLoggable` 的条件遵从时发生冲突。

```swift
protocol MarkedLoggable: Loggable { func markAndLog() }

extension MarkedLoggable { func markAndLog() { print("----------") log() } }

extension Array: Loggable where Element: Loggable { } 
extension Array: TitledLoggable where Element: TitledLoggable { static var logTitle: String { return "Array of '\(Element.logTitle)'" } }
extension Array: MarkedLoggable where Element: MarkedLoggable { }
```

<!-- - test: `conditional-conformance`

  ```swifttest -> protocol MarkedLoggable: Loggable { func markAndLog() } --- extension MarkedLoggable { func markAndLog() { print("----------") log() } } --- extension Array: Loggable where Element: Loggable { } extension Array: TitledLoggable where Element: TitledLoggable { static var logTitle: String { return "Array of '\(Element.logTitle)'" } } extension Array: MarkedLoggable where Element: MarkedLoggable { } ``` -->

如果没有显式扩展声明 Array 在某些条件下符合 Loggable 协议，其他 Array 扩展会隐式创建这些声明，从而导致错误:

```swift 
extension Array: Loggable where Element: TitledLoggable { } 
extension Array: Loggable where Element: MarkedLoggable { }
// 错误: Array<Element> 对协议 Loggable 的冗余符合性声明
```

在这里，Loggable 是一个协议，TitledLoggable 和 MarkedLoggable 是它的子协议。代码片段展示了在不同条件下，Array 如何符合这些协议。

<!-- - test: `conditional-conformance-implicit-overlap`

  ```swifttest >> protocol Loggable { } >> protocol MarkedLoggable : Loggable { } >> protocol TitledLoggable : Loggable { } -> extension Array: Loggable where Element: TitledLoggable { } extension Array: Loggable where Element: MarkedLoggable { } // 错误: Array<Element> 对协议 Loggable 的冗余符合性 !$ error: Array<Element> 对协议 Loggable 存在冲突的符合性; 即使有不同的条件边界,也不能有多于一个符合性 !! extension Array: Loggable where Element: MarkedLoggable { } !! ^ !$ note: Array<Element> 在这里声明对协议 Loggable 的符合性 !! extension Array: Loggable where Element: TitledLoggable { } !! ^ ``` -->

<!-- - test: `types-cant-have-multiple-implicit-conformances`

  ```swifttest >> protocol Loggable { } protocol TitledLoggable: Loggable { } protocol MarkedLoggable: Loggable { } extension Array: TitledLoggable where Element: TitledLoggable { // ...
     } extension Array: MarkedLoggable where Element: MarkedLoggable { } !$ error: Array<Element> 对协议 TitledLoggable 的条件符合性不意味着对继承协议 Loggable 的符合性 !! extension Array: TitledLoggable where Element: TitledLoggable { !! ^ !$ note: 你是否想像这样显式声明符合性 'extension Array: Loggable where ...'?
  !! extension Array: TitledLoggable where Element: TitledLoggable { !! ^ !$ error: 类型 Array<Element> 不符合协议 MarkedLoggable !! extension Array: MarkedLoggable where Element: MarkedLoggable { } !! ^ !$ error: 类型 Element 不符合协议 TitledLoggable !! extension Array: MarkedLoggable where Element: MarkedLoggable { } !! ^ !$ error: MarkedLoggable 要求 Element 符合 TitledLoggable !! extension Array: MarkedLoggable where Element: MarkedLoggable { } !! ^ !$ note: 要求指定为 Element : TitledLoggable !! extension Array: MarkedLoggable where Element: MarkedLoggable { } !! ^ !$ note: 来自 Array<Element> 对 Loggable 的条件符合性的要求 !! extension Array: MarkedLoggable where Element: MarkedLoggable { } !! ^ ``` -->

这里展示了一些错误信息,主要是由于类型符合多个协议时的冲突引起的。比如 Array 类型试图同时符合 TitledLoggable 和 MarkedLoggable 协议,但这两个协议都要求 Element 类型分别符合对应的协议,从而导致了冲突。编译器会提示你显式声明 Array 符合基协议 Loggable,或者修改代码避免这种冲突。

<!-- - test: `extension-can-have-where-clause`

  ```swifttest >> extension Array where Element: Equatable { func f(x: Array) -> Int { return 7 } } >> let x = [1, 2, 3] >> let y = [10, 20, 30] >> let r0 = x.f(x: y) >> assert(r0 == 7) ``` -->

<!-- - test: `extensions-can-have-where-clause-and-inheritance-together`

  ```swifttest >> protocol P { func foo() -> Int } >> extension Array: P where Element: Equatable { >>    func foo() -> Int { return 0 } >> } >> let r0 = [1, 2, 3].foo() >> assert(r0 == 0) ``` -->

这两个代码片段展示了在扩展中使用 where 子句的情况。where 子句可以添加对泛型类型的约束,比如要求 Element 类型符合 Equatable 协议。同时,扩展也可以结合协议继承,使得扩展的类型符合某个协议。

下标声明允许你为特定类型添加下标访问支持,通常用于方便地访问集合、列表或序列中的元素。

下标声明使用 `subscript` 关键字声明,形式如下:

```swift
subscript (<#parameters#>) -> <#return type#> {
    get {
        <#statements#>
    }
    set(<#setter name#>) {
        <#statements#>
    }
}
```

下标声明只能出现在类、结构体、枚举、扩展或协议声明的上下文中。

*parameters* 指定一个或多个索引,用于在下标表达式中访问相应类型的元素(例如,表达式 `object[i]` 中的 `i`)。虽然用于访问元素的索引可以是任何类型,但每个参数都必须包含一个类型注解,以指定每个索引的类型。*return type* 指定被访问元素的类型。

与计算属性一样,下标声明支持读取和写入被访问元素的值。getter 用于读取值,setter 用于写入值。如果只需要 getter,可以省略 setter 子句,直接返回请求的值。不过,如果你提供了 setter 子句,你也必须提供 getter 子句。

*setter name* 和包围的括号是可选的。如果你提供了 setter 名称,它将用作 setter 的参数名称。如果你没有提供 setter 名称,则 setter 的默认参数名称为 `value`。setter 参数的类型与 *return type* 相同。

你可以在声明它的类型中重载下标声明,只要 *parameters* 或 *return type* 与你要重载的不同即可。你也可以重写继承自超类的下标声明。这时,你必须使用 `override` 声明修饰符标记被重写的下标声明。

与函数、方法和构造器不同,下标参数默认没有参数标签。但是,你可以使用与函数、方法和构造器相同的语法提供显式参数标签。另外,下标不能有 in-out 参数。下标参数可以有默认值,使用 <doc:Declarations#Special-Kinds-of-Parameters> 中描述的语法。

你还可以在协议声明的上下文中声明下标,如 <doc:Declarations#Protocol-Subscript-Declaration> 所述。有关下标和下标声明示例的更多信息,请参阅 <doc:Subscripts>。

### 类型下标声明

要声明由类型而不是类型实例公开的下标,请使用 `static` 声明修饰符标记下标声明。类可以使用 `class` 声明修饰符而不是 `static` 来标记类型计算属性,以允许子类重写超类的实现。在类中,使用 `static` 关键字声明的成员与使用 `class` 和 `final` 修饰符声明的效果相同。

<!-- - test: `cant-override-static-subscript-in-subclass`

  ```swifttest
-> class Super { static subscript(i: Int) -> Int { return 10 } }
-> class Sub: Super { override static subscript(i: Int) -> Int { return 100 } }
!$ error: cannot override static subscript
!! class Sub: Super { override static subscript(i: Int) -> Int { return 100 } }
!!                                    ^
!$ note: overridden declaration is here
!! class Super { static subscript(i: Int) -> Int { return 10 } }
!!                      ^
```
-->

下标声明的语法规则如下:

> *下标声明* → *下标头* *下标结果* *泛型where子句*_?_ *代码块* \
> *下标声明* → *下标头* *下标结果* *泛型where子句*_?_ *getter-setter块* \
> *下标声明* → *下标头* *下标结果* *泛型where子句*_?_ *getter-setter关键字块* \
> *下标头* → *属性*_?_ *声明修饰符*_?_ **`subscript`** *泛型参数子句*_?_ *参数子句* \
> *下标结果* → **`->`** *属性*_?_ *类型*

## 宏声明

*宏声明* 引入一个新的宏。它以 `macro` 关键字开头,形式如下:

```swift
macro <#名称#> = <#宏实现#>
```

*宏实现* 是另一个宏,指示执行此宏展开的代码位置。执行宏展开的代码是一个独立的 Swift 程序,它使用 [SwiftSyntax][] 模块与 Swift 代码交互。从 Swift 标准库调用 `externalMacro(module:type:)` 宏,传入包含宏实现的类型名称和包含该类型的模块名称。

[SwiftSyntax]: http://github.com/apple/swift-syntax/

宏可以像函数一样重载。宏声明只出现在文件作用域。

有关 Swift 中宏的概述,请参阅 <doc:Macros>。

> 宏声明的语法规则:
> > *宏声明* → *宏头* *标识符* *泛型参数子句*_?_ *宏签名* *宏定义*_?_ *泛型where子句* \
> > *宏头* → *属性*_?_ *声明修饰符*_?_ **`macro`** \
> > *宏签名* → *参数子句* *宏函数签名结果*_?_ \
> > *宏函数签名结果* → **`->`** *类型* \
> > *宏定义* → **`=`** *表达式*

## 运算符声明

*运算符声明* 使用 `operator` 关键字将一个新的中缀、前缀或后缀运算符引入你的程序。

你可以声明三种不同结合性的运算符: 中缀、前缀和后缀。运算符的*结合性* 指定运算符与其操作数的相对位置。

运算符声明有三种基本形式,每种结合性一种。在 `operator` 关键字之前使用 `infix`、`prefix` 或 `postfix` 声明修饰符指定运算符的结合性。在每种形式中,运算符名称只能包含 <doc:LexicalStructure#Operators> 中定义的运算符字符。

以下形式声明一个新的中缀运算符:

```swift
infix operator <#运算符名称#>: <#优先级组#>
```

*中缀运算符* 是一个二元运算符,写在两个操作数之间,例如表达式 `1 + 2` 中的加法运算符 (`+`)。

中缀运算符可以选择指定一个优先级组。如果省略运算符的优先级组,Swift 将使用默认优先级组 `DefaultPrecedence`,它的优先级略高于 `TernaryPrecedence`。更多信息,请参阅 <doc:Declarations#Precedence-Group-Declaration>。

以下形式声明一个新的前缀运算符:

```swift
prefix operator <#运算符名称#>
```

*前缀运算符* 是一个一元运算符,写在其操作数之前,例如表达式 `!a` 中的前缀逻辑非运算符 (`!`)。

前缀运算符声明不指定优先级。前缀运算符是非结合的。

以下形式声明一个新的后缀运算符:

```swift 
postfix operator <#运算符名称#>
```

*后缀运算符* 是一个一元运算符,写在其操作数之后,例如表达式 `a!` 中的后缀强制解包运算符 (`!`)。

与前缀运算符一样,后缀运算符声明不指定优先级。后缀运算符是非结合的。

在声明了一个新的运算符之后,程序员需要通过声明一个与该运算符同名的静态方法来实现它。该静态方法属于该运算符的操作数类型之一的成员方法 - 例如,将 Double 与 Int 相乘的运算符就是作为 Double 或 Int 结构体的静态方法来实现的。如果您正在实现前缀或后缀运算符,您还需要在方法声明前使用相应的 prefix 或 postfix 声明修饰符。要查看如何创建和实现新运算符的示例,请参阅<doc:AdvancedOperators#Custom-Operators>。

> 运算符声明的语法规则如下:
> > *operator-declaration* → *prefix-operator-declaration* | *postfix-operator-declaration* | *infix-operator-declaration* > > *prefix-operator-declaration* → **`prefix`** **`operator`** *operator* \ > *postfix-operator-declaration* → **`postfix`** **`operator`** *operator* \ > *infix-operator-declaration* → **`infix`** **`operator`** *operator* *infix-operator-group*_?_ > > *infix-operator-group* → **`:`** *precedence-group-name*

## 优先级组声明

优先级组声明用于在程序中引入一个新的中缀运算符优先级分组。运算符的优先级决定了在没有使用分组括号的情况下,该运算符与其操作数结合的紧密程度。

优先级组声明的形式如下:

```swift precedencegroup <#precedence group name#> { higherThan: <#lower group names#> lowerThan: <#higher group names#> associativity: <#associativity#> assignment: <#assignment#> } ```

`lowerThan` 优先级组属性只能用于引用当前模块之外声明的优先级组。当两个运算符相互竞争操作数时,例如在表达式 `2 + 3 * 5` 中,具有更高相对优先级的运算符会更紧密地绑定其操作数。

> 注意: 使用 *lower group names* 和 *higher group names* 相互关联的优先级组必须符合单一的关系层次结构,但它们不必须形成线性层次结构。这意味着可能存在相对优先级未定义的优先级组。来自这些优先级组的运算符在彼此相邻时必须使用分组括号。

Swift 为了配合 Swift 标准库提供的运算符,定义了许多优先级组。例如,加法 (+) 和减法 (-) 运算符属于 AdditionPrecedence 组,乘法 (*) 和除法 (/) 运算符属于 MultiplicationPrecedence 组。有关 Swift 标准库提供的优先级组的完整列表,请参阅 [Operator Declarations](https://developer.apple.com/documentation/swift/operator_declarations)。

运算符的关联性指定了在没有分组括号的情况下,具有相同优先级的一系列运算符如何组合在一起。您可以通过编写上下文敏感关键字 left、right 或 none 之一来指定运算符的关联性 - 如果省略关联性,则默认为 none。左关联的运算符按从左到右的顺序进行分组。例如,减法运算符 (-) 是左关联的,因此表达式 `4 - 5 - 6` 被分组为 `(4 - 5) - 6`,计算结果为 -7。右关联的运算符按从右到左的顺序进行分组。具有相同优先级的非关联运算符不能彼此相邻出现。例如,< 运算符的关联性为 none,这意味着 `1 < 2 < 3` 不是一个有效的表达式。

优先级组的赋值指定了在包含可选链式调用的操作中使用该运算符时的优先级。当设置为 true 时,相应优先级组中的运算符在可选链式调用期间使用与 Swift 标准库中的赋值运算符相同的分组规则。否则,当设置为 false 或省略时,该优先级组中的运算符遵循与不执行赋值的运算符相同的可选链式调用规则。

以下是对原文的意译:

## 优先级组声明语法

优先级组是一种语法结构,用于自定义运算符的优先级和结合性。它允许你控制运算符在表达式中的求值顺序。

> *优先级组声明* → **`precedencegroup`** *优先级组名称* **`{`** *优先级组属性*_?_ **`}`**
> *优先级组属性* → *优先级组关系* | *优先级组赋值* | *优先级组结合性*
> *优先级组关系* → **`higherThan`** **`:`** *优先级组名称列表* | **`lowerThan`** **`:`** *优先级组名称列表*
> *优先级组赋值* → **`assignment`** **`:`** *布尔文字*
> *优先级组结合性* → **`associativity`** **`:`** **`left`** | **`right`** | **`none`**
> *优先级组名称列表* → *优先级组名称* | *优先级组名称* **`,`** *优先级组名称列表*
> *优先级组名称* → *标识符*

## 声明修饰符

*声明修饰符*是一些关键字或上下文敏感关键字,用于修改声明的行为或含义。你可以在声明的属性(如果有)和引入声明的关键字之间,写入相应的修饰符。

- `class`: 将此修饰符应用于类的成员,表示该成员属于类本身,而非类的实例。被标记为 `class` 且没有 `final` 修饰符的超类成员,可以在子类中被重写。

- `dynamic`: 将此修饰符应用于可由 Objective-C 表示的任何类成员。当一个成员被标记为 `dynamic` 时,对它的访问都会动态分派到 Objective-C 运行时,编译器不会内联或去虚拟化对它的访问。由于使用了 Objective-C 运行时,因此这些声明必须标记 `objc` 属性。

- `final`: 将此修饰符应用于类、类的属性、方法或下标成员。用于类时,表示该类不能被继承;用于属性、方法或下标成员时,表示该成员在子类中不能被重写。

- `lazy`: 将此修饰符应用于类或结构体的存储型变量属性,表示该属性的初始值最多只计算和存储一次,即在第一次访问该属性时。

- `optional`: 将此修饰符应用于协议的属性、方法或下标成员,表示符合该协议的类型不需要实现这些成员。只有标记 `objc` 属性的协议才能使用 `optional` 修饰符,因此只有类类型才能采用包含可选成员要求的协议。如何使用 `optional` 修饰符以及如何访问可选协议成员的指南,请参阅<doc:Protocols#Optional-Protocol-Requirements>。

- `required`: 将此修饰符应用于类的指定构造器或便利构造器,表示每个子类都必须实现该构造器,子类对该构造器的实现也必须标记 `required` 修饰符。

- 术语 `static`：
将这个修饰符应用于结构体、类、枚举或协议的成员时,表示该成员属于类型本身,而非该类型的实例。在类声明的作用域内,为成员声明添加 `static` 修饰符,效果等同于添加 `class` 和 `final` 修饰符。但是,类的常量类型属性例外:在那里 `static` 保持其正常的非类含义,因为你无法在那些声明上使用 `class` 或 `final`。

- 术语 `unowned`：
将此修饰符应用于存储型变量、常量或属性,表示它们对存储为其值的类实例拥有无主引用。如果在该实例被销毁后尝试访问这些变量或属性,将引发运行时错误。与弱引用类似,它们的类型必须是类类型;与弱引用不同的是,类型为非可选。更多示例和相关信息,请参阅 <doc:AutomaticReferenceCounting#Unowned-References>。

- 术语 `unowned(safe)`：
`unowned` 的显式拼写形式。

- 术语 `unowned(unsafe)`：
将此修饰符应用于存储型变量、常量或属性,表示它们对存储为其值的类实例拥有无主引用。如果在该实例被销毁后尝试访问这些变量或属性,你将访问该实例曾经所在的内存位置,这是一种内存不安全的操作。与弱引用类似,它们的类型必须是类类型;与弱引用不同的是,类型为非可选。更多示例和相关信息,请参阅 <doc:AutomaticReferenceCounting#Unowned-References>。

- 术语 `weak`：
将此修饰符应用于存储型变量或属性,表示它们对存储为其值的对象拥有弱引用。该变量或属性的类型必须为可选类类型。如果在该对象被销毁后访问这些变量或属性,它们的值将为 `nil`。更多示例和相关信息,请参阅 <doc:AutomaticReferenceCounting#Weak-References>。

### 访问控制级别

Swift 提供五个访问控制级别:open、public、internal、file private 和 private。你可以使用下面的访问级别修饰符之一标记声明,以指定其访问级别。访问控制的详细内容在 <doc:AccessControl> 中有说明。

- 术语 `open`：
将此修饰符应用于声明,表示该声明可以在同一模块中被访问和子类化。标记有 `open` 访问级别修饰符的声明也可以被导入该模块的其他模块访问和子类化。

- 术语 `public`：
将此修饰符应用于声明,表示该声明可以在同一模块中被访问和子类化。标记有 `public` 访问级别修饰符的声明也可以被导入该模块的其他模块访问,但不能被子类化。

- 术语 `package`：
将此修饰符应用于声明,表示该声明只能被同一包中的代码访问。包是你在使用的构建系统中定义的代码分发单元。当构建系统编译代码时,它会通过向 Swift 编译器传递 `-package-name` 标志来指定包名。如果构建系统在构建它们时指定了相同的包名,则两个模块属于同一个包。

- 术语 `internal`：
将此修饰符应用于声明,表示该声明只能在同一模块中被访问。默认情况下,大多数声明都隐式标记有 `internal` 访问级别修饰符。

- 术语 `fileprivate`：
将此修饰符应用于声明,表示该声明只能在同一源文件中被访问。

- 术语 `private`：
将此修饰符应用于声明,表示该声明只能在声明的直接作用域内被访问。

对于访问控制而言,扩展的行为如下:如果同一文件中有多个扩展扩展了同一类型,那么所有这些扩展都具有相同的访问控制作用域。扩展和它们扩展的类型可以位于不同的文件中。

- 如果扩展与它们扩展的类型在同一个文件中,那么这些扩展具有与它们扩展的类型相同的访问控制范围。

- 在类型声明中声明的私有成员可以从该类型的扩展中访问。在一个扩展中声明的私有成员可以从其他扩展和被扩展类型的声明中访问。

上述每个访问级别修饰符都可以选择性地接受一个由 `set` 关键字括在括号中的单个参数 —— 例如,`private(set)`。当你想为变量或下标的 setter 指定一个低于或等于变量或下标本身访问级别的访问级别时,请使用这种形式的访问级别修饰符,正如在 <doc:AccessControl#Getters-and-Setters> 中所讨论的那样。

> *declaration-modifier* → **`class`** | **`convenience`** | **`dynamic`** | **`final`** | **`infix`** | **`lazy`** | **`optional`** | **`override`** | **`postfix`** | **`prefix`** | **`required`** | **`static`** | **`unowned`** | **`unowned`** **`(`** **`safe`** **`)`** | **`unowned`** **`(`** **`unsafe`** **`)`** | **`weak`** \ 
> *declaration-modifier* → *access-level-modifier* \
> *declaration-modifier* → *mutation-modifier* \
> *declaration-modifier* → *actor-isolation-modifier* \
> *declaration-modifiers* → *declaration-modifier* *declaration-modifiers*_?_ >
> *access-level-modifier* → **`private`** | **`private`** **`(`** **`set`** **`)`** \
> *access-level-modifier* → **`fileprivate`** | **`fileprivate`** **`(`** **`set`** **`)`** \
> *access-level-modifier* → **`internal`** | **`internal`** **`(`** **`set`** **`)`** \
> *access-level-modifier* → **`package`** | **`package`** **`(`** **`set`** **`)`** \
> *access-level-modifier* → **`public`** | **`public`** **`(`** **`set`** **`)`** \
> *access-level-modifier* → **`open`** | **`open`** **`(`** **`set`** **`)`** >
> *mutation-modifier* → **`mutating`** | **`nonmutating`** >
> *actor-isolation-modifier* → **`nonisolated`**

> 测试版软件:
> > 本文档包含有关正在开发中的 API 或技术的初步信息。此信息可能会发生变化,根据此文档实施的软件应该与最终的操作系统软件一起进行测试。
> > 了解更多关于使用 [Apple 的测试版软件](https://developer.apple.com/support/beta-software/)。