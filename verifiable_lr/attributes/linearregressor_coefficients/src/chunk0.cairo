use orion::numbers::{FixedTrait, FP16x16};

fn compute(ref a: Array<FP16x16>) {
a.append(FP16x16 { mag: 546473, sign: false });
a.append(FP16x16 { mag: 578200, sign: true });
a.append(FP16x16 { mag: 63473, sign: false });
a.append(FP16x16 { mag: 0, sign: false });
a.append(FP16x16 { mag: 45, sign: false });
a.append(FP16x16 { mag: 60, sign: true });
a.append(FP16x16 { mag: 0, sign: true });
a.append(FP16x16 { mag: 14, sign: false });
a.append(FP16x16 { mag: 587108, sign: true });
a.append(FP16x16 { mag: 609192, sign: false });
}