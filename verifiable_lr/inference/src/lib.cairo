use orion::operators::tensor::{Tensor, TensorTrait};
use orion::operators::tensor::{U32Tensor, I32Tensor, I8Tensor, FP8x23Tensor, FP16x16Tensor, FP32x32Tensor, BoolTensor};
use orion::numbers::{FP8x23, FP16x16, FP32x32};
use orion::operators::matrix::{MutMatrix, MutMatrixImpl};
use orion::operators::nn::{NNTrait, FP16x16NN};
use orion::operators::ml;


use linearregressor_coefficients::get_linearregressor_coefficients;
use linearregressor_intercepts::get_linearregressor_intercepts;

fn main(node_float_input: Tensor<FP16x16>) -> Tensor<FP16x16> {
let node_variable = 
    ml::LinearRegressorTrait::predict(
        ml::LinearRegressor {
            coefficients: get_linearregressor_coefficients(),
            intercepts: Option::Some(get_linearregressor_intercepts()),
            target: 1,
            post_transform: ml::POST_TRANSFORM::NONE
        }
        , node_float_input)
    ;

        node_variable
    }