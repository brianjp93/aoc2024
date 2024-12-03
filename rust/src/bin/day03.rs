use regex::Regex;
use std::fs::read_to_string;

fn main() {
    let data = read_to_string("../data/day03.txt").unwrap();
    let re = Regex::new(r"mul\((\d+),(\d+)\)").unwrap();
    let p1: i32 = re
        .captures_iter(&data)
        .map(|m| {
            let a = m.get(1).unwrap().as_str().parse::<i32>().unwrap();
            let b = m.get(2).unwrap().as_str().parse::<i32>().unwrap();
            a * b
        })
        .sum();
    let p2: i32 = data
        .split("do()")
        .into_iter()
        .map(|part| {
            re.captures_iter(part.split("don't()").next().unwrap())
                .map(|x| {
                    x.get(1).unwrap().as_str().parse::<i32>().unwrap()
                        * x.get(2).unwrap().as_str().parse::<i32>().unwrap()
                })
                .sum::<i32>()
        })
        .sum();
    println!("Part 1: {}", p1);
    println!("Part 2: {}", p2);
}
