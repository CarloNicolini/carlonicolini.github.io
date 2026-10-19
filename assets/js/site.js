const themeButton = document.querySelector('.theme-toggle');
function updateThemeLabel() { const dark = document.documentElement.dataset.theme === 'dark'; themeButton.setAttribute('aria-label', `Switch to ${dark ? 'light' : 'dark'} theme`); themeButton.setAttribute('aria-pressed', String(dark)); }
updateThemeLabel();
themeButton.addEventListener('click', () => { const theme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark'; document.documentElement.dataset.theme = theme; try { localStorage.setItem('theme', theme); } catch(e) {} updateThemeLabel(); });
const search = document.querySelector('[data-search]');
const topic = document.querySelector('[data-topic]');
if (search) {
 const rows = [...document.querySelectorAll('[data-search-item]')];
 const parameters = new URLSearchParams(location.search);
 const initialQuery = parameters.get('q');
 if (initialQuery) search.value = initialQuery;
 const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
 const searchTexts = rows.map(row => normalize(row.dataset.searchText || row.textContent));
 function filter() {
   const terms = normalize(search.value.trim()).split(/\s+/).filter(Boolean);
   let count = 0;
   rows.forEach((row, index) => {
     const text = searchTexts[index];
     const words = text.split(/[^a-z0-9]+/);
     const match = terms.every(term => term.length <= 2 ? words.includes(term) : text.includes(term))
       && (!topic || topic.value === 'all' || row.dataset.category.split(' ').includes(topic.value));
     row.hidden = !match;
     count += match ? 1 : 0;
   });
   const empty = document.querySelector('.empty-state');
   if (empty) empty.hidden = count > 0;
   const counter = document.querySelector('[data-result-count]');
   if (counter) counter.textContent = count;
   const label = document.querySelector('[data-result-label]');
   if (label) label.textContent = count === 1 ? 'article' : 'articles';
 }
 function updateFilters() {
   filter();
   if (topic) {
     const url = new URL(location.href);
     if (search.value.trim()) url.searchParams.set('q', search.value.trim()); else url.searchParams.delete('q');
     if (topic.value !== 'all') url.searchParams.set('topic', topic.value); else url.searchParams.delete('topic');
     history.replaceState(null, '', url);
   }
 }
 search.addEventListener('input', updateFilters);
 if (topic) {
   const aliases = {tech: 'engineering', 'deep-learning': 'ai', 'machine-learning': 'ai'};
   const value = aliases[parameters.get('topic')] || parameters.get('topic');
   if ([...topic.options].some(option => option.value === value)) topic.value = value;
   topic.addEventListener('change', updateFilters);
 }
 filter();
}

// A suggested sequence based on the learner's stated starting experience.
const academyGoal = document.querySelector('[data-academy-goal]');
const academyBackground = document.querySelector('[data-academy-background]');
const academyPlan = document.querySelector('[data-academy-plan]');
if (academyGoal && academyBackground && academyPlan) {
  function updateLearningPlan() {
    const track = academyGoal.value;
    const trackSection = document.getElementById(track);
    const title = trackSection.dataset.trackTitle;
    const lessonCount = Number(trackSection.dataset.trackLessons);
    const background = academyBackground.value;
    const preparation = background === 'new'
      ? '<li><a href="#preparation-python">P1 · Getting comfortable with Python</a></li><li><a href="#preparation-data">P2 · Working with data and uncertainty</a></li>'
      : background === 'some'
      ? '<li><a href="#preparation-data">P2 · Review data and uncertainty</a></li>'
      : '';
    const preparationCount = background === 'new' ? 2 : background === 'some' ? 1 : 0;
    academyPlan.innerHTML = `<h3>${title}: a suggested starting route</h3><ol>${preparation}<li><a href="#${track}-lesson-1">${title}, lessons 1–${lessonCount}</a></li></ol><p>${lessonCount + preparationCount} suggested meetings. We can skip familiar topics, add practice, or choose individual lessons.</p><a href="#lesson-enquiry">Discuss this plan →</a>`;

  }
  academyGoal.addEventListener('change', updateLearningPlan);
  academyBackground.addEventListener('change', updateLearningPlan);
  updateLearningPlan();
}
