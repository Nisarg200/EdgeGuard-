# EdgeGuard Report Structure

This document maps the sample BTP report format to our project:

**EdgeGuard: An Adaptive Privacy-Preserving Gateway for Secure Industrial LLM Integration**

## 1. Format Observed From Sample Report

The sample report follows this structure:

1. Title Page
2. Certificate
3. Declaration
4. Acknowledgements
5. Abstract
6. Contents
7. List of Figures
8. Abbreviations
9. Chapter 1: Introduction
10. Chapter 2: Literature Review & Comparative Study
11. Chapter 3: System Design
12. Chapter 4: Software / Architecture
13. Chapter 5: Analysis and Results
14. Chapter 6: Conclusions and Practical Implications
15. Appendices
16. Bibliography

This is a very standard and safe academic pattern, so we should keep the same macro-structure.

## 2. Recommended EdgeGuard Report Layout

### Title Page

Title:
**EdgeGuard: An Adaptive Privacy-Preserving Gateway for Secure Industrial LLM Integration**

Subtitle:
A B.Tech project report submitted in partial fulfillment of the requirements for the award of the degree of Bachelor of Technology

Authors:
- Nisarg Parmar (Roll No. 202201443)
- Saish Pagar (Roll No. 202201092)

Supervisor:
- Prof. [Supervisor Name]

Institute:
- DA-IICT, Gandhinagar

### Certificate

Keep the same tone and institutional format as the sample report, replacing names, title, and supervisor.

### Declaration

Keep the same style as the sample report with both student names and roll numbers.

### Acknowledgements

Short and formal:
- supervisor
- institute
- faculty or lab support if needed

### Abstract

Write in the same style as the sample:
- start with the industry problem
- present the proposed system
- describe the architecture in compact technical language
- summarize implementation and simulation
- end with the key findings and practical value

### Contents

Auto-generated later.

### List of Figures

We should plan figures such as:
- EdgeGuard overall architecture
- request processing pipeline
- semantic de-identification flow
- adversarial filtering logic
- secure RAG flow
- dashboard screenshots
- result comparison charts

### Abbreviations

Likely entries:
- AI
- API
- EI
- IIoT
- JSON
- KB
- LLM
- PII
- RAG
- SOP
- UI
- WAN
- Zero Trust

## 3. Chapter-by-Chapter Mapping

## Chapter 1: Introduction

Keep the same sectioning pattern as the sample report.

### 1.1 Motivation

Explain:
- industrial organizations want LLM reasoning
- cloud-only LLM usage creates privacy, latency, and trust issues
- edge-only deployments are weaker for advanced reasoning
- a hybrid gateway architecture is needed

### 1.2 Problem Statement

Define the engineering problem clearly:
- how to safely integrate powerful LLMs into industrial workflows
- how to protect sensitive operational data
- how to defend against prompt injection
- how to ground responses in local knowledge without exposing the knowledge base

### 1.3 Project Objectives

Use bullet points similar to the sample:
- build semantic de-identification layer
- build adversarial input filtering layer
- build secure local contextualization using RAG
- integrate a cloud or external LLM safely
- simulate attack and benign scenarios
- evaluate privacy, security, latency, and contextual accuracy

### 1.4 Dissertation Organization

Use the same style as the sample report:
- Chapter 1 introduction
- Chapter 2 literature review
- Chapter 3 architecture and system design
- Chapter 4 implementation and software architecture
- Chapter 5 analysis and results
- Chapter 6 conclusions and future work

## Chapter 2: Literature Review & Comparative Study

This should mirror the style of the sample but be aligned to our topic.

### 2.1 Introduction

State that the chapter reviews literature in:
- edge intelligence
- industrial LLM deployment
- prompt injection defense
- privacy-preserving inference
- secure RAG

### 2.2 Existing Academic and Architectural Approaches

Cover:
- cloud-only LLM deployment
- edge-only LLM deployment
- cloud-edge-client architecture
- RAG-based grounding
- API gateway security

### 2.3 Security and Privacy Challenges

Discuss:
- prompt injection
- jailbreaking
- exfiltration
- membership inference in RAG
- data sovereignty concerns

### 2.4 Research Gaps and Proposed Novelty

This is where EdgeGuard becomes distinct:
- existing works discuss parts separately
- few combine privacy, adversarial filtering, and secure retrieval in one gateway
- EdgeGuard proposes a unified adaptive sleeve before cloud inference

### 2.5 Summary

Short summary paragraph.

## Chapter 3: EdgeGuard System Design

This chapter replaces the hardware chapter in the sample with architecture-focused system design.

### 3.1 Introduction

Introduce the EdgeGuard gateway.

### 3.2 Overall Architecture

Describe:
- user/client layer
- local edge gateway
- isolated knowledge base
- external/cloud LLM

### 3.3 Semantic De-identification Module

Explain:
- identifier patterns
- masking logic
- preservation of semantic intent

### 3.4 Adversarial Input Filtering Module

Explain:
- rule-based scoring
- attack indicators
- monitored vs blocked decisions

### 3.5 Secure Local Contextualization Module

Explain:
- local document tagging
- role-based access control
- minimum necessary retrieval
- restricted document isolation

### 3.6 Data Flow and Trust Boundaries

Very important for presentation and report:
- what stays local
- what is sanitized
- what goes to the LLM
- what is blocked before inference

### 3.7 Summary

## Chapter 4: Implementation and Software Architecture

This chapter should explain the actual app and simulation stack.

### 4.1 Introduction

### 4.2 Interactive Dashboard

Describe:
- hero panel
- scenario selector
- query form
- metrics strip
- timeline
- retrieval panel
- final response panel

### 4.3 Backend Gateway Service

Explain:
- request routing
- pipeline orchestration
- JSON response structure

### 4.4 LLM Connector and Fallback Strategy

Explain:
- OpenAI-compatible backend
- live mode vs offline fallback
- policy blocking before inference

### 4.5 Scenario Dataset and Local Knowledge Base

Explain:
- benign scenarios
- attack scenarios
- operations/maintenance/security roles

### 4.6 Deployment Workflow

Explain how the app runs on the local machine.

### 4.7 Summary

## Chapter 5: Analysis and Results

This chapter should look closest in spirit to the sample report’s validation chapter.

### 5.1 Introduction

### 5.2 Experimental Setup

Explain:
- baseline cloud path
- EdgeGuard path
- metrics used

### 5.3 Scenario-Based Validation

Include:
- benign operations query
- sensitive maintenance query
- prompt injection attempt
- data exfiltration attempt
- policy question
- mixed benign-malicious query

### 5.4 Quantitative Results

Use our simulation numbers:
- attack blocking rate
- redactions applied
- restricted exposures prevented
- latency comparison

### 5.5 Qualitative Interpretation

Explain:
- why modest latency overhead is acceptable
- why privacy and trustworthiness improve
- why grounded responses are more suitable for industry

### 5.6 Summary

## Chapter 6: Conclusions and Practical Implications

Same spirit as sample report.

### 6.1 Summary
### 6.2 Study Findings
### 6.3 Conclusive Contribution of the Project
### 6.4 Practical Implications
### 6.5 Study Limitations
### 6.6 Scope for Future Work

## 4. Appendices

Possible appendices:

- Appendix A: Core Python Simulation Code
- Appendix B: Web App Backend Architecture
- Appendix C: Prompt Scenarios and Test Cases
- Appendix D: Screenshots of Dashboard

## 5. Writing Style To Match the Sample

To stay similar to the sample report:

- keep formal academic language
- use engineering-focused phrasing
- use precise subsection numbering
- use short concluding summaries at the end of each chapter
- use figures and tables frequently
- make the abstract dense and technical
- keep novelty clearly stated in Chapter 2
- keep implementation clearly separated from results

## 6. What We Should Write Next

The next best step is to draft these sections in order:

1. Title Page
2. Certificate
3. Declaration
4. Acknowledgements
5. Abstract
6. Chapter 1
7. Chapter 2

Then we move to architecture, implementation, and results.
