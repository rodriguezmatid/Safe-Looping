mod chunk0;

use orion::numbers::{FixedTrait, FP16x16};

fn get_linearregressor_coefficients() -> Span<FP16x16> {

    let mut data = array![];
     chunk0::compute(ref data);

    data.span()
}