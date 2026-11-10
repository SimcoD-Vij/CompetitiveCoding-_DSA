# Two Pointers — Complete Pattern Deep-Dive

---

## 1. Pattern Overview

**What it is:** Two Pointers is a technique where you maintain **two indices** that move through a data structure (usually a sorted array, string, or linked list) according to some rule, instead of using nested loops. The two indices can move toward each other, in the same direction at different speeds, or independently across two different structures.

**Fundamental idea:** Many `O(n²)` brute-force problems check every pair `(i, j)`. If the data has enough structure (sortedness, a known target sum, a palindrome shape), you can often prove that once you've checked a pair, an entire *set* of other pairs is provably irrelevant — so you can skip them by moving a pointer, rather than checking them one by one.

**Problem it solves:** Finding pairs/triplets satisfying a condition, comparing structure from both ends, partitioning data in place, merging sorted sequences, or removing/deduplicating in place — all in a single linear pass instead of nested loops.

**Why it works:** Each pointer only ever moves forward (or toward the other pointer) — never backward. That guarantees each index is visited a bounded number of times (usually once), so the total work is linear even though it "looks like" it's checking pairs.

**What's happening internally, step by step (opposite-direction example — pair sum in sorted array):**
1. Place `left` at the start, `right` at the end.
2. Compute `arr[left] + arr[right]`.
3. If the sum equals target, record/return it.
4. If the sum is too small, move `left` right (need a bigger sum).
5. If the sum is too large, move `right` left (need a smaller sum).
6. Repeat until `left` and `right` cross.

**Data structures involved:** Typically none beyond the array/string itself — the "structure" is two integer indices. Occasionally paired with a HashMap for a 3-pointer-plus-lookup hybrid.

**Intuition:** Picture two people walking toward each other from opposite ends of a sorted line of numbers — every time the pair they're standing on is "too small," the left person steps forward; every time it's "too big," the right person steps back. They can never need to re-check a pair they've already ruled out, because sortedness guarantees the direction of the fix.

**When to think of it:**
- The array/string is sorted, or can be sorted without losing needed information (e.g., original index).
- You're looking for pairs/triplets with a sum, difference, or product condition.
- You're comparing from both ends (palindrome checks).
- You need to partition or overwrite an array in place with O(1) extra space.
- You're merging two already-sorted sequences.

**When NOT to use it:**
- The data isn't sorted and sorting would destroy information you need (e.g., original indices) and re-deriving them is more expensive than an alternative (like a HashMap, which solves unsorted pair-sum in O(n) without sorting).
- The problem needs a **variable-size contiguous window** rather than two independent pointers — that's Sliding Window, a close cousin but a different invariant.
- You need every combination, not just pairs that satisfy a monotonic condition (then Backtracking is more appropriate).

---

## 2. Visualization

**Opposite-direction — Two Sum II on sorted array, target = 9:**

```
Index:   0   1   2   3   4   5
Array:  [1,  2,  4,  6,  8, 11]

Step 1: L=0, R=5 → arr[0]+arr[5] = 1+11 = 12 > 9 → too big → R-- 

         L                       R
        [1,  2,  4,  6,  8, 11]
         0   1   2   3   4   5

Step 2: L=0, R=4 → arr[0]+arr[4] = 1+8 = 9 == 9 → FOUND (indices 0,4)

         L                   R
        [1,  2,  4,  6,  8, 11]
         0   1   2   3   4   5
```

**Same-direction (fast/slow) — Remove duplicates from sorted array in place:**

```
Array: [1, 1, 2, 2, 3]

slow=0, fast=1
  fast=1: arr[1]==arr[0] → duplicate → fast++ (slow stays)
  fast=2: arr[2]!=arr[0] → slow++ , arr[slow]=arr[2] → [1,2,2,2,3], slow=1
  fast=3: arr[3]==arr[slow]=2 → duplicate → fast++
  fast=4: arr[4]!=arr[slow] → slow++, arr[slow]=arr[4] → [1,2,3,2,3], slow=2

Result: first slow+1 = 3 elements are the deduplicated array: [1, 2, 3]
```

`slow` marks "the boundary of the unique-so-far region," `fast` scans ahead looking for the next value worth keeping — classic same-direction two pointers.

---

## 3. Recognition — How Do I Know This Is the Pattern?

### Common keywords
- "pair" / "pair sum" / "two numbers that add up to"
- "sorted array"
- "palindrome"
- "in-place"
- "remove duplicates"
- "container with most water"
- "triplet" / "3Sum" / "4Sum"
- "merge two sorted"
- "reverse in place"
- "closest to target"

### Why these keywords signal Two Pointers
- **"sorted" + "pair sum"** — sortedness gives you a monotonic direction to move: too small → move left pointer up, too big → move right pointer down. Without sortedness, this monotonic guarantee disappears.
- **"in-place" + "remove/deduplicate"** — this is the signature of same-direction (read/write) two pointers, where one index tracks "confirmed valid so far" and the other scans ahead.
- **"palindrome"** — comparing from both ends simultaneously is the definition of opposite-direction two pointers.
- **"container with most water" / "closest to target"** — these are optimization-over-pairs problems where sortedness or geometric structure lets you discard one side without missing a better answer.
- **"merge two sorted [arrays/lists]"** — advancing two independent pointers, each through its own sorted structure, is a two-pointer merge.

### Question → Pattern Recognition

| Question | → Pattern | Why |
|---|---|---|
| "Given a sorted array, find two numbers that sum to target." | Two Pointers (opposite) | Sorted + pair-sum → monotonic direction to move |
| "Check if a string is a palindrome." | Two Pointers (opposite) | Compare from both ends inward |
| "Remove duplicates from sorted array in place." | Two Pointers (same direction) | One pointer tracks write position, other scans |
| "Merge two sorted linked lists." | Two Pointers (independent) | Advance whichever pointer has the smaller current value |
| "Find the longest substring without repeating characters." | ❌ NOT Two Pointers → Sliding Window | Needs a *dynamic contiguous window* with a shrink/grow rule, not two independently-moving indices toward each other |

---

## 4. Core Template

**Variables normally needed:** `left`, `right` (or `slow`, `fast`), sometimes a running sum/count.

**Data structure normally needed:** None — array/string indices only.

**Initialization:** `left = 0, right = n - 1` (opposite direction) or `slow = 0, fast = 1` (same direction).

**Inside the loop:** evaluate the condition using `arr[left]`/`arr[right]` (or `arr[slow]`/`arr[fast]`); decide which pointer moves.

**Loop condition:** `while (left < right)` (opposite direction, converges); `while (fast < n)` (same direction, fast scans to the end).

**State change condition:** whenever the current pair doesn't satisfy the target condition, move the pointer that can fix it.

**Answer update:** record whenever the condition is satisfied; for optimization problems (like "max water"), update the best value on every valid pair before moving a pointer.

**Termination:** `left >= right` (opposite direction) or `fast` reaches the end (same direction).

### Reusable pseudocode

```
// Opposite direction (sorted pair sum)
left = 0, right = n - 1
while left < right:
    sum = arr[left] + arr[right]
    if sum == target: return [left, right]
    else if sum < target: left++
    else: right--
return not found

// Same direction (fast/slow, in-place dedup/filter)
slow = 0
for fast in 0..n-1:
    if arr[fast] meets keep-condition:
        arr[slow] = arr[fast]
        slow++
return slow  // new length

// Independent pointers (merge two sorted sequences)
i = 0, j = 0
while i < len(A) and j < len(B):
    if A[i] <= B[j]: append A[i]; i++
    else: append B[j]; j++
append remaining A[i:] and B[j:]
```

---

## 5. Java Implementation

```java
public int[] twoSumSorted(int[] arr, int target) {
    int left = 0, right = arr.length - 1;
    while (left < right) {
        int sum = arr[left] + arr[right];
        if (sum == target) {
            return new int[]{left, right};
        } else if (sum < target) {
            left++;  // need a bigger sum
        } else {
            right--; // need a smaller sum
        }
    }
    return new int[]{-1, -1};
}
```

**Line-by-line:**
- `left = 0, right = arr.length - 1` — brackets the whole sorted array. O(1).
- `sum = arr[left] + arr[right]` — O(1) per check.
- `if (sum == target)` — early exit on match.
- `else if (sum < target) left++` — because the array is sorted ascending, increasing `left` is the *only* way to increase the sum without decreasing `right` (which we haven't ruled out yet). This is the key correctness argument: moving `left` rightward never skips a valid pair, because any pair `(left, right')` with `right' < right` and `arr[left]` unchanged was already implicitly too small (since we know `arr[left] + arr[right] < target` and `arr[right'] <= arr[right]`).
- `else right--` — symmetric argument for shrinking `right`.
- Loop runs `O(n)` total because `left` and `right` together traverse the array once, converging.

**In-place dedup (same-direction):**

```java
public int removeDuplicates(int[] arr) {
    if (arr.length == 0) return 0;
    int slow = 0;
    for (int fast = 1; fast < arr.length; fast++) {
        if (arr[fast] != arr[slow]) {
            slow++;
            arr[slow] = arr[fast];
        }
    }
    return slow + 1; // new length
}
```
- `slow` always points at the last confirmed-unique element written.
- `fast` scans ahead; whenever it finds a genuinely new value, `slow` advances and copies it in.
- Time: O(n) — `fast` visits each element once. Space: O(1) — done in place.

---

## 6. Built-in Function vs Manual Implementation

| Operation | Manual Approach | Java Built-in | Time Complexity | Which to Prefer? |
|---|---|---|---|---|
| Two Sum on sorted array | Manual `left/right` loop | None direct (no built-in "find pair sum") | O(n) manual vs O(n²) naive built-in-free brute force | Manual — this *is* the algorithm |
| Deduplicate a collection | Manual `slow/fast` in-place loop | `new LinkedHashSet<>(list)` (loses in-place/array constraint) | O(n) both, but built-in uses extra O(n) space | Manual when in-place/O(1) space is required; built-in for quick unordered scripts |
| Merge two sorted lists | Manual `i/j` merge loop | `Collections.sort()` after concatenation | O(n+m) manual vs O((n+m) log(n+m)) built-in | Manual — built-in ignores that both are already sorted, doing unnecessary work |
| Reverse array/string in place | Manual `left/right` swap loop | `Collections.reverse(list)` / `StringBuilder.reverse()` | O(n) both | Built-in for production code; manual for interviews or primitive arrays |

**When built-in is better:** `StringBuilder.reverse()` and `Collections.reverse()` are fine and idiomatic for production string/list reversal — no algorithmic insight is being tested there.

**When manual is better:** Anything where the *point* of the exercise is the two-pointer logic itself — pair-sum, in-place partitioning, merging sorted structures. There's often no built-in that captures "exploit sortedness with two indices," because that's an algorithmic technique, not a library operation.

**Does it hide the algorithmic concept?** Yes for merge/dedup — `Collections.sort()` after concatenating hides the fact you're throwing away O(n+m) of already-sorted information.

**Does it change complexity?** Sometimes significantly worse (see merge example above: O(n log n) vs O(n)).

---

## 7. Similar Patterns

| Pattern | Use When | Recognition Keywords | Time | Space |
|---|---|---|---|---|
| **Sliding Window** | Contiguous subarray/substring, dynamic size, need to track a running aggregate | "subarray," "substring," "at most K," "longest/shortest window" | O(n) | O(1)–O(k) |
| **Binary Search** | Static sorted space, single boundary/value to find | "find index," "first/last occurrence," "minimum X such that" | O(log n) | O(1) |
| **Fast & Slow Pointers (cycle detection)** | Linked list, detecting a cycle or finding the middle | "cycle," "linked list," "middle of list" | O(n) | O(1) |
| **Merge Sort (merge step)** | Combining two/more pre-sorted sequences into one | "merge k sorted," "merge intervals" | O(n log k) with heap, O(n) for two lists | O(n) |

> **If the question changes from "find a pair with a fixed target" to "find the longest/shortest contiguous range satisfying a condition," switch from Two Pointers to Sliding Window** — the pointers stop moving independently and start defining a *window* with a grow/shrink invariant.
>
> **If the question changes from "two indices in one array" to "am I revisiting the same node," switch to Fast & Slow Pointers** — a same-direction two-pointer variant specialized for cycle detection, moving at different *speeds* rather than converging.
>
> **If you only need one boundary/value rather than a pair, switch to Binary Search** — that's a single-pointer halving search, not two indices moving together.

---

## 8. Alternative Solutions

**Problem type: "Find a pair in an array that sums to target"**

1. **Brute Force — Nested Loops**
   - Idea: check every pair `(i, j)`.
   - Time: O(n²). Space: O(1).
   - Advantage: works on unsorted data, no preprocessing.
   - Disadvantage: quadratic, too slow for large n.

2. **Better — Sort + Two Pointers**
   - Idea: sort the array, then use opposite-direction two pointers.
   - Time: O(n log n) (dominated by sort). Space: O(1) extra (or O(n) if sort isn't in-place) — but **loses original indices** unless you track them separately.
   - Advantage: simple, in-place, easy to extend to 3Sum/4Sum.
   - Disadvantage: sorting destroys original index order.

3. **Optimized — HashMap (single pass)**
   - Idea: for each element, check if `target - arr[i]` has already been seen.
   - Time: O(n). Space: O(n).
   - Advantage: doesn't require sorting, preserves original indices naturally, strictly faster.
   - Disadvantage: uses O(n) extra space; doesn't generalize as cleanly to 3Sum without care.

4. **Best Practical — Depends on constraints:**
   - If the array is **already sorted** and you don't need original indices: **Two Pointers**, O(n) time, O(1) space — beats HashMap on space with equal time.
   - If the array is **unsorted** and you need original indices, or need strictly the fastest solution regardless of space: **HashMap**, O(n) time.
   - For **3Sum/4Sum**, Two Pointers (after sorting) is generally preferred because HashMap-based k-sum gets complicated with duplicate handling — sorting + two pointers deduplicates naturally by skipping equal adjacent values.

**Why Two Pointers wins for sorted data:** it matches HashMap's O(n) time while using O(1) space, and it extends naturally to k-sum variants where HashMap approaches get unwieldy.

---

## 9. Complexity Analysis

### Time Complexity
- **Best case:** O(1) if the very first pair checked satisfies the condition (e.g., pointers start already at the answer).
- **Average case:** O(n) — each pointer moves at most `n` times total across the whole run.
- **Worst case:** O(n) — even when no valid pair exists, `left` and `right` converge in at most `n` total steps.

**Where O(n) comes from:** `left` only ever increases, `right` only ever decreases (opposite-direction), or `fast` only ever increases while `slow` trails it (same-direction). Each pointer visits each index at most once across the entire run, so total work is bounded by `2n` or `n` comparisons — linear, not quadratic, even though you're "checking pairs."

### Space Complexity
- **Auxiliary space:** O(1) — just the two pointer variables (plus maybe a running sum/count).
- **Input space:** O(n) for the array (not counted as extra).
- **If sorting is required first:** add O(log n) to O(n) depending on the sort algorithm's stack/space usage — but the two-pointer scan itself remains O(1) extra.

### How complexity changes
- **Input size increases:** time grows linearly — this is the whole appeal versus the O(n²) brute force.
- **Nested loop introduced** (e.g., 3Sum = fix one element with a loop, two-pointer the rest): total becomes O(n²) — still far better than the O(n³) brute force for triplets.
- **Sorting required first:** adds O(n log n), which then dominates the O(n) two-pointer scan — total is O(n log n).
- **Hashing introduced instead:** trades the O(n log n) sort for O(n) time but adds O(n) space — a real trade-off depending on whether index order matters.
- **Recursion introduced:** rare for this pattern, but if used (e.g., recursive 3Sum-via-2Sum), adds O(n) stack space in the worst case.
- **Another data structure added** (e.g., two-pointer over two separate sorted arrays instead of one): still O(n+m) — same principle, just tracking two independent indices.

---

## 10. Edge Cases

| Edge Case | How Two Pointers Handles It |
|---|---|
| Empty input (`n = 0`) | `left=0, right=-1` → loop condition `left < right` is false immediately → no valid pair |
| Single element | `left == right` from the start → loop never executes → correctly "no pair possible" |
| Two elements | One comparison decides everything |
| Duplicate values | Opposite-direction: still finds *a* valid pair correctly; for triplets (3Sum), must explicitly skip duplicate values to avoid repeated triplets in the output |
| All values identical | Sum comparisons behave predictably; may need duplicate-skipping logic depending on whether repeats are wanted in output |
| Already sorted input | This is the assumption for opposite-direction two pointers — works as designed |
| Reverse-sorted input | Must re-sort ascending first, or flip pointer movement logic to match |
| Negative numbers | No issue for sum-based problems — comparisons still work correctly |
| Zero | No special handling needed unless zero has domain meaning (e.g., "container with water" — a zero-height wall) |
| Very large values | Watch for integer overflow when summing two large values — use `long` if needed |
| Very large input | Still O(n) — scales linearly, no special concern |
| No valid answer | Loop terminates with `left >= right`; return sentinel (`-1,-1` or empty list) |
| Multiple valid answers | Decide whether to return first found, all pairs, or a specific one — logic must be added explicitly (two pointers naturally finds one match per convergence, not all) |
| Answer at beginning / end | Handled naturally by the pointer positions — no special-casing needed |
| Entire input is the answer | E.g., in "container with most water," this happens naturally if the tallest walls are at both ends |
| Minimum/maximum possible constraints | Sanity-check pointer initialization matches array bounds (`right = n-1`, not `n`) |

---

## 11. Failure Modes

❌ **Wrong:** `while (left <= right)` for opposite-direction pair search when `left == right` would mean using the same element twice.
✅ **Correct:** `while (left < right)` — ensures two *distinct* indices are always used.

❌ **Wrong:** Moving both pointers on every iteration regardless of the comparison result.
✅ **Correct:** Move only the pointer that can actually fix the condition (`left++` if sum too small, `right--` if too big) — moving both blindly can skip valid pairs.

❌ **Wrong:** Forgetting to skip duplicate values in 3Sum/4Sum, producing repeated triplets in the output.
✅ **Correct:** After finding a valid triplet, advance `left`/`right` past any repeated values (`while (left < right && arr[left] == arr[left-1]) left++`).

❌ **Wrong:** Using two pointers on unsorted data expecting the monotonic "too big/too small" logic to still hold.
✅ **Correct:** Sort first (if index order doesn't matter), or switch to HashMap if it does.

❌ **Wrong:** In same-direction (slow/fast) problems, incrementing `slow` even when the fast-pointer element doesn't meet the keep-condition — corrupting the "confirmed valid" region.
✅ **Correct:** Only advance `slow` (and write) when `fast`'s element actually qualifies.

❌ **Wrong:** Off-by-one in merge-two-sorted-lists — forgetting to append the remaining tail of whichever list wasn't exhausted first.
✅ **Correct:** After the main loop, explicitly copy any remaining elements from both `A[i:]` and `B[j:]`.

❌ **Wrong:** Infinite loop from a condition branch that doesn't move either pointer.
✅ **Correct:** Every branch of your logic must strictly advance `left`, `right`, `slow`, or `fast` — never leave all pointers unchanged.

---

## 12. Pattern Decision Tree

```
Does the problem involve comparing/combining elements from an
array, string, or linked list?
 ├── NO → Two Pointers likely doesn't apply.
 └── YES
      │
      Is the data sorted (or can it be sorted without losing
      needed info like original index)?
      ├── NO → Consider HashMap/HashSet instead
      │         (unless index order truly doesn't matter — then sort first)
      └── YES
           │
           Are you comparing from both ends toward the middle
           (pair sum, palindrome, container with water)?
           ├── YES → Opposite-Direction Two Pointers
           └── NO
                │
                Are you scanning forward, writing only elements
                that meet some keep-condition (dedup, partition,
                remove element)?
                ├── YES → Same-Direction (slow/fast) Two Pointers
                └── NO
                     │
                     Are you combining two SEPARATE already-sorted
                     sequences into one?
                     ├── YES → Independent Two Pointers (merge)
                     └── NO → Re-examine — likely Sliding Window
                               (if window size is dynamic) or
                               Binary Search (if searching a single
                               boundary/value)
```

---

## 13. Problem-Solving Checklist

1. What is the input — array, string, or linked list? Sorted or unsorted?
2. Is the answer a pair, a triplet, an in-place transformation, or a merge?
3. Can I sort without losing information I need (like original indices)?
4. Should my pointers move toward each other, in the same direction, or independently across two structures?
5. What condition tells me which pointer to move?
6. Am I correctly excluding `left == right` where a distinct pair is required?
7. Do I need to skip duplicates to avoid repeated results?
8. Can I reduce an O(n²) brute force to O(n) with this technique?
9. What invariant should remain true at every step (e.g., "everything before `slow` is confirmed valid")?
10. What are the edge cases — empty input, all duplicates, no valid pair?

---

## 14. Practice Questions — Progressive Difficulty

*Attempt each one before scrolling for hints. I've included problem statement, constraints, a hint, the pattern being tested, and expected complexity — ask me for the full solution to any specific one when you're ready to check your work.*

### Level 1 — Recognition
**Q1.1** Given a sorted array, return indices of two numbers that sum to target (1-indexed).
- Input: `[2,7,11,15], target=9` → `[1,2]`
- Hint: This is the direct opposite-direction template.
- Pattern: Two Pointers (opposite direction). Expected: O(n) / O(1).

**Q1.2** Check if a string is a palindrome (ignoring non-alphanumeric characters).
- Input: `"A man, a plan, a canal: Panama"` → `true`
- Hint: Compare characters from both ends, skipping non-alphanumeric ones.
- Pattern: Two Pointers (opposite direction). Expected: O(n) / O(1).

### Level 2 — Basic Application
**Q2.1** Remove duplicates from a sorted array in place, return new length.
- Input: `[0,0,1,1,1,2,2,3,3,4]` → `5`, array becomes `[0,1,2,3,4,...]`
- Hint: `slow` tracks the last unique write position.
- Pattern: Two Pointers (same direction). Expected: O(n) / O(1).

**Q2.2** Merge two sorted arrays into one sorted array in place (second array has trailing space in first).
- Input: `nums1=[1,2,3,0,0,0], m=3, nums2=[2,5,6], n=3` → `[1,2,2,3,5,6]`
- Hint: Merge from the *back* to avoid overwriting unprocessed elements.
- Pattern: Two Pointers (independent, reverse merge). Expected: O(n+m) / O(1).

### Level 3 — Modified Pattern
**Q3.1** Container With Most Water — maximize area between two vertical lines.
- Input: `[1,8,6,2,5,4,8,3,7]` → `49`
- Hint: Always move the pointer at the *shorter* line — moving the taller one can never improve the area.
- Pattern: Two Pointers (opposite direction, greedy). Expected: O(n) / O(1).

**Q3.2** Given a sorted array, find all unique triplets that sum to zero (3Sum).
- Input: `[-1,0,1,2,-1,-4]` → `[[-1,-1,2],[-1,0,1]]`
- Hint: Fix one element with an outer loop, two-pointer the rest; skip duplicates at every level.
- Pattern: Two Pointers + Outer Loop. Expected: O(n²) / O(1) extra (excluding output).

### Level 4 — Pattern Combination
**Q4.1** 3Sum Closest — find the triplet whose sum is closest to target.
- Hint: Same 3Sum skeleton, but track the closest sum seen instead of exact matches.
- Pattern: Two Pointers + Running Best. Expected: O(n²) / O(1).

**Q4.2** Sort an array of 0s, 1s, and 2s in place (Dutch National Flag).
- Hint: Three pointers this time — `low`, `mid`, `high` — partitioning into three regions.
- Pattern: Two/Three Pointers (partitioning). Expected: O(n) / O(1).

### Level 5 — Interview-Level
**Q5.1** Trapping Rain Water — compute total trapped water given elevation heights.
- Hint: Track `leftMax` and `rightMax` as you move two pointers inward; the shorter side determines trapped water at that position.
- Pattern: Two Pointers + Running Max. Expected: O(n) / O(1).

**Q5.2** 4Sum — find all unique quadruplets summing to target.
- Hint: Two nested loops to fix two elements, then two-pointer the rest; skip duplicates at every nesting level.
- Pattern: Two Pointers + Double Outer Loop. Expected: O(n³) / O(1) extra.

### Level 6 — Advanced
**Q6.1** Minimum Window that contains all characters of another string (technically a sliding-window/two-pointer hybrid).
- Hint: This tests whether you can distinguish "two pointers converging" from "two pointers defining a dynamic window" — think carefully about which this actually is before coding.
- Pattern: Sliding Window (with two-pointer boundaries) — a good test of pattern-boundary awareness. Expected: O(n) / O(k).

**Q6.2** Given two sorted arrays, find the median of the combined array without fully merging them.
- Hint: This is *not* a simple two-pointer merge if you want better than O(n+m) — it needs Binary Search on partitions instead. A good test of knowing when two pointers is *not* optimal.
- Pattern: Binary Search (not Two Pointers) for the optimal O(log(min(m,n))) solution; O(n+m) two-pointer merge is a valid but suboptimal fallback.

---

## 15. Pattern-Based Question Bank

**Easy**
- [Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)
- [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/)
- [Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/)
- [Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/)
- [Reverse String](https://leetcode.com/problems/reverse-string/)

**Medium**
- [3Sum](https://leetcode.com/problems/3sum/)
- [3Sum Closest](https://leetcode.com/problems/3sum-closest/)
- [Container With Most Water](https://leetcode.com/problems/container-with-most-water/)
- [Sort Colors](https://leetcode.com/problems/sort-colors/)
- [Remove Duplicates from Sorted Array II](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/)
- [4Sum](https://leetcode.com/problems/4sum/)
- [Boats to Save People](https://leetcode.com/problems/boats-to-save-people/)

**Hard**
- [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/)
- [Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/) (edge case — better solved with Binary Search, see Q6.2)

**Interview-style**
- [3Sum Smaller](https://leetcode.com/problems/3sum-smaller/) (counting variant — tests understanding of *why* the pointer moves, not just pattern recall)
- [Squares of a Sorted Array](https://leetcode.com/problems/squares-of-a-sorted-array/) (opposite-direction with negative-number twist)

**Trick questions**
- [Two Sum](https://leetcode.com/problems/two-sum/) (unsorted!) — looks identical to Two Sum II but the array is unsorted; sorting loses original indices, so HashMap is actually the correct approach unless you track indices separately
- [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) — looks like it could use two pointers, but it's Sliding Window (dynamic window with a shrink rule, not two converging indices)

**Pattern recognition questions**
- [Valid Triangle Number](https://leetcode.com/problems/valid-triangle-number/) — disguised as a combinatorics/counting problem; sorting + two pointers finds valid triangle triplets in O(n²)
- [Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/) — looks like Two Pointers, but the window size is dynamic based on a running sum — actually Sliding Window

**Optimization questions**
- [3Sum](https://leetcode.com/problems/3sum/) — brute force is O(n³); two pointers after sorting brings it to O(n²)
- [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) — brute force with per-element max-scan is O(n²); two pointers with running max brings it to O(n)

**Edge-case questions**
- [3Sum](https://leetcode.com/problems/3sum/) — duplicate-skipping logic is where most implementations break
- [Remove Duplicates from Sorted Array II](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/) — allows up to 2 duplicates, testing whether you generalize the pointer logic correctly instead of hardcoding "no duplicates allowed"

**Where Two Pointers looks applicable but is NOT the correct approach**
- **"Longest substring without repeating characters"** — the "window" needs to grow and shrink dynamically based on a condition (no repeats), which is Sliding Window's job, not two pointers converging toward each other.
- **"Two Sum" (unsorted, need original indices)** — sorting to enable two pointers destroys index information; a HashMap solves it in O(n) without that trade-off.
- **"Find the median of two sorted arrays" (optimal solution)** — a two-pointer merge gets you O(n+m), but the truly optimal answer is O(log(min(m,n))) via Binary Search on partitions — two pointers is a valid fallback, not the best solution.

---

## 16. Solution Comparison

### Problem: 3Sum (find all unique triplets summing to zero)

**Approach 1 — Brute Force (Triple Nested Loop)**
- Complexity: O(n³) time, O(1) extra space (excluding output).
- Check every triplet directly; requires a Set to dedupe results.

**Approach 2 — HashSet-based (fix one, HashMap the rest)**
- Complexity: O(n²) time, O(n) space.
- For each pair `(i, j)`, check if `-(arr[i]+arr[j])` exists in a HashSet built as you scan — but duplicate-triplet handling gets messy without sorting first.

**Approach 3 — Pattern-Based (Sort + Two Pointers)**
- Complexity: O(n²) time, O(1) extra space (excluding output and sort's internal space).
- Sort once (O(n log n)), fix one element with an outer loop, two-pointer the rest — duplicates are naturally skippable by comparing to the previous value.

**Approach 4 — Alternative (Sort + Binary Search for third element)**
- Complexity: O(n² log n) time, O(1) extra space.
- For each pair `(i, j)`, binary search for the required third value — correct, but strictly worse than Approach 3 because it does `log n` work where two pointers does O(1) amortized work per step.

**Which is preferable and why:** Approach 3 is optimal in practice — same O(n²) time as Approach 2 but O(1) extra space instead of O(n), and cleaner duplicate handling than either HashSet or nested-binary-search approaches. Approach 1 is only useful as a correctness baseline for tiny inputs.

---

## 17. Interview Thinking

**Obvious version:** "Given a sorted array, find two numbers that sum to a target." — direct textbook Two Pointers.

**Disguised version:** "You're given the heights of vertical lines on the x-axis. Find two lines that, together with the x-axis, form a container holding the most water." This doesn't mention "pair" or "sum" at all, but it's still a pair-optimization problem over an array, and the greedy insight ("always move the shorter line") is what makes it Two Pointers rather than brute-force O(n²).

**Difficult version:** "Given an array of non-negative integers representing an elevation map, compute how much water it can trap after raining." This combines Two Pointers with a running-max invariant on *both* sides simultaneously, disguised as a simulation/geometry problem rather than a search problem. The key realization — water trapped at any position is bounded by `min(leftMax, rightMax) - height[i]` — isn't obviously a "two pointer" insight until you see that you can maintain `leftMax`/`rightMax` incrementally while converging two pointers inward.

**Clues that reveal the underlying pattern:**
- Any problem comparing/combining exactly two elements or two ends of a structure.
- A monotonic relationship between moving one side and the resulting value getting bigger/smaller.
- Constraints suggesting O(n) or O(n²) (for the k-sum family) is intended, when brute force would clearly be worse.

---

## 18. Real-World Application

- **Databases:** Merge joins in query engines use two pointers advancing through two sorted input streams (already-sorted indexes) to produce joined rows in linear time.
- **Networking:** TCP sliding-window-adjacent algorithms sometimes use two-pointer bookkeeping to track acknowledged vs. sent packet ranges.
- **Operating systems:** Memory compaction algorithms use same-direction two pointers (like the in-place dedup pattern) to compact live objects toward one end of a heap region during garbage collection.
- **Web applications:** Diffing/comparison algorithms (e.g., comparing two version arrays for a "what changed" view) often use two independent pointers walking through both versions.
- **AI/ML:** Two-pointer techniques appear in data preprocessing pipelines — e.g., merging sorted timestamped event logs from multiple sources into one chronological stream.
- **Distributed systems:** Merge-sort-based external sorting (sorting data too large for memory) relies on the same two-pointer merge step, repeated across many sorted chunks.

---

## 19. Memory Trick

> "If I see **sorted + pair/triplet sum**, or **compare from both ends**, think **Two Pointers**."

**Mnemonic: "Two hands, one line."** Picture two hands closing in on a single sorted line from opposite ends (or one hand chasing the other) — every movement is justified by sortedness, so nothing needs to be re-checked.

---

## 20. Active Recall Test

Answer these before moving on — I'll evaluate your reasoning, not just whether you got the "right" word:

1. What problem does Two Pointers solve, in your own words?
2. What are the recognition keywords/phrases that should make you think of it?
3. What is the core invariant maintained throughout the loop (for both opposite-direction and same-direction variants)?
4. What variables do you maintain, and what does each represent?
5. Why does moving only one pointer at a time (based on the comparison) guarantee correctness — i.e., why doesn't it risk skipping a valid pair?
6. What is its time complexity, and how does that compare to the brute-force alternative?
7. What is its space complexity?
8. Name two edge cases that could break a naive implementation.
9. Name one pattern that's easily confused with Two Pointers, and explain how to tell them apart.
10. Give an example of a problem where Two Pointers looks tempting but is NOT the right (or not the optimal) choice — and say why.

**Coding problem (identify the pattern yourself — I won't tell you which one this is):**

> You're given an array of integers `heights` representing the heights of people standing in a line, and an integer `k`. You may swap the positions of at most `k` pairs of adjacent people. Find whether it's possible, after at most `k` swaps, for the array to become non-decreasing (sorted in ascending order).

Work through it: does this fit the Two Pointers shape, or does something about "adjacent swaps" and "at most k" suggest a different pattern entirely? Explain your reasoning.

---

## 21. Final Cheat Sheet

```
Pattern:                Two Pointers
Purpose:                Reduce O(n²) pair/triplet or in-place transformation
                        problems to O(n) by exploiting sortedness or structure
                        with two moving indices instead of nested loops.
Recognition keywords:   pair sum, sorted array, palindrome, in-place, remove
                        duplicates, container with most water, triplet,
                        3Sum/4Sum, merge two sorted
Core idea:              Two indices move toward each other (opposite),
                        one chases the other (same direction), or both
                        advance independently through two structures —
                        each guided by a monotonic comparison.
Typical data structure: None (array/string/linked-list indices only)
Core variables:         left, right (opposite) OR slow, fast (same direction)
                        OR i, j (independent merge)
Core operations:        compare arr[left]/arr[right]; move the pointer
                        that can fix the condition; record on match
Time complexity:        O(n) single pass; O(n²) for k-sum variants with
                        an outer fixing loop
Space complexity:       O(1) extra (excluding sort's own space/output)
Common alternatives:    Sliding Window (dynamic window), HashMap (unsorted,
                        need original indices), Binary Search (single value/
                        boundary, not a pair)
Common mistakes:        left <= right causing same-element reuse, moving
                        both pointers blindly, forgetting duplicate-skipping
                        in k-sum, using it on unsorted data without sorting
                        first, off-by-one in leftover-tail merging
Important edge cases:   empty array, single/two elements, all duplicates,
                        no valid pair, very large values (overflow on sum)
When NOT to use:        unsorted data where index order matters (use
                        HashMap), dynamic-size contiguous ranges (use
                        Sliding Window), single boundary/value search
                        (use Binary Search)
Java functions/classes: none built-in for the core logic; StringBuilder.
                        reverse() / Collections.reverse() for simple
                        reversal only
Top 10 problems:        Two Sum II, Valid Palindrome, Remove Duplicates
                        from Sorted Array, Merge Sorted Array, 3Sum,
                        3Sum Closest, Container With Most Water, Sort
                        Colors, 4Sum, Trapping Rain Water
```

> **One-line recognition rule:** "When you see a sorted structure and a pair/triplet condition, an in-place transformation, or two ends to compare, immediately consider Two Pointers."
