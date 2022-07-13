#product_spec
LQ=3_645
P0=105.4
P1=108.3
ETC=.0_7

def iv(
    lq=LQ,
    p0=P0,
    p1=P1,
    etc=ETC,
    type=False):

    #delta
    delta=abs(p1-p0)/p0
    
    #prod_type
    if type:
        basis=1+delta
    else:
        basis=1-delta
    
    #value_diff
    diff=lq*(basis-1)
    #intraday value
    iv=(lq*basis)*(1-(etc/365))
    print(
        (LQ,P0,P1,ETC,round(ETC/365,5))
    )

    return {
        "delta":delta,
        "difference":diff,
        "iv":iv}

def pro(
    cap):
    
    q=cap/10
    w=q*2
    e=w*2
    r=q*5

    return {
        "10":q,
        "20":w,
        "40":e,
        "50":r}

def vwp(
    alpha,
    beta,
    delta
    ):
    return "vwap"