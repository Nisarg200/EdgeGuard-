# EdgeGuard: An Adaptive Privacy-Preserving Gateway for Secure Industrial LLM Integration

## Title Page

**EdgeGuard: An Adaptive Privacy-Preserving Gateway for Secure Industrial LLM Integration**

A B.Tech project report submitted in partial fulfillment of the requirements for the award of the degree of

**Bachelor of Technology**

by

**Nisarg Parmar (Roll No. 202201443)**  
**Saish Pagar (Roll No. 202201092)**

Under the Supervision of

**Prof. [Supervisor Name]**

DA-IICT, Gandhinagar

---

## Certificate

This is to certify that the report entitled **“EdgeGuard: An Adaptive Privacy-Preserving Gateway for Secure Industrial LLM Integration”**, submitted by **Nisarg Parmar** and **Saish Pagar** to DA-IICT, for the award of the degree of **Bachelor of Technology in Information and Communication Technology (ICT)**, is a record of the original, bona fide work carried out by them under my supervision and guidance. The report has reached the standards fulfilling the requirements of the regulations related to the award of the degree.

The results contained in this report have not been submitted in part or in full to any other University or Institute for the award of any degree or diploma to the best of my knowledge.

....................................  
**Prof. [Supervisor Name]**  
DA-IICT, Gandhinagar

---

## Declaration

We declare that this written submission represents our ideas in our own words and where others’ ideas or words have been included, we have adequately cited and referenced the original sources. We also declare that we have adhered to all principles of academic honesty and integrity and have not misrepresented or fabricated or falsified any data in our submission. We understand that any violation of the above will be cause for disciplinary action by the Institute and can also evoke penal action from the sources which have thus not been properly cited or from whom proper permission has not been taken when needed.

...........................  
**Nisarg Parmar**  
Roll No.: 202201443

...........................  
**Saish Pagar**  
Roll No.: 202201092

Date:  
Place: DA-IICT, Gandhinagar

---

## Acknowledgements

We would like to express our sincere gratitude to our supervisor, **Prof. [Supervisor Name]**, for the guidance, encouragement, and technical direction provided throughout this B.Tech project. His insights were instrumental in shaping both the research perspective and the engineering realization of this work.

We also thank the faculty and institute for providing an academic environment that encouraged us to explore contemporary problems in secure AI systems. Finally, we are grateful to our peers and well-wishers whose feedback and support helped us refine the conceptual and practical aspects of this project.

**Nisarg Parmar**  
**Saish Pagar**

---

## Abstract

The rapid adoption of Large Language Models (LLMs) in industrial decision-support systems has created a tension between the computational benefits of cloud-scale reasoning and the operational constraints of real-world industrial environments. While cloud-hosted LLMs offer strong language understanding and reasoning capability, their direct use in industrial settings raises critical concerns related to data privacy, network latency, prompt injection, and the uncontrolled exposure of sensitive local knowledge. Conversely, fully edge-only deployments often fail to provide the reasoning depth required for complex operational queries. This project addresses that gap through the design and implementation of **EdgeGuard**, an adaptive privacy-preserving gateway for secure industrial LLM integration.

EdgeGuard is engineered as a hybrid cloud-edge-client protective architecture that inserts a trust-enforcing gateway before external model inference. The system consists of three principal technical layers: **semantic de-identification**, which detects and masks sensitive industrial identifiers before transmission; **adversarial input filtering**, which identifies prompt injection, policy bypass, and data exfiltration attempts at the network entry point; and **secure local contextualization**, which uses Retrieval-Augmented Generation (RAG) principles to inject only minimal, role-appropriate local knowledge into the LLM workflow while preserving strict isolation of restricted documents.

To demonstrate the feasibility of the proposed architecture, a complete simulation and interactive web-based prototype were developed. The prototype includes a browser-based control dashboard, a gateway processing backend, a curated industrial knowledge base, scenario-driven validation, and an OpenAI-compatible backend connector with safe offline fallback support. Experimental evaluation across benign and adversarial industrial query scenarios showed that the EdgeGuard pipeline successfully blocked all simulated malicious requests in the test set, applied semantic redaction to sensitive identifiers, prevented exposure of restricted local records, and produced grounded, safety-oriented responses for legitimate users. Although the gateway introduces modest latency overhead compared to a direct cloud path, the resulting gains in trustworthiness, privacy, and operational safety demonstrate the practical value of a secure gateway model for industrial AI deployment.

---

## Proposed Table of Contents

1. Introduction
2. Literature Review & Comparative Study
3. EdgeGuard System Design
4. Implementation and Software Architecture
5. Analysis and Results
6. Conclusions and Practical Implications
7. Appendices
8. Bibliography

---

## Chapter 1: Introduction

### 1.1 Motivation

Industrial organizations are increasingly exploring the use of Large Language Models (LLMs) to assist in maintenance support, anomaly explanation, operational guidance, compliance checking, and knowledge retrieval. These models offer the ability to convert large volumes of technical information into natural-language recommendations, thereby improving decision support for engineers, operators, and analysts. However, the direct deployment of cloud-based LLMs in industrial settings remains problematic. Production systems, machine identifiers, maintenance histories, proprietary formulas, and internal procedures often constitute sensitive operational assets that cannot be safely transmitted to external services without strict controls.

In addition to privacy concerns, network latency and connectivity reliability further complicate the industrial use of LLMs. Time-sensitive industrial tasks often demand rapid, context-aware, and safe responses, yet a purely cloud-dependent architecture may introduce delay or failure under constrained network conditions. At the same time, edge-only language systems often lack the reasoning strength and flexibility of larger external models. This creates a practical need for a hybrid architecture capable of safely mediating between local industrial systems and high-capability LLM services.

The concept of **EdgeGuard** emerges from this requirement. Instead of treating the LLM itself as a trusted component, EdgeGuard introduces a localized trust boundary in front of the model. This trust boundary ensures that sensitive industrial data is sanitized, malicious prompt patterns are intercepted, and only approved contextual knowledge is forwarded for inference. In doing so, the system attempts to convert the theoretical trustworthiness requirements of modern edge-intelligence literature into a practical architecture suitable for real-world industrial deployment.

### 1.2 Problem Statement

The objective of this B.Tech project is to design and implement **EdgeGuard**, an adaptive privacy-preserving gateway that enables the safe use of external or cloud-based LLMs in industrial settings. The system must ensure that sensitive identifiers and proprietary information are not directly exposed to external models, that adversarial prompt patterns are detected and blocked before inference, and that local operational context is incorporated through a secure retrieval layer without revealing the contents of restricted internal knowledge bases.

The gateway must therefore solve three tightly coupled problems. First, it must preserve privacy through real-time semantic masking of industrial identifiers. Second, it must protect the inference pipeline from prompt injection, policy bypass, and exfiltration attempts at the network entry point. Third, it must support accurate and contextually grounded answers by selectively retrieving role-appropriate local knowledge while maintaining zero-trust isolation of restricted content. The final system must be demonstrable through a working simulation and a presentation-ready interactive interface.

### 1.3 Project Objectives

To address the above problem, this project is structured around the following engineering objectives:

- To design a **semantic de-identification layer** capable of identifying and masking sensitive industrial identifiers such as machine asset tags, employee identifiers, batch references, and other structured operational tokens.
- To develop an **adversarial input filtering layer** that detects prompt injection attempts, privilege escalation patterns, policy bypass requests, and sensitive-data harvesting language before the query reaches the LLM inference stage.
- To implement a **secure local contextualization module** based on Retrieval-Augmented Generation (RAG) principles, allowing only approved and role-appropriate operational knowledge to be used for response grounding.
- To build a **hybrid edge-cloud architecture** in which a local gateway mediates between industrial users and external LLM services, enforcing trust boundaries on all outgoing requests.
- To create a **working simulation and interactive software prototype** that demonstrates the full EdgeGuard pipeline across realistic industrial scenarios.
- To evaluate the system on the basis of **security, privacy, latency, and contextual relevance**, and compare the gateway-based architecture with a direct cloud-only baseline.

### 1.4 Dissertation Organization

This dissertation is organized into six chapters to systematically present the conceptual, architectural, implementation, and evaluative aspects of EdgeGuard:

- **Chapter 1 (Introduction):** Describes the motivation, problem statement, and technical objectives of the proposed project.
- **Chapter 2 (Literature Review & Comparative Study):** Reviews the literature on LLM-based edge intelligence, prompt injection defenses, privacy-preserving inference, and secure RAG architectures, while identifying the research gap addressed by EdgeGuard.
- **Chapter 3 (EdgeGuard System Design):** Presents the overall architecture of the EdgeGuard gateway and details the design of its semantic de-identification, adversarial filtering, and secure retrieval modules.
- **Chapter 4 (Implementation and Software Architecture):** Describes the implementation of the simulation engine, interactive dashboard, backend gateway service, and OpenAI-compatible LLM connector.
- **Chapter 5 (Analysis and Results):** Evaluates the proposed system using benign and adversarial industrial scenarios and compares the security and privacy behavior of EdgeGuard against a direct baseline architecture.
- **Chapter 6 (Conclusions and Practical Implications):** Summarizes the contributions of the work, discusses its implications for secure industrial AI deployment, identifies limitations, and outlines directions for future work.

---

## Chapter 2: Literature Review & Comparative Study

### 2.1 Introduction

The secure integration of Large Language Models (LLMs) into industrial environments lies at the intersection of multiple research domains, including edge intelligence, privacy-preserving inference, adversarial prompt defense, and Retrieval-Augmented Generation (RAG). While the capabilities of LLMs have made them attractive for industrial decision support and operational assistance, their deployment in sensitive environments introduces new attack surfaces and trust challenges. This chapter examines recent academic and architectural literature relevant to these concerns and identifies the gap that motivates the EdgeGuard approach.

### 2.2 Existing Academic and Architectural Approaches

Recent surveys on LLM-based edge intelligence highlight the emerging importance of hybrid cloud-edge-client architectures in enabling real-time, privacy-aware intelligent systems. Such architectures attempt to balance the reasoning power of large external models with the locality and responsiveness of edge computation. At the same time, academic work on secure RAG systems has emphasized the need to inject contextual information into LLM pipelines without exposing complete private knowledge bases. Parallel work in API gateway security and edge-level policy enforcement demonstrates that the network entry point is a natural location for adaptive security controls.

### 2.3 Security and Privacy Challenges

The literature consistently identifies prompt injection and jailbreaking as major threats to integrated LLM systems. These attacks seek to override system instructions, bypass policies, or extract sensitive data by manipulating input language. In industrial settings, the consequences of such attacks may include the disclosure of proprietary formulas, operational procedures, maintenance secrets, or internal credentials. Another major concern is the privacy risk associated with cloud-bound inference, where even benign user queries may inadvertently reveal machine identifiers, supplier data, or confidential process details. Research on secure RAG further warns of membership inference and knowledge exfiltration risks when private retrieval systems are loosely connected to generative models.

### 2.4 Research Gaps and Proposed Novelty

Although prior research has studied prompt filtering, privacy-aware inference, and secure retrieval separately, relatively little work has focused on a unified industrial gateway that combines all three functions into a single adaptive pre-inference architecture. Existing solutions are often cloud-only, which weakens privacy guarantees, or edge-only, which limits reasoning capability. The key novelty of EdgeGuard lies in framing the trust problem as a gateway design problem. Instead of modifying the external LLM directly, EdgeGuard creates a localized protective sleeve that sanitizes sensitive inputs, intercepts adversarial instructions, and injects only minimal approved context before inference. This architecture offers a practical way to operationalize trustworthiness in industrial LLM deployment.

### 2.5 Summary

The literature indicates that the safe industrial use of LLMs requires a hybrid design that jointly addresses privacy, security, and contextual grounding. Prompt injection defense, semantic masking, and secure retrieval have each been studied independently, but their integration into a unified industrial gateway remains underexplored. This gap provides the central motivation for the EdgeGuard system developed in the subsequent chapters.
