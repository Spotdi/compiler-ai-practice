; Loop example:
; int main() {
;   int sum = 0;
;   for (int i = 1; i <= 5; i++) {
;     sum += i;
;   }
;   return sum;
; }

define i32 @main() {
entry:
  br label %loop_header

loop_header:
  %i = phi i32 [ 1, %entry ], [ %next_i, %loop_body ]
  %sum = phi i32 [ 0, %entry ], [ %next_sum, %loop_body ]
  %cond = icmp sle i32 %i, 5
  br i1 %cond, label %loop_body, label %loop_end

loop_body:
  %next_sum = add i32 %sum, %i
  %next_i = add i32 %i, 1
  br label %loop_header

loop_end:
  ret i32 %sum
}

