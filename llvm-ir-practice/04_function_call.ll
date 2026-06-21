; Function call example:
; int add_twice(int x) {
;   return x + x;
; }
;
; int main() {
;   return add_twice(21);
; }

define i32 @add_twice(i32 %x) {
entry:
  %result = add i32 %x, %x
  ret i32 %result
}

define i32 @main() {
entry:
  %value = call i32 @add_twice(i32 21)
  ret i32 %value
}

