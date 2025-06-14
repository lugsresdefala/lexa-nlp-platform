"""
LEXA Advanced Visualizations
Implements sophisticated analytical visualizations including:
- Multi-dimensional radar charts
- Textual heat maps
- Performance comparison charts
- Error localization maps
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any
import re
from collections import defaultdict

class LEXAVisualizations:
    """Advanced visualization system for LEXA academic analysis"""
    
    def __init__(self):
        self.colors = {
            'primary': '#42a5f5',
            'secondary': '#ffd54f',
            'success': '#66bb6a',
            'warning': '#ff9800',
            'error': '#f44336',
            'background': 'rgba(13, 21, 38, 0.95)',
            'surface': 'rgba(232, 238, 247, 0.05)',
            'text': '#e8eef7'
        }
        
        self.dimension_colors = {
            'macroestrutura_argumentativa': '#42a5f5',
            'coesao_coerencia': '#66bb6a',
            'sofisticacao_lexico_gramatical': '#ff9800',
            'complexidade_sintatica': '#9c27b0',
            'metadiscursividade': '#00bcd4',
            'intertextualidade': '#4caf50',
            'rigor_metodologico': '#f44336',
            'estilo_adequacao': '#ffd54f'
        }

    def create_radar_chart(self, metrics: Dict[str, Any], title: str = "Análise Multidimensional LEXA") -> go.Figure:
        """
        Create sophisticated radar chart for 8-dimensional analysis
        """
        dimensions = [
            'Macroestrutura\nArgumentativa',
            'Coesão e\nCoerência',
            'Sofisticação\nLéxico-Gramatical',
            'Complexidade\nSintática',
            'Metadiscursividade',
            'Intertextualidade',
            'Rigor\nMetodológico',
            'Estilo e\nAdequação'
        ]
        
        scores = [
            metrics.get('macroestrutura_argumentativa', {}).get('score', 0.05),
            metrics.get('coesao_coerencia', {}).get('score', 0.05),
            metrics.get('sofisticacao_lexico_gramatical', {}).get('score', 0.05),
            metrics.get('complexidade_sintatica', {}).get('score', 0.05),
            metrics.get('metadiscursividade', {}).get('score', 0.05),
            metrics.get('intertextualidade', {}).get('score', 0.05),
            metrics.get('rigor_metodologico', {}).get('score', 0.05),
            metrics.get('estilo_adequacao', {}).get('score', 0.05)
        ]
        
        # Convert to 0-100 scale for better visualization
        scores_100 = [score * 100 for score in scores]
        
        fig = go.Figure()
        
        # Add main trace
        fig.add_trace(go.Scatterpolar(
            r=scores_100,
            theta=dimensions,
            fill='toself',
            name='Análise Atual',
            line=dict(color=self.colors['primary'], width=3),
            fillcolor=f"rgba(66, 165, 245, 0.2)",
            marker=dict(size=8, color=self.colors['primary'])
        ))
        
        # Add reference lines for performance levels
        reference_levels = [25, 45, 65, 85]  # Performance thresholds
        reference_labels = ['Insatisfatório', 'Intermediário', 'Satisfatório', 'Excelência']
        
        for i, (level, label) in enumerate(zip(reference_levels, reference_labels)):
            fig.add_trace(go.Scatterpolar(
                r=[level] * len(dimensions),
                theta=dimensions,
                mode='lines',
                name=label,
                line=dict(
                    color=f"rgba(232, 238, 247, {0.3 - i*0.05})",
                    width=1,
                    dash='dash'
                ),
                showlegend=True
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(color=self.colors['text'], size=10),
                    gridcolor='rgba(232, 238, 247, 0.2)',
                    linecolor='rgba(232, 238, 247, 0.3)',
                    tick0=0,
                    dtick=20
                ),
                angularaxis=dict(
                    tickfont=dict(color=self.colors['text'], size=11, family="Arial"),
                    gridcolor='rgba(232, 238, 247, 0.2)',
                    linecolor='rgba(232, 238, 247, 0.3)',
                    rotation=45
                ),
                bgcolor='rgba(0,0,0,0)'
            ),
            showlegend=True,
            title=dict(
                text=title,
                x=0.5,
                font=dict(color=self.colors['text'], size=16, family="Arial")
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5,
                font=dict(color=self.colors['text'])
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=self.colors['text'], family="Arial"),
            margin=dict(t=80, b=80, l=80, r=80)
        )
        
        return fig

    def create_dimensional_bars(self, metrics: Dict[str, Any]) -> go.Figure:
        """
        Create individual dimensional bar charts with detailed breakdowns
        """
        dimensions = [
            'Macroestrutura Argumentativa',
            'Coesão e Coerência',
            'Sofisticação Léxico-Gramatical',
            'Complexidade Sintática',
            'Metadiscursividade',
            'Intertextualidade',
            'Rigor Metodológico',
            'Estilo e Adequação'
        ]
        
        dimension_keys = [
            'macroestrutura_argumentativa',
            'coesao_coerencia',
            'sofisticacao_lexico_gramatical',
            'complexidade_sintatica',
            'metadiscursividade',
            'intertextualidade',
            'rigor_metodologico',
            'estilo_adequacao'
        ]
        
        scores = []
        colors = []
        
        for key in dimension_keys:
            score = metrics.get(key, {}).get('score', 0.05) * 100
            scores.append(score)
            
            # Color based on performance level
            if score < 25:
                colors.append('#f44336')  # Red
            elif score < 45:
                colors.append('#ff9800')  # Orange
            elif score < 65:
                colors.append('#ffc107')  # Yellow
            elif score < 85:
                colors.append('#4caf50')  # Green
            else:
                colors.append('#2196f3')  # Blue
        
        fig = go.Figure(data=[
            go.Bar(
                x=scores,
                y=dimensions,
                orientation='h',
                marker=dict(
                    color=colors,
                    line=dict(color='rgba(232, 238, 247, 0.3)', width=1)
                ),
                text=[f"{score:.1f}" for score in scores],
                textposition='inside',
                textfont=dict(color='white', size=12, family="Arial Bold")
            )
        ])
        
        # Add performance level zones
        fig.add_vline(x=25, line_dash="dash", line_color="rgba(244, 67, 54, 0.5)", 
                     annotation_text="Insatisfatório", annotation_position="top")
        fig.add_vline(x=45, line_dash="dash", line_color="rgba(255, 152, 0, 0.5)", 
                     annotation_text="Intermediário", annotation_position="top")
        fig.add_vline(x=65, line_dash="dash", line_color="rgba(255, 193, 7, 0.5)", 
                     annotation_text="Satisfatório", annotation_position="top")
        fig.add_vline(x=85, line_dash="dash", line_color="rgba(76, 175, 80, 0.5)", 
                     annotation_text="Excelência", annotation_position="top")
        
        fig.update_layout(
            title=dict(
                text="Desempenho por Dimensão",
                x=0.5,
                font=dict(color=self.colors['text'], size=16, family="Arial")
            ),
            xaxis=dict(
                title="Pontuação (0-100)",
                range=[0, 100],
                gridcolor='rgba(232, 238, 247, 0.2)',
                color=self.colors['text']
            ),
            yaxis=dict(
                gridcolor='rgba(232, 238, 247, 0.2)',
                color=self.colors['text']
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=self.colors['text'], family="Arial"),
            height=600,
            margin=dict(l=200, r=50, t=80, b=50)
        )
        
        return fig

    def create_text_heatmap(self, text: str, problems: List[Dict], 
                           analysis_results: Dict) -> go.Figure:
        """
        Create textual heat map highlighting problem areas
        """
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return self._create_empty_heatmap()
        
        # Calculate problem density per sentence
        sentence_problems = defaultdict(list)
        sentence_scores = []
        
        for i, sentence in enumerate(sentences):
            # Simple problem detection based on length and complexity
            words = len(sentence.split())
            
            # Score based on multiple factors
            length_score = min(1.0, words / 25)  # Optimal ~25 words
            
            # Check for specific issues
            issues = 0
            if words < 5:  # Too short
                issues += 1
            if words > 40:  # Too long
                issues += 1
            if sentence.count(',') / words > 0.15 if words > 0 else False:  # Too many commas
                issues += 1
            if not re.search(r'[.!?]$', sentence):  # Missing punctuation
                issues += 1
            
            issue_score = max(0, 1 - (issues * 0.25))
            final_score = (length_score + issue_score) / 2
            sentence_scores.append(final_score)
        
        # Create heatmap data
        y_labels = [f"Sentença {i+1}" for i in range(len(sentences))]
        z_values = [[score] for score in sentence_scores]
        
        fig = go.Figure(data=go.Heatmap(
            z=z_values,
            y=y_labels,
            x=['Qualidade'],
            colorscale=[
                [0, '#f44336'],      # Red (poor)
                [0.25, '#ff9800'],   # Orange
                [0.5, '#ffc107'],    # Yellow
                [0.75, '#4caf50'],   # Green
                [1, '#2196f3']       # Blue (excellent)
            ],
            text=[[f"{score:.2f}"] for score in sentence_scores],
            texttemplate="%{text}",
            textfont={"size": 10, "color": "white"},
            hoverongaps=False,
            hovertemplate='Sentença: %{y}<br>Qualidade: %{z:.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title=dict(
                text="Mapa de Qualidade Textual por Sentença",
                x=0.5,
                font=dict(color=self.colors['text'], size=16, family="Arial")
            ),
            xaxis=dict(color=self.colors['text']),
            yaxis=dict(color=self.colors['text']),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=self.colors['text'], family="Arial"),
            height=max(400, len(sentences) * 25),
            margin=dict(l=100, r=100, t=80, b=50)
        )
        
        return fig

    def create_performance_comparison(self, current_metrics: Dict[str, Any], 
                                    reference_level: str = "mestrado") -> go.Figure:
        """
        Create comparison chart against academic level benchmarks
        """
        # Reference benchmarks (simulated based on academic levels)
        benchmarks = {
            'graduacao': {
                'macroestrutura_argumentativa': 0.55,
                'coesao_coerencia': 0.50,
                'sofisticacao_lexico_gramatical': 0.45,
                'complexidade_sintatica': 0.40,
                'metadiscursividade': 0.35,
                'intertextualidade': 0.40,
                'rigor_metodologico': 0.45,
                'estilo_adequacao': 0.50
            },
            'mestrado': {
                'macroestrutura_argumentativa': 0.70,
                'coesao_coerencia': 0.65,
                'sofisticacao_lexico_gramatical': 0.60,
                'complexidade_sintatica': 0.55,
                'metadiscursividade': 0.50,
                'intertextualidade': 0.60,
                'rigor_metodologico': 0.65,
                'estilo_adequacao': 0.65
            },
            'doutorado': {
                'macroestrutura_argumentativa': 0.85,
                'coesao_coerencia': 0.80,
                'sofisticacao_lexico_gramatical': 0.75,
                'complexidade_sintatica': 0.70,
                'metadiscursividade': 0.65,
                'intertextualidade': 0.75,
                'rigor_metodologico': 0.80,
                'estilo_adequacao': 0.80
            }
        }
        
        dimensions = [
            'Macroestrutura',
            'Coesão/Coerência',
            'Léxico-Gramatical',
            'Sintática',
            'Metadiscursividade',
            'Intertextualidade',
            'Rigor Metodológico',
            'Estilo/Adequação'
        ]
        
        dimension_keys = [
            'macroestrutura_argumentativa',
            'coesao_coerencia',
            'sofisticacao_lexico_gramatical',
            'complexidade_sintatica',
            'metadiscursividade',
            'intertextualidade',
            'rigor_metodologico',
            'estilo_adequacao'
        ]
        
        current_scores = [current_metrics.get(key, {}).get('score', 0.05) * 100 
                         for key in dimension_keys]
        reference_scores = [benchmarks[reference_level][key] * 100 
                           for key in dimension_keys]
        
        fig = go.Figure()
        
        # Current performance
        fig.add_trace(go.Bar(
            name='Seu Texto',
            x=dimensions,
            y=current_scores,
            marker=dict(color=self.colors['primary']),
            text=[f"{score:.1f}" for score in current_scores],
            textposition='outside'
        ))
        
        # Reference level
        fig.add_trace(go.Bar(
            name=f'Referência {reference_level.capitalize()}',
            x=dimensions,
            y=reference_scores,
            marker=dict(color='rgba(232, 238, 247, 0.3)'),
            text=[f"{score:.1f}" for score in reference_scores],
            textposition='outside'
        ))
        
        fig.update_layout(
            title=dict(
                text=f"Comparação com Nível {reference_level.capitalize()}",
                x=0.5,
                font=dict(color=self.colors['text'], size=16, family="Arial")
            ),
            xaxis=dict(
                title="Dimensões",
                color=self.colors['text'],
                tickangle=45
            ),
            yaxis=dict(
                title="Pontuação (0-100)",
                range=[0, 100],
                gridcolor='rgba(232, 238, 247, 0.2)',
                color=self.colors['text']
            ),
            barmode='group',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=self.colors['text'], family="Arial"),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                font=dict(color=self.colors['text'])
            ),
            height=500,
            margin=dict(l=50, r=50, t=100, b=100)
        )
        
        return fig

    def create_improvement_timeline(self, historical_data: List[Dict]) -> go.Figure:
        """
        Create timeline showing improvement over multiple analyses
        """
        if not historical_data:
            return self._create_empty_timeline()
        
        dates = [entry.get('date', f"Análise {i+1}") for i, entry in enumerate(historical_data)]
        overall_scores = [entry.get('overall_score', 0.5) * 100 for entry in historical_data]
        
        fig = go.Figure()
        
        # Overall score line
        fig.add_trace(go.Scatter(
            x=dates,
            y=overall_scores,
            mode='lines+markers',
            name='Pontuação Geral',
            line=dict(color=self.colors['primary'], width=3),
            marker=dict(size=8, color=self.colors['primary'])
        ))
        
        # Add trend line
        if len(overall_scores) > 1:
            z = np.polyfit(range(len(overall_scores)), overall_scores, 1)
            trend_line = np.poly1d(z)
            trend_y = [trend_line(i) for i in range(len(overall_scores))]
            
            fig.add_trace(go.Scatter(
                x=dates,
                y=trend_y,
                mode='lines',
                name='Tendência',
                line=dict(color=self.colors['secondary'], width=2, dash='dash')
            ))
        
        # Performance level zones
        fig.add_hline(y=25, line_dash="dot", line_color="rgba(244, 67, 54, 0.5)")
        fig.add_hline(y=45, line_dash="dot", line_color="rgba(255, 152, 0, 0.5)")
        fig.add_hline(y=65, line_dash="dot", line_color="rgba(255, 193, 7, 0.5)")
        fig.add_hline(y=85, line_dash="dot", line_color="rgba(76, 175, 80, 0.5)")
        
        fig.update_layout(
            title=dict(
                text="Evolução do Desempenho",
                x=0.5,
                font=dict(color=self.colors['text'], size=16, family="Arial")
            ),
            xaxis=dict(
                title="Análises",
                color=self.colors['text']
            ),
            yaxis=dict(
                title="Pontuação (0-100)",
                range=[0, 100],
                gridcolor='rgba(232, 238, 247, 0.2)',
                color=self.colors['text']
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=self.colors['text'], family="Arial"),
            height=400,
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        return fig

    def _create_empty_heatmap(self) -> go.Figure:
        """Create empty heatmap for when no text is available"""
        fig = go.Figure()
        fig.add_annotation(
            text="Nenhum texto disponível para análise",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            xanchor="center", yanchor="middle",
            font=dict(size=16, color=self.colors['text'])
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=300
        )
        return fig

    def _create_empty_timeline(self) -> go.Figure:
        """Create empty timeline for when no historical data is available"""
        fig = go.Figure()
        fig.add_annotation(
            text="Nenhum histórico disponível",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            xanchor="center", yanchor="middle",
            font=dict(size=16, color=self.colors['text'])
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=300
        )
        return fig