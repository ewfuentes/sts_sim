use pyo3::prelude::*;
use rand::rngs::StdRng;
use rand::{Rng, SeedableRng};

#[pyclass]
#[derive(Clone, Debug)]
pub struct TheDie {
    rng: StdRng,
}

#[pymethods]
impl TheDie {
    #[new]
    #[pyo3(signature = (seed=None))]
    pub fn new(seed: Option<u64>) -> Self {
        let rng = match seed {
            Some(s) => StdRng::seed_from_u64(s),
            None => StdRng::from_entropy(),
        };
        TheDie { rng }
    }

    pub fn roll(&mut self) -> u8 {
        self.rng.gen_range(1..=6)
    }

    #[staticmethod]
    pub fn behavior_index(roll: u8) -> usize {
        match roll {
            1 | 2 => 0,
            3 | 4 => 1,
            5 | 6 => 2,
            _ => panic!("Invalid die roll: {}", roll),
        }
    }
}
