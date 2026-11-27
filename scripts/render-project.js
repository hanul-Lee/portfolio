// Build-only HTML rendering; data is supplied by build-site.cjs.
const icon = (name) => {
  const paths = {
    search: '<circle cx="10" cy="10" r="6"/><path d="m15 15 5 5"/>',
    flow: '<path d="M4 6h7M13 6h7M7 6v12h10V6M4 18h7M13 18h7"/>',
    data: '<path d="M5 19V9M12 19V4M19 19v-7"/>',
    action: '<path d="m5 12 4 4L19 6"/>',
    voice:
      '<path d="M16 10a2 2 0 0 1-2 2H6.828a2 2 0 0 0-1.414.586l-2.202 2.202A.71.71 0 0 1 2 14.286V4a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/><path d="M20 9a2 2 0 0 1 2 2v10.286a.71.71 0 0 1-1.212.502l-2.202-2.202A2 2 0 0 0 17.172 19H10a2 2 0 0 1-2-2v-1"/>',
  };
  const className =
    name === "voice" ? "lucide lucide-messages-square preview-icon" : "";
  return `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="${className}" aria-hidden="true">${paths[name] || paths.action}</svg>`;
};

const renderMockup = (type, finalVisual, pending) => {
  if (finalVisual)
    return `<div class="mock-window final-mockup ${finalVisual[3]}"><img src="${finalVisual[0]}" alt="${finalVisual[1]}" decoding="async"></div>`;
  return pending ? renderPendingVisual(pending) : "";
};

// Cases still in progress keep their layout with labelled empty phone frames until the screens are added.
const renderPendingVisual = (pending) =>
  `<div class="mock-window visual-pending" role="img" aria-label="${pending.label}"><ol style="--frames: ${pending.frames.length}">${pending.frames.map((frame, i) => `<li><span>${String(i + 1).padStart(2, "0")}</span><b>${frame}</b></li>`).join("")}</ol><p>${pending.label}</p></div>`;

const renderReframe = (item, number) =>
  item
    ? `
  <article class="story-section reframe" id="reframe">
    <header><p>${number} ${item.label || "문제 재정의"}</p><h3>${item.title || "기존 업무에서 해결할 문제와 설계 방향을 정리했습니다."}</h3></header>
    <div class="reframe-flow">
      <div><small>${item.labels?.[0] || "설계 과제"}</small><p>${item.request}</p></div>
      <span>→</span>
      <div><small>${item.labels?.[1] || "관찰한 문제"}</small><p>${item.observed}</p></div>
      <span>→</span>
      <div class="reframed"><small>${item.labels?.[2] || "다시 정의한 문제"}</small><p>${item.result}</p></div>
    </div>
  </article>`
    : "";

const renderIteration = (item, number) =>
  item
    ? `
  <article class="story-section iteration" id="iteration">
    <header><p>${number} 설계 조정</p><h3>기존 구조와 설계한 화면을 비교합니다.</h3></header>
    <div class="iteration-compare">
      <div><small>초기안</small><strong>${item.initial}</strong>${item.initialImage ? `<div class="comparison-image ${item.initialCrop ? `split-${item.initialCrop}` : ""}"><img src="${item.initialImage}" alt="초기안 화면" loading="lazy" decoding="async"></div>` : '<div class="wireframe initial"><i></i><i></i><i></i><i></i></div>'}</div>
      <blockquote><small>설계에 반영한 내용</small><p>${item.feedback}</p></blockquote>
      <div class="final"><small>최종안</small><strong>${item.final}</strong>${item.finalImage ? `<div class="comparison-image ${item.finalCrop ? `split-${item.finalCrop}` : ""}"><img src="${item.finalImage}" alt="최종안 화면" loading="lazy" decoding="async"></div>` : '<div class="wireframe"><i></i><i></i><i></i></div>'}</div>
    </div>
  </article>`
    : "";

const renderReflection = (item, number) =>
  item
    ? `
  <article class="story-section reflection" id="reflection">
    <header><p>${number} 회고</p><h3>설계하며 배운 점, 다음에 확인할 점</h3></header>
    <div class="reflection-grid"><div><small>배운 점</small><p>${item.learned}</p></div><div><small>다시 한다면</small><p>${item.next}</p></div></div>
  </article>`
    : "";

const renderVisuals = (items, label = "설계 자료", title = "실제 화면과 설계 자료") =>
  items?.length
    ? `
  <article class="story-section project-visuals" id="visuals">
    <header><p>${label}</p><h3>${title}</h3></header>
    <div class="project-visual-grid">${items
      .map(
        (item, index) => `
      <figure class="${index === 0 ? "featured" : ""} ${item[3] || ""}">
        <div class="visual-frame ${item[3] || ""}"><img src="${item[0]}" alt="${item[1]}" loading="lazy" decoding="async"></div>
        <figcaption><b>${item[1]}</b><span>${item[2]}</span><small>${item[0].includes("/public-concepts/") ? "공개용 재설계 · 가상 데이터" : item[0].includes("/20261024/") ? "포트폴리오 설명용 재구성" : "해당 프로젝트 설계 자료"}</small></figcaption>
      </figure>`,
      )
      .join("")}</div>
  </article>`
    : "";

// ---- Story blocks: one core problem, the reason for a choice, equal-size states, and proposals kept apart from delivered work.
const renderStoryFlow = (flow, number) =>
  flow
    ? `
  <article class="story-section story-flow" id="${flow.id || "flow"}">
    <header><p>${number} ${flow.label}</p><h3>${flow.title}</h3></header>
    ${flow.intro ? `<p class="block-intro">${flow.intro}</p>` : ""}
    <ol class="flow-steps" style="--steps: ${flow.steps.length}">${flow.steps
      .map(([tag, title, text]) => `<li><small>${tag}</small><strong>${title}</strong><p>${text}</p></li>`)
      .join("")}</ol>
    ${flow.callout ? `<aside class="flow-callout"><strong>${flow.callout[0]}</strong><p>${flow.callout[1]}</p></aside>` : ""}
  </article>`
    : "";

const renderRationale = (item, number) =>
  item
    ? `
  <article class="story-section rationale" id="${item.id || "rationale"}">
    <header><p>${number} ${item.label || "선택 이유"}</p><h3>${item.title}</h3></header>
    ${item.intro ? `<p class="block-intro">${item.intro}</p>` : ""}
    ${item.criteria ? `<ul class="rationale-criteria" aria-label="비교 기준">${item.criteria.map((x) => `<li>${x}</li>`).join("")}</ul>` : ""}
    <div class="rationale-options">${item.rows
      .map(([option, text, chosen]) => `<div${chosen ? ' class="is-chosen"' : ""}><h4>${chosen ? '<span class="chosen-badge">선택</span>' : ""}${option}</h4><p>${text}</p></div>`)
      .join("")}</div>
    ${item.note ? `<p class="block-note">${item.note}</p>` : ""}
  </article>`
    : "";

const renderStateCompare = (item, number) =>
  item
    ? `
  <article class="story-section state-compare" id="${item.id || "states"}">
    <header><p>${number} ${item.label || "상태 비교"}</p><h3>${item.title}</h3></header>
    ${item.intro ? `<p class="block-intro">${item.intro}</p>` : ""}
    <div class="state-grid ${item.layout || ""}" style="--cols: ${item.items.length}">${item.items
      .map(([src, title, text, tag]) => `<figure${tag ? ' class="is-proposal"' : ""}><div class="state-frame"><img src="${src}" alt="${title} 상태 화면" loading="lazy" decoding="async"></div><figcaption>${tag ? `<span class="proposal-badge">${tag}</span>` : ""}<b>${title}</b><span>${text}</span></figcaption></figure>`)
      .join("")}</div>
    ${item.note ? `<p class="block-note">${item.note}</p>` : ""}
  </article>`
    : "";

// HTML states read sharply on mobile, unlike state names drawn inside an image.
const renderInputStates = (item, number) =>
  item
    ? `
  <article class="story-section input-states" id="${item.id || "input-states"}">
    <header><p>${number} ${item.label}</p><h3>${item.title}</h3></header>
    ${item.intro ? `<p class="block-intro">${item.intro}</p>` : ""}
    <div class="input-state-grid">${item.states
      .map(([name, value, mod, rule]) => `<div class="input-state ${mod}"><small>${name}</small><div class="demo-field" aria-hidden="true"><span>${value}</span>${mod === "is-typing" ? "<i></i>" : ""}</div><p>${rule}</p></div>`)
      .join("")}</div>
    ${item.reuse ? `<dl class="reuse-split">${item.reuse.map(([title, text]) => `<div><dt>${title}</dt><dd>${text}</dd></div>`).join("")}</dl>` : ""}
    ${item.note ? `<p class="block-note">${item.note}</p>` : ""}
  </article>`
    : "";

// Crop slide-style source images to the screen area; explanations move into the page body.
const cropStyle = (crop) => {
  if (!crop) return "";
  const zoom = 1 / crop.w;
  const ratio = (crop.w * crop.aspect) / crop.h;
  return `--crop-ratio: ${ratio.toFixed(4)}; --crop-zoom: ${(zoom * 100).toFixed(3)}%; --crop-x: ${(-crop.x * zoom * 100).toFixed(3)}%; --crop-y: ${(-crop.y / crop.h * 100).toFixed(3)}%`;
};
const renderCropFigure = (shot) => `<figure class="annotated-shot"><div class="${shot.crop ? "crop-frame" : "visual-frame landscape"}"${shot.crop ? ` style="${cropStyle(shot.crop)}"` : ""}><img src="${shot.image}" alt="${shot.alt}" loading="lazy" decoding="async"></div>${shot.caption ? `<figcaption>${shot.caption}</figcaption>` : ""}</figure>`;
const renderAnnotated = (item, number) =>
  item
    ? `
  <article class="story-section annotated" id="${item.id || "annotated"}">
    <header><p>${number} ${item.label}</p><h3>${item.title}</h3></header>
    ${item.intro ? `<p class="block-intro">${item.intro}</p>` : ""}
    ${item.groups
      .map(
        (group) => `
    <div class="annotated-group ${group.layout || ""}">
      <div class="annotated-shots">${group.shots.map(renderCropFigure).join("")}</div>
      ${group.notes ? `<dl class="annotated-notes">${group.notes.map(([title, text]) => `<div><dt>${title}</dt><dd>${text}</dd></div>`).join("")}</dl>` : ""}
    </div>`,
      )
      .join("")}
    ${item.note ? `<p class="block-note">${item.note}</p>` : ""}
  </article>`
    : "";

const renderProposals = (item, number) =>
  item
    ? `
  <article class="story-section proposals" id="proposals">
    <header><p>${number} ${item.label || "다음 개선 제안"}</p><h3>${item.title}</h3></header>
    <p class="proposal-scope"><span class="proposal-badge">개선 제안</span>${item.scope || "실제 프로젝트에서 수행한 작업이 아니라, 사례를 돌아보며 정리한 다음 단계입니다."}</p>
    <dl class="proposal-list">${item.items.map(([title, text]) => `<div><dt>${title}</dt><dd>${text}</dd></div>`).join("")}</dl>
  </article>`
    : "";

// Slots for evidence that is described now and attached as images later.
const renderEvidenceSlots = (item, number) => `
  <article class="story-section evidence-slots" id="${item.id || "evidence-slots"}">
    <header><p>${number} ${item.label}</p><h3>${item.title}</h3></header>
    ${item.intro ? `<p class="block-intro">${item.intro}</p>` : ""}
    <div class="evidence-slot-grid">${item.slots
      .map(([title, text, rows]) => `<figure class="evidence-slot">${rows ? `<dl class="slot-rows">${rows.map(([k, v, swatch]) => `<div>${swatch ? `<i style="background:${swatch}" aria-hidden="true"></i>` : ""}<dt>${k}</dt><dd>${v}</dd></div>`).join("")}</dl>` : `<div class="slot-frame"><span>자료 추가 예정</span></div>`}<figcaption><b>${title}</b><span>${text}</span></figcaption></figure>`)
      .join("")}</div>
    ${item.note ? `<p class="block-note">${item.note}</p>` : ""}
  </article>`;

// Existing project decisions, with explicit follow-up questions rather than invented test results.
const decisionNotes = {
  "designsystem": [
    ["본인 담당", "가이드 기획과 Figma 디자인: 컬러 역할, 입력·검색 상태, 배치 예시를 정의했습니다."],
    ["선임 담당", "가이드를 바탕으로 재사용 컴포넌트를 구현해 Git에 공유했습니다."],
    ["공개 자료의 성격", "아래 화면은 설명용 재구성입니다. 당시 Figma 라이브러리나 실제 서비스 코드를 대신하지 않습니다."]
  ],
  "dashboard": [
    ["전사", "전체 예산이 계획대로 쓰이고 있는지 판단합니다."],
    ["프로젝트", "비용이 몰린 프로젝트가 어디이고, 어떤 인원·직무에서 생겼는지 찾습니다."],
    ["개인", "본인이 기록한 투입 시간과 기준 초과 여부를 확인합니다."]
  ],
  "intranet": [
    ["팀 참여", "디자이너 팀에서 기획·UI·퍼블리싱에 참여했습니다."],
    ["실제 범위", "회의실 현황 → 예약 입력 / 문서 상태 → 근태 신청 입력"],
    ["확인 범위", "미배포 · 팀 내부 설계·구현 확인"]
  ]
};

const renderDecisionNotes = (key) => decisionNotes[key] ? `<aside class="decision-notes" aria-label="설계 판단과 후속 확인">${decisionNotes[key].map(([title, text]) => `<div><h4>${title}</h4><p>${text}</p></div>`).join("")}</aside>` : "";

const renderDecisionDetail = (detail) => detail ? `
    <div class="decision-detail">
      <div class="decision-detail-copy"><p class="detail-eyebrow">${detail.eyebrow}</p><h4>${detail.title}</h4><p>${detail.intro}</p></div>
      <dl class="decision-options">${detail.options.map(([title, text, x], i) => `<div${i === detail.options.length - 1 ? ' class="is-selected"' : ""}><dt>${title}</dt><dd><div class="option-preview" style="--source-left: ${-(x / 549) * 100}%"><img src="${detail.image}" alt="${title} 메뉴 시안의 지도와 메뉴 부분" loading="lazy" decoding="async"></div><p>${text}</p></dd></div>`).join("")}</dl>
      <details class="decision-source"><summary>원본 시안 비교 자료 보기</summary><figure><div class="visual-frame landscape"><img src="${detail.image}" alt="${detail.alt}" loading="lazy" decoding="async"></div><figcaption>${detail.caption}</figcaption></figure></details>
      <p class="comparison-context">같은 크기로 비교할 수 있도록 당시 메뉴 디자인 시안의 지도·메뉴 부분을 발췌했습니다.</p>
    </div>` : "";

const renderDocumentStory = (study) => {
  const story = study.documentStory;
  let section = 1;
  const n = () => String(section++).padStart(2, "0");
  return `
  ${study.storyFlow ? renderStoryFlow(study.storyFlow, n()) : ""}
  ${renderVisuals([study.finalVisual, ...study.visuals], "현장 작업자의 휴대폰 화면", "매일 쓰는 일지 작성·확인·서명 화면")}
  <article class="story-section tbm-document-story" id="decision">
    <header><p>${n()} 함께 설계한 기준</p><h3>${story.decisionTitle}</h3></header>
    <dl class="tbm-state-list">${story.decisions.map(([title, text]) => `<div><dt>${title}</dt><dd>${text}</dd></div>`).join("")}</dl>
    ${story.supportText ? `<p class="tbm-body-copy tbm-support-copy">${story.supportText}</p>` : ""}
  </article>
  <article class="story-section tbm-document-story" id="solution">
    <header><p>${n()} 운영 중 추가한 PC 화면</p><h3>${story.screenTitle}</h3></header>
    <figure class="tbm-primary-screen"><div class="visual-frame landscape"><img src="${study.impact.visual[0]}" alt="${study.impact.visual[1]}" decoding="async"></div><figcaption>${story.screenText}</figcaption></figure>
    <p class="tbm-source-note">파일 목록과 PDF 열람 화면 · 가상 데이터로 재구성</p>
  </article>
  ${study.stateCompare ? renderStateCompare(study.stateCompare, n()) : ""}
  ${study.rationale ? renderRationale(study.rationale, n()) : ""}
  <article class="story-section tbm-document-story" id="impact">
    <header><p>${n()} 결과</p><h3>${story.resultTitle}</h3></header>
    <p class="tbm-body-copy">${story.resultText}</p>
    ${story.evidence ? `<dl class="evidence-basis">${story.evidence.map(([title, text]) => `<div><dt>${title}</dt><dd>${text}</dd></div>`).join("")}</dl>` : ""}
    <p class="tbm-delivery-callout">${story.deliveryText}</p>
    <section class="tbm-ai-workflow" aria-labelledby="tbm-ai-title"><h4 id="tbm-ai-title">${story.aiTitle}</h4><dl>${story.aiWorkflow.map(([title, text]) => `<div><dt>${title}</dt><dd>${text}</dd></div>`).join("")}</dl></section>
    <p class="tbm-source-note">${story.note}</p>
  </article>
  ${study.proposals ? renderProposals(study.proposals, n()) : ""}`;
};

const renderStudy = (study) => {
  if (study.documentStory) return renderDocumentStory(study);
  let section = 2;
  const nextSection = () => String(section++).padStart(2, "0");
  const renderSolution = () => `
  <article class="story-section solution" id="solution">
    <div class="solution-copy"><p>${nextSection()} ${study.solutionLabel || "설계 화면과 흐름"}</p><h3>${study.uiTitle}</h3><span>${study.uiText}</span>${study.solutionSteps ? `<ol class="solution-steps">${study.solutionSteps.map((x) => `<li><b>${x[0]}</b><span>${x[1]}</span></li>`).join("")}</ol>` : ""}</div>
    <div class="ui-stage">${renderMockup(study.ui, study.finalVisual, study.pendingVisual)}</div>
  </article>
`;
  return `
  ${study.briefFacts ? "" : `<article class="story-section evidence" id="evidence">
    <header><p>${nextSection()} ${study.evidenceLabel || "설계 과제"}</p><h3>${study.insight}</h3></header>
    ${study.evidenceLink ? `<aside class="evidence-source"><p>${study.evidenceLink[0]}</p><a href="${study.evidenceLink[2] || "#visuals"}">${study.evidenceLink[1]} <span aria-hidden="true">↓</span></a></aside>` : ""}
    <div class="evidence-grid">${study.pains.map((x, i) => `<div><small>0${i + 1}</small><h4>${x[0]}</h4><p>${x[1]}</p></div>`).join("")}</div>
  </article>`}
  ${study.storyFlow ? renderStoryFlow(study.storyFlow, nextSection()) : ""}
  ${study.reframe ? renderReframe(study.reframe, nextSection()) : ""}
  ${study.solutionFirst ? renderSolution() : ""}
  <article class="story-section strategy" id="decision">
    <header><p>${nextSection()} ${study.strategyLabel || "설계 결정"}</p><h3>${study.strategyHeadline}</h3></header>
    <div class="strategy-list">${study.strategies.map((x) => `<div><b>${x[0]}</b><h4>${x[1]}</h4><small>설계 내용</small><p>${x[2]}</p></div>`).join("")}</div>
    ${renderDecisionDetail(study.decisionDetail)}
    ${renderDecisionNotes(slug)}
  </article>
  ${study.rationale ? renderRationale(study.rationale, nextSection()) : ""}
  ${study.inputStates ? renderInputStates(study.inputStates, nextSection()) : ""}
  ${study.extensionFlow ? renderStoryFlow(study.extensionFlow, nextSection()) : ""}
  ${study.stateCompare ? renderStateCompare(study.stateCompare, nextSection()) : ""}
  ${study.annotated ? renderAnnotated(study.annotated, nextSection()) : ""}
  ${study.iteration ? renderIteration(study.iteration, nextSection()) : ""}
  ${study.solutionFirst ? "" : renderSolution()}
  ${renderVisuals(study.visuals, study.visualsLabel, study.visualsTitle)}
  ${(study.evidenceSlots || []).map((item) => renderEvidenceSlots(item, nextSection())).join("")}
  ${study.impact ? renderImpact(study.impact, nextSection()) : ""}
  ${study.testFlow ? renderStoryFlow(study.testFlow, nextSection()) : ""}
  ${study.proposals ? renderProposals(study.proposals, nextSection()) : ""}
  ${study.reflection ? renderReflection(study.reflection, nextSection()) : ""}`;
};

const renderImpact = (impact, number) => `
  <article class="story-section impact impact-${impact.type}" id="impact">
    <header><p>${number} ${impact.label}</p><h3>${impact.title}</h3></header>
    <div class="impact-flow">
      <div><small>BEFORE</small><strong>${impact.before}</strong></div>
      <span aria-hidden="true"><i></i><b>→</b></span>
      <div class="after"><small>AFTER</small><strong>${impact.after}</strong></div>
    </div>
    ${impact.visual ? `<figure class="delivery-visual"><div class="visual-frame"><img src="${impact.visual[0]}" alt="${impact.visual[1]}" loading="lazy" decoding="async"></div><figcaption>${impact.visual[2]}</figcaption></figure>` : ""}
    ${impact.feedback ? `<aside class="feedback-record"><p class="feedback-label">${impact.feedback.label}</p><blockquote>${impact.feedback.text}</blockquote><p>${impact.feedback.context}</p></aside>` : ""}
    ${impact.facts ? `<dl class="delivery-facts">${impact.facts.map(([title, text]) => `<div><dt>${title}</dt><dd>${text}</dd></div>`).join("")}</dl>` : ""}
    ${impact.note ? `<p class="impact-note">${impact.note}</p>` : ""}
  </article>`;

const slug = document.body.dataset.project;
const p = projects[slug];
if (p) {
  document.documentElement.style.setProperty("--case-bg", p.bg);
  document.documentElement.style.setProperty("--case-ink", p.ink);
  document.documentElement.style.setProperty("--case-accent", p.accent);
  document.documentElement.style.setProperty(
    "--case-text-accent",
    p.textAccent || p.accent,
  );
  document.documentElement.style.setProperty("--case-muted", p.muted);
  document.title = `${p.title} | 이한울 · UX/UI 디자이너`;
  document.querySelector(".case-eyebrow").textContent =
    `PROJECT ${p.no} · ${p.type}`;
  document.querySelector(".case-title").textContent = p.title;
  document.querySelector(".case-lead").textContent = p.lead;
  document.querySelector(".period").textContent = p.period;
  document.querySelector(".role").textContent = p.role;
  document.querySelector(".contribution").textContent = p.contribution;
  if (p.team) document.querySelector(".team").textContent = p.team;
  else document.querySelector(".team").parentElement.remove();
  document.querySelector(".stage").textContent = p.stage;
  const resultText = document.createElement("span");
  resultText.textContent = `"${p.summary}"`;
  document.querySelector(".case-result").replaceChildren(resultText);
  document.querySelector(".case-cover").innerHTML = renderMockup(
    caseStudies[slug].ui,
    caseStudies[slug].heroVisual || caseStudies[slug].finalVisual,
    caseStudies[slug].pendingVisual,
  );
  document.querySelector(".problem").textContent = p.problem;
  document.querySelector(".detail").textContent = p.detail;
  document.querySelector(".context-facts").innerHTML = caseStudies[slug].context
    .map((x) => `<div><small>${x[0]}</small><span>${x[1]}</span></div>`)
    .join("");
  document.querySelector(".outcomes").innerHTML = p.outcomes
    .map(
      (x) =>
        `<div class="outcome"><strong>${x[0]}</strong><span>${x[1]}</span></div>`,
    )
    .join("");
  document.querySelector(".gallery").innerHTML = renderStudy(caseStudies[slug]);
  const study = caseStudies[slug];
  document.querySelector(".case-hero").insertAdjacentHTML("afterend", `
    <section class="case-brief" id="brief" aria-labelledby="brief-title">
      <div class="brief-heading">
        <div class="brief-title-group"><p>CASE AT A GLANCE</p><h2 id="brief-title">이 사례의 핵심</h2></div>
        <a href="#solution">설계 화면 보기 <span aria-hidden="true">↓</span></a>
      </div>
      <dl class="brief-facts">
        ${(study.briefFacts || [["설계 과제", study.pains[0][1]], ["핵심 설계 결정", study.strategyHeadline], ["직접 담당한 범위", p.contribution]]).map(([label, text], index) => `<div${index === 1 ? ' class="brief-decision"' : ""}><dt><span aria-hidden="true">0${index + 1}</span> ${label}</dt><dd>${text}</dd></div>`).join("")}
      </dl>
      <div class="brief-scope"><strong>${p.deliverySummary && study.briefFacts ? "직접 담당" : "결과의 범위"}</strong><p>${p.deliverySummary && study.briefFacts ? p.contribution : p.deliverySummary || p.outcomeBasis}</p></div>
    </section>`);
  if (["tbm", "intranet", "measure", "dashboard", "kanvan", "intranet-day", "settle"].includes(slug)) {
    document.querySelector(".case-brief").insertAdjacentHTML("beforeend", `<aside class="public-concept-note" aria-label="공개 자료 안내"><strong>${study.publicNotice?.title || "공개용 재설계 · 가상 데이터"}</strong><p>${study.publicNotice?.text || "프로젝트 경험을 설명하기 위해 UI를 새로 디자인했습니다. 브랜드·인물·조직·현장·일정·문서·수치·그래프는 모두 가상이며, 실제 운영 화면과 내부 자료를 사용하지 않았습니다. 프로젝트 이력과 담당 역할은 실제 경험을 기준으로 기술했습니다."}</p></aside>`);
  }
  // 배경·결과 요약은 한 영역으로 묶어 외부 간격을 중복하지 않는다.
  const context = document.createElement("section");
  context.className = "case-context";
  context.setAttribute("aria-label", "프로젝트 배경과 결과 요약");
  const summary = document.querySelector(".case-summary");
  summary.before(context);
  context.append(summary, document.querySelector(".outcomes"));
  const nextSlug = projectOrder[(projectOrder.indexOf(slug) + 1) % projectOrder.length];
  document.querySelector(".next a").href = `project-${nextSlug}.html`;
  const nextProject=projects[nextSlug];
  const nextStudy=caseStudies[nextSlug];
  const nextVisual=nextStudy.heroVisual||nextStudy.finalVisual;
  const nextLink=document.querySelector(".next a");
  nextLink.classList.add("next-project");
  nextLink.innerHTML=`<div class="next-preview">${nextVisual?`<img src="${nextVisual[0]}" alt="" loading="lazy" decoding="async">`:`<span class="next-pending">화면 작업 중</span>`}</div><div class="next-copy"><span>다음 프로젝트</span><h3></h3><p></p></div>`;
  nextLink.querySelector("h3").textContent=nextProject.title;
  nextLink.querySelector("p").textContent=nextProject.summary;
  document.body.setAttribute("data-prerendered", "true");
}
