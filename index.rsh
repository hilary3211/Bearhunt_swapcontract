'reach 0.1'

export const main = Reach.App(() => {
    const User1 = Participant('User1', {
        funds: UInt,
        getaddress: Fun([], Address),
    })
    const User2 = Participant('User2', {
        funds: UInt,

    })

    init()

    User1.only(() => {
        const funds = declassify(interact.funds)
        const getadd = declassify(interact.getaddress())
    })
    User1.publish(funds, getadd)
        .pay(funds)
    commit()
    User2.only(() => {
        const fund = declassify(interact.funds)
    })
    User2.publish(fund)
        .pay(fund)

    if (getadd == User2) {
        transfer(funds).to(User2)
        transfer(fund).to(User1)
    } else {
        transfer(funds).to(User1)
        transfer(fund).to(User2)
    }
    commit()




})
