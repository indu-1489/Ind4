#!/usr/bin/env python3
"""
cp_tools.py
Combined competitive-programming utilities:
- cf1372d: Subsequence Permutation (CF 1372D) solver (single or multi-test)
- palindrome: palindrome utilities (string/number/longest substring)

Usage examples:
  python3 cp_tools.py cf1372d --single   # read single test: n then array
  python3 cp_tools.py cf1372d --multi    # read t then t test cases
  python3 cp_tools.py palindrome string "A man, a plan, a canal: Panama" --ignore-non-alnum --case-insensitive
  python3 cp_tools.py palindrome number 12321
  python3 cp_tools.py palindrome longest "babad"

Author: GitHub Copilot Chat Assistant
"""
from typing import Optional
import sys
import argparse
import re

# ---------- CF 1372D: Subsequence Permutation ----------

def solve_cf1372d_single_from_lines(lines: list[str]) -> str:
    """Solve single test case: first token n, then n integers."""
    it = iter(lines)
    try:
        n = int(next(it))
    except StopIteration:
        return "0"
    a = [int(next(it)) for _ in range(n)]
    expected = 1
    for x in a:
        if x == expected:
            expected += 1
    return str(expected - 1)


def solve_cf1372d_multi_from_ints(data: list[int]) -> str:
    """Solve multi-test input where data is a flat list of integers: t, then each test n and n values."""
    it = iter(data)
    try:
        t = next(it)
    except StopIteration:
        return ""
    out = []
    for _ in range(t):
        n = next(it)
        a = [next(it) for _ in range(n)]
        expected = 1
        for x in a:
            if x == expected:
                expected += 1
        out.append(str(expected - 1))
    return "\n".join(out)

# ---------- Palindrome utilities ----------

def is_palindrome_str(s: str, ignore_non_alnum: bool = True, case_insensitive: bool = True) -> bool:
    if ignore_non_alnum:
        s = re.sub(r'[^A-Za-z0-9]', '', s)
    if case_insensitive:
        s = s.lower()
    return s == s[::-1]


def is_palindrome_number(n: int) -> bool:
    if n < 0:
        return False
    s = str(n)
    return s == s[::-1]


def longest_palindromic_substring(s: str) -> str:
    if not s:
        return ""
    start, end = 0, 0
    for i in range(len(s)):
        # odd
        l, r = i, i
        while l >= 0 and r < len(s) and s[l] == s[r]:
            if (r - l) > (end - start):
                start, end = l, r
            l -= 1
            r += 1
        # even
        l, r = i, i + 1
        while l >= 0 and r < len(s) and s[l] == s[r]:
            if (r - l) > (end - start):
                start, end = l, r
            l -= 1
            r += 1
    return s[start:end+1]

# ---------- CLI Entrypoint ----------

def main(argv: Optional[list] = None) -> None:
    p = argparse.ArgumentParser(prog="cp_tools.py", description="CP helper utilities: cf1372d and palindrome")
    sub = p.add_subparsers(dest="cmd", required=True)

    # cf1372d subcommand
    sc_cf = sub.add_parser("cf1372d", help="Solve CF 1372D: Subsequence Permutation")
    group = sc_cf.add_mutually_exclusive_group()
    group.add_argument("--single", action="store_true", help="Single test: read n then array from stdin (default if no other flags)")
    group.add_argument("--multi", action="store_true", help="Multi-test: read t then test cases from stdin")

    # palindrome subcommand
    sc_pal = sub.add_parser("palindrome", help="Palindrome utilities")
    sc_pal.add_argument("mode", choices=["string", "number", "longest"], help="Operation mode")
    sc_pal.add_argument("value", nargs="?", help="Value to check (if omitted, read from stdin)")
    sc_pal.add_argument("--ignore-non-alnum", action="store_true", help="Ignore non-alphanumeric characters when checking strings")
    sc_pal.add_argument("--case-insensitive", action="store_true", help="Case-insensitive string checks")

    args = p.parse_args(argv)

    if args.cmd == "cf1372d":
        # Read all tokens from stdin
        data = sys.stdin.read().strip().split()
        if not data:
            print(0)
            return
        if args.multi:
            ints = list(map(int, data))
            print(solve_cf1372d_multi_from_ints(ints))
        else:
            # default to single if not specified
            print(solve_cf1372d_single_from_lines(data))

    elif args.cmd == "palindrome":
        if args.value is None:
            lines = sys.stdin.read().splitlines()
            if not lines:
                print("No input provided", file=sys.stderr)
                sys.exit(1)
            value = "\n".join(lines) if args.mode == "longest" else lines[0]
        else:
            value = args.value

        if args.mode == "string":
            res = is_palindrome_str(value, ignore_non_alnum=args.ignore_non_alnum, case_insensitive=args.case_insensitive)
            print("YES" if res else "NO")
        elif args.mode == "number":
            try:
                n = int(value.strip())
            except ValueError:
                print("Invalid integer", file=sys.stderr)
                sys.exit(1)
            print("YES" if is_palindrome_number(n) else "NO")
        else:
            print(longest_palindromic_substring(value))

if __name__ == "__main__":
    main()
