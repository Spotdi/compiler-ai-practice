; Arithmetic example:
; int main() {
;   int x = 10;
;   int y = 3;
;   return (x + y) * 2 - 4;
; }

define i32 @main() {
entry:
  %x = add i32 10, 0
  %y = add i32 3, 0
  %sum = add i32 %x, %y
  %mul = mul i32 %sum, 2
  %result = sub i32 %mul, 4
  ret i32 %result
}

