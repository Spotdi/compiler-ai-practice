; If-else example:
; int main() {
;   int x = 7;
;   if (x > 5) {
;     return 1;
;   } else {
;     return 0;
;   }
; }

define i32 @main() {
entry:
  %x = add i32 7, 0
  %cond = icmp sgt i32 %x, 5
  br i1 %cond, label %then_block, label %else_block

then_block:
  ret i32 1

else_block:
  ret i32 0
}

