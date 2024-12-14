drop table if exists nums;
create table nums (a integer, b integer);

COPY nums (a, b) from '/home/brian/code/aoc2024/data/day01_sql.txt' with DELIMITER ',';

-- part 1
with a_sorted as (
  select a, row_number() over(order by a) as row from nums
), b_sorted as (
  select  b, row_number() over(order by b) as row from nums
) select sum(abs(a - b)) as part1 from a_sorted
join b_sorted on a_sorted.row = b_sorted.row;

-- part 2
with b_counts as (
  select b, count(b) as b_count from nums group by b
) select sum(a * b_count) as part2 from nums
join b_counts on nums.a = b_counts.b;
