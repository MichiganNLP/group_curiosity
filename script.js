const dimensions = {
  epistemic: {
    symbol: '?', label: 'EPISTEMIC CURIOSITY',
    question: '“What missing fact would change our answer?”',
    copy: 'Agents reduce information gaps by asking clarifying questions before committing to an answer.',
    tasks: ['CommonsenseQA', 'StrategyQA', 'Novel Concepts']
  },
  novelty: {
    symbol: '✦', label: 'NOVELTY-SEEKING CURIOSITY',
    question: '“What unexpected direction have we not tried?”',
    copy: 'Agents search beyond the first plausible continuation, opening space for diverse stories, hypotheses, and associations.',
    tasks: ['Story generation', 'Hypothesis generation', 'Codenames']
  },
  social: {
    symbol: '↔', label: 'SOCIAL CURIOSITY',
    question: '“Which perspective or assumption are we missing?”',
    copy: 'Agents inquire into other viewpoints, listen, and revise—supporting perspective-taking in social judgments.',
    tasks: ['Bias scenarios', 'ETHICS']
  }
};

const modes = {
  all: {
    meter: '88%', score: 'HIGH',
    messages: [
      ['A1', true, 'CURIOUS · INDIA', 'What if the light is a message rather than a warning?'],
      ['A2', true, 'CURIOUS · NIGERIA', 'Who has been waiting to see it—and what story did they inherit?'],
      ['A3', true, 'CURIOUS · ROMANIA', 'Could the keeper be gone, while the lighthouse itself remembers?']
    ]
  },
  one: {
    meter: '64%', score: 'FOCUSED',
    messages: [
      ['A1', true, 'CURIOUS · INDIA', 'What single mystery should organize the next scene?'],
      ['A2', false, 'RESPONDING · NIGERIA', 'The village follows the beam inland, where no sea has ever been.'],
      ['A3', false, 'RESPONDING · ROMANIA', 'They find a brass door pulsing in time with the light.']
    ]
  },
  none: {
    meter: '31%', score: 'DIRECT',
    messages: [
      ['A1', false, 'WRITER · INDIA', 'The keeper climbed the long stair toward the lantern room.'],
      ['A2', false, 'WRITER · NIGERIA', 'Outside, the villagers gathered along the dark shore.'],
      ['A3', false, 'WRITER · ROMANIA', 'At dawn, the ancient mechanism finally fell silent.']
    ]
  }
};

function renderMode(name) {
  const mode = modes[name];
  const thread = document.querySelector('[data-agent-thread]');
  thread.innerHTML = mode.messages.map(([id, curious, label, text], i) => `
    <div class="agent-message ${curious ? 'is-curious' : ''}" style="animation-delay:${i * 55}ms">
      <div class="agent-id">${id}</div>
      <div class="message-body"><span>${label}</span><p>${text}</p></div>
    </div>`).join('');
  document.querySelector('[data-meter]').style.width = mode.meter;
  document.querySelector('[data-score]').textContent = mode.score;
}

document.querySelectorAll('[data-mode]').forEach(button => {
  button.addEventListener('click', () => {
    document.querySelectorAll('[data-mode]').forEach(other => {
      const active = other === button;
      other.classList.toggle('is-active', active);
      other.setAttribute('aria-selected', String(active));
    });
    renderMode(button.dataset.mode);
  });
});
renderMode('all');

document.querySelectorAll('[data-dimension]').forEach(button => {
  button.addEventListener('click', () => {
    const data = dimensions[button.dataset.dimension];
    document.querySelectorAll('[data-dimension]').forEach(other => {
      const active = other === button;
      other.classList.toggle('is-active', active);
      other.setAttribute('aria-selected', String(active));
    });
    document.querySelector('[data-dimension-symbol]').textContent = data.symbol;
    document.querySelector('[data-dimension-label]').textContent = data.label;
    document.querySelector('[data-dimension-question]').textContent = data.question;
    document.querySelector('[data-dimension-copy]').textContent = data.copy;
    document.querySelector('[data-dimension-tasks]').innerHTML = data.tasks.map(task => `<span>${task}</span>`).join('');
  });
});

const header = document.querySelector('[data-header]');
window.addEventListener('scroll', () => header.classList.toggle('is-scrolled', window.scrollY > 20), {passive: true});

const toggle = document.querySelector('[data-menu-toggle]');
const nav = document.querySelector('[data-nav]');
toggle.addEventListener('click', () => {
  const open = toggle.getAttribute('aria-expanded') === 'true';
  toggle.setAttribute('aria-expanded', String(!open));
  nav.classList.toggle('is-open', !open);
});
nav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
  nav.classList.remove('is-open');
  toggle.setAttribute('aria-expanded', 'false');
}));

const revealObserver = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
      revealObserver.unobserve(entry.target);
    }
  });
}, {threshold: .12});
document.querySelectorAll('.reveal').forEach(element => revealObserver.observe(element));

const copyButton = document.querySelector('[data-copy-citation]');
copyButton.addEventListener('click', async () => {
  const citation = document.querySelector('[data-citation]').textContent;
  try {
    await navigator.clipboard.writeText(citation);
    copyButton.textContent = 'Copied';
    setTimeout(() => copyButton.textContent = 'Copy citation', 1600);
  } catch {
    copyButton.textContent = 'Select text to copy';
  }
});
