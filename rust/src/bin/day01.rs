use std::{collections::HashMap, fs::read_to_string, iter::zip};

fn main() {
    let data = read_to_string("../data/day01.txt").unwrap();
    let mut l1: Vec<i32> = vec![];
    let mut l2: Vec<i32> = vec![];
    let mut l2_counter = HashMap::<i32, i32>::new();
    for line in data.lines() {
        let mut parts = line.split_whitespace().map(|x| {x.parse::<i32>().unwrap()});
        let a = parts.next().unwrap();
        let b = parts.next().unwrap();
        l1.push(a);
        l2.push(b);
        *l2_counter.entry(b).or_insert(0) += 1;
    }
    l1.sort_unstable();
    l2.sort_unstable();
    let p1 = zip(&l1, &l2).map(|(a, b)| {
        (a - b).abs()
    }).sum::<i32>();
    let p2 = l1.into_iter().map(|a| {
        let b = if let Some(b) = l2_counter.get(&a) {
            b
        } else {
            &0
        };
        a * b
    }).sum::<i32>();
    println!("Part 1: {}", p1);
    println!("Part 2: {}", p2);
}
