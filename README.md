## ELB-internal-hosted-zone

This is a tool that's used to update a hosted zone with the internal IP address of an ELB (Elastic Load Balancer).

I could not think of a better name, so feel free to suggest one in issue #1.

---

The use case for this is where you have an internet-facing service that uses ELB, and you want to connect other applications within the VPC to that ELB without traffic going outside your VPC. 

By default, the internal IP address for this ELB is hard to find and dynamically updated, making it unreliable to simply get the internal IP once and then update your R53 updated zone with that internal IP address. This script has a scheduler to update a route53 hosted zone record every few minutes with the internal ELB ip, in case it changes.

#### Requirements

1. Existing hosted zone
2. Existing internet-facing ELB
3. [Serverless framework](https://serverless.com/framework/docs/providers/aws/guide/installation/) and [Yarn](https://yarnpkg.com/)

#### Setup

1. Clone this repository
2. `yarn install`
3. Copy `.env.example` to `.env` and fill in the relevant variables
4. `serverless deploy`

###### Origin

The code was adapted from [here](https://gist.github.com/darylounet/3c6253c60b7dc52da927b80a0ae8d428), credit to @darylounet, and inspired from [this SO question](https://stackoverflow.com/q/36584595/3878893).
