# Product-Screenshot-Automation
This project was designed to extract to automate screenshot taking of online products given the url, without the use of apis to remove the modals, ads, or anything that might block us from taking appropriate screenshots of the target webpage.

It has a success rate of over 97%, across the sites that I tried and can be used as a tool for market analysis.

Currently it only saves the screenshots to a local dir but can be altered to store anywhere else.

Also the parameters for the ad/modal blockers can be reconfigured, and you can implement a user-agent and ip switcher to avoid detection as of now it works just fine across most websites but with persistent visits to the same domain, the website will enforce a captcha but the fetch blocker implemented might mitigate the problem in some scenarios.
