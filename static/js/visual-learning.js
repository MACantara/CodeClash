/**
 * Visual Learning Components
 * Interactive visualizations for Python concepts
 */

class VisualLearning {
    /**
     * Render a flowchart diagram
     */
    static renderFlowchart(containerId, flowchartData) {
        const container = document.getElementById(containerId);
        if (!container) return;

        let svg = `
            <svg viewBox="0 0 400 ${flowchartData.steps.length * 80 + 40}" class="w-full">
                <defs>
                    <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
                        <polygon points="0 0, 10 3, 0 6" fill="#60a5fa" />
                    </marker>
                </defs>
        `;

        flowchartData.steps.forEach((step, index) => {
            const y = index * 80 + 20;
            const shapeType = step.type || 'process';
            
            if (shapeType === 'decision') {
                // Diamond shape for decisions
                svg += `
                    <polygon points="200,${y} 280,${y + 30} 200,${y + 60} 120,${y + 30}" 
                             fill="#1e293b" stroke="#60a5fa" stroke-width="2"/>
                    <text x="200" y="${y + 35}" text-anchor="middle" fill="#e2e8f0" font-size="12">${step.text}</text>
                `;
            } else if (shapeType === 'start' || shapeType === 'end') {
                // Rounded rectangle for start/end
                svg += `
                    <rect x="120" y="${y}" width="160" height="40" rx="20" 
                          fill="#1e293b" stroke="#10b981" stroke-width="2"/>
                    <text x="200" y="${y + 25}" text-anchor="middle" fill="#e2e8f0" font-size="14">${step.text}</text>
                `;
            } else {
                // Rectangle for process
                svg += `
                    <rect x="120" y="${y}" width="160" height="50" 
                          fill="#1e293b" stroke="#60a5fa" stroke-width="2"/>
                    <text x="200" y="${y + 30}" text-anchor="middle" fill="#e2e8f0" font-size="12">${step.text}</text>
                `;
            }

            // Arrow to next step
            if (index < flowchartData.steps.length - 1) {
                svg += `
                    <line x1="200" y1="${y + (shapeType === 'decision' ? 60 : 50)}" 
                          x2="200" y2="${y + 80}" 
                          stroke="#60a5fa" stroke-width="2" marker-end="url(#arrowhead)"/>
                `;
            }
        });

        svg += '</svg>';
        container.innerHTML = svg;
    }

    /**
     * Animate a loop execution
     */
    static animateLoop(containerId, loopData) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `
            <div class="bg-gray-700 rounded-lg p-6">
                <h4 class="font-bold mb-4 text-center">Loop Visualization</h4>
                <div class="flex items-center justify-center gap-4 mb-4">
                    <div class="text-center">
                        <div class="text-sm text-gray-400">Loop Variable</div>
                        <div id="loopVar" class="text-3xl font-bold text-blue-400">0</div>
                    </div>
                    <div class="text-center">
                        <div class="text-sm text-gray-400">Iteration</div>
                        <div id="iterationCount" class="text-3xl font-bold text-purple-400">0</div>
                    </div>
                </div>
                <div id="loopSteps" class="space-y-2 mb-4"></div>
                <div class="flex justify-center gap-3">
                    <button onclick="loopAnimation.start()" 
                            class="bg-green-600 hover:bg-green-700 px-4 py-2 rounded text-sm">
                        <i class="bi bi-play-fill"></i> Start
                    </button>
                    <button onclick="loopAnimation.step()" 
                            class="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded text-sm">
                        <i class="bi bi-skip-forward"></i> Step
                    </button>
                    <button onclick="loopAnimation.reset()" 
                            class="bg-gray-600 hover:bg-gray-700 px-4 py-2 rounded text-sm">
                        <i class="bi bi-arrow-clockwise"></i> Reset
                    </button>
                </div>
            </div>
        `;

        window.loopAnimation = new LoopAnimation(loopData);
    }

    /**
     * Visualize variable assignment
     */
    static visualizeVariables(containerId, variables) {
        const container = document.getElementById(containerId);
        if (!container) return;

        let html = '<div class="grid grid-cols-1 md:grid-cols-2 gap-4">';
        
        Object.entries(variables).forEach(([name, data]) => {
            const typeColor = {
                'int': 'blue',
                'str': 'green',
                'float': 'purple',
                'bool': 'orange',
                'list': 'pink',
                'dict': 'yellow'
            }[data.type] || 'gray';

            html += `
                <div class="bg-gray-700 rounded-lg p-4 border-l-4 border-${typeColor}-500">
                    <div class="flex justify-between items-start mb-2">
                        <code class="text-${typeColor}-400 font-mono font-bold">${name}</code>
                        <span class="text-xs bg-${typeColor}-600/20 text-${typeColor}-300 px-2 py-1 rounded">${data.type}</span>
                    </div>
                    <div class="text-2xl font-bold mb-1">${JSON.stringify(data.value)}</div>
                    <div class="text-xs text-gray-400">${data.description || ''}</div>
                </div>
            `;
        });

        html += '</div>';
        container.innerHTML = html;
    }

    /**
     * Show data structure visualization
     */
    static visualizeDataStructure(containerId, structure) {
        const container = document.getElementById(containerId);
        if (!container) return;

        if (structure.type === 'list') {
            this.visualizeList(container, structure.data);
        } else if (structure.type === 'dict') {
            this.visualizeDict(container, structure.data);
        } else if (structure.type === 'stack') {
            this.visualizeStack(container, structure.data);
        } else if (structure.type === 'queue') {
            this.visualizeQueue(container, structure.data);
        }
    }

    static visualizeList(container, data) {
        let html = `
            <div class="bg-gray-700 rounded-lg p-6">
                <h4 class="font-bold mb-4 flex items-center gap-2">
                    <i class="bi bi-list-ol text-blue-400"></i> List Structure
                </h4>
                <div class="flex gap-2 flex-wrap">
        `;

        data.forEach((item, index) => {
            html += `
                <div class="relative">
                    <div class="absolute -top-6 left-1/2 transform -translate-x-1/2 text-xs text-gray-400">
                        [${index}]
                    </div>
                    <div class="bg-blue-600 text-white px-4 py-3 rounded border-2 border-blue-400 font-mono">
                        ${JSON.stringify(item)}
                    </div>
                </div>
            `;
        });

        html += `
                </div>
                <div class="mt-4 text-sm text-gray-400">
                    Length: ${data.length} | Indices: 0 to ${data.length - 1}
                </div>
            </div>
        `;

        container.innerHTML = html;
    }

    static visualizeDict(container, data) {
        let html = `
            <div class="bg-gray-700 rounded-lg p-6">
                <h4 class="font-bold mb-4 flex items-center gap-2">
                    <i class="bi bi-braces text-purple-400"></i> Dictionary Structure
                </h4>
                <div class="space-y-2">
        `;

        Object.entries(data).forEach(([key, value]) => {
            html += `
                <div class="flex items-center gap-3 bg-gray-800 p-3 rounded">
                    <div class="bg-purple-600 text-white px-3 py-2 rounded font-mono text-sm">
                        "${key}"
                    </div>
                    <i class="bi bi-arrow-right text-purple-400"></i>
                    <div class="bg-blue-600 text-white px-3 py-2 rounded font-mono text-sm flex-1">
                        ${JSON.stringify(value)}
                    </div>
                </div>
            `;
        });

        html += `
                </div>
                <div class="mt-4 text-sm text-gray-400">
                    Keys: ${Object.keys(data).length} | Key-Value Pairs
                </div>
            </div>
        `;

        container.innerHTML = html;
    }

    /**
     * Create interactive code execution visualization
     */
    static createCodeExecutionViz(containerId, code, steps) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `
            <div class="bg-gray-700 rounded-lg p-6">
                <h4 class="font-bold mb-4">Step-by-Step Code Execution</h4>
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
                    <div>
                        <div class="text-sm text-gray-400 mb-2">Code:</div>
                        <pre class="bg-gray-800 p-4 rounded text-sm overflow-x-auto"><code id="codeDisplay">${code}</code></pre>
                    </div>
                    <div>
                        <div class="text-sm text-gray-400 mb-2">Execution Steps:</div>
                        <div id="executionSteps" class="bg-gray-800 p-4 rounded space-y-2 max-h-64 overflow-y-auto"></div>
                    </div>
                </div>
                <div class="mt-4 flex gap-3">
                    <button onclick="codeExecution.start()" class="bg-green-600 hover:bg-green-700 px-4 py-2 rounded text-sm">
                        <i class="bi bi-play-fill"></i> Start
                    </button>
                    <button onclick="codeExecution.next()" class="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded text-sm">
                        <i class="bi bi-skip-forward"></i> Next Step
                    </button>
                    <button onclick="codeExecution.reset()" class="bg-gray-600 hover:bg-gray-700 px-4 py-2 rounded text-sm">
                        <i class="bi bi-arrow-clockwise"></i> Reset
                    </button>
                </div>
            </div>
        `;

        window.codeExecution = new CodeExecutionVisualizer(steps);
    }
}

/**
 * Loop Animation Controller
 */
class LoopAnimation {
    constructor(loopData) {
        this.loopData = loopData;
        this.currentIteration = 0;
        this.isRunning = false;
        this.intervalId = null;
    }

    start() {
        if (this.isRunning) return;
        this.isRunning = true;
        
        this.intervalId = setInterval(() => {
            if (this.currentIteration < this.loopData.iterations) {
                this.step();
            } else {
                this.stop();
            }
        }, 1000);
    }

    step() {
        if (this.currentIteration >= this.loopData.iterations) {
            this.stop();
            return;
        }

        const value = this.loopData.start + (this.currentIteration * this.loopData.step);
        document.getElementById('loopVar').textContent = value;
        document.getElementById('iterationCount').textContent = this.currentIteration + 1;

        const stepsContainer = document.getElementById('loopSteps');
        const stepDiv = document.createElement('div');
        stepDiv.className = 'bg-blue-600/20 border border-blue-500 rounded p-2 text-sm animate-pulse';
        stepDiv.innerHTML = `
            <div class="flex items-center gap-2">
                <i class="bi bi-arrow-right text-blue-400"></i>
                <span>Iteration ${this.currentIteration + 1}: i = ${value}</span>
            </div>
        `;
        stepsContainer.appendChild(stepDiv);
        
        setTimeout(() => stepDiv.classList.remove('animate-pulse'), 500);

        this.currentIteration++;
    }

    stop() {
        this.isRunning = false;
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
    }

    reset() {
        this.stop();
        this.currentIteration = 0;
        document.getElementById('loopVar').textContent = '0';
        document.getElementById('iterationCount').textContent = '0';
        document.getElementById('loopSteps').innerHTML = '';
    }
}

/**
 * Code Execution Visualizer
 */
class CodeExecutionVisualizer {
    constructor(steps) {
        this.steps = steps;
        this.currentStep = 0;
    }

    start() {
        this.reset();
        this.next();
    }

    next() {
        if (this.currentStep >= this.steps.length) return;

        const step = this.steps[this.currentStep];
        const stepsContainer = document.getElementById('executionSteps');
        
        const stepDiv = document.createElement('div');
        stepDiv.className = 'bg-green-600/20 border border-green-500 rounded p-3 animate-pulse';
        stepDiv.innerHTML = `
            <div class="flex items-center justify-between mb-1">
                <span class="text-xs text-gray-400">Step ${this.currentStep + 1}</span>
                <span class="text-xs text-green-400">${step.line}</span>
            </div>
            <div class="text-sm">${step.description}</div>
            ${step.variables ? `
                <div class="mt-2 text-xs text-gray-400">
                    Variables: <code class="bg-gray-700 px-2 py-1 rounded">${JSON.stringify(step.variables)}</code>
                </div>
            ` : ''}
        `;
        
        stepsContainer.appendChild(stepDiv);
        setTimeout(() => stepDiv.classList.remove('animate-pulse'), 500);
        
        this.currentStep++;
    }

    reset() {
        this.currentStep = 0;
        document.getElementById('executionSteps').innerHTML = '';
    }
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VisualLearning;
}
