extern crate rug;
use rug::{Assign, Integer};
use pyo3::prelude::*;
use numext_fixed_uint::U4096;

#[pyfunction]
fn amultiply(a: &str, b: &str) -> PyResult<String> {
    let mut int1 = Integer::new();
    int1.assign(Integer::parse(a).unwrap());

    let mut int2 = Integer::new();
    int2.assign(Integer::parse(b).unwrap());

    Ok((int1 * int2).to_string())
}

#[pyfunction]
fn aadd(a: &str, b: &str) -> PyResult<String> {
    let mut int1 = Integer::new();
    int1.assign(Integer::parse(a).unwrap());

    let mut int2 = Integer::new();
    int2.assign(Integer::parse(b).unwrap());

    Ok((int1 + int2).to_string())
}

#[pyfunction]
fn multiplybig(a: &str, b: &str) -> PyResult<String> {
    let int1 = U4096::from_dec_str(a).unwrap();
    let int2 = U4096::from_dec_str(b).unwrap();

    Ok((int1 * int2).to_string())
}

#[pyfunction]
fn multiply(a: u128, b: u128) -> PyResult<u128> {
    Ok(a * b)
}

#[pyfunction]
fn add(a: u128, b: u128) -> PyResult<u128> {
    Ok(a + b)
}

#[pymodule]
fn rust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(amultiply, m)?)?;
    m.add_function(wrap_pyfunction!(aadd, m)?)?;
    m.add_function(wrap_pyfunction!(multiplybig, m)?)?;
    m.add_function(wrap_pyfunction!(multiply, m)?)?;
    m.add_function(wrap_pyfunction!(add, m)?)?;
    Ok(())
}
