import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import re
import base64
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from collections import Counter
import ast
from functools import lru_cache
import requests
import time
import math
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="FLUX-ON Leitura Quântica",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS CSS AVANÇADOS ---
st.markdown("""
<style>
    /* Tema principal aprimorado */
    .main {
        background: linear-gradient(135deg, #0f0c29, #1a1a2e, #16213e);
        color: #e6e6fa;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    /* Tipografia moderna */
    h1, h2, h3, h4, h5, h6 {
        color: #e0aaff;
        font-family: 'Georgia', serif;
        text-shadow: 0 0 15px rgba(224, 170, 255, 0.4);
        margin-bottom: 1rem;
    }
    
    h1 {
        font-size: 2.8rem;
        background: linear-gradient(135deg, #e0aaff, #9d4edd, #7b2cbf);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        border-bottom: 3px solid #7b2cbf;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
    }
    
    /* Cards e containers futuristas */
    .metric-card {
        background: rgba(45, 45, 65, 0.8);
        border-left: 5px solid #9d4edd;
        padding: 20px;
        margin: 15px 0;
        border-radius: 15px;
        box-shadow: 0 6px 25px rgba(157, 78, 221, 0.3);
        backdrop-filter: blur(12px);
        transition: all 0.3s ease;
        border: 1px solid rgba(157, 78, 221, 0.2);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 35px rgba(157, 78, 221, 0.4);
        border-color: rgba(157, 78, 221, 0.4);
    }
    
    /* Text area styling aprimorado */
    .text-container {
        background: rgba(30, 30, 46, 0.95);
        padding: 30px;
        border-radius: 20px;
        border: 2px solid #7b2cbf;
        box-shadow: 0 0 40px rgba(123, 44, 191, 0.25);
        backdrop-filter: blur(8px);
        line-height: 1.9;
        font-size: 17px;
        max-height: 600px;
        overflow-y: auto;
        font-family: 'Georgia', serif;
    }
    
    /* Highlight styles melhorados */
    .highlight {
        background: linear-gradient(120deg, #9d4edd50, #5a189a70);
        padding: 3px 8px;
        border-radius: 5px;
        border-bottom: 2px solid #e0aaff;
        font-weight: 600;
        color: #f8f9fa;
    }
    
    .highlight-important {
        background: linear-gradient(120deg, #ff6b6b50, #ee5a2470);
        padding: 3px 8px;
        border-radius: 5px;
        border-bottom: 2px solid #ff6b6b;
        font-weight: 700;
        color: #f8f9fa;
    }
    
    .user-highlight {
        background: linear-gradient(120deg, #4cc9f050, #4895ef70);
        padding: 3px 8px;
        border-radius: 5px;
        border-bottom: 2px solid #4cc9f0;
        font-weight: 600;
        color: #f8f9fa;
    }
    
    /* Botões de navegação quântica */
    .nav-button {
        background: linear-gradient(135deg, #9d4edd, #7b2cbf);
        color: white;
        border: none;
        padding: 14px 24px;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
        margin: 5px;
        box-shadow: 0 4px 15px rgba(157, 78, 221, 0.3);
    }
    
    .nav-button:hover {
        background: linear-gradient(135deg, #7b2cbf, #5a189a);
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(157, 78, 221, 0.5);
    }
    
    /* Sidebar quântica */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 3px solid #9d4edd;
        box-shadow: 5px 0 25px rgba(0, 0, 0, 0.3);
    }
    
    /* Abas estilizadas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background: rgba(45, 45, 65, 0.7);
        border-radius: 10px 10px 0 0;
        gap: 10px;
        padding: 10px 20px;
        border-bottom: 2px solid #7b2cbf;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #9d4edd, #7b2cbf);
        color: white;
    }
    
    /* Barras de progresso quânticas */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #9d4edd, #5a189a);
        box-shadow: 0 0 10px rgba(157, 78, 221, 0.5);
    }
    
    /* Métricas personalizadas */
    [data-testid="stMetric"] {
        background: rgba(45, 45, 65, 0.8);
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #9d4edd;
        box-shadow: 0 4px 20px rgba(157, 78, 221, 0.2);
    }
    
    /* Animações suaves */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    .pulse-animation {
        animation: pulse 3s infinite;
    }
    
    /* Scrollbar personalizada */
    .text-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .text-container::-webkit-scrollbar-track {
        background: rgba(30, 30, 46, 0.5);
        border-radius: 10px;
    }
    
    .text-container::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #9d4edd, #7b2cbf);
        border-radius: 10px;
    }
    
    /* Efeitos de foco */
    .focus-effect {
        transition: all 0.3s ease;
    }
    
    .focus-effect:hover {
        box-shadow: 0 0 25px rgba(157, 78, 221, 0.4);
    }
</style>
""", unsafe_allow_html=True)

class NavigationSystem:
    def __init__(self, total_pages=1):
        self.total_pages = total_pages
    
    # ✅ NOVO MÉTODO INTERMEDIÁRIO
    def navigate_from_slider(self):
        """
        Lê o valor do slider a partir do session_state e navega para a página.
        """
        # A 'key' do slider é 'page_selector_optimized'
        new_page = st.session_state.page_selector_optimized
        self.navigate_to(new_page)
        
    def navigate_to(self, page_number):
        """Navega para uma página específica com verificação de limites"""
        if 1 <= page_number <= self.total_pages:
            st.session_state.pending_page = page_number
            st.session_state.page_change_confirmed = False
            return True
        return False

    def confirm_page_change(self):
        """Confirma a mudança de página"""
        if hasattr(st.session_state, 'pending_page'):
            st.session_state.current_page = st.session_state.pending_page
            # Limpa estados relacionados à página atual
            if hasattr(st.session_state, 'ia_analysis_result'):
                st.session_state.ia_analysis_result = None
            if hasattr(st.session_state, 'show_ia_analysis'):
                st.session_state.show_ia_analysis = False
    
    # ... (o restante da classe 'NavigationSystem' permanece igual) ...
    def next_page(self):
        current = st.session_state.get('current_page', 1)
        if current < self.total_pages:
            return self.navigate_to(current + 1)
        return False
    
    def prev_page(self):
        current = st.session_state.get('current_page', 1)
        if current > 1:
            return self.navigate_to(current - 1)
        return False
    
    def first_page(self):
        return self.navigate_to(1)
    
    def last_page(self):
        return self.navigate_to(self.total_pages)
        
    def update_total_pages(self, total_pages):
        self.total_pages = total_pages

class RenderController:
    def __init__(self):
        self._render_lock = False
        self._pending_operations = []
        self._last_render_time = 0
        self._render_interval = 0.5
        
    def should_render(self):
        current_time = time.time()
        if (current_time - self._last_render_time < self._render_interval or 
            self._render_lock):
            return False
        return True
        
    def acquire_lock(self):
        if not self._render_lock:
            self._render_lock = True
            return True
        return False
        
    def release_lock(self):
        self._render_lock = False
        self._last_render_time = time.time()
        
    def queue_operation(self, operation):
        self._pending_operations.append(operation)
        
    def execute_queued(self):
        for operation in self._pending_operations:
            try:
                operation()
            except Exception as e:
                print(f"Erro na operação enfileirada: {e}")
        self._pending_operations = []

class SearchEngine:
    """Motor de busca otimizado para livros grandes"""
    
    def __init__(self, segments, chapters):
        self.segments = segments
        self.chapters = chapters
        self._lazy_indexing = len(segments) > 1000  # Ativar indexação preguiçosa para livros grandes
        self.index_loaded = False
        
    def _ensure_index_loaded(self):
        """Garante que o índice está carregado (lazy loading)"""
        if not self.index_loaded:
            with st.spinner("📚 Carregando índice de busca..."):
                self._build_index()
                self.index_loaded = True
    
    def _build_index(self):
        """Constrói índice invertido para busca rápida"""
        self.word_index = {}
        self.phrase_index = {}
        self.chapter_index = {}
        
        # Indexar por capítulos
        for chapter in self.chapters:
            self.chapter_index[chapter['number']] = {
                'title': chapter['title'],
                'start_page': chapter['start_page'],
                'end_page': chapter['end_page']
            }
        
        # Indexar palavras e frases
        for i, segment in enumerate(self.segments):
            text = segment.get('text', '').lower()
            page_num = i + 1
            
            # Indexar palavras
            words = re.findall(r'\b\w+\b', text)
            for word in words:
                if word not in self.word_index:
                    self.word_index[word] = []
                self.word_index[word].append({
                    'page': page_num,
                    'positions': [m.start() for m in re.finditer(r'\b' + re.escape(word) + r'\b', text)]
                })
            
            # Indexar frases comuns (3-5 palavras)
            sentences = re.split(r'[.!?]+', text)
            for sentence in sentences:
                sentence = sentence.strip()
                if 15 <= len(sentence) <= 200:  # Frases de tamanho razoável
                    if sentence not in self.phrase_index:
                        self.phrase_index[sentence] = []
                    self.phrase_index[sentence].append(page_num)
    
    def search_word(self, word, exact_match=False):
        """Busca com lazy loading"""
        if not self.index_loaded:
            self._ensure_index_loaded()
            
        results = []
        search_term = word.lower()
        
        if exact_match:
            if search_term in self.word_index:
                for entry in self.word_index[search_term]:
                    results.append({
                        'type': 'word',
                        'page': entry['page'],
                        'count': len(entry['positions']),
                        'excerpt': self._get_excerpt(entry['page'], search_term)
                    })
        else:
            # Busca parcial
            for term, entries in self.word_index.items():
                if search_term in term:
                    for entry in entries:
                        results.append({
                            'type': 'word',
                            'page': entry['page'],
                            'count': len(entry['positions']),
                            'excerpt': self._get_excerpt(entry['page'], term),
                            'matched_term': term
                        })
        
        return sorted(results, key=lambda x: x['count'], reverse=True)
    
    def _build_index_optimized(self):
        """Indexação otimizada para livros grandes"""
        self.word_index = {}
        self.phrase_index = {}
        self.chapter_index = {}
        
        # Indexar capítulos primeiro
        for chapter in self.chapters:
            self.chapter_index[chapter['number']] = {
                'title': chapter['title'],
                'start_page': chapter['start_page'],
                'end_page': chapter['end_page']
            }
        
        # Indexar em lotes para evitar sobrecarga de memória
        batch_size = 100  # Processar 100 páginas por vez
        total_pages = len(self.segments)
        
        for batch_start in range(0, total_pages, batch_size):
            batch_end = min(batch_start + batch_size, total_pages)
            
            for i in range(batch_start, batch_end):
                segment = self.segments[i]
                text = segment.get('text', '').lower()
                page_num = i + 1
                
                # Indexar palavras importantes (evitar palavras muito comuns)
                words = re.findall(r'\b\w+\b', text)
                word_counts = Counter(words)
                
                for word, count in word_counts.items():
                    # Ignorar palavras muito comuns ou muito curtas
                    if (len(word) > 3 and count > 0 and 
                        word not in self._get_stopwords()):
                        if word not in self.word_index:
                            self.word_index[word] = []
                        self.word_index[word].append({
                            'page': page_num,
                            'count': count
                        })
            
            # Limpar memória periodicamente
            if batch_start % 1000 == 0:
                import gc
                gc.collect()
    
    def _get_stopwords(self):
        """Lista de palavras comuns para ignorar na indexação"""
        return {
            'o', 'a', 'e', 'de', 'da', 'do', 'em', 'para', 'com', 'que', 'é', 'um', 'uma', 
            'os', 'as', 'se', 'por', 'uma', 'com', 'não', 'são', 'como', 'mas', 'foi', 'ao',
            'das', 'dos', 'nas', 'nos', 'pelo', 'pela', 'pelos', 'pelas', 'esse', 'essa',
            'isso', 'isto', 'aquele', 'aquela', 'aquilo', 'outro', 'outra', 'outros', 'outras',
            'qual', 'quais', 'quando', 'onde', 'quem', 'cujo', 'cuja', 'cujos', 'cujas',
            'que', 'quê', 'como', 'porque', 'porquê', 'porquê', 'porquê', 'porquê'
        }
    
    def search_phrase(self, phrase):
        """Busca por frase exata"""
        results = []
        search_phrase = phrase.lower().strip()
        
        # Busca direta no índice de frases
        if search_phrase in self.phrase_index:
            for page in self.phrase_index[search_phrase]:
                results.append({
                    'type': 'phrase',
                    'page': page,
                    'excerpt': self._get_excerpt(page, search_phrase, context_words=10)
                })
        
        # Busca aproximada para frases longas
        if not results and len(search_phrase.split()) > 3:
            words = search_phrase.split()
            first_word = words[0]
            
            if first_word in self.word_index:
                for entry in self.word_index[first_word]:
                    page_text = self.segments[entry['page'] - 1].get('text', '').lower()
                    if search_phrase in page_text:
                        results.append({
                            'type': 'phrase',
                            'page': entry['page'],
                            'excerpt': self._get_excerpt(entry['page'], search_phrase, context_words=15)
                        })
        
        return results
    
    def search_chapter(self, chapter_ref):
        """Busca por capítulo"""
        results = []
        
        # Tentar encontrar por número
        if isinstance(chapter_ref, int) or chapter_ref.isdigit():
            chapter_num = int(chapter_ref)
            if chapter_num in self.chapter_index:
                chapter = self.chapter_index[chapter_num]
                results.append({
                    'type': 'chapter',
                    'number': chapter_num,
                    'title': chapter['title'],
                    'start_page': chapter['start_page'],
                    'end_page': chapter['end_page']
                })
        
        # Buscar por título
        for chapter_num, chapter_info in self.chapter_index.items():
            if (isinstance(chapter_ref, str) and 
                chapter_ref.lower() in chapter_info['title'].lower()):
                results.append({
                    'type': 'chapter',
                    'number': chapter_num,
                    'title': chapter_info['title'],
                    'start_page': chapter_info['start_page'],
                    'end_page': chapter_info['end_page']
                })
        
        return results
    
    def search_verse(self, verse_ref):
        """Busca por versículo (padrão: capítulo:versículo)"""
        results = []
        
        # Padrão: 3:16 (capítulo 3, versículo 16)
        verse_pattern = r'(\d+)[:\.](\d+)'
        match = re.search(verse_pattern, verse_ref)
        
        if match:
            chapter_num = int(match.group(1))
            verse_num = int(match.group(2))
            
            # Encontrar capítulo
            if chapter_num in self.chapter_index:
                chapter = self.chapter_index[chapter_num]
                
                # Procurar versículo no capítulo
                verse_pattern = re.compile(rf'\b{verse_num}\b|\b{verse_num}[\.\:]', re.IGNORECASE)
                
                for page in range(chapter['start_page'], chapter['end_page'] + 1):
                    if page <= len(self.segments):
                        text = self.segments[page - 1].get('text', '')
                        if verse_pattern.search(text):
                            results.append({
                                'type': 'verse',
                                'chapter': chapter_num,
                                'verse': verse_num,
                                'page': page,
                                'excerpt': self._get_excerpt(page, str(verse_num), context_words=5)
                            })
        
        return results
    
    def _get_excerpt(self, page_num, search_term, context_words=5):
        """Obtém trecho do texto com o termo pesquisado"""
        if page_num > len(self.segments):
            return ""
        
        text = self.segments[page_num - 1].get('text', '')
        if not text:
            return ""
        
        # Encontrar posição do termo
        term_lower = search_term.lower()
        text_lower = text.lower()
        pos = text_lower.find(term_lower)
        
        if pos == -1:
            return text[:200] + "..." if len(text) > 200 else text
        
        # Obter contexto ao redor
        words = text.split()
        term_words = search_term.split()
        
        # Encontrar índice aproximado das palavras
        start_idx = max(0, len(text[:pos].split()) - context_words)
        end_idx = min(len(words), start_idx + len(term_words) + (context_words * 2))
        
        excerpt_words = words[start_idx:end_idx]
        excerpt = ' '.join(excerpt_words)
        
        # Destacar o termo encontrado
        highlighted = re.sub(
            re.escape(search_term), 
            f'<mark style="background-color: #ffeb3b; color: black; padding: 2px 4px; border-radius: 3px;">{search_term}</mark>',
            excerpt, 
            flags=re.IGNORECASE
        )
        
        return highlighted + "..." if end_idx < len(words) else highlighted
    
    def advanced_search(self, query, search_type="all", max_results=50):
        """Busca avançada com múltiplos critérios"""
        results = []
        
        if search_type in ["all", "word"]:
            results.extend(self.search_word(query, exact_match=(search_type == "word")))
        
        if search_type in ["all", "phrase"] and len(query.split()) > 1:
            results.extend(self.search_phrase(query))
        
        if search_type in ["all", "chapter"]:
            results.extend(self.search_chapter(query))
        
        if search_type in ["all", "verse"] and re.search(r'\d+[:\.]\d+', query):
            results.extend(self.search_verse(query))
        
        # Limitar resultados
        return results[:max_results]
    
class BookStateManager:
    def __init__(self):
        self.current_position = 0
        self.total_pages = 0
        self.loaded = False
        self.segments = []
        self._change_listeners = []
        
    def load_book(self, analysis_data):
        self.segments = analysis_data.get('segments', [])
        self.total_pages = len(self.segments)
        self.current_position = min(st.session_state.get('current_page', 1), self.total_pages)
        self.loaded = True
        return True
        
    def navigate_to(self, page_number):
        if 1 <= page_number <= self.total_pages:
            self.current_position = page_number
            self._notify_change()
            return True
        return False
        
    def _notify_change(self):
        for listener in self._change_listeners:
            try:
                listener(self.current_position)
            except Exception as e:
                print(f"Erro no listener: {e}")
                
    def get_current_segment(self):
        if 0 <= self.current_position - 1 < len(self.segments):
            return self.segments[self.current_position - 1]
        return {}
    
    def add_change_listener(self, listener):
        self._change_listeners.append(listener)

def safe_json_dump(data):
    try:
        return json.dumps(data, ensure_ascii=False, indent=2)
    except Exception:
        def escape_str(obj):
            if isinstance(obj, str):
                return (obj.replace("\\", "\\\\")
                         .replace('"', '\\"')
                         .replace('\n', '\\n')
                         .replace('\r', '\\r')
                         .replace('\t', '\\t'))
            elif isinstance(obj, dict):
                return {k: escape_str(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [escape_str(i) for i in obj]
            else:
                return obj
        return json.dumps(escape_str(data), ensure_ascii=False, indent=2)

def render_book_opener():
    st.title("📖 FLUX-ON Quantum Reader")
    st.markdown("""
    <div style='text-align: center; padding: 3rem; background: rgba(45, 45, 65, 0.8); border-radius: 20px; border: 3px solid #9d4edd;'>
        <h1 style='color: #e0aaff; margin-bottom: 2rem;'>Bem-vindo ao Leitor Quântico</h1>
        <p style='color: #c77dff; font-size: 1.2rem; margin-bottom: 3rem;'>
            Sistema avançado de análise e leitura multidimensional
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='text-align: center; margin: 2rem 0;'>
            <h3 style='color: #e0aaff;'>📚 Carregar Livro para Análise</h3>
            <p style='color: #c77dff;'>Selecione uma das opções abaixo para começar</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📊 Carregar Análise Existente", use_container_width=True, key="load_existing"):
            st.session_state.book_loaded = True
        
        st.button("🆕 Analisar Novo Livro (Em Breve)", use_container_width=True, disabled=True)
        
        st.markdown("---")
        st.info("""
        **💡 Dica:** Use a opção 'Carregar Análise Existente' para visualizar 
        relatórios já processados pelo sistema FLUX-ON.
        """)

class QuantumBookReader:
    def __init__(self, analysis_data=None):
        self.analysis_data = analysis_data or {}
        self.segments = self.analysis_data.get('segments', [])
        
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 1
            
        # CORREÇÃO: Atualizar total_pages do nav_system
        self.nav_system = NavigationSystem(len(self.segments))
        self.state_manager = BookStateManager()
        self.render_controller = RenderController()
        
        self.state_manager.add_change_listener(self._on_page_change)
        
        if analysis_data:
            self.state_manager.load_book(analysis_data)
            
        self.ia_prompts = self._initialize_prompts()
        self._processed_text_cache = {}
        
        self.chapters = self._extract_chapters_advanced()
        
        self.search_engine = SearchEngine(self.segments, self.chapters)
        self.search_results = []
        self.current_search_query = ""
        
        self.api_config = {
            'configured': False,
            'api_key': '',
            'api_url': 'https://api.deepseek.com/v1/chat/completions',
            'model': 'deepseek-chat'
        }
        
        self.extended_themes = {
            'política': {
                'keywords': ['governo', 'presidente', 'eleições', 'democracia', 'ditadura', 'político', 
                        'partido', 'estado', 'lei', 'justiça', 'poder', 'corrupção', 'voto', 'parlamento',
                        'legislativo', 'executivo', 'ministro', 'prefeito', 'vereador', 'senador',
                        'deputado', 'política', 'ideologia', 'partidário', 'coalizão', 'oposição'],
                'weight': 0.7
            },
            'religião': {
                'keywords': ['deus', 'fé', 'igreja', 'bíblia', 'oração', 'espiritual', 'divino', 'sagrado',
                        'profeta', 'religioso', 'crença', 'culto', 'ritual', 'teologia', 'pecado',
                        'bispo', 'padre', 'pastor', 'templo', 'sinagoga', 'mesquita', 'deus',
                        'jesus', 'cristo', 'allah', 'budismo', 'hinduísmo', 'espiritualidade'],
                'weight': 0.6
            },
            'sexo': {
                'keywords': ['sexual', 'gênero', 'masculino', 'feminino', 'relação', 'corpo', 'desejo',
                        'intimidade', 'orientação', 'identidade', 'atração', 'reprodução', 'prazer',
                        'sensual', 'erótico', 'afetividade', 'casamento', 'namoro', 'paixão', 'amor',
                        'heterossexual', 'homossexual', 'bissexual', 'transgênero', 'libido'],
                'weight': 0.5
            },
            'cultura': {
                'keywords': ['arte', 'música', 'literatura', 'tradição', 'costumes', 'sociedade', 'valores',
                        'identidade', 'folclore', 'herança', 'expressão', 'cultural', 'patrimônio',
                        'dança', 'teatro', 'cinema', 'pintura', 'escultura', 'fotografia', 'arquitetura',
                        'festival', 'celebração', 'ritual', 'mitologia', 'história', 'ancestral'],
                'weight': 0.8
            }
        }
        
        self._initialize_session_state()
        self.book_analysis = self.analysis_data.get('book_analysis', {})
    
    def _initialize_session_state(self):
        # CORREÇÃO: Garantir que current_page está inicializado
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 1
            
        if 'user_highlights' not in st.session_state:
            st.session_state.user_highlights = {}
            
        if 'user_notes' not in st.session_state:
            st.session_state.user_notes = {}
            
        if 'show_ia_analysis' not in st.session_state:
            st.session_state.show_ia_analysis = False
            
        if 'selected_text_for_analysis' not in st.session_state:
            st.session_state.selected_text_for_analysis = ""
            
        if 'ia_analysis_result' not in st.session_state:
            st.session_state.ia_analysis_result = None
            
        if 'ia_prompt_used' not in st.session_state:
            st.session_state.ia_prompt_used = None
            
        if 'book_loaded' not in st.session_state:
            st.session_state.book_loaded = False
            
        if 'book_cover_shown' not in st.session_state:
            st.session_state.book_cover_shown = False
            
        if 'api_configured' not in st.session_state:
            st.session_state.api_configured = False
            
        if 'deepseek_response' not in st.session_state:
            st.session_state.deepseek_response = None
            
        if 'local_analysis' not in st.session_state:
            st.session_state.local_analysis = None
            
        if 'copied_prompt' not in st.session_state:
            st.session_state.copied_prompt = None
        
        if 'page_change_confirmed' not in st.session_state:
            st.session_state.page_change_confirmed = False
    
    def _on_page_change(self, new_page):
        st.session_state.current_page = new_page
        if 'ia_analysis_result' in st.session_state:
            st.session_state.ia_analysis_result = None
    
    def load_analysis_data(self, analysis_data):
        self.analysis_data = analysis_data
        self.segments = analysis_data.get('segments', [])
        self.state_manager.load_book(analysis_data)
        self.nav_system.update_total_pages(len(self.segments))
        self.chapters = self._extract_chapters_advanced()
        st.session_state.book_loaded = True
        
    def render_advanced_search_sidebar(self):
        """Sidebar com busca avançada e filtros"""
        with st.sidebar:
            st.markdown("---")
            st.header("🔍 Busca Avançada")
            
            # Campo de busca principal
            search_query = st.text_input(
                "O que você está procurando?",
                placeholder="Digite palavra, frase, capítulo ou versículo...",
                key="main_search_input"
            )
            
            # Filtros avançados
            with st.expander("⚙️ Filtros Avançados", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    search_type = st.selectbox(
                        "Tipo de busca:",
                        ["Todos", "Palavras", "Frases", "Capítulos", "Versículos"],
                        key="search_type_filter"
                    )
                    
                    case_sensitive = st.checkbox("Diferenciar maiúsc/minúsc", False)
                
                with col2:
                    min_word_length = st.slider("Tamanho mínimo palavra:", 3, 10, 4)
                    max_results = st.slider("Máx. resultados:", 10, 200, 50)
            
            # Botões de ação
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🔎 Buscar", use_container_width=True) and search_query:
                    self.perform_search(search_query, search_type, case_sensitive, max_results)
            
            with col2:
                if st.button("🧹 Limpar", use_container_width=True):
                    self.search_results = []
                    self.current_search_query = ""
            
            # Resultados rápidos na sidebar
            if self.search_results:
                st.markdown("---")
                st.subheader("📋 Resultados Encontrados")
                
                for i, result in enumerate(self.search_results[:3]):
                    emoji = "📖" if result['type'] == 'chapter' else "📜" if result['type'] == 'verse' else "📄"
                    st.info(f"{emoji} {self._format_search_result(result)}")
                    
                    if st.button("Ir →", key=f"sidebar_goto_{i}", use_container_width=True):
                        st.session_state.current_page = result['page']
                        st.rerun()
                
                if len(self.search_results) > 3:
                    st.info(f"📊 ... e mais {len(self.search_results) - 3} resultados")
                    
                    if st.button("Ver todos os resultados", use_container_width=True):
                        st.session_state.current_menu = "🔍 Resultados Busca"
                        st.rerun()

    def _format_search_result(self, result):
        """Formata resultado para exibição compacta"""
        if result['type'] == 'chapter':
            return f"Capítulo {result['number']}: {result['title']}"
        elif result['type'] == 'verse':
            return f"Versículo {result['chapter']}:{result['verse']}"
        elif result['type'] == 'word':
            return f"Palavra: {result.get('matched_term', '')} ({result['count']}x)"
        elif result['type'] == 'phrase':
            return "Frase encontrada"
        return "Resultado"
    
    @st.cache_data(show_spinner=False, max_entries=100)
    def _process_text_highlights_cached(_self, text, keywords, entities, page_highlights):
        highlighted_text = text
        
        for highlight_id, highlight_data in page_highlights.items():
            highlighted_text = highlighted_text.replace(
                highlight_data['text'],
                f'<span class="user-highlight" title="Destacado pelo usuário">{highlight_data["text"]}</span>'
            )
        
        for entity, label in entities[:10]:
            if entity not in highlighted_text:
                highlighted_text = re.sub(
                    re.escape(entity),
                    f'<span class="highlight-important" title="{label}">{entity}</span>',
                    highlighted_text,
                    flags=re.IGNORECASE
                )
        
        for keyword in keywords[:15]:
            if keyword not in highlighted_text:
                highlighted_text = re.sub(
                    f'\\b{re.escape(keyword)}\\b',
                    f'<span class="highlight">{keyword}</span>',
                    highlighted_text,
                    flags=re.IGNORECASE
                )
        
        return highlighted_text
    
    def _generate_text_analysis_prompt(self, prompt_type, text, segment=None):
        """Gera prompt contextualizado baseado no tipo de análise"""
        book_name = self.analysis_data.get('book_name', 'este livro')
        current_page = st.session_state.current_page
        current_chapter = self._get_current_chapter()
        
        chapter_info = f"Capítulo {current_chapter['number']}: {current_chapter['title']}" if current_chapter else "Contexto geral"
        
        prompts = {
            'page_summary': f"""Gere um resumo detalhado da página {current_page} do livro "{book_name}".
    Contexto: {chapter_info}
    Texto: {text[:2000]}
    Inclua os principais pontos, ideias-chave e como esta página se conecta com o conteúdo geral do livro.""",
            
            'analysis': f"""Analise profundamente este texto considerando:
    1. Contexto histórico e significado filosófico
    2. Metáforas, simbolismos e linguagem figurada  
    3. Relações com temas maiores da obra
    4. Implicações científicas, filosóficas ou sociais
    5. Conexões com outros conceitos apresentados no livro

    Contexto: {chapter_info}
    Livro: {book_name}
    Texto para análise: {text[:2000]}""",
            
            'explain_concepts': f"""Explique os conceitos complexos presentes no texto:
    Contexto: {chapter_info}
    Livro: {book_name}
    Texto: {text[:2000]}
    Forneça definições claras, exemplos práticos e relação com o contexto do livro.""",
            
            'chapter_context': f"""Considerando que este texto faz parte do {chapter_info} do livro "{book_name}",
    analise como este trecho se relaciona com:
    1. O contexto geral do capítulo
    2. A estrutura narrativa do livro  
    3. Os temas principais da obra
    4. O desenvolvimento de ideias ao longo do livro

    Trecho para análise: {text[:2000]}"""
        }
        
        return prompts.get(prompt_type, f"Analise o seguinte texto: {text[:2000]}")
    
    def _format_text_for_display(self, text):
        if not text:
            return text
            
        text = re.sub(r'([.!?])([A-Za-z])', r'\1 \2', text)
        text = re.sub(r'([,:;])([A-Za-z])', r'\1 \2', text)
        
        chapter_patterns = [
            r'(?i)^(capítulo|chapter|cap\.)\s+(\d+|[IVXLCDM]+)[\s:-]*(.*)$',
            r'^(CAPÍTULO|CHAPTER)\s+(\d+|[IVXLCDM]+)[\s:-]*(.*)$',
            r'^(\d+|[IVXLCDM]+)[\s.-]+\s*(.*)$'
        ]
        
        lines = text.split('\n')
        formatted_lines = []
        
        for line in lines:
            line_formatted = line
            for pattern in chapter_patterns:
                match = re.match(pattern, line.strip())
                if match:
                    groups = match.groups()
                    if len(groups) >= 3 and groups[2]:
                        line_formatted = f'<h3 class="chapter-title">{groups[0]} {groups[1]}: {groups[2]}</h3>'
                    elif len(groups) >= 2:
                        line_formatted = f'<h3 class="chapter-title">{groups[0]} {groups[1]}</h3>'
                    break
            formatted_lines.append(line_formatted)
        
        text = '\n'.join(formatted_lines)
        
        paragraphs = text.split('\n\n')
        if len(paragraphs) > 1:
            formatted_paragraphs = []
            for paragraph in paragraphs:
                if paragraph.strip():
                    if len(paragraph.strip()) < 100 and not re.search(r'[.!?]$', paragraph):
                        formatted_paragraphs.append(f'<p class="short-paragraph">{paragraph.strip()}</p>')
                    else:
                        paragraph_text = paragraph.strip()
                        formatted_paragraphs.append(f'<p>{paragraph_text}</p>')
            text = '\n\n'.join(formatted_paragraphs)
        else:
            text = f'<p>{text}</p>'
        
        text = re.sub(r'\s+', ' ', text)
        
        return text
    
    def render_search_interface(self):
        """Renderiza a interface de busca avançada"""
        st.sidebar.markdown("---")
        st.sidebar.header("🔍 Busca Avançada")
        
        # Campo de busca
        search_query = st.sidebar.text_input(
            "Digite sua busca:",
            placeholder="Palavra, frase, capítulo ou versículo...",
            key="search_input"
        )
        
        # Tipo de busca
        search_type = st.sidebar.selectbox(
            "Tipo de busca:",
            ["Todos", "Palavras", "Frases", "Capítulos", "Versículos"],
            key="search_type"
        )
        
        # Botão de busca
        if st.sidebar.button("🔎 Buscar", use_container_width=True) and search_query:
            with st.spinner("Buscando..."):
                search_type_map = {
                    "Todos": "all",
                    "Palavras": "word", 
                    "Frases": "phrase",
                    "Capítulos": "chapter",
                    "Versículos": "verse"
                }
                
                self.current_search_query = search_query
                self.search_results = self.search_engine.advanced_search(
                    search_query, 
                    search_type_map[search_type]
                )
        
        # Exibir resultados se houver
        if self.search_results:
            st.sidebar.markdown(f"**📊 {len(self.search_results)} resultado(s) encontrado(s)**")
            
            for i, result in enumerate(self.search_results[:5]):  # Mostrar primeiros 5
                result_type = result['type']
                if result_type == 'chapter':
                    st.sidebar.info(f"📖 Capítulo {result['number']}: {result['title']} (páginas {result['start_page']}-{result['end_page']})")
                elif result_type == 'verse':
                    st.sidebar.info(f"📜 {result['chapter']}:{result['verse']} - Página {result['page']}")
                else:
                    st.sidebar.info(f"📄 Página {result['page']} - {result.get('count', 1)} ocorrência(s)")
                
                if st.sidebar.button("Ir para", key=f"goto_{i}", use_container_width=True):
                    st.session_state.current_page = result['page']
                    st.rerun()
            
            if len(self.search_results) > 5:
                st.sidebar.info(f"📋 ... e mais {len(self.search_results) - 5} resultados")
    
    def render_search_results_page(self):
        """Página dedicada aos resultados de busca"""
        if not self.search_results:
            return
        
        st.title(f"🔍 Resultados da busca: '{self.current_search_query}'")
        st.markdown(f"**📊 {len(self.search_results)} resultado(s) encontrado(s)**")
        
        # Agrupar resultados por página
        results_by_page = {}
        for result in self.search_results:
            page = result['page']
            if page not in results_by_page:
                results_by_page[page] = []
            results_by_page[page].append(result)
        
        # Exibir resultados organizados
        for page, page_results in sorted(results_by_page.items()):
            with st.expander(f"📄 Página {page} - {len(page_results)} resultado(s)", expanded=False):
                for result in page_results:
                    if result['type'] == 'word':
                        st.markdown(f"**Palavra:** {result.get('matched_term', self.current_search_query)}")
                        st.markdown(f"**Ocorrências:** {result['count']}")
                    elif result['type'] == 'phrase':
                        st.markdown("**Frase encontrada:**")
                    elif result['type'] == 'verse':
                        st.markdown(f"**Versículo:** {result['chapter']}:{result['verse']}")
                    
                    # Exibir trecho
                    if 'excerpt' in result:
                        st.markdown(f"**Trecho:** {result['excerpt']}", unsafe_allow_html=True)
                    
                    # Botão para ir para a página
                    if st.button("Ir para esta página", key=f"result_goto_{page}_{result['type']}"):
                        st.session_state.current_page = page
                        st.rerun()
                    
                    st.markdown("---")

    def _render_interactive_text(self, segment):
        raw_text = segment.get('text', '')
        
        if not raw_text:
            st.warning("📝 Conteúdo não disponível para esta página")
            return
        
        formatted_text = self._format_text_for_display(raw_text)
        
        analysis = segment.get('analysis', {})
        keywords = analysis.get('keywords', [])[:8]
        entities = analysis.get('entities', [])[:5]
        
        page_highlights = {}
        if (st.session_state.current_page in st.session_state.user_highlights and 
            st.session_state.user_highlights[st.session_state.current_page]):
            page_highlights = st.session_state.user_highlights[st.session_state.current_page]
        
        highlighted_text = self._process_text_highlights_cached(
            formatted_text, keywords, entities, page_highlights
        )
        
        st.markdown("""
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;'>
            <h2>📖 Conteúdo da Página</h2>
            <div style='color: #c77dff; font-size: 1rem;'>
                🎨 <strong>Destacados:</strong> 
                <span style='background: #9d4edd40; padding: 3px 8px; border-radius: 5px; margin: 0 3px;'>Palavras-chave</span>
                <span style='background: #ff6b6b40; padding: 3px 8px; border-radius: 5px; margin: 0 3px;'>Entidades</span>
                <span style='background: #4cc9f040; padding: 3px 8px; border-radius: 5px; margin: 0 3px;'>Seleção</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='text-container focus-effect'>
            {highlighted_text}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("🔍 Ferramentas de Análise de Texto")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            selected_text = st.text_input(
                "Selecionar texto para análise:",
                placeholder="Digite ou cole o texto que deseja analisar",
                key=f"text_select_{st.session_state.current_page}"
            )
        
        with col2:
            st.markdown("<div style='height: 30px'></div>", unsafe_allow_html=True)
            if st.button("🔍 Analisar Texto", use_container_width=True) and selected_text:
                if st.session_state.current_page not in st.session_state.user_highlights:
                    st.session_state.user_highlights[st.session_state.current_page] = {}
                
                highlight_id = f"highlight_{len(st.session_state.user_highlights[st.session_state.current_page]) + 1}"
                st.session_state.user_highlights[st.session_state.current_page][highlight_id] = {
                    'text': selected_text,
                    'page': st.session_state.current_page
                }
                
                st.session_state.selected_text_for_analysis = selected_text
                st.session_state.show_ia_analysis = True
                
                st.success("Texto destacado para análise!")
        
        if keywords or entities or page_highlights:
            st.markdown("---")
            info_col1, info_col2, info_col3 = st.columns(3)
            
            with info_col1:
                if keywords:
                    st.caption(f"🔑 **Palavras-chave:** {', '.join(keywords[:5])}{'...' if len(keywords) > 5 else ''}")
            
            with info_col2:
                if entities:
                    entity_list = [f"{e[0]} ({e[1]})" for e in entities[:3]]
                    st.caption(f"🏷️ **Entidades:** {', '.join(entity_list)}{'...' if len(entities) > 3 else ''}")
            
            with info_col3:
                if page_highlights:
                    highlight_count = len(page_highlights)
                    st.caption(f"⭐ **Seleções do usuário:** {highlight_count} texto(s) destacado(s)")
    
    def _initialize_prompts(self):
        return {
            'summary': """Analise o seguinte texto e forneça um resumo conciso em português. 
Destaque os pontos principais, conceitos-chave e a mensagem central:""",
            
            'analysis': """Analise profundamente este texto considerando:
1. Contexto histórico e significado filosófico
2. Metáforas, simbolismos e linguagem figurada
3. Relações com temas maiores da obra
4. Implicações científicas, filosóficas ou sociais
5. Conexões com outros conceitos apresentados no livro

Texto para análise:""",
            
            'explain_concepts': """Explique os seguintes conceitos presentes no texto: {concepts}
Forneça definições claras, exemplos práticos e relação con o contexto do livro:""",
            
            'chapter_context': """Considerando que este texto faz parte do capítulo "{chapter}" do livro "{book_name}",
analise como este trecho se relaciona con:
1. O contexto geral do capítulo
2. A estrutura narrativa do livro
3. Os temas principais da obra
4. O desenvolvimento de ideias ao longo do livro

Trecho para análise:""",
            
            'page_summary': """Gere um resumo detalhado da página {page} do livro "{book_name}". 
Inclua os principais pontos, ideias-chave e como esta página se conecta com o conteúdo geral do livro:""",
            
            'highlight_analysis': """Analise o seguinte texto destacado pelo usuário: "{highlighted_text}"
Contexto do trecho: {context}
Forneça uma análise aprofundada do significado, importância e relações com o conteúdo do livro:"""
        }
    
    def _extract_chapters_advanced(self):
        chapters = []
        current_chapter = None
        chapter_patterns = [
            r'(capítulo|chapter|cap\.)\s+(\d+|[IVXLCDM]+)[\s:-]*(.*)',
            r'^(CAPÍTULO|CHAPTER)\s+(\d+|[IVXLCDM]+)[\s:-]*(.*)',
            r'^(\d+|[IVXLCDM]+)[\s.-]*(.*)',
            r'^.*\b(capítulo|chapter)\b.*$'
        ]
        
        for i, segment in enumerate(self.segments):
            text = segment.get('text', '').strip()
            
            if len(text) > 300:
                if current_chapter:
                    current_chapter['end_page'] = i
                continue
                
            chapter_detected = False
            chapter_title = ""
            chapter_number = ""
            
            for pattern in chapter_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    chapter_detected = True
                    groups = match.groups()
                    
                    if len(groups) >= 2:
                        chapter_number = groups[1] if groups[1] else str(len(chapters) + 1)
                        chapter_title = groups[2] if len(groups) > 2 and groups[2] else f"Capítulo {chapter_number}"
                    else:
                        chapter_number = str(len(chapters) + 1)
                        chapter_title = text
                    
                    break
            
            is_toc = any(word in text.lower() for word in ['sumário', 'índice', 'conteúdo', 'contents'])
            
            if chapter_detected and not is_toc:
                if current_chapter:
                    current_chapter['end_page'] = i
                
                current_chapter = {
                    'number': chapter_number,
                    'title': chapter_title,
                    'start_page': i + 1,
                    'end_page': len(self.segments),
                    'segments': [i + 1]
                }
                chapters.append(current_chapter)
            elif current_chapter and not is_toc:
                current_chapter['segments'].append(i + 1)
        
        return chapters
    
    def render_advanced_sidebar(self):
        with st.sidebar:
            st.markdown("""
            <div style='text-align: center; margin-bottom: 2rem; padding: 1rem; background: rgba(157, 78, 221, 0.1); border-radius: 15px;'>
                <h1 style='font-size: 2rem; margin-bottom: 0.5rem; background: linear-gradient(135deg, #e0aaff, #9d4edd); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>📖 FLUX-ON READER</h1>
                <p style='color: #c77dff; margin: 0; font-size: 1.1rem;'>Leitura Quântica Multidimensional</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.header("🔢 Navegação Rápida")
            nav_col1, nav_col2, nav_col3 = st.columns(3)
            
            with nav_col1:
                if st.button("⏮️ Primeira", use_container_width=True, help="Ir para a primeira página"):
                    self.nav_system.first_page()
            
            with nav_col2:
                if st.button("◀️ Anterior", use_container_width=True, help="Página anterior"):
                    self.nav_system.prev_page()
            
            with nav_col3:
                if st.button("Próxima ▶️", use_container_width=True, help="Próxima página"):
                    self.nav_system.next_page()
            
            # ✅ BOTÃO DE CONFIRMAÇÃO (só aparece quando há mudança pendente)
            if hasattr(st.session_state, 'pending_page') and st.session_state.pending_page != st.session_state.get('current_page', 1):
                st.markdown("---")
                if st.button("✅ **CONFIRMAR MUDANÇA DE PÁGINA**", 
                            use_container_width=True,
                            type="primary",
                            help="Clique para carregar a página selecionada"):
                    self.nav_system.confirm_page_change()
                    st.rerun()  # Força a atualização após confirmação
                
                st.info(f"📖 Página {st.session_state.pending_page} selecionada. Confirme para carregar.")
            
            st.header("🎯 Navegação por Página")

            # ✅ CORREÇÃO: O select_slider já funciona bem com o session_state
            selected_page = st.select_slider(
                "Selecionar página:",
                options=list(range(1, len(self.segments) + 1)),
                value=st.session_state.current_page,
                key="page_selector_optimized",
                on_change=lambda: setattr(st.session_state, 'pending_page', st.session_state.page_selector_optimized)
            )
            
            metrics_data = [
                ("📄 Total de páginas", len(self.segments)),
                ("📝 Palavras totais", self.book_analysis.get('total_words', 0)),
                ("🎯 Dificuldade média", f"{self.book_analysis.get('avg_difficulty', 0):.1f}/100"),
                ("📈 Variação de dificuldade", f"{self.book_analysis.get('max_difficulty', 0) - self.book_analysis.get('min_difficulty', 0):.1f}")
            ]
            
            for metric, value in metrics_data:
                st.metric(metric, value)
            
            st.header("🎯 Temas Principais")
            # CORREÇÃO: Usar self.book_analysis
            theme_dist = self.book_analysis.get('theme_distribution', {})
            
            if theme_dist:
                all_text = " ".join([segment.get('text', '') for segment in self.segments])
                extended_themes = self._analyze_extended_themes(all_text)
                
                combined_themes = {**theme_dist, **extended_themes}
                
                for theme, score in sorted(combined_themes.items(), key=lambda x: x[1], reverse=True)[:8]:
                    st.progress(score/100, f"{theme}: {score:.1f}%")
            else:
                st.info("Análise de temas em andamento...")
                
            st.markdown("---")
            if st.button("🏠 Voltar à Tela Inicial", use_container_width=True, key="back_to_main"):
                st.session_state.book_loaded = False
    
    def _get_current_chapter(self):
        current_page = st.session_state.current_page
        for chapter in self.chapters:
            if current_page >= chapter['start_page'] and current_page <= chapter['end_page']:
                return chapter
        return None
    
    def _render_visual_analysis(self, segment):
        st.markdown("---")
        st.header("📊 Análise Visual da Página")
        
        col1, col2 = st.columns(2)
        
        with col1:
            metrics = segment.get('complexity_metrics', {})
            if metrics:
                metrics_names = ['Palavras', 'Sentenças', 'Pal./Sentença', 'Tam. Médio']
                metrics_values = [
                    metrics.get('word_count', 0),
                    metrics.get('sentence_count', 0),
                    metrics.get('avg_sentence_length', 0),
                    metrics.get('avg_word_length', 0)
                ]
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatterpolar(
                    r=metrics_values,
                    theta=metrics_names,
                    fill='toself',
                    name='Métricas',
                    line_color='#e0aaff',
                    fillcolor='rgba(224, 170, 255, 0.3)'
                ))
                
                fig.update_layout(
                    polar=dict(
                        bgcolor='rgba(30, 30, 46, 0.3)',
                        radialaxis=dict(
                            visible=True,
                            range=[0, max(metrics_values) * 1.2]
                        ),
                    ),
                    showlegend=False,
                    title="📈 Métricas de Complexidade (Radar)",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#e0aaff', size=12),
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            themes = segment.get('themes', {})
            if themes and len(themes) > 0:
                text_analysis = self._analyze_text_patterns(segment.get('text', ''))
                extended_themes = text_analysis.get('extended_themes', {})
                
                all_themes = {**themes, **extended_themes}
                themes_df = pd.DataFrame({
                    'Tema': list(all_themes.keys()),
                    'Intensidade': list(all_themes.values())
                }).sort_values('Intensidade', ascending=False).head(8)
                
                fig = px.pie(themes_df, values='Intensidade', names='Tema', 
                            title="🎯 Distribuição de Temas (Incluindo Novos)",
                            hole=0.4,
                            color_discrete_sequence=px.colors.qualitative.Set3)
                
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#e0aaff'),
                    showlegend=True,
                    height=400,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.2,
                        xanchor="center",
                        x=0.5
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("🔍 Análise de temas em andamento...")
        
        st.markdown("---")
        st.subheader("🌍 Análise de Temas Sociais e Culturais")
        
        text_analysis = self._analyze_text_patterns(segment.get('text', ''))
        extended_themes = text_analysis.get('extended_themes', {})
        
        if extended_themes:
            theme_cols = st.columns(4)
            
            for i, (theme, score) in enumerate(extended_themes.items()):
                if score > 5:
                    with theme_cols[i % 4]:
                        icons = {
                            'política': '🏛️',
                            'religião': '🙏',
                            'sexo': '❤️',
                            'cultura': '🎭'
                        }
                        
                        st.metric(
                            label=f"{icons.get(theme, '📊')} {theme.capitalize()}",
                            value=f"{score:.1f}%",
                            help=f"Intensidade do tema {theme} nesta página"
                        )
            
            if any(score > 5 for score in extended_themes.values()):
                extended_df = pd.DataFrame({
                    'Tema': list(extended_themes.keys()),
                    'Intensidade': list(extended_themes.values())
                }).sort_values('Intensidade', ascending=False)
                
                fig = px.bar(extended_df, x='Tema', y='Intensidade',
                            title="📊 Intensidade dos Temas Sociais",
                            color='Intensidade',
                            color_continuous_scale='viridis')
                
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#e0aaff'),
                    height=300
                )
                
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("🤔 Nenhum tema social significativo detectado nesta página.")
        
        sentiment_score = max(0, min(100, segment.get('difficulty', 0) * 0.8))
        sentiment_label = "Positivo" if sentiment_score > 60 else "Neutro" if sentiment_score > 40 else "Desafiador"
        sentiment_icon = "😊" if sentiment_score > 60 else "😐" if sentiment_score > 40 else "😔"
        
        st.markdown("---")
        sentiment_col1, sentiment_col2, sentiment_col3 = st.columns([1, 2, 1])
        
        with sentiment_col2:
            html = f"""
            <div style='text-align: center; padding: 1.5rem; background: rgba(45, 45, 65, 0.7); border-radius: 15px; border-left: 5px solid #7b2cbf;'>
                <h3 style='color: #e0aaff; margin-bottom: 1rem;'>🎭 Tom Emocional da Página</h3>
                <div style='font-size: 2.5rem; font-weight: bold; color: #e0aaff; margin: 0.5rem 0;'>{sentiment_icon} {sentiment_label}</div>
                <div style='margin-top: 1.5rem; position: relative;'>
                    <div style='background: rgba(255,255,255,0.1); height: 25px; border-radius: 12px; overflow: hidden;'>
                        <div style='background: linear-gradient(90deg, #f44336, #ff9800, #4caf50); 
                                height: 100%; width: {sentiment_score:.1f}%; border-radius: 12px; 
                                position: relative;'>
                            <div style='position: absolute; right: 5px; top: 50%; transform: translateY(-50%); 
                                    color: white; font-weight: bold; font-size: 12px;'>
                                {sentiment_score:.1f}%
                            </div>
                        </div>
                    </div>
                    <div style='display: flex; justify-content: space-between; margin-top: 0.5rem; color: #c77dff; font-size: 0.9rem;'>
                        <span>Desafiador</span>
                        <span>Neutro</span>
                        <span>Positivo</span>
                    </div>
                </div>
            </div>
            """
            st.markdown(html, unsafe_allow_html=True)
    
    def _analyze_extended_themes(self, text):
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        total_words = len(words)
        
        if total_words == 0:
            return {theme: 0 for theme in self.extended_themes.keys()}
        
        theme_scores = {}
        
        for theme, theme_data in self.extended_themes.items():
            score = 0
            keyword_count = 0
            
            for keyword in theme_data['keywords']:
                pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
                count = len(re.findall(pattern, text_lower))
                
                if count > 0:
                    word_weight = theme_data['weight']
                    
                    common_word_penalty = 1.0
                    if keyword in ['poder', 'estado', 'lei', 'corpo', 'valor']:
                        common_word_penalty = 0.6
                    
                    score += (count * word_weight * common_word_penalty)
                    keyword_count += count
            
            density = (keyword_count / total_words) * 1000
            
            if density > 0:
                normalized_score = min(100, 20 * math.log1p(density))
            else:
                normalized_score = 0
            
            diversity_bonus = 1.0
            if keyword_count > 5:
                diversity_bonus = 1.2
            
            theme_scores[theme] = min(100, normalized_score * diversity_bonus)
        
        return theme_scores

    def _analyze_text_patterns(self, text):
        words = re.findall(r'\b\w+\b', text.lower())
        word_freq = Counter(words)
        
        stopwords = {'o', 'a', 'e', 'de', 'da', 'do', 'em', 'para', 'com', 'que', 'é', 'um', 'uma', 'os', 'as'}
        relevant_words = {word: count for word, count in word_freq.items() 
                         if word not in stopwords and len(word) > 3 and count > 1}
        
        scientific_terms = {'energia', 'quantum', 'consciência', 'evolução', 'comportamento', 
                           'física', 'mente', 'universo', 'realidade', 'matéria', 'filosofia'}
        
        found_terms = {term: word_freq.get(term, 0) for term in scientific_terms 
                      if term in word_freq}
        
        extended_themes = self._analyze_extended_themes(text)
        
        return {
            'frequent_words': dict(sorted(relevant_words.items(), 
                                        key=lambda x: x[1], reverse=True)[:15]),
            'scientific_terms': found_terms,
            'extended_themes': extended_themes,
            'total_words': len(words),
            'unique_words': len(set(words))
        }

    def _render_api_configuration(self):
        st.markdown("---")
        st.header("🔧 Configuração da API DeepSeek")
        
        with st.expander("⚙️ Configurar Conexão com IA", expanded=False):
            st.info("""
            **Para usar análises com IA em tempo real:**
            1. Obtenha uma chave API em: https://platform.deepseek.com/
            2. Cole sua chave API abaixo
            3. Salve as configurações
            """)
            
            api_key = st.text_input(
                "🔑 Chave API DeepSeek:",
                type="password",
                placeholder="sk-...",
                help="Insira sua chave API do DeepSeek"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Salvar Configurações", use_container_width=True):
                    if api_key:
                        self.api_config['api_key'] = api_key
                        self.api_config['configured'] = True
                        st.session_state.api_configured = True
                        st.success("✅ Configurações salvas com sucesso!")
                    else:
                        st.error("❌ Por favor, insira uma chave API válida")
            
            with col2:
                if st.button("🧪 Testar Conexão", use_container_width=True):
                    if api_key:
                        with st.spinner("Testando conexão com DeepSeek..."):
                            success = self._test_api_connection(api_key)
                            if success:
                                st.success("✅ Conexão com API estabelecida com sucesso!")
                            else:
                                st.error("❌ Falha na conexão. Verifique sua chave API.")
                    else:
                        st.warning("⚠️ Insira uma chave API primeiro")
            
            if self.api_config['configured']:
                st.markdown("---")
                st.success("✅ API Configurada - Análises em tempo real disponíveis")
                if st.button("🗑️ Remover Configuração", type="secondary", use_container_width=True):
                    self.api_config['configured'] = False
                    self.api_config['api_key'] = ''
                    st.session_state.api_configured = False
    
    def _test_api_connection(self, api_key: str) -> bool:
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": "Teste de conexão. Responda com 'OK'."}],
                "max_tokens": 10,
                "temperature": 0.1
            }
            
            response = requests.post(
                self.api_config['api_url'],
                headers=headers,
                json=payload,
                timeout=15
            )
            
            return response.status_code == 200
            
        except Exception:
            return False
    
    def _call_deepseek_api(self, prompt: str, max_tokens: int = 4000) -> Optional[str]:
        try:
            if not self.api_config['configured'] or not self.api_config['api_key']:
                st.warning("🔧 API não configurada. Usando análise inteligente local.")
                return self._fallback_analysis(prompt)
            
            headers = {
                "Authorization": f"Bearer {self.api_config['api_key']}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": "Você é um especialista em análise literária e científica. Forneça análises profundas e insights valiosos baseados no texto fornecido. Seja conciso, claro e focado nos aspectos mais relevantes. Responda em português."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": max_tokens,
                "temperature": 0.7,
                "top_p": 0.9,
                "stream": False
            }
            
            api_url = "https://api.deepseek.com/v1/chat/completions"
            
            with st.spinner("🔗 Conectando com DeepSeek AI..."):
                response = requests.post(
                    api_url,
                    headers=headers,
                    json=payload,
                    timeout=30
                )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                st.error(f"❌ Erro na API: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            st.error("⏰ Timeout na conexão com a API. Verifique sua internet.")
            return self._fallback_analysis(prompt)
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                st.error("🔐 Erro de autenticação. Verifique sua chave API.")
            elif e.response.status_code == 429:
                st.warning("🚦 Limite de requisições excedido. Usando análise local.")
            else:
                st.error(f"❌ Erro HTTP {e.response.status_code}: {e.response.text}")
            return self._fallback_analysis(prompt)
            
        except Exception as e:
            st.error(f"⚠️ Erro na chamada da API: {str(e)}")
            return self._fallback_analysis(prompt)
    
    def _fallback_analysis(self, prompt: str) -> str:
        return f"""
        **📊 Análise Local - FLUX-ON Reader**

        🔧 **Status:** API DeepSeek não disponível no momento

        💡 **Para ativar análises completas:**
        1. Configure sua chave API em: https://platform.deepseek.com/
        2. Adicione créditos à sua conta
        3. Sua chave atual: `{self.api_config.get('api_key', 'Não configurada')}`

        **📋 Prompt que seria enviado:**
        {prompt}
        """

    def _render_analysis_tools(self, segment):
        st.markdown("---")
        
        # MOVER AS ABAS PARA A SIDEBAR - ESTRUTURA REORGANIZADA
        with st.sidebar:
            st.markdown("---")
            st.header("🧰 Ferramentas de Análise")
            
            # Abas verticais na sidebar
            selected_tool = st.radio(
                "Selecione a ferramenta:",
                ["🤖 Análise IA", "🔍 Insights", "📝 Anotações", "⭐ Textos Destacados"],
                key="analysis_tools_sidebar"
            )
        
        # Container principal para o conteúdo das ferramentas
        analysis_container = st.container()
        
        with analysis_container:
            if selected_tool == "🤖 Análise IA":
                self._render_ia_analysis_tab(segment)
                
            elif selected_tool == "🔍 Insights":
                self._render_insights_tab(segment)
                
            elif selected_tool == "📝 Anotações":
                self._render_notes_tab()
                
            elif selected_tool == "⭐ Textos Destacados":
                self._render_highlights_tab()

    def _render_ia_analysis_tab(self, segment):
        st.subheader("🤖 Análise com Inteligência Artificial")
        
        if self.api_config['configured']:
            st.success("✅ API Configurada - Análises em tempo real")
        else:
            st.warning("🔧 API não configurada - Usando análise local")
            st.info("💡 Configure a API DeepSeek para análises mais precisas")
        
        analysis_options = {
            "Resumo da Página": "page_summary",
            "Análise Profunda": "analysis",
            "Explicar Conceitos": "explain_concepts",
            "Contexto do Capítulo": "chapter_context"
        }
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            analysis_type = st.selectbox(
                "Tipo de análise:",
                list(analysis_options.keys()),
                help="Selecione o tipo de análise que deseja realizar"
            )
        
        with col2:
            st.markdown("<div style='height: 28px'></div>", unsafe_allow_html=True)
            if st.button("🚀 Gerar Análise", use_container_width=True):
                with st.spinner("🤖 Processando análise..."):
                    prompt_type = analysis_options[analysis_type]
                    # CORREÇÃO: Usar o método correto para gerar prompt
                    prompt = self._generate_text_analysis_prompt(prompt_type, segment.get('text', '')[:3000], segment)
                    
                    st.session_state.ia_prompt = prompt
                    analysis_result = self._call_deepseek_api(prompt)
                    
                    if not analysis_result:
                        analysis_result = self._generate_generic_analysis(prompt)
                    
                    st.session_state.ia_analysis_result = analysis_result
                    st.success("✅ Análise concluída!")
        
        # Preview de padrões detectados
        text_to_analyze = segment.get('text', '')[:3000]
        if text_to_analyze:
            patterns = self._analyze_text_patterns(text_to_analyze)
            
            with st.expander("🔍 Visualizar Padrões Detectados", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    if patterns['frequent_words']:
                        st.write("**📊 Palavras frequentes:**")
                        for word, count in list(patterns['frequent_words'].items())[:4]:
                            st.write(f"- `{word}`: {count}x")
                
                with col2:
                    if patterns['extended_themes']:
                        relevant_themes = {theme: score for theme, score in patterns['extended_themes'].items() if score > 5}
                        if relevant_themes:
                            st.write("**🌍 Temas detectados:**")
                            for theme, score in list(relevant_themes.items())[:3]:
                                st.write(f"- `{theme}`: {score:.1f}%")
        
        # Exibir resultado da análise
        if 'ia_analysis_result' in st.session_state and st.session_state.ia_analysis_result:
            st.markdown("---")
            st.subheader("📋 Resultado da Análise")
            st.markdown(st.session_state.ia_analysis_result)
            
    def _generate_contextual_prompt(self, prompt_type, text, segment):
        """Gera prompt contextualizado baseado no tipo de análise"""
        book_name = self.analysis_data.get('book_name', 'este livro')
        current_page = st.session_state.current_page
        current_chapter = self._get_current_chapter()
        
        chapter_info = f"Capítulo {current_chapter['number']}: {current_chapter['title']}" if current_chapter else "Contexto geral"
        
        prompts = {
            'page_summary': f"""Gere um resumo detalhado da página {current_page} do livro "{book_name}".
Contexto: {chapter_info}
Texto: {text[:2000]}
Inclua os principais pontos, ideias-chave e como esta página se conecta com o conteúdo geral do livro.""",
            
            'analysis': f"""Analise profundamente este texto considerando:
1. Contexto histórico e significado filosófico
2. Metáforas, simbolismos e linguagem figurada  
3. Relações com temas maiores da obra
4. Implicações científicas, filosóficas ou sociais
5. Conexões com outros conceitos apresentados no livro

Contexto: {chapter_info}
Livro: {book_name}
Texto para análise: {text[:2000]}""",
            
            'explain_concepts': f"""Explique os conceitos complexos presentes no texto:
Contexto: {chapter_info}
Livro: {book_name}
Texto: {text[:2000]}
Forneça definições claras, exemplos práticos e relação com o contexto do livro.""",
            
            'chapter_context': f"""Considerando que este texto faz parte do {chapter_info} do livro "{book_name}",
analise como este trecho se relaciona com:
1. O contexto geral do capítulo
2. A estrutura narrativa do livro  
3. Os temas principais da obra
4. O desenvolvimento de ideias ao longo do livro

Trecho para análise: {text[:2000]}"""
        }
        
        return prompts.get(prompt_type, f"Analise o seguinte texto: {text[:2000]}")

    def _render_insights_tab(self, segment):
        st.subheader("🔍 Insights Automáticos")
        
        insights = self._generate_insights(segment)
        
        if insights:
            st.info("💡 **Insights detectados:**")
            for insight in insights[:3]:  # Limitar a 3 insights principais
                st.write(f"• {insight}")
            
            if len(insights) > 3:
                with st.expander("Ver mais insights"):
                    for insight in insights[3:]:
                        st.write(f"• {insight}")
            
            insights_text = "\n".join(insights)
            if st.button("📋 Copiar Insights", use_container_width=True):
                self._copy_to_clipboard(insights_text)
                st.success("✅ Insights copiados!")
        else:
            st.info("🤔 Nenhum insight automático detectado.")
        
        # Análise de padrões compacta
        st.markdown("---")
        st.subheader("📊 Análise Rápida")
        
        text_analysis = self._analyze_text_patterns(segment.get('text', ''))
        
        col1, col2 = st.columns(2)
        
        with col1:
            if text_analysis['frequent_words']:
                st.write("**🔤 Palavras-chave:**")
                for word, count in list(text_analysis['frequent_words'].items())[:4]:
                    st.write(f"`{word}` ({count}x)")
        
        with col2:
            if text_analysis['extended_themes']:
                relevant_themes = {t: s for t, s in text_analysis['extended_themes'].items() if s > 5}
                if relevant_themes:
                    st.write("**🎯 Temas:**")
                    for theme, score in list(relevant_themes.items())[:2]:
                        st.write(f"`{theme}`: {score:.1f}%")

    def _render_notes_tab(self):
        st.subheader("📝 Anotações Pessoais")
        
        # Área de nova anotação
        new_note = st.text_area(
            "✍️ Nova anotação:",
            placeholder="Digite suas anotações aqui...",
            height=120,
            key=f"new_note_{st.session_state.current_page}"
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("💾 Salvar", use_container_width=True) and new_note:
                st.session_state.user_notes[st.session_state.current_page] = new_note
                st.success("✅ Salvo!")
        
        with col2:
            if st.button("🧹 Limpar", use_container_width=True):
                st.session_state.user_notes[st.session_state.current_page] = ""
        
        # Anotações salvas
        st.markdown("---")
        st.subheader("📓 Anotações Salvas")
        
        current_notes = st.session_state.user_notes.get(st.session_state.current_page, "")
        if current_notes.strip():
            st.text_area(
                f"Anotação Página {st.session_state.current_page}:",
                value=current_notes,
                height=200,
                key=f"current_note_display"
            )
        else:
            st.info("📝 Nenhuma anotação para esta página.")

    def _render_highlights_tab(self):
        st.subheader("⭐ Textos Destacados")
        
        current_page = st.session_state.current_page
        page_highlights = st.session_state.user_highlights.get(current_page, {})
        
        if page_highlights:
            st.success(f"📖 **{len(page_highlights)} destaque(s)**")
            
            for highlight_id, highlight_data in list(page_highlights.items())[:3]:  # Limitar a 3
                with st.expander(f"🔖 Destaque {list(page_highlights.keys()).index(highlight_id) + 1}", expanded=False):
                    st.info(f'"{highlight_data["text"]}"')
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"📋 Copiar", key=f"copy_{highlight_id}"):
                            self._copy_to_clipboard(highlight_data["text"])
                            st.success("✅ Copiado!")
                    with col2:
                        if st.button(f"🗑️ Remover", key=f"remove_{highlight_id}"):
                            del st.session_state.user_highlights[current_page][highlight_id]
                            st.success("✅ Removido!")
            
            if len(page_highlights) > 3:
                with st.expander("Ver todos os destaques"):
                    for highlight_id, highlight_data in list(page_highlights.items())[3:]:
                        st.info(f'"{highlight_data["text"]}"')
        else:
            st.info("⭐ Nenhum texto destacado nesta página.")
        
        # Estatísticas rápidas
        total_highlights = sum(len(highlights) for highlights in st.session_state.user_highlights.values())
        if total_highlights > 0:
            st.markdown("---")
            st.metric("📊 Total no livro", total_highlights)
            
    def _copy_to_clipboard(self, text):
        try:
            import pyperclip
            pyperclip.copy(text)
            return True
        except:
            try:
                js_code = f"""
                navigator.clipboard.writeText(`{text}`).then(() => {{
                    console.log('Texto copiado para a área de transferência');
                }}).catch(err => {{
                    console.error('Erro ao copiar texto: ', err);
                }});
                """
                st.components.v1.html(f"<script>{js_code}</script>", height=0)
                return True
            except:
                st.error("❌ Não foi possível copiar para a área de transferência")
                return False
        
    def _generate_insights(self, segment):
        insights = []
        difficulty = segment.get('difficulty', 0)
        themes = segment.get('themes', {})
        readability = segment.get('analysis', {}).get('readability_score', 0)
        
        text_analysis = self._analyze_text_patterns(segment.get('text', ''))
        extended_themes = text_analysis.get('extended_themes', {})
        
        if difficulty > 70:
            insights.append("💡 **Alta complexidade conceptual**: Esta página contém conceitos avançados de filosofia e ciência. Considere ler com atenção extra e fazer pausas para reflexão.")
        elif difficulty < 30:
            insights.append("💡 **Leitura acessível**: Conteúdo de fácil compreensão. Ideal para revisão rápida e absorção de conceitos fundamentais.")
        
        if themes:
            main_theme = max(themes, key=themes.get) if themes else None
            if main_theme:
                insights.append(f"🎯 **Tema principal**: {main_theme} ({themes[main_theme]:.1f}% de relevância). Este tema é central para a compreensão do capítulo atual.")
        
        for theme, score in extended_themes.items():
            if score > 20:
                icons = {'política': '🏛️', 'religião': '🙏', 'sexo': '❤️', 'cultura': '🎭'}
                insights.append(f"{icons.get(theme, '📊')} **Tema {theme}**: Forte presença ({score:.1f}%) - relevante para análise social do conteúdo.")
        
        if readability > 80:
            insights.append("📖 **Excelente legibilidade**: Texto bem estruturado e de fácil leitura. Aproveite para absorver os conceitos rapidamente.")
        elif readability < 50:
            insights.append("⚠️ **Texto complexo**: Estrutura de frases mais complexa. Considere ler em voz alta para melhor compreensão.")
        
        text = segment.get('text', '').lower()
        if any(word in text for word in ['tesla', 'energia', 'elétrica']):
            insights.append("🔌 **Contexto científico**: Esta página faz referência a conceitos de física e energia. Esses conceitos são usados como metáfora para processos conscientes.")
        
        if any(word in text for word in ['comportamento', 'humano', 'evolução']):
            insights.append("🧠 **Análise comportamental**: O texto explora padrões de comportamento humano. Preste atenção nas conexões entre biologia e psicologia.")
        
        return insights

    def _render_selected_text_analysis(self):
        if hasattr(st.session_state, 'show_ia_analysis') and st.session_state.show_ia_analysis:
            st.markdown("---")
            st.header("🧠 Análise Avançada do Texto Selecionado")
            
            selected_text = st.session_state.selected_text_for_analysis
            current_segment = self.segments[st.session_state.current_page - 1]
            context_text = current_segment.get('text', '')
            
            prompt = self._generate_text_analysis_prompt('analysis', selected_text)
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown("**📝 Texto Selecionado para Análise:**")
                st.info(f'"{selected_text}"')
            
            with col2:
                if st.button("🔄 Gerar Nova Análise", use_container_width=True):
                    st.session_state.ia_analysis_result = None
                
                if st.button("❌ Fechar Análise", use_container_width=True):
                    st.session_state.show_ia_analysis = False
            
            patterns = self._analyze_text_patterns(selected_text)
            with st.expander("🔍 Padrões Detectados no Texto", expanded=False):
                if patterns['frequent_words']:
                    st.write("**📊 Palavras-chave:**")
                    for word, count in list(patterns['frequent_words'].items())[:5]:
                        st.write(f"- `{word}` ({count}x)")
                
                extended_themes = patterns.get('extended_themes', {})
                relevant_themes = {t: s for t, s in extended_themes.items() if s > 10}
                if relevant_themes:
                    st.write("**🌍 Temas Detectados:**")
                    for theme, score in relevant_themes.items():
                        st.write(f"- `{theme}`: {score:.1f}%")
            
            if 'ia_analysis_result' not in st.session_state:
                with st.spinner("🤖 Analisando texto com IA multidimensional..."):
                    analysis_result = self._call_deepseek_api(prompt)
                    st.session_state.ia_analysis_result = analysis_result
                    st.session_state.ia_prompt_used = prompt
            
            if st.session_state.ia_analysis_result:
                st.markdown("---")
                st.subheader("📋 Resultado da Análise Multidimensional")
                st.markdown(st.session_state.ia_analysis_result)
                
                with st.expander("🔧 Detalhes Técnicos da Análise"):
                    st.text_area("Prompt utilizado:", st.session_state.ia_prompt_used, height=200)
            
            st.markdown("---")
    
    def _render_segment_safely(self, segment):
        try:
            if not segment:
                st.warning("📄 Segmento não disponível")
                return
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                self._render_interactive_text(segment)
                
            with col2:
                self._render_analysis_tools(segment)
            
            self._render_visual_analysis(segment)
            
            self._render_selected_text_analysis()
            
        except Exception as e:
            st.error(f"❌ Erro ao renderizar página: {str(e)}")
            st.info("📋 Recarregue a página ou volte para a página anterior")

    def render_quantum_reader(self):
        """
        Renderiza o conteúdo principal da página atual do livro.
        """
        # ✅ Verificar se há uma mudança de página pendente
        if hasattr(st.session_state, 'pending_page') and st.session_state.pending_page != st.session_state.current_page:
            st.warning(f"📖 Página {st.session_state.pending_page} selecionada. Clique em 'Confirmar Mudança de Página' na sidebar para carregar.")
        
        # CORREÇÃO: Forçar rerun quando a página mudar (mantido para compatibilidade)
        if 'last_page' not in st.session_state:
            st.session_state.last_page = st.session_state.current_page
        
        if st.session_state.last_page != st.session_state.current_page:
            st.session_state.last_page = st.session_state.current_page
            st.rerun()
            
        if not self.render_controller.should_render():
            st.info("⏳ Carregando conteúdo...")
            return
            
        if not self.render_controller.acquire_lock():
            return
        
        try:
            current_page = st.session_state.current_page
            total_pages = len(self.segments)
            
            # CORREÇÃO: Verificar limites antes de renderizar
            if current_page > total_pages:
                st.session_state.current_page = total_pages
                st.rerun()
                return
                
            if current_page < 1:
                st.session_state.current_page = 1
                st.rerun()
                return
            
            # CORREÇÃO: Usar state_manager para obter segmento atual
            segment = self.state_manager.get_current_segment()
            
            st.markdown(f"""
            <div style='display: flex; justify-content: space-between; align-items: center; 
                        background: rgba(157, 78, 221, 0.1); padding: 1rem; border-radius: 10px; 
                        margin-bottom: 1.5rem; border-left: 4px solid #9d4edd;'>
                <div>
                    <h2 style='color: #e0aaff; margin: 0; font-size: 1.8rem;'>📖 {self.analysis_data.get('book_name', 'Livro')}</h2>
                    <p style='color: #c77dff; margin: 0;'>Página {current_page} de {total_pages}</p>
                </div>
                <div style='text-align: right;'>
                    <p style='color: #c77dff; margin: 0;'>Dificuldade: {segment.get('difficulty', 0):.1f}/100</p>
                    <p style='color: #c77dff; margin: 0;'>{segment.get('complexity_metrics', {}).get('word_count', 0)} palavras</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # CORREÇÃO: Chamar método de renderização seguro
            self._render_segment_safely(segment)
            
        except Exception as e:
            st.error(f"Erro na renderização: {e}")
            # CORREÇÃO: Definir segment antes de usar no except
            segment = self.state_manager.get_current_segment() if hasattr(self, 'state_manager') else {}
            if segment and 'text' in segment:
                st.text_area("Conteúdo da página:", segment['text'], height=300)
        finally:
            self.render_controller.release_lock()

    def render_book_overview(self):
        st.title("📊 Visão Geral do Livro")
        
        book_analysis = self.analysis_data.get('book_analysis', {})
        theme_analysis = self.analysis_data.get('theme_analysis', {})
        
        st.subheader("📈 Métricas Principais")
        col1, col2, col3, col4 = st.columns(4)
        metrics = [
            ("📄 Total de Páginas", book_analysis.get('total_segments', 0), "#4cc9f0"),
            ("📝 Palavras", book_analysis.get('total_words', 0), "#9d4edd"),
            ("🎯 Dificuldade Média", f"{book_analysis.get('avg_difficulty', 0):.1f}/100", "#ff9800"),
            ("📈 Variação", f"{book_analysis.get('max_difficulty', 0) - book_analysis.get('min_difficulty', 0):.1f}", "#f44336")
        ]
        
        for i, (label, value, color) in enumerate(metrics):
            with [col1, col2, col3, col4][i]:
                st.markdown(f"""
                <div class='metric-card pulse-animation'>
                    <h3 style='color: {color}; margin: 0; font-size: 1.2rem;'>{label}</h3>
                    <p style='font-size: 2.2rem; font-weight: bold; color: {color}; margin: 0;'>{value}</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("📊 Evolução da Dificuldade")
        difficulties = [s.get('difficulty', 0) for s in self.segments]
        
        if difficulties:
            df = pd.DataFrame({
                'Página': range(1, len(difficulties) + 1),
                'Dificuldade': difficulties,
                'Capítulo': ['Geral'] * len(difficulties)
            })
            
            if self.chapters:
                for i, chapter in enumerate(self.chapters):
                    start, end = chapter['start_page'] - 1, min(chapter['end_page'], len(difficulties))
                    df.loc[start:end, 'Capítulo'] = f"Cap {chapter['number']}"
            
            fig = px.line(df, x='Página', y='Dificuldade', 
                        title="Evolução da Dificuldade por Página",
                        color='Capítulo',
                        color_discrete_sequence=px.colors.qualitative.Set3)
            
            avg_difficulty = book_analysis.get('avg_difficulty', 0)
            fig.add_hline(y=avg_difficulty, 
                        line_dash="dash", line_color="red",
                        annotation_text=f"Média: {avg_difficulty:.1f}")
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e0aaff'),
                height=500,
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        if theme_analysis:
            st.markdown("---")
            st.subheader("🎭 Mapa de Calor Temático")
            
            extended_theme_analysis = {}
            for theme_name in self.extended_themes.keys():
                extended_theme_analysis[theme_name] = []
            
            for i, segment in enumerate(self.segments):
                text = segment.get('text', '')
                segment_themes = self._analyze_extended_themes(text)
                
                for theme_name, score in segment_themes.items():
                    extended_theme_analysis[theme_name].append({
                        'segment': i + 1,
                        'score': score
                    })
            
            combined_theme_analysis = {**theme_analysis, **extended_theme_analysis}
            
            theme_names = list(combined_theme_analysis.keys())
            max_pages = max(len(data) for data in combined_theme_analysis.values())
            
            heatmap_data = []
            for theme in theme_names:
                theme_scores = [0] * max_pages
                for point in combined_theme_analysis[theme]:
                    if point['segment'] <= max_pages:
                        theme_scores[point['segment'] - 1] = point['score']
                heatmap_data.append(theme_scores)
            
            fig = px.imshow(heatmap_data,
                        labels=dict(x="Página", y="Tema", color="Intensidade"),
                        x=list(range(1, max_pages + 1)),
                        y=theme_names,
                        aspect="auto",
                        color_continuous_scale="viridis")
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e0aaff'),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.subheader("🌍 Análise de Temas Sociais e Culturais")
        
        all_text = " ".join([segment.get('text', '') for segment in self.segments])
        extended_themes = self._analyze_extended_themes(all_text)
        
        if extended_themes:
            theme_cols = st.columns(4)
            
            for i, (theme, score) in enumerate(extended_themes.items()):
                if score > 5:
                    with theme_cols[i % 4]:
                        icons = {
                            'política': '🏛️',
                            'religião': '🙏',
                            'sexo': '❤️',
                            'cultura': '🎭'
                        }
                        
                        st.metric(
                            label=f"{icons.get(theme, '📊')} {theme.capitalize()}",
                            value=f"{score:.1f}%",
                            help=f"Intensidade do tema {theme} no livro"
                        )
            
            if any(score > 5 for score in extended_themes.values()):
                extended_df = pd.DataFrame({
                    'Tema': list(extended_themes.keys()),
                    'Intensidade': list(extended_themes.values())
                }).sort_values('Intensidade', ascending=False)
                
                fig = px.bar(extended_df, x='Tema', y='Intensidade',
                            title="📊 Intensidade dos Temas Sociais no Livro",
                            color='Intensidade',
                            color_continuous_scale='viridis')
                
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#e0aaff'),
                    height=300
                )
                
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("🤔 Nenhum tema social significativo detectado no livro.")
        
        st.markdown("---")
        st.subheader("🧠 Estatísticas de Leitura")
        
        total_words = book_analysis.get('total_words', 0)
        reading_time_min = total_words / 200
        
        stat_col1, stat_col2, stat_col3 = st.columns(3)
        
        with stat_col1:
            st.metric("⏱️ Tempo Estimado", f"{reading_time_min:.0f} min")
        
        with stat_col2:
            avg_difficulty = book_analysis.get('avg_difficulty', 0)
            level = "Fácil" if avg_difficulty < 40 else "Médio" if avg_difficulty < 70 else "Difícil"
            st.metric("📊 Nível", level)
        
        with stat_col3:
            st.metric("📖 Densidade", f"{(total_words/book_analysis.get('total_segments', 1)):.0f} palavras/página")
    
    def render_export_section(self):
        st.title("💾 Exportar Dados e Relatórios")
        
        st.info("""
        **Exporte seus dados de leitura** para análise externa, compartilhamento ou backup.
        Todos os relatórios incluem suas anotações pessoais e destaques.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Dados de Análise")
            
            if st.button("📄 JSON Completo", use_container_width=True, help="Exportar todos os dados de análise em formato JSON"):
                try:
                    export_data = self.analysis_data.copy()
                    export_data['user_notes'] = st.session_state.user_notes
                    export_data['user_highlights'] = st.session_state.user_highlights

                    data_str = safe_json_dump(export_data)

                    b64 = base64.b64encode(data_str.encode()).decode()
                    href = f'<a href="data:application/json;base64,{b64}" download="analise_livro_completa.json">⬇️ Baixar JSON Completo</a>'
                    st.markdown(href, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Erro ao gerar JSON: {str(e)}")
            
            if st.button("📈 Dados Estatísticos", use_container_width=True, help="Exportar métricas e estatísticas em CSV"):
                try:
                    output = "Página,Dificuldade,Palavras,Sentenças,Tema Principal\n"
                    for i, segment in enumerate(self.segments):
                        themes = segment.get('themes', {})
                        main_theme = max(themes, key=themes.get) if themes else 'Nenhum'
                        output += f"{i + 1},{segment.get('difficulty', 0)},{segment.get('complexity_metrics', {}).get('word_count', 0)},{segment.get('complexity_metrics', {}).get('sentence_count', 0)},{main_theme}\n"
                    
                    b64 = base64.b64encode(output.encode()).decode()
                    href = f'<a href="data:file/csv;base64,{b64}" download="estatisticas_livro.csv">⬇️ Baixar CSV Estatístico</a>'
                    st.markdown(href, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Erro ao gerar CSV: {str(e)}")
        
        with col2:
            st.subheader("📝 Conteúdo Personalizado")
            
            if st.button("📖 Anotações Pessoais", use_container_width=True, help="Exportar apenas suas anotações e destaques"):
                self._export_notes()
            
            if st.button("🖼️ Gráficos de Análise", use_container_width=True, help="Exportar visualizações gráficas (em breve)"):
                st.info("Recurso em desenvolvimento - em breve disponível!")
            
            if st.button("🤖 Análises com IA", use_container_width=True, help="Exportar análises geradas pela IA (em breve)"):
                st.info("Recurso em desenvolvimento - em breve disponível!")
    
    def _export_notes(self):
        if not st.session_state.user_notes:
            st.warning("Não há anotações para exportar.")
            return
        
        notes_text = "# Anotações Pessoais - FLUX-ON Reader\n\n"
        for page, note in st.session_state.user_notes.items():
            if note.strip():
                notes_text += f"## Página {page}\n\n{note}\n\n---\n\n"
        
        b64 = base64.b64encode(notes_text.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="anotacoes_fluxon.txt">📥 Baixar Anotações</a>'
        st.markdown(href, unsafe_allow_html=True)
        st.success("Anotações preparadas para download!")

    def render(self):
        if 'book_cover_shown' not in st.session_state:
            book_cover = self.analysis_data.get('book_cover')
            if book_cover:
                st.markdown("""
                <div style='text-align: center; margin: 2rem 0; padding: 2rem; background: rgba(45, 45, 65, 0.8); border-radius: 20px;'>
                    <h1 style='color: #e0aaff; margin-bottom: 2rem;'>📖 {}</h1>
                    <img src="{}" style="max-width: 300px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
                </div>
                """.format(self.analysis_data.get('book_name', 'Livro'), book_cover), 
                unsafe_allow_html=True)
                
                st.markdown("---")
                st.session_state.book_cover_shown = True
        
        self.render_search_interface()
        
        # Adicionar opção de menu para resultados de busca
        menu_options = {
            "📖 Ler Livro": self.render_quantum_reader,
            "📊 Visão Geral": self.render_book_overview,
            "🔍 Resultados Busca": self.render_search_results_page,  # NOVO
            "🔧 Configurações": self._render_api_configuration,
            "💾 Exportar": self.render_export_section
        }
        
        with st.sidebar:
            selected_menu = st.selectbox(
                "**Navegação Principal**",
                list(menu_options.keys()),
                index=0
            )
        
        self.render_advanced_sidebar()
        
        menu_options[selected_menu]()
        
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #c77dff; padding: 2rem; background: rgba(157, 78, 221, 0.1); border-radius: 15px;'>
            <p style='font-size: 1.2rem; margin-bottom: 0.5rem;'>✨ <strong>FLUX-ON Quantum Reader v8.0</strong> - Sistema Avançado de Análise Literária</p>
            <p style='margin: 0;'>📚 Transformando leitura em experiência quântica multidimensional</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    try:
        if 'book_loaded' not in st.session_state:
            st.session_state.book_loaded = False
        
        if not st.session_state.book_loaded:
            render_book_opener()
            return
            
        analysis_data_str = """{
  "book_analysis": {
    "total_segments": 180,
    "total_chapters": 13,
    "total_pages": 180,
    "avg_difficulty": 27.936589895011757,
    "max_difficulty": 45.06435331230284,
    "min_difficulty": 20.185625,
    "theme_distribution": {
      "ciencia": 63.75750998182838,
      "tecnologia": 27.958671860081104,
      "filosofia": 68.43493128421471,
      "arte": 70.14962004245483,
      "historia": 57.927097057531846
    },
    "total_words": 44738,
    "avg_words_per_segment": 248.54444444444445,
    "formatting_preservation": 79.22222222222223,
    "preservation_score": 1.2534039661318943e-05,
    "book_name": "miolo_caos do passado sendo vivido no futuro_28032022.pdf",
    "analysis_timestamp": "2025-09-15T18:46:55",
    "structure_preserved": false
  },
  "theme_analysis": {
    "ciencia": [
      {
        "segment": 1,
        "score": 56.52173913043479,
        "position": 5459,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 56.52173913043479,
        "position": 31035,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 46.42857142857144,
        "position": 32937,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 46.42857142857144,
        "position": 38583,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 53370,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 34.21052631578947,
        "position": 56391,
        "chapter": 7
      },
      {
        "segment": 1,
        "score": 27.083333333333336,
        "position": 59660,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 36.61971830985916,
        "position": 61358,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 11.504424778761061,
        "position": 63098,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 30.232558139534888,
        "position": 76590,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 91126,
        "chapter": 3
      },
      {
        "segment": 1,
        "score": 30.232558139534888,
        "position": 94653,
        "chapter": 3
      },
      {
        "segment": 1,
        "score": 56.52173913043479,
        "position": 110986,
        "chapter": 3
      },
      {
        "segment": 1,
        "score": 39.3939393939394,
        "position": 121456,
        "chapter": 3
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 128946,
        "chapter": 4
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 130821,
        "chapter": 4
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 132747,
        "chapter": 4
      },
      {
        "segment": 1,
        "score": 46.42857142857143,
        "position": 138362,
        "chapter": 4
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 142394,
        "chapter": 4
      },
      {
        "segment": 1,
        "score": 83.87096774193549,
        "position": 144092,
        "chapter": 4
      },
      {
        "segment": 1,
        "score": 72.22222222222221,
        "position": 145860,
        "chapter": 4
      },
      {
        "segment": 1,
        "score": 56.52173913043479,
        "position": 149630,
        "chapter": 4
      },
      {
        "segment": 1,
        "score": 72.22222222222221,
        "position": 151542,
        "chapter": 4
      },
      {
        "segment": 1,
        "score": 46.42857142857144,
        "position": 155003,
        "chapter": 10
      },
      {
        "segment": 1,
        "score": 46.42857142857144,
        "position": 159646,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 83.87096774193549,
        "position": 161747,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 46.42857142857144,
        "position": 163865,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 56.52173913043479,
        "position": 165284,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 170814,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 172945,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 174691,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 86.66666666666667,
        "position": 176370,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 30.232558139534888,
        "position": 178473,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 39.3939393939394,
        "position": 180193,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 182020,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 72.22222222222221,
        "position": 194542,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 30.232558139534888,
        "position": 201116,
        "chapter": 12
      },
      {
        "segment": 1,
        "score": 39.3939393939394,
        "position": 204771,
        "chapter": 6
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 210385,
        "chapter": 6
      },
      {
        "segment": 1,
        "score": 30.232558139534888,
        "position": 212455,
        "chapter": 6
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 231154,
        "chapter": 6
      },
      {
        "segment": 1,
        "score": 56.52173913043479,
        "position": 235130,
        "chapter": 7
      },
      {
        "segment": 1,
        "score": 56.52173913043479,
        "position": 267568,
        "chapter": 7
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 271104,
        "chapter": 8
      },
      {
        "segment": 1,
        "score": 46.42857142857144,
        "position": 272319,
        "chapter": 8
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 277681,
        "chapter": 8
      },
      {
        "segment": 1,
        "score": 46.42857142857144,
        "position": 280261,
        "chapter": 8
      },
      {
        "segment": 1,
        "score": 46.42857142857144,
        "position": 285618,
        "chapter": 8
      },
      {
        "segment": 1,
        "score": 24.528301886792455,
        "position": 287522,
        "chapter": 8
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 290440,
        "chapter": 8
      }
    ],
    "tecnologia": [
      {
        "segment": 1,
        "score": 43.47826086956522,
        "position": 5459,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 14.084507042253522,
        "position": 61358,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 23.25581395348837,
        "position": 94653,
        "chapter": 3
      },
      {
        "segment": 1,
        "score": 16.129032258064516,
        "position": 144092,
        "chapter": 4
      },
      {
        "segment": 1,
        "score": 43.47826086956522,
        "position": 165284,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 23.25581395348837,
        "position": 178473,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 23.25581395348837,
        "position": 201116,
        "chapter": 12
      },
      {
        "segment": 1,
        "score": 30.303030303030305,
        "position": 204771,
        "chapter": 6
      },
      {
        "segment": 1,
        "score": 43.47826086956522,
        "position": 235130,
        "chapter": 7
      },
      {
        "segment": 1,
        "score": 18.867924528301888,
        "position": 287522,
        "chapter": 8
      }
    ],
    "filosofia": [
      {
        "segment": 1,
        "score": 100.0,
        "position": 7467,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 24753,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 26420,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 53.57142857142857,
        "position": 32937,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 53.57142857142857,
        "position": 38583,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 42.857142857142854,
        "position": 42592,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 55442,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 39.473684210526315,
        "position": 56391,
        "chapter": 7
      },
      {
        "segment": 1,
        "score": 42.857142857142854,
        "position": 57788,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 31.25,
        "position": 59660,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 21.126760563380284,
        "position": 61358,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 79.64601769911503,
        "position": 63098,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 81.81818181818183,
        "position": 64884,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 42.857142857142854,
        "position": 72752,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 69.76744186046511,
        "position": 76590,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 78486,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 80265,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 60.0,
        "position": 89554,
        "chapter": 8
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 109534,
        "chapter": 9
      },
      {
        "segment": 1,
        "score": 60.0,
        "position": 114410,
        "chapter": 3
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 119975,
        "chapter": 3
      },
      {
        "segment": 1,
        "score": 69.23076923076923,
        "position": 127194,
        "chapter": 4
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 134493,
        "chapter": 4
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 136534,
        "chapter": 4
      },
      {
        "segment": 1,
        "score": 53.57142857142857,
        "position": 138362,
        "chapter": 4
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 140385,
        "chapter": 4
      },
      {
        "segment": 1,
        "score": 53.57142857142857,
        "position": 155003,
        "chapter": 10
      },
      {
        "segment": 1,
        "score": 53.57142857142857,
        "position": 159646,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 16.129032258064516,
        "position": 161747,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 53.57142857142857,
        "position": 163865,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 167103,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 75.0,
        "position": 189323,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 69.76744186046511,
        "position": 212455,
        "chapter": 6
      },
      {
        "segment": 1,
        "score": 60.0,
        "position": 258663,
        "chapter": 7
      },
      {
        "segment": 1,
        "score": 53.57142857142857,
        "position": 272319,
        "chapter": 8
      },
      {
        "segment": 1,
        "score": 53.57142857142857,
        "position": 280261,
        "chapter": 8
      },
      {
        "segment": 1,
        "score": 53.57142857142857,
        "position": 285618,
        "chapter": 8
      },
      {
        "segment": 1,
        "score": 56.60377358490566,
        "position": 287522,
        "chapter": 8
      }
    ],
    "arte": [
      {
        "segment": 1,
        "score": 100.0,
        "position": 11960,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 14410,
        "chapter": 11
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 17330,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 19218,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 29426,
        "chapter": 6
      },
      {
        "segment": 1,
        "score": 43.47826086956522,
        "position": 31035,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 34852,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 36535,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 57.14285714285714,
        "position": 42592,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 44260,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 26.31578947368421,
        "position": 56391,
        "chapter": 7
      },
      {
        "segment": 1,
        "score": 57.14285714285714,
        "position": 57788,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 41.66666666666667,
        "position": 59660,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 28.169014084507044,
        "position": 61358,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 8.849557522123893,
        "position": 63098,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 18.181818181818183,
        "position": 64884,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 66864,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 68901,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 71125,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 57.14285714285714,
        "position": 72752,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 87945,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 40.0,
        "position": 89554,
        "chapter": 8
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 92994,
        "chapter": 3
      },
      {
        "segment": 1,
        "score": 46.51162790697674,
        "position": 94653,
        "chapter": 3
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 96434,
        "chapter": 3
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 102509,
        "chapter": 9
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 106446,
        "chapter": 3
      },
      {
        "segment": 1,
        "score": 40.0,
        "position": 114410,
        "chapter": 3
      },
      {
        "segment": 1,
        "score": 60.60606060606061,
        "position": 121456,
        "chapter": 3
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 123209,
        "chapter": 3
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 125403,
        "chapter": 4
      },
      {
        "segment": 1,
        "score": 30.76923076923077,
        "position": 127194,
        "chapter": 4
      },
      {
        "segment": 1,
        "score": 27.77777777777778,
        "position": 145860,
        "chapter": 4
      },
      {
        "segment": 1,
        "score": 43.47826086956522,
        "position": 149630,
        "chapter": 4
      },
      {
        "segment": 1,
        "score": 27.77777777777778,
        "position": 151542,
        "chapter": 4
      },
      {
        "segment": 1,
        "score": 13.333333333333334,
        "position": 176370,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 46.51162790697674,
        "position": 178473,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 30.303030303030305,
        "position": 180193,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 25.0,
        "position": 189323,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 27.77777777777778,
        "position": 194542,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 46.51162790697674,
        "position": 201116,
        "chapter": 12
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 202651,
        "chapter": 6
      },
      {
        "segment": 1,
        "score": 30.303030303030305,
        "position": 204771,
        "chapter": 6
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 206371,
        "chapter": 6
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 208556,
        "chapter": 6
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 217418,
        "chapter": 6
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 219244,
        "chapter": 6
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 221108,
        "chapter": 6
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 223065,
        "chapter": 6
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 225040,
        "chapter": 6
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 227218,
        "chapter": 6
      },
      {
        "segment": 1,
        "score": 40.0,
        "position": 258663,
        "chapter": 7
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 260475,
        "chapter": 7
      },
      {
        "segment": 1,
        "score": 43.47826086956522,
        "position": 267568,
        "chapter": 7
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 269266,
        "chapter": 8
      }
    ],
    "historia": [
      {
        "segment": 1,
        "score": 43.47826086956522,
        "position": 110986,
        "chapter": 3
      },
      {
        "segment": 1,
        "score": 30.303030303030305,
        "position": 180193,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 196667,
        "chapter": 6
      }
    ]
  },
  "difficulty_map": [
    {
      "segment": 1,
      "difficulty": 20.5,
      "position": 113,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 27,
      "preservation_score": 8.74846531394367e-08
    },
    {
      "segment": 1,
      "difficulty": 20.586666666666666,
      "position": 422,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 20,
      "preservation_score": 0.0
    },
    {
      "segment": 1,
      "difficulty": 21.147727272727273,
      "position": 691,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 33,
      "preservation_score": 1.749693062788734e-07
    },
    {
      "segment": 1,
      "difficulty": 21.189473684210526,
      "position": 1041,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 76,
      "preservation_score": 1.8371777159281706e-06
    },
    {
      "segment": 1,
      "difficulty": 29.452707440592132,
      "position": 1673,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 302,
      "preservation_score": 1.3742380930653183e-05
    },
    {
      "segment": 1,
      "difficulty": 28.756315789473682,
      "position": 3606,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 285,
      "preservation_score": 1.564517213643593e-05
    },
    {
      "segment": 1,
      "difficulty": 26.70544871794872,
      "position": 5459,
      "chapter": 1,
      "main_theme": "ciencia",
      "word_count": 312,
      "preservation_score": 1.3108117195392265e-05
    },
    {
      "segment": 1,
      "difficulty": 34.702140762463344,
      "position": 7467,
      "chapter": 1,
      "main_theme": "filosofia",
      "word_count": 310,
      "preservation_score": 1.2882115174782053e-05
    },
    {
      "segment": 1,
      "difficulty": 35.27872714486639,
      "position": 9491,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 316,
      "preservation_score": 1.672414952515565e-05
    },
    {
      "segment": 1,
      "difficulty": 21.48913043478261,
      "position": 11530,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 46,
      "preservation_score": 2.1871163284859175e-07
    },
    {
      "segment": 1,
      "difficulty": 23.97335223245925,
      "position": 11960,
      "chapter": 1,
      "main_theme": "arte",
      "word_count": 83,
      "preservation_score": 0.0004264585225037074
    },
    {
      "segment": 1,
      "difficulty": 22.8825974025974,
      "position": 14410,
      "chapter": 11,
      "main_theme": "arte",
      "word_count": 35,
      "preservation_score": 2.752850418787608e-05
    },
    {
      "segment": 1,
      "difficulty": 28.681818181818183,
      "position": 15248,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 264,
      "preservation_score": 1.1810428173823954e-05
    },
    {
      "segment": 1,
      "difficulty": 20.91449275362319,
      "position": 17051,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 23,
      "preservation_score": 5.8323102092957795e-08
    },
    {
      "segment": 1,
      "difficulty": 33.090770901194354,
      "position": 17330,
      "chapter": 2,
      "main_theme": "arte",
      "word_count": 307,
      "preservation_score": 1.061480458091832e-05
    },
    {
      "segment": 1,
      "difficulty": 34.82439427312775,
      "position": 19218,
      "chapter": 1,
      "main_theme": "arte",
      "word_count": 227,
      "preservation_score": 6.415541230225359e-06
    },
    {
      "segment": 1,
      "difficulty": 36.4052,
      "position": 20729,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 250,
      "preservation_score": 7.348710863712682e-06
    },
    {
      "segment": 1,
      "difficulty": 20.91449275362319,
      "position": 22287,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 23,
      "preservation_score": 5.8323102092957795e-08
    },
    {
      "segment": 1,
      "difficulty": 33.356654888103655,
      "position": 22566,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 283,
      "preservation_score": 1.1227197152894378e-05
    },
    {
      "segment": 1,
      "difficulty": 20.664655172413795,
      "position": 24429,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 29,
      "preservation_score": 8.019426537781696e-08
    },
    {
      "segment": 1,
      "difficulty": 25.910673546985333,
      "position": 24753,
      "chapter": 5,
      "main_theme": "filosofia",
      "word_count": 263,
      "preservation_score": 1.1219906765132756e-05
    },
    {
      "segment": 1,
      "difficulty": 33.044782140935986,
      "position": 26420,
      "chapter": 1,
      "main_theme": "filosofia",
      "word_count": 338,
      "preservation_score": 1.3560121236612687e-05
    },
    {
      "segment": 1,
      "difficulty": 24.21666666666667,
      "position": 28466,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 90,
      "preservation_score": 9.185888579640854e-07
    },
    {
      "segment": 1,
      "difficulty": 20.91449275362319,
      "position": 29147,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 23,
      "preservation_score": 5.8323102092957795e-08
    },
    {
      "segment": 1,
      "difficulty": 29.564444444444444,
      "position": 29426,
      "chapter": 6,
      "main_theme": "arte",
      "word_count": 230,
      "preservation_score": 1.0235704417314092e-05
    },
    {
      "segment": 1,
      "difficulty": 26.36360544217687,
      "position": 31035,
      "chapter": 1,
      "main_theme": "ciencia",
      "word_count": 294,
      "preservation_score": 1.458806591100107e-05
    },
    {
      "segment": 1,
      "difficulty": 31.12991169977925,
      "position": 32937,
      "chapter": 1,
      "main_theme": "filosofia",
      "word_count": 302,
      "preservation_score": 1.2896695950305296e-05
    },
    {
      "segment": 1,
      "difficulty": 23.188498098859313,
      "position": 34852,
      "chapter": 1,
      "main_theme": "arte",
      "word_count": 263,
      "preservation_score": 1.0425254499116206e-05
    },
    {
      "segment": 1,
      "difficulty": 34.27589098532495,
      "position": 36535,
      "chapter": 1,
      "main_theme": "arte",
      "word_count": 318,
      "preservation_score": 1.0848096989290151e-05
    },
    {
      "segment": 1,
      "difficulty": 45.06435331230284,
      "position": 38583,
      "chapter": 1,
      "main_theme": "filosofia",
      "word_count": 317,
      "preservation_score": 1.1752105071730996e-05
    },
    {
      "segment": 1,
      "difficulty": 39.40981012658228,
      "position": 40604,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 316,
      "preservation_score": 1.3778832869461282e-05
    },
    {
      "segment": 1,
      "difficulty": 35.303530689842475,
      "position": 42592,
      "chapter": 1,
      "main_theme": "arte",
      "word_count": 263,
      "preservation_score": 8.529753681095077e-06
    },
    {
      "segment": 1,
      "difficulty": 22.741922946941536,
      "position": 44260,
      "chapter": 1,
      "main_theme": "arte",
      "word_count": 269,
      "preservation_score": 1.220410911295142e-05
    },
    {
      "segment": 1,
      "difficulty": 23.919344308827704,
      "position": 45963,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 271,
      "preservation_score": 1.061480458091832e-05
    },
    {
      "segment": 1,
      "difficulty": 24.182284541723668,
      "position": 47745,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 258,
      "preservation_score": 9.448342539059164e-06
    },
    {
      "segment": 1,
      "difficulty": 25.0640522875817,
      "position": 49433,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 306,
      "preservation_score": 1.1839589724870433e-05
    },
    {
      "segment": 1,
      "difficulty": 24.622511724856697,
      "position": 51363,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 303,
      "preservation_score": 1.4216256135158465e-05
    },
    {
      "segment": 1,
      "difficulty": 29.293478260869566,
      "position": 53370,
      "chapter": 1,
      "main_theme": "ciencia",
      "word_count": 322,
      "preservation_score": 1.2882115174782053e-05
    },
    {
      "segment": 1,
      "difficulty": 26.051136363636363,
      "position": 55442,
      "chapter": 1,
      "main_theme": "filosofia",
      "word_count": 88,
      "preservation_score": 9.696215722954234e-07
    },
    {
      "segment": 1,
      "difficulty": 20.91449275362319,
      "position": 56112,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 23,
      "preservation_score": 5.8323102092957795e-08
    },
    {
      "segment": 1,
      "difficulty": 25.854020100502513,
      "position": 56391,
      "chapter": 7,
      "main_theme": "filosofia",
      "word_count": 199,
      "preservation_score": 7.217483884003528e-06
    },
    {
      "segment": 1,
      "difficulty": 25.29798136645963,
      "position": 57788,
      "chapter": 2,
      "main_theme": "arte",
      "word_count": 276,
      "preservation_score": 1.1839589724870433e-05
    },
    {
      "segment": 1,
      "difficulty": 22.405450923578414,
      "position": 59660,
      "chapter": 2,
      "main_theme": "arte",
      "word_count": 251,
      "preservation_score": 1.2131205235335221e-05
    },
    {
      "segment": 1,
      "difficulty": 24.87590909090909,
      "position": 61358,
      "chapter": 2,
      "main_theme": "ciencia",
      "word_count": 264,
      "preservation_score": 1.4172513808588745e-05
    },
    {
      "segment": 1,
      "difficulty": 26.902478632478633,
      "position": 63098,
      "chapter": 2,
      "main_theme": "filosofia",
      "word_count": 260,
      "preservation_score": 1.0046154335511981e-05
    },
    {
      "segment": 1,
      "difficulty": 21.704666666666668,
      "position": 64884,
      "chapter": 2,
      "main_theme": "filosofia",
      "word_count": 300,
      "preservation_score": 1.5433750891348957e-05
    },
    {
      "segment": 1,
      "difficulty": 22.91193548387097,
      "position": 66864,
      "chapter": 2,
      "main_theme": "arte",
      "word_count": 310,
      "preservation_score": 1.4916133360273956e-05
    },
    {
      "segment": 1,
      "difficulty": 25.265938410320434,
      "position": 68901,
      "chapter": 2,
      "main_theme": "arte",
      "word_count": 356,
      "preservation_score": 1.563059136091269e-05
    },
    {
      "segment": 1,
      "difficulty": 23.133453784709015,
      "position": 71125,
      "chapter": 2,
      "main_theme": "arte",
      "word_count": 239,
      "preservation_score": 1.1562554989928884e-05
    },
    {
      "segment": 1,
      "difficulty": 21.935451505016722,
      "position": 72752,
      "chapter": 2,
      "main_theme": "arte",
      "word_count": 276,
      "preservation_score": 1.1613587704260222e-05
    },
    {
      "segment": 1,
      "difficulty": 28.269893048128342,
      "position": 74525,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 330,
      "preservation_score": 1.2656113154171841e-05
    },
    {
      "segment": 1,
      "difficulty": 27.753969869706843,
      "position": 76590,
      "chapter": 2,
      "main_theme": "filosofia",
      "word_count": 307,
      "preservation_score": 1.115429327527818e-05
    },
    {
      "segment": 1,
      "difficulty": 26.67919708029197,
      "position": 78486,
      "chapter": 2,
      "main_theme": "filosofia",
      "word_count": 274,
      "preservation_score": 1.1431328010219729e-05
    },
    {
      "segment": 1,
      "difficulty": 28.543841642228738,
      "position": 80265,
      "chapter": 2,
      "main_theme": "filosofia",
      "word_count": 341,
      "preservation_score": 1.4012125277833111e-05
    },
    {
      "segment": 1,
      "difficulty": 26.226258992805754,
      "position": 82353,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 278,
      "preservation_score": 1.1839589724870433e-05
    },
    {
      "segment": 1,
      "difficulty": 28.203125,
      "position": 84141,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 288,
      "preservation_score": 1.2451982296846492e-05
    },
    {
      "segment": 1,
      "difficulty": 26.85200868621064,
      "position": 85978,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 307,
      "preservation_score": 1.3108117195392267e-05
    },
    {
      "segment": 1,
      "difficulty": 25.032941176470587,
      "position": 87945,
      "chapter": 2,
      "main_theme": "arte",
      "word_count": 255,
      "preservation_score": 7.69864947627043e-06
    },
    {
      "segment": 1,
      "difficulty": 24.98805418719212,
      "position": 89554,
      "chapter": 8,
      "main_theme": "filosofia",
      "word_count": 232,
      "preservation_score": 8.383945925862683e-06
    },
    {
      "segment": 1,
      "difficulty": 29.380196399345337,
      "position": 91126,
      "chapter": 3,
      "main_theme": "ciencia",
      "word_count": 282,
      "preservation_score": 1.2051010969957405e-05
    },
    {
      "segment": 1,
      "difficulty": 24.02426948051948,
      "position": 92994,
      "chapter": 3,
      "main_theme": "arte",
      "word_count": 231,
      "preservation_score": 1.1941655153533109e-05
    },
    {
      "segment": 1,
      "difficulty": 23.518454545454546,
      "position": 94653,
      "chapter": 3,
      "main_theme": "arte",
      "word_count": 275,
      "preservation_score": 1.0002412008942265e-05
    },
    {
      "segment": 1,
      "difficulty": 27.376490528414756,
      "position": 96434,
      "chapter": 3,
      "main_theme": "arte",
      "word_count": 295,
      "preservation_score": 1.2685274705218321e-05
    },
    {
      "segment": 1,
      "difficulty": 29.96656346749226,
      "position": 98424,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 323,
      "preservation_score": 1.4464129319053534e-05
    },
    {
      "segment": 1,
      "difficulty": 36.66645962732919,
      "position": 100470,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 322,
      "preservation_score": 1.2882115174782053e-05
    },
    {
      "segment": 1,
      "difficulty": 29.45448717948718,
      "position": 102509,
      "chapter": 9,
      "main_theme": "arte",
      "word_count": 312,
      "preservation_score": 1.2896695950305296e-05
    },
    {
      "segment": 1,
      "difficulty": 24.496904761904762,
      "position": 104391,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 315,
      "preservation_score": 1.2247851439521137e-05
    },
    {
      "segment": 1,
      "difficulty": 28.511666666666667,
      "position": 106446,
      "chapter": 3,
      "main_theme": "arte",
      "word_count": 300,
      "preservation_score": 1.5309814299401422e-05
    },
    {
      "segment": 1,
      "difficulty": 33.137499999999996,
      "position": 108333,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 144,
      "preservation_score": 1.9246623690676078e-06
    },
    {
      "segment": 1,
      "difficulty": 20.91449275362319,
      "position": 109255,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 23,
      "preservation_score": 5.8323102092957795e-08
    },
    {
      "segment": 1,
      "difficulty": 35.17807017543859,
      "position": 109534,
      "chapter": 9,
      "main_theme": "filosofia",
      "word_count": 209,
      "preservation_score": 6.036441066621133e-06
    },
    {
      "segment": 1,
      "difficulty": 30.453396029258098,
      "position": 110986,
      "chapter": 3,
      "main_theme": "ciencia",
      "word_count": 261,
      "preservation_score": 8.369365150339445e-06
    },
    {
      "segment": 1,
      "difficulty": 28.54089180781196,
      "position": 112694,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 263,
      "preservation_score": 8.777626864990149e-06
    },
    {
      "segment": 1,
      "difficulty": 26.71333333333333,
      "position": 114410,
      "chapter": 3,
      "main_theme": "filosofia",
      "word_count": 270,
      "preservation_score": 9.302534783826768e-06
    },
    {
      "segment": 1,
      "difficulty": 24.24740470397405,
      "position": 116243,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 274,
      "preservation_score": 8.981757722315501e-06
    },
    {
      "segment": 1,
      "difficulty": 27.04629049111808,
      "position": 118051,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 319,
      "preservation_score": 1.32685057261479e-05
    },
    {
      "segment": 1,
      "difficulty": 21.77774703557312,
      "position": 119975,
      "chapter": 3,
      "main_theme": "filosofia",
      "word_count": 230,
      "preservation_score": 8.566205619903178e-06
    },
    {
      "segment": 1,
      "difficulty": 25.791219649915302,
      "position": 121456,
      "chapter": 3,
      "main_theme": "arte",
      "word_count": 253,
      "preservation_score": 1.0038863947750362e-05
    },
    {
      "segment": 1,
      "difficulty": 28.38935574229692,
      "position": 123209,
      "chapter": 3,
      "main_theme": "arte",
      "word_count": 357,
      "preservation_score": 1.376425209393804e-05
    },
    {
      "segment": 1,
      "difficulty": 24.50095090667846,
      "position": 125403,
      "chapter": 4,
      "main_theme": "arte",
      "word_count": 266,
      "preservation_score": 1.1431328010219729e-05
    },
    {
      "segment": 1,
      "difficulty": 25.089774236387782,
      "position": 127194,
      "chapter": 4,
      "main_theme": "filosofia",
      "word_count": 251,
      "preservation_score": 9.645183008622898e-06
    },
    {
      "segment": 1,
      "difficulty": 25.29105215827338,
      "position": 128946,
      "chapter": 4,
      "main_theme": "ciencia",
      "word_count": 278,
      "preservation_score": 1.1205325989609518e-05
    },
    {
      "segment": 1,
      "difficulty": 27.295127748068925,
      "position": 130821,
      "chapter": 4,
      "main_theme": "ciencia",
      "word_count": 297,
      "preservation_score": 1.1628168479783462e-05
    },
    {
      "segment": 1,
      "difficulty": 24.79347985347985,
      "position": 132747,
      "chapter": 4,
      "main_theme": "ciencia",
      "word_count": 260,
      "preservation_score": 9.667054171907756e-06
    },
    {
      "segment": 1,
      "difficulty": 28.097,
      "position": 134493,
      "chapter": 4,
      "main_theme": "filosofia",
      "word_count": 300,
      "preservation_score": 1.1074099009900364e-05
    },
    {
      "segment": 1,
      "difficulty": 25.645555555555553,
      "position": 136534,
      "chapter": 4,
      "main_theme": "filosofia",
      "word_count": 270,
      "preservation_score": 1.0818935438243673e-05
    },
    {
      "segment": 1,
      "difficulty": 36.524755700325734,
      "position": 138362,
      "chapter": 4,
      "main_theme": "filosofia",
      "word_count": 307,
      "preservation_score": 1.246656307236973e-05
    },
    {
      "segment": 1,
      "difficulty": 31.74303605313093,
      "position": 140385,
      "chapter": 4,
      "main_theme": "filosofia",
      "word_count": 310,
      "preservation_score": 1.6068014626609876e-05
    },
    {
      "segment": 1,
      "difficulty": 32.07140221402214,
      "position": 142394,
      "chapter": 4,
      "main_theme": "ciencia",
      "word_count": 271,
      "preservation_score": 8.267299721676767e-06
    },
    {
      "segment": 1,
      "difficulty": 23.950000000000003,
      "position": 144092,
      "chapter": 4,
      "main_theme": "ciencia",
      "word_count": 264,
      "preservation_score": 1.1839589724870433e-05
    },
    {
      "segment": 1,
      "difficulty": 34.13793847814355,
      "position": 145860,
      "chapter": 4,
      "main_theme": "ciencia",
      "word_count": 327,
      "preservation_score": 1.1752105071730996e-05
    },
    {
      "segment": 1,
      "difficulty": 24.006945428773918,
      "position": 147921,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 249,
      "preservation_score": 1.0432544886877827e-05
    },
    {
      "segment": 1,
      "difficulty": 24.782879818594104,
      "position": 149630,
      "chapter": 4,
      "main_theme": "ciencia",
      "word_count": 294,
      "preservation_score": 1.0148219764174657e-05
    },
    {
      "segment": 1,
      "difficulty": 24.74249249249249,
      "position": 151542,
      "chapter": 4,
      "main_theme": "ciencia",
      "word_count": 296,
      "preservation_score": 1.1628168479783462e-05
    },
    {
      "segment": 1,
      "difficulty": 26.88726726726727,
      "position": 153482,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 185,
      "preservation_score": 5.205336861796483e-06
    },
    {
      "segment": 1,
      "difficulty": 20.91449275362319,
      "position": 154724,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 23,
      "preservation_score": 5.8323102092957795e-08
    },
    {
      "segment": 1,
      "difficulty": 27.02285714285714,
      "position": 155003,
      "chapter": 10,
      "main_theme": "filosofia",
      "word_count": 245,
      "preservation_score": 1.2043720582195786e-05
    },
    {
      "segment": 1,
      "difficulty": 26.76273726273726,
      "position": 156791,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 143,
      "preservation_score": 2.1871163284859175e-06
    },
    {
      "segment": 1,
      "difficulty": 25.50233540925267,
      "position": 157732,
      "chapter": 11,
      "main_theme": "none",
      "word_count": 281,
      "preservation_score": 1.2896695950305296e-05
    },
    {
      "segment": 1,
      "difficulty": 33.44842252396166,
      "position": 159646,
      "chapter": 5,
      "main_theme": "filosofia",
      "word_count": 313,
      "preservation_score": 2.6464107574679605e-05
    },
    {
      "segment": 1,
      "difficulty": 34.17310126582279,
      "position": 161747,
      "chapter": 5,
      "main_theme": "ciencia",
      "word_count": 316,
      "preservation_score": 1.3108117195392265e-05
    },
    {
      "segment": 1,
      "difficulty": 24.487428571428573,
      "position": 163865,
      "chapter": 5,
      "main_theme": "filosofia",
      "word_count": 225,
      "preservation_score": 7.202903108480288e-06
    },
    {
      "segment": 1,
      "difficulty": 26.413333333333334,
      "position": 165284,
      "chapter": 5,
      "main_theme": "ciencia",
      "word_count": 270,
      "preservation_score": 1.1227197152894378e-05
    },
    {
      "segment": 1,
      "difficulty": 23.25931330472103,
      "position": 167103,
      "chapter": 5,
      "main_theme": "filosofia",
      "word_count": 233,
      "preservation_score": 8.383945925862683e-06
    },
    {
      "segment": 1,
      "difficulty": 33.32905268490374,
      "position": 168653,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 329,
      "preservation_score": 1.376425209393804e-05
    },
    {
      "segment": 1,
      "difficulty": 27.37512899896801,
      "position": 170814,
      "chapter": 5,
      "main_theme": "ciencia",
      "word_count": 323,
      "preservation_score": 1.0396092948069726e-05
    },
    {
      "segment": 1,
      "difficulty": 24.277837089758798,
      "position": 172945,
      "chapter": 5,
      "main_theme": "ciencia",
      "word_count": 281,
      "preservation_score": 1.0002412008942265e-05
    },
    {
      "segment": 1,
      "difficulty": 22.455712769720552,
      "position": 174691,
      "chapter": 5,
      "main_theme": "ciencia",
      "word_count": 257,
      "preservation_score": 1.1023066295569023e-05
    },
    {
      "segment": 1,
      "difficulty": 39.98443665867601,
      "position": 176370,
      "chapter": 5,
      "main_theme": "ciencia",
      "word_count": 319,
      "preservation_score": 1.2656113154171841e-05
    },
    {
      "segment": 1,
      "difficulty": 28.23359073359073,
      "position": 178473,
      "chapter": 5,
      "main_theme": "arte",
      "word_count": 259,
      "preservation_score": 8.981757722315501e-06
    },
    {
      "segment": 1,
      "difficulty": 28.1395738481151,
      "position": 180193,
      "chapter": 5,
      "main_theme": "ciencia",
      "word_count": 289,
      "preservation_score": 1.3472636583473252e-05
    },
    {
      "segment": 1,
      "difficulty": 42.965384615384615,
      "position": 182020,
      "chapter": 5,
      "main_theme": "ciencia",
      "word_count": 338,
      "preservation_score": 1.0170090927459515e-05
    },
    {
      "segment": 1,
      "difficulty": 24.608925097276263,
      "position": 184158,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 257,
      "preservation_score": 1.2007268643387689e-05
    },
    {
      "segment": 1,
      "difficulty": 25.48278911564626,
      "position": 185848,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 245,
      "preservation_score": 8.070459252113036e-06
    },
    {
      "segment": 1,
      "difficulty": 25.357978723404255,
      "position": 187510,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 282,
      "preservation_score": 1.061480458091832e-05
    },
    {
      "segment": 1,
      "difficulty": 22.868237704918034,
      "position": 189323,
      "chapter": 5,
      "main_theme": "filosofia",
      "word_count": 244,
      "preservation_score": 7.348710863712683e-06
    },
    {
      "segment": 1,
      "difficulty": 26.983946078431373,
      "position": 190800,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 306,
      "preservation_score": 1.4376644665914097e-05
    },
    {
      "segment": 1,
      "difficulty": 26.35433789954338,
      "position": 192663,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 292,
      "preservation_score": 1.2896695950305296e-05
    },
    {
      "segment": 1,
      "difficulty": 37.769000000000005,
      "position": 194542,
      "chapter": 5,
      "main_theme": "ciencia",
      "word_count": 325,
      "preservation_score": 1.0731450785104233e-05
    },
    {
      "segment": 1,
      "difficulty": 36.6964406779661,
      "position": 196667,
      "chapter": 6,
      "main_theme": "historia",
      "word_count": 295,
      "preservation_score": 1.0622094968679941e-05
    },
    {
      "segment": 1,
      "difficulty": 29.031980056980057,
      "position": 198608,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 324,
      "preservation_score": 1.672414952515565e-05
    },
    {
      "segment": 1,
      "difficulty": 23.03,
      "position": 200687,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 50,
      "preservation_score": 2.405827961334509e-07
    },
    {
      "segment": 1,
      "difficulty": 23.42864782276547,
      "position": 201116,
      "chapter": 12,
      "main_theme": "arte",
      "word_count": 231,
      "preservation_score": 1.0024283172227121e-05
    },
    {
      "segment": 1,
      "difficulty": 31.142471590909093,
      "position": 202651,
      "chapter": 6,
      "main_theme": "arte",
      "word_count": 320,
      "preservation_score": 1.3334119216002477e-05
    },
    {
      "segment": 1,
      "difficulty": 29.245535714285715,
      "position": 204771,
      "chapter": 6,
      "main_theme": "ciencia",
      "word_count": 240,
      "preservation_score": 1.137300490812677e-05
    },
    {
      "segment": 1,
      "difficulty": 33.92867547882385,
      "position": 206371,
      "chapter": 6,
      "main_theme": "arte",
      "word_count": 337,
      "preservation_score": 1.2597790052078883e-05
    },
    {
      "segment": 1,
      "difficulty": 25.89265944645006,
      "position": 208556,
      "chapter": 6,
      "main_theme": "arte",
      "word_count": 277,
      "preservation_score": 1.1839589724870433e-05
    },
    {
      "segment": 1,
      "difficulty": 26.18544517504887,
      "position": 210385,
      "chapter": 6,
      "main_theme": "ciencia",
      "word_count": 331,
      "preservation_score": 1.695015154576586e-05
    },
    {
      "segment": 1,
      "difficulty": 36.50962099125364,
      "position": 212455,
      "chapter": 6,
      "main_theme": "filosofia",
      "word_count": 343,
      "preservation_score": 1.0731450785104233e-05
    },
    {
      "segment": 1,
      "difficulty": 26.202802359882007,
      "position": 214670,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 113,
      "preservation_score": 2.332924083718312e-06
    },
    {
      "segment": 1,
      "difficulty": 38.594904181184674,
      "position": 215521,
      "chapter": 13,
      "main_theme": "none",
      "word_count": 287,
      "preservation_score": 1.0818935438243673e-05
    },
    {
      "segment": 1,
      "difficulty": 32.8602787456446,
      "position": 217418,
      "chapter": 6,
      "main_theme": "arte",
      "word_count": 287,
      "preservation_score": 1.1227197152894378e-05
    },
    {
      "segment": 1,
      "difficulty": 24.887686274509804,
      "position": 219244,
      "chapter": 6,
      "main_theme": "arte",
      "word_count": 300,
      "preservation_score": 1.2262432215044376e-05
    },
    {
      "segment": 1,
      "difficulty": 31.31452380952381,
      "position": 221108,
      "chapter": 6,
      "main_theme": "arte",
      "word_count": 315,
      "preservation_score": 1.1591716540975364e-05
    },
    {
      "segment": 1,
      "difficulty": 33.913430420711975,
      "position": 223065,
      "chapter": 6,
      "main_theme": "arte",
      "word_count": 309,
      "preservation_score": 1.1591716540975364e-05
    },
    {
      "segment": 1,
      "difficulty": 44.4702183121538,
      "position": 225040,
      "chapter": 6,
      "main_theme": "arte",
      "word_count": 341,
      "preservation_score": 1.4930714135797195e-05
    },
    {
      "segment": 1,
      "difficulty": 27.38515037593985,
      "position": 227218,
      "chapter": 6,
      "main_theme": "arte",
      "word_count": 304,
      "preservation_score": 1.6840795729341564e-05
    },
    {
      "segment": 1,
      "difficulty": 33.79638157894737,
      "position": 229142,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 304,
      "preservation_score": 1.3786123257222901e-05
    },
    {
      "segment": 1,
      "difficulty": 24.938032786885245,
      "position": 231154,
      "chapter": 6,
      "main_theme": "ciencia",
      "word_count": 305,
      "preservation_score": 1.4165223420827126e-05
    },
    {
      "segment": 1,
      "difficulty": 31.39560327198364,
      "position": 233070,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 326,
      "preservation_score": 1.268527470521832e-05
    },
    {
      "segment": 1,
      "difficulty": 35.03885077186964,
      "position": 235130,
      "chapter": 7,
      "main_theme": "ciencia",
      "word_count": 318,
      "preservation_score": 1.2882115174782053e-05
    },
    {
      "segment": 1,
      "difficulty": 24.34410480349345,
      "position": 237176,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 229,
      "preservation_score": 1.0235704417314092e-05
    },
    {
      "segment": 1,
      "difficulty": 20.845360339142722,
      "position": 238796,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 193,
      "preservation_score": 6.736318291736626e-06
    },
    {
      "segment": 1,
      "difficulty": 30.65714285714286,
      "position": 240056,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 199,
      "preservation_score": 4.571073126535567e-06
    },
    {
      "segment": 1,
      "difficulty": 29.669522314420274,
      "position": 241371,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 343,
      "preservation_score": 1.4690131339663746e-05
    },
    {
      "segment": 1,
      "difficulty": 30.226219512195122,
      "position": 243463,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 328,
      "preservation_score": 1.58201414427148e-05
    },
    {
      "segment": 1,
      "difficulty": 28.950184246890835,
      "position": 245548,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 334,
      "preservation_score": 1.2656113154171841e-05
    },
    {
      "segment": 1,
      "difficulty": 27.483206106870227,
      "position": 247576,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 262,
      "preservation_score": 9.842023478186629e-06
    },
    {
      "segment": 1,
      "difficulty": 29.870060437006046,
      "position": 249251,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 239,
      "preservation_score": 7.676778312985571e-06
    },
    {
      "segment": 1,
      "difficulty": 39.90310734463277,
      "position": 250808,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 354,
      "preservation_score": 3.0750855578512005e-05
    },
    {
      "segment": 1,
      "difficulty": 27.242100909842847,
      "position": 252920,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 279,
      "preservation_score": 1.0206542866267617e-05
    },
    {
      "segment": 1,
      "difficulty": 28.524087426768816,
      "position": 254674,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 317,
      "preservation_score": 1.4653679400855648e-05
    },
    {
      "segment": 1,
      "difficulty": 27.55350547195622,
      "position": 256596,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 344,
      "preservation_score": 1.4690131339663746e-05
    },
    {
      "segment": 1,
      "difficulty": 27.89217715231788,
      "position": 258663,
      "chapter": 7,
      "main_theme": "filosofia",
      "word_count": 302,
      "preservation_score": 1.2262432215044376e-05
    },
    {
      "segment": 1,
      "difficulty": 29.71795665634675,
      "position": 260475,
      "chapter": 7,
      "main_theme": "arte",
      "word_count": 323,
      "preservation_score": 1.6272145483935225e-05
    },
    {
      "segment": 1,
      "difficulty": 24.115151515151517,
      "position": 262592,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 264,
      "preservation_score": 1.2262432215044376e-05
    },
    {
      "segment": 1,
      "difficulty": 32.82895393691854,
      "position": 264317,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 339,
      "preservation_score": 1.539729895254086e-05
    },
    {
      "segment": 1,
      "difficulty": 27.724675324675324,
      "position": 266469,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 154,
      "preservation_score": 3.936809391274651e-06
    },
    {
      "segment": 1,
      "difficulty": 28.669453450671604,
      "position": 267568,
      "chapter": 7,
      "main_theme": "ciencia",
      "word_count": 254,
      "preservation_score": 1.1839589724870433e-05
    },
    {
      "segment": 1,
      "difficulty": 26.922635135135135,
      "position": 269266,
      "chapter": 8,
      "main_theme": "arte",
      "word_count": 296,
      "preservation_score": 1.2903986338066913e-05
    },
    {
      "segment": 1,
      "difficulty": 30.722970639032813,
      "position": 271104,
      "chapter": 8,
      "main_theme": "ciencia",
      "word_count": 193,
      "preservation_score": 3.594161166478524e-06
    },
    {
      "segment": 1,
      "difficulty": 39.369278996865205,
      "position": 272319,
      "chapter": 8,
      "main_theme": "filosofia",
      "word_count": 319,
      "preservation_score": 1.0935581642429588e-05
    },
    {
      "segment": 1,
      "difficulty": 36.12857142857143,
      "position": 274206,
      "chapter": 8,
      "main_theme": "none",
      "word_count": 168,
      "preservation_score": 2.5516357165669033e-06
    },
    {
      "segment": 1,
      "difficulty": 26.021339347675227,
      "position": 275137,
      "chapter": 8,
      "main_theme": "none",
      "word_count": 262,
      "preservation_score": 9.251502069495433e-06
    },
    {
      "segment": 1,
      "difficulty": 20.185625,
      "position": 276577,
      "chapter": 8,
      "main_theme": "none",
      "word_count": 160,
      "preservation_score": 8.20168623182219e-06
    },
    {
      "segment": 1,
      "difficulty": 27.285328638497653,
      "position": 277681,
      "chapter": 8,
      "main_theme": "ciencia",
      "word_count": 284,
      "preservation_score": 1.061480458091832e-05
    },
    {
      "segment": 1,
      "difficulty": 22.563157894736843,
      "position": 279372,
      "chapter": 8,
      "main_theme": "none",
      "word_count": 57,
      "preservation_score": 4.374232656971835e-07
    },
    {
      "segment": 1,
      "difficulty": 21.823684210526316,
      "position": 279868,
      "chapter": 8,
      "main_theme": "none",
      "word_count": 38,
      "preservation_score": 1.9684046956373255e-07
    },
    {
      "segment": 1,
      "difficulty": 29.919871794871796,
      "position": 280261,
      "chapter": 8,
      "main_theme": "filosofia",
      "word_count": 273,
      "preservation_score": 1.141674723469649e-05
    },
    {
      "segment": 1,
      "difficulty": 29.76766917293233,
      "position": 282004,
      "chapter": 8,
      "main_theme": "none",
      "word_count": 133,
      "preservation_score": 6.036441066621133e-06
    },
    {
      "segment": 1,
      "difficulty": 27.493034825870648,
      "position": 282826,
      "chapter": 8,
      "main_theme": "none",
      "word_count": 201,
      "preservation_score": 3.3681591458683127e-06
    },
    {
      "segment": 1,
      "difficulty": 29.48390410958904,
      "position": 283777,
      "chapter": 8,
      "main_theme": "none",
      "word_count": 292,
      "preservation_score": 9.842023478186629e-06
    },
    {
      "segment": 1,
      "difficulty": 29.014576365663324,
      "position": 285618,
      "chapter": 8,
      "main_theme": "filosofia",
      "word_count": 299,
      "preservation_score": 1.5433750891348957e-05
    },
    {
      "segment": 1,
      "difficulty": 35.187767584097855,
      "position": 287522,
      "chapter": 8,
      "main_theme": "filosofia",
      "word_count": 327,
      "preservation_score": 1.7176153566376073e-05
    },
    {
      "segment": 1,
      "difficulty": 23.255384615384614,
      "position": 289630,
      "chapter": 8,
      "main_theme": "none",
      "word_count": 65,
      "preservation_score": 5.467790821214793e-07
    },
    {
      "segment": 1,
      "difficulty": 20.953623188405796,
      "position": 290157,
      "chapter": 8,
      "main_theme": "none",
      "word_count": 23,
      "preservation_score": 5.8323102092957795e-08
    },
    {
      "segment": 1,
      "difficulty": 32.15615501519757,
      "position": 290440,
      "chapter": 8,
      "main_theme": "ciencia",
      "word_count": 329,
      "preservation_score": 1.640337246364438e-05
    },
    {
      "segment": 1,
      "difficulty": 25.17310924369748,
      "position": 292495,
      "chapter": 8,
      "main_theme": "none",
      "word_count": 119,
      "preservation_score": 1.6038853075563393e-06
    },
    {
      "segment": 1,
      "difficulty": 20.64666666666667,
      "position": 293350,
      "chapter": 8,
      "main_theme": "none",
      "word_count": 20,
      "preservation_score": 0.0
    },
    {
      "segment": 1,
      "difficulty": 21.561486486486487,
      "position": 293625,
      "chapter": 9,
      "main_theme": "none",
      "word_count": 37,
      "preservation_score": 2.0413085732535226e-07
    }
  ],
  "segments": [
    {
      "id": 1,
      "text": "Caos do passado sendo \\nvívido no futuro\\ncaos do passado sendo vivido no futuro editável.indd   1caos do passado sendo vivido no futuro editável.indd   1 28/03/2022   14:53:3728/03/2022   14:53:37",
      "position": 113,
      "chapter": 1,
      "page": 1,
      "segment_type": "page",
      "themes": {},
      "difficulty": 20.5,
      "complexity_metrics": {
        "word_count": 27,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 9.0,
        "avg_word_length": 5.925925925925926,
        "unique_word_ratio": 0.5555555555555556,
        "avg_paragraph_length": 27.0,
        "punctuation_density": 0.2222222222222222,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "passado",
          "sendo",
          "futuro",
          "caos",
          "vivido",
          "editável",
          "indd",
          "vívido"
        ],
        "entities": [
          [
            "editável.indd",
            "CARDINAL"
          ],
          [
            "1caos",
            "CARDINAL"
          ],
          [
            "editável.indd",
            "CARDINAL"
          ],
          [
            "1",
            "CARDINAL"
          ],
          [
            "14:53:3728/03/2022   14:53:37",
            "MONEY"
          ]
        ],
        "readability_score": 93.72222222222223,
        "semantic_density": 0,
        "word_count": 27,
        "unique_words": 15,
        "lexical_diversity": 0.5555555555555556
      },
      "preservation_score": 8.74846531394367e-08
    },
    {
      "id": 1,
      "text": "caos do passado sendo vivido no futuro editável.indd   2caos do passado sendo vivido no futuro editável.indd   2 28/03/2022   14:53:3728/03/2022   14:53:37",
      "position": 422,
      "chapter": 1,
      "page": 2,
      "segment_type": "page",
      "themes": {},
      "difficulty": 20.586666666666666,
      "complexity_metrics": {
        "word_count": 20,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 6.666666666666667,
        "avg_word_length": 6.4,
        "unique_word_ratio": 0.65,
        "avg_paragraph_length": 20.0,
        "punctuation_density": 0.3,
        "line_break_count": 0,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "caos"
        ],
        "entities": [
          [
            "editável.indd",
            "CARDINAL"
          ],
          [
            "2caos",
            "CARDINAL"
          ],
          [
            "editável.indd",
            "CARDINAL"
          ],
          [
            "2",
            "CARDINAL"
          ],
          [
            "14:53:3728/03/2022   14:53:37",
            "MONEY"
          ]
        ],
        "readability_score": 94.74666666666667,
        "semantic_density": 0,
        "word_count": 20,
        "unique_words": 13,
        "lexical_diversity": 0.65
      },
      "preservation_score": 0.0
    },
    {
      "id": 1,
      "text": "Rio de Janeiro, 2022Marcelo J. Catharino\\nCaos do passado sendo \\nvívido no futuro\\ncaos do passado sendo vivido no futuro editável.indd   3caos do passado sendo vivido no futuro editável.indd   3 28/03/2022   14:53:3728/03/2022   14:53:37",
      "position": 691,
      "chapter": 1,
      "page": 3,
      "segment_type": "page",
      "themes": {},
      "difficulty": 21.147727272727273,
      "complexity_metrics": {
        "word_count": 33,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 8.25,
        "avg_word_length": 5.909090909090909,
        "unique_word_ratio": 0.6363636363636364,
        "avg_paragraph_length": 33.0,
        "punctuation_density": 0.24242424242424243,
        "line_break_count": 3,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "passado",
          "sendo",
          "futuro",
          "caos",
          "vivido",
          "editável",
          "indd",
          "janeiro",
          "catharino",
          "vívido"
        ],
        "entities": [
          [
            "Rio de Janeiro",
            "GPE"
          ],
          [
            "2022Marcelo",
            "CARDINAL"
          ],
          [
            "editável.indd",
            "CARDINAL"
          ],
          [
            "3caos",
            "CARDINAL"
          ],
          [
            "editável.indd   3",
            "CARDINAL"
          ],
          [
            "14:53:3728/03/2022   14:53:37",
            "MONEY"
          ]
        ],
        "readability_score": 94.10227272727273,
        "semantic_density": 0,
        "word_count": 33,
        "unique_words": 21,
        "lexical_diversity": 0.6363636363636364
      },
      "preservation_score": 1.749693062788734e-07
    },
    {
      "id": 1,
      "text": "Caos do passado sendo vívido no futuro\\nMarcelo Jubilado Catharino\\nisbn: \\n1ª edição, março de 2022.\\nEditora Autografía\\nRua Mairink Veiga, 6 - 10 andar - Centro\\nRio de Janeiro, RJ - CEP: 20090-050\\nwww.autografia.com.br\\nTodos os direitos reservados.  \\nProibida a reprodução deste livro  \\npara fins comerciais sem a permissão dos autores  \\ne da Autografía Editorial.\\ncaos do passado sendo vivido no futuro editável.indd   4caos do passado sendo vivido no futuro editável.indd   4 28/03/2022   14:53:3728/03/2022   14:53:37",
      "position": 1041,
      "chapter": 1,
      "page": 4,
      "segment_type": "page",
      "themes": {},
      "difficulty": 21.189473684210526,
      "complexity_metrics": {
        "word_count": 76,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 8.444444444444445,
        "avg_word_length": 5.631578947368421,
        "unique_word_ratio": 0.7763157894736842,
        "avg_paragraph_length": 76.0,
        "punctuation_density": 0.2236842105263158,
        "line_break_count": 12,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "passado",
          "sendo",
          "futuro",
          "caos",
          "autografía",
          "vivido",
          "editável",
          "indd",
          "vívido",
          "marcelo",
          "jubilado",
          "catharino",
          "isbn",
          "edição",
          "março",
          "editora",
          "mairink",
          "veiga",
          "andar",
          "centro"
        ],
        "entities": [
          [
            "Marcelo Jubilado Catharino",
            "PERSON"
          ],
          [
            "1ª",
            "CARDINAL"
          ],
          [
            "março de 2022",
            "ORG"
          ],
          [
            "Editora Autografía",
            "PERSON"
          ],
          [
            "Rua Mairink Veiga",
            "PERSON"
          ],
          [
            "6",
            "CARDINAL"
          ],
          [
            "20090",
            "CARDINAL"
          ],
          [
            "para fins",
            "PERSON"
          ],
          [
            "editável.indd   4caos",
            "QUANTITY"
          ],
          [
            "editável.indd   4",
            "CARDINAL"
          ]
        ],
        "readability_score": 94.08830409356725,
        "semantic_density": 0,
        "word_count": 76,
        "unique_words": 59,
        "lexical_diversity": 0.7763157894736842
      },
      "preservation_score": 1.8371777159281706e-06
    },
    {
      "id": 1,
      "text": "O caos do passado, sendo vívido no futuro!\\nNós humanos, não sabemos nada sobre nós mesmos, nos ques -\\ntionamos coisas as quais não há necessidade em ser questio -\\nnado, muito menos ocorrer críticas. Esses pensamentos, junto \\ncom um pouco de estudo e o estilo de vida a qual eu tenho, \\nme fizeram enxergar questionamentos bem explicativos, com \\nbastante contexto e uma visão mais humana sobre a aceitação \\nperante as situações de incômodos as quais vivemos.\\nPor que nos perguntamos quem nós somos? Por que estamos \\nvivos? Por que temos essa personalidade? Por que temos pre -\\nconceitos e pré-conceitos? São tantos porquês, que nunca con -\\nseguiremos chegar a uma satisfação de vida. \\nAntes de você começar a ler, você primeiramente tem que estar \\ncom a mente aberta, pois eu irei expor pensamentos em uma \\nvisão preconceituosa e muitas vezes extremista. \\nPara ter melhor compreensão sobre a leitura, irei explicar \\ncomo analisar.\\nEx.: uma pessoa vai para escola, aquela pessoa está aprendendo \\nportuguês, nessa aula de português, ele entendeu o contexto \\ndo tema que foi ensinado, porém ele não aprendeu e não se \\ninteressou, pois, no seu modo de ver a vida, ele não achou “im -\\nportante” dar valor àquela matéria, pois ele a achava chata, sen -\\ndo desnecessário aprender, pois o que aquilo iria acrescentar \\nem sua vida? O que aquilo iria me fazer melhor para quem eu \\namo? Nesse contexto de pensamento, vamos analisar a falta de \\ninteresse do ser humano em não querer aprender sobre si pró -\\nprio, ocorrendo o egoísmo material, o egoísmo de pensamen -\\nto, egoísmo de se sentir melhor que outros, a “necessidade” de \\nser exaltado, “necessidade de querer” mais... \\ncaos do passado sendo vivido no futuro editável.indd   5caos do passado sendo vivido no futuro editável.indd   5 28/03/2022   14:53:3728/03/2022   14:53:37",
      "position": 1673,
      "chapter": 1,
      "page": 5,
      "segment_type": "page",
      "themes": {},
      "difficulty": 29.452707440592132,
      "complexity_metrics": {
        "word_count": 302,
        "sentence_count": 17,
        "paragraph_count": 1,
        "avg_sentence_length": 17.764705882352942,
        "avg_word_length": 4.940397350993377,
        "unique_word_ratio": 0.6291390728476821,
        "avg_paragraph_length": 302.0,
        "punctuation_density": 0.16556291390728478,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "vida",
          "pois",
          "passado",
          "sendo",
          "futuro",
          "necessidade",
          "contexto",
          "melhor",
          "egoísmo",
          "caos",
          "quais",
          "pensamentos",
          "visão",
          "mais",
          "quem",
          "temos",
          "conceitos",
          "você",
          "irei",
          "analisar"
        ],
        "entities": [
          [
            "não sabemos",
            "ORG"
          ],
          [
            "nada sobre",
            "ORG"
          ],
          [
            "nós mesmos",
            "PERSON"
          ],
          [
            "muito menos",
            "PERSON"
          ],
          [
            "eu tenho",
            "PERSON"
          ],
          [
            "visão",
            "ORG"
          ],
          [
            "perguntamos quem nós somos",
            "FAC"
          ],
          [
            "Antes de você",
            "PERSON"
          ],
          [
            "pois eu irei",
            "PERSON"
          ],
          [
            "melhor compreensão",
            "FAC"
          ]
        ],
        "readability_score": 89.63552785352552,
        "semantic_density": 0,
        "word_count": 302,
        "unique_words": 190,
        "lexical_diversity": 0.6291390728476821
      },
      "preservation_score": 1.3742380930653183e-05
    },
    {
      "id": 1,
      "text": "O que é necessário para vivermos bem?\\nNós humanos tivemos um início, nesse início, criamos costu -\\nmes, criamos necessidades, criamos objetivos, metas, família, \\nquando criamos todos esses objetivos, esses sentimentos, foi \\nnecessário ter a ganância, a conquista, a ambição, o amor. Por \\nque tivemos que criar todos esses “problemas”? Pelo simples \\nfator de evolução! \\nComo seguimos em uma evolução se éramos animais irracio -\\nnais?\\nNós humanos, sentimos uma energia dos cosmos, mundo, na -\\ntureza, pessoas, religião, boa, ruim, amor, paixão, sentimento...\\nComo se foi gerada essa energia e o que isso têm haver? \\nQuando foi criado o universo e o nosso mundo, teve liberação \\nde energia, seja ela vindo do Big Bang , Deus, Ala, Buda, Odin, \\nBrahma. Então, independentemente de qual é a sua religião, \\nsua crença sobre energia, seja ela espiritual ou através de estu -\\ndo da física, temos uma concordância que a energia paira no \\nuniverso e no nosso mundo.\\nSe formos analisarmos a nossa proporção de tamanho perante \\no universo, o que nós somos? \\nEu venho respondendo essa pergunta através da física quânti -\\nca, da seguinte forma: no mundo quântico não existe tempo, a \\nenergia é uma constância, ela não se propaga relativamente ao \\ntempo, ela simplesmente existe sendo onipresente.\\nTempo não existe, tempo é a marcação da propagação da ener -\\ngia no mundo físico, nós medimos as nossas vidas, a veloci -\\ndade da luz, velocidade do som, nós sempre colocamos uma \\nmedição de tempo perante a propagação dele mesmo, nos tor -\\nnando escravos de uma regra que não tem exatidão diante das \\ncaos do passado sendo vivido no futuro editável.indd   6caos do passado sendo vivido no futuro editável.indd   6 28/03/2022   14:53:3728/03/2022   14:53:37",
      "position": 3606,
      "chapter": 1,
      "page": 6,
      "segment_type": "page",
      "themes": {},
      "difficulty": 28.756315789473682,
      "complexity_metrics": {
        "word_count": 285,
        "sentence_count": 14,
        "paragraph_count": 1,
        "avg_sentence_length": 20.357142857142858,
        "avg_word_length": 5.021052631578947,
        "unique_word_ratio": 0.631578947368421,
        "avg_paragraph_length": 285.0,
        "punctuation_density": 0.22456140350877193,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "mundo",
          "tempo",
          "criamos",
          "esses",
          "universo",
          "existe",
          "sendo",
          "necessário",
          "humanos",
          "tivemos",
          "início",
          "objetivos",
          "quando",
          "todos",
          "amor",
          "evolução",
          "como",
          "religião",
          "essa"
        ],
        "entities": [
          [
            "necessário",
            "GPE"
          ],
          [
            "para vivermos bem",
            "PERSON"
          ],
          [
            "quando",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "objetivos",
            "DATE"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "Pelo",
            "PERSON"
          ],
          [
            "éramos animais",
            "FAC"
          ],
          [
            "irracio -\\nnais",
            "PERSON"
          ]
        ],
        "readability_score": 88.3151127819549,
        "semantic_density": 0,
        "word_count": 285,
        "unique_words": 180,
        "lexical_diversity": 0.631578947368421
      },
      "preservation_score": 1.564517213643593e-05
    },
    {
      "id": 1,
      "text": "energias que não conseguimos medir por não ter tecnologia \\nou conhecimento sobre todas as energias que envolvem o nos -\\nso universo!!!\\nComo falei antes, foi gerado uma grande energia quando o \\nuniverso foi gerado e nós seres humanos somos como uma \\nantena sintonizando na rede de energias que envolve o univer -\\nso, mundo, natureza, religião, pessoas, boa, ruim, amor, paixão, \\nsentimento.\\nExemplo: se você estudar um pouco de cada religião, haverá \\numa semelhança de comportamento, histórias e sentimento \\nsemelhante em todas as religiões de seguimento da energia, \\nde necessidade perante a um contexto melhor para o mundo \\ne o universo, uma regra de viver de uma forma de se ligar ao \\nmundo e o mundo a você.\\nEssas energias são onipresentes e a nossa pessoa interpreta de \\nvárias formas de contexto diferente, uns interpretam na reli -\\ngião (Moisés, Jesus, Buda) outros na física (Tesla, Einstein), são \\nformas de recepção da energia diante de si próprio.\\nComo assim energia que está no mundo?\\nPensa na energia como ondas de energia invisível, nós somos \\nos receptores dessas ondas, que oscilam e se propagam de acor -\\ndo com a própria recepção de si próprio, gerando entendimen -\\nto da propagação futura da mesma energia que você captou. \\nComo assim Jesus captou a energia de Deus. Buda captou a \\nenergia da natureza. Da Vinci captou a energia da criação. Tesla \\ncaptou a propagação da energia. Einstein captou a energia do \\nuniverso. Nostradamus captou a energia da vidência. A Bíblia \\n(é a religião na qual eu fui criado, tenho mais conhecimento \\nsobre) é escrita por várias pessoas com captações semelhantes, \\nde vivência e vidência da mesma frequência da energia vinda \\nde Deus, como a própria origem da palavra Deus vem de celes -\\ncaos do passado sendo vivido no futuro editável.indd   7caos do passado sendo vivido no futuro editável.indd   7 28/03/2022   14:53:3728/03/2022   14:53:37",
      "position": 5459,
      "chapter": 1,
      "page": 7,
      "segment_type": "page",
      "themes": {
        "ciencia": 56.52173913043479,
        "tecnologia": 43.47826086956522
      },
      "difficulty": 26.70544871794872,
      "complexity_metrics": {
        "word_count": 312,
        "sentence_count": 15,
        "paragraph_count": 1,
        "avg_sentence_length": 20.8,
        "avg_word_length": 4.983974358974359,
        "unique_word_ratio": 0.5897435897435898,
        "avg_paragraph_length": 312.0,
        "punctuation_density": 0.14743589743589744,
        "line_break_count": 31,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "captou",
          "como",
          "mundo",
          "energias",
          "universo",
          "religião",
          "você",
          "deus",
          "conhecimento",
          "todas",
          "gerado",
          "somos",
          "natureza",
          "pessoas",
          "sentimento",
          "contexto",
          "várias",
          "formas",
          "jesus"
        ],
        "entities": [
          [
            "quando",
            "PERSON"
          ],
          [
            "universo foi",
            "PERSON"
          ],
          [
            "pouco de cada",
            "PERSON"
          ],
          [
            "contexto melhor para",
            "ORG"
          ],
          [
            "Essas",
            "GPE"
          ],
          [
            "Jesus",
            "PERSON"
          ],
          [
            "Tesla",
            "PERSON"
          ],
          [
            "Einstein",
            "PERSON"
          ],
          [
            "diante de si próprio",
            "PERSON"
          ],
          [
            "receptores dessas ondas",
            "PERSON"
          ]
        ],
        "readability_score": 88.10480769230769,
        "semantic_density": 0,
        "word_count": 312,
        "unique_words": 184,
        "lexical_diversity": 0.5897435897435898
      },
      "preservation_score": 1.3108117195392265e-05
    },
    {
      "id": 1,
      "text": "tial ou brilhante, é um fato que Deus é energia!\\nE o Tesla o que têm a ver com isso?\\nTesla interpretou como a energia trabalha do mundo quântico \\npara o mundo físico, enxergando os padrões da frequência da \\nenergia elétrica, como funciona e é reproduzida essa energia \\nno mundo físico.\\nSem esses fatores, seriamos animais, pois não teríamos senti -\\nmento, imagina uma pessoa sem sentimento, porém com a \\ninteligência semelhante a de qualquer ser humano, como ele \\nseria? Os nossos valores de ser humano, vêm do sentimento, se \\numa pessoa não dá valor a essas questões, como ela vai saber o \\nque é ser humano? Todos esses elementos de conduta vêm de \\numa evolução de vida de aceitação, perante a um contexto do \\nque a nossa vida nos mostra o que é certo e melhor para viver -\\nmos em uma sociedade, na qual podemos desfrutar do melhor \\nque pode nos proporcionar.\\nQuando você pratica algo, você pode não ser o melhor, mas \\nconsegue executar com facilidade, essa facilidade é semelhante \\naos nossos instintos, movimento involuntário, podendo ocor -\\nrer um trauma (semelhante a um esforço repetitivo sabendo \\ndessa metáfora, imagina seu corpo coletando dados durante \\ntoda a existência do ser humano, como seria essa questão física \\ne mental, quantos traumas iríamos possuir, quantas ações invo -\\nluntárias praticaríamos? \\nDurante milênios nossos corpos fazem isso e sendo seres \\n“avançados” , temos que conhecer o nosso início para saber de \\nonde vem essas ações, precisamos saber o início desses precon -\\nceitos e pré-conceitos, amor, inveja, religião... A interpretação \\nque criamos sobre expectativas é referente à vida que nós vi -\\nvemos, dentro dessa nossa vida, temos  pré-conceitos sobre ter \\numa vida digna, temos uma predisposição devido a milênios \\ncaos do passado sendo vivido no futuro editável.indd   8caos do passado sendo vivido no futuro editável.indd   8 28/03/2022   14:53:3728/03/2022   14:53:37",
      "position": 7467,
      "chapter": 1,
      "page": 8,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 34.702140762463344,
      "complexity_metrics": {
        "word_count": 310,
        "sentence_count": 11,
        "paragraph_count": 1,
        "avg_sentence_length": 28.181818181818183,
        "avg_word_length": 5.067741935483871,
        "unique_word_ratio": 0.6258064516129033,
        "avg_paragraph_length": 310.0,
        "punctuation_density": 0.14838709677419354,
        "line_break_count": 31,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "como",
          "vida",
          "energia",
          "humano",
          "mundo",
          "essa",
          "semelhante",
          "nossos",
          "saber",
          "melhor",
          "sendo",
          "temos",
          "tesla",
          "isso",
          "físico",
          "esses",
          "imagina",
          "pessoa",
          "sentimento",
          "seria"
        ],
        "entities": [
          [
            "Tesla",
            "NORP"
          ],
          [
            "para o mundo físico",
            "PERSON"
          ],
          [
            "padrões da frequência da \\nenergia elétrica",
            "PERSON"
          ],
          [
            "essa",
            "GPE"
          ],
          [
            "seriamos animais",
            "PERSON"
          ],
          [
            "não teríamos",
            "PERSON"
          ],
          [
            "de ser humano",
            "PERSON"
          ],
          [
            "como ela",
            "PERSON"
          ],
          [
            "mostra",
            "LOC"
          ],
          [
            "Quando",
            "PERSON"
          ]
        ],
        "readability_score": 84.38876832844575,
        "semantic_density": 0,
        "word_count": 310,
        "unique_words": 194,
        "lexical_diversity": 0.6258064516129033
      },
      "preservation_score": 1.2882115174782053e-05
    },
    {
      "id": 1,
      "text": "de adaptação corporal, mental e estrutural. As análises que eu \\ndescrevo são uma análise contextual de um todo e não de uma \\npessoa doutrinada, cheia de vícios, cheia de estereótipos, colo -\\ncando em uma linguagem popular, “parece um cavalo!!!” . \\nComo chegaremos a uma resposta concreta quando se fala de \\ncomportamento humano? Nós humanos estamos sempre à \\nprocura de algo, nessa procura, a pessoa que possui uma acei -\\ntação maior que as demais é a que consegue chegar o mais \\npróximo de um comportamento aceitável, como sabemos o \\nque é aceitável? Simples, porém complexo...\\nSou um admirador de filmes, séries, documentários, vídeos de \\ncuriosidades. Ao decorrer desta leitura, irei fazer algumas refe -\\nrências e metáforas baseadas em filmes, séries etc.\\nComo assim? \\nNa série Mindhunter, uma equipe policial é designada a pren -\\nder um serial killer . Geralmente nós temos comportamentos \\npadronizados, como vamos conhecer um padrão comporta -\\nmental de um serial killer ? Temos que pensar igual a um serial \\nkiller  para chegar próximo de um padrão comportamental que \\nele pensa e age. Assim é como conseguimos chegar perto, de \\numa coerência de raciocínio perante o outro. A partir desse \\nponto de vista, para sermos flexíveis e compreender melhor o \\noutro, temos que pensar de uma forma semelhante, perante a \\npessoa seja ela cadeirante, homossexual, branco, preto, mata -\\ndor, ladrão, gordo, magro, musculoso, racista, feminista, fascis -\\nta... \\nEssa é uma leitura de aceitação perante o semelhante, pois a \\nideia de escrever os meus pensamentos é para somar e analisar -\\nmos um ponto de vista de aceitação perante um pensamento, \\nseja ele ruim ou bom. Por mais que julguemos e vejamos os er -\\nros, não temos muito o que fazer, só temos que aceitar e apren -\\ncaos do passado sendo vivido no futuro editável.indd   9caos do passado sendo vivido no futuro editável.indd   9 28/03/2022   14:53:3728/03/2022   14:53:37",
      "position": 9491,
      "chapter": 1,
      "page": 9,
      "segment_type": "page",
      "themes": {},
      "difficulty": 35.27872714486639,
      "complexity_metrics": {
        "word_count": 316,
        "sentence_count": 18,
        "paragraph_count": 1,
        "avg_sentence_length": 17.555555555555557,
        "avg_word_length": 5.003164556962025,
        "unique_word_ratio": 0.6139240506329114,
        "avg_paragraph_length": 316.0,
        "punctuation_density": 0.1962025316455696,
        "line_break_count": 31,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "como",
          "temos",
          "perante",
          "pessoa",
          "chegar",
          "serial",
          "killer",
          "mental",
          "cheia",
          "comportamento",
          "procura",
          "mais",
          "próximo",
          "aceitável",
          "filmes",
          "séries",
          "leitura",
          "fazer",
          "assim",
          "padrão"
        ],
        "entities": [
          [
            "que eu \\ndescrevo",
            "PERSON"
          ],
          [
            "cheia de vícios",
            "PERSON"
          ],
          [
            "quando se fala de \\n",
            "PERSON"
          ],
          [
            "procura de algo",
            "ORG"
          ],
          [
            "nessa procura",
            "PERSON"
          ],
          [
            "decorrer desta leitura",
            "PERSON"
          ],
          [
            "algumas refe -\\n",
            "PERSON"
          ],
          [
            "metáforas baseadas",
            "PERSON"
          ],
          [
            "Mindhunter",
            "PERSON"
          ],
          [
            "nós temos comportamentos",
            "ORG"
          ]
        ],
        "readability_score": 89.72127285513362,
        "semantic_density": 0,
        "word_count": 316,
        "unique_words": 194,
        "lexical_diversity": 0.6139240506329114
      },
      "preservation_score": 1.672414952515565e-05
    },
    {
      "id": 1,
      "text": "der com os erros que aquela “pessoa” está fazendo. O enxergar \\nos nossos próprios erros nos faz perceber o quão desnecessário \\nsão os nossos próprios erros! \\ncaos do passado sendo vivido no futuro editável.indd   10caos do passado sendo vivido no futuro editável.indd   10 28/03/2022   14:53:3728/03/2022   14:53:37",
      "position": 11530,
      "chapter": 1,
      "page": 10,
      "segment_type": "page",
      "themes": {},
      "difficulty": 21.48913043478261,
      "complexity_metrics": {
        "word_count": 46,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 9.2,
        "avg_word_length": 5.630434782608695,
        "unique_word_ratio": 0.7391304347826086,
        "avg_paragraph_length": 46.0,
        "punctuation_density": 0.17391304347826086,
        "line_break_count": 3,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "erros",
          "nossos",
          "próprios",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "aquela",
          "pessoa",
          "está",
          "fazendo",
          "enxergar",
          "perceber",
          "quão",
          "desnecessário",
          "caos"
        ],
        "entities": [
          [
            "faz",
            "ORG"
          ],
          [
            "perceber o",
            "PRODUCT"
          ],
          [
            "editável.indd",
            "CARDINAL"
          ],
          [
            "10caos",
            "CARDINAL"
          ],
          [
            "sendo vivido",
            "PERSON"
          ],
          [
            "editável.indd   10",
            "CARDINAL"
          ],
          [
            "14:53:3728/03/2022   14:53:37",
            "MONEY"
          ]
        ],
        "readability_score": 93.7108695652174,
        "semantic_density": 0,
        "word_count": 46,
        "unique_words": 34,
        "lexical_diversity": 0.7391304347826086
      },
      "preservation_score": 2.1871163284859175e-07
    },
    {
      "id": 1,
      "text": "SUMÁRIO\\nCapítulo 1.........................................................13\\nCapítulo 2.........................................................15\\nparte 1...............................................................15\\nparte 2...............................................................16\\nCapítulo 3.........................................................17\\nCapítulo 4.........................................................19\\nCapítulo 5.........................................................21\\nCapítulo 6.........................................................25\\nparte 1............................................................25\\nparte 2............................................................28\\nparte 3............................................................32\\nparte 4............................................................32\\nCapítulo 7.........................................................41\\nparte 1............................................................41\\nparte 2............................................................42\\nparte 3............................................................42\\nparte 4............................................................43\\nparte 5............................................................43\\nparte 6............................................................44\\nparte 7............................................................44\\nparte 8............................................................45\\nparte 9............................................................46\\nparte 10..........................................................46\\nparte 11..........................................................47\\nparte 12..........................................................49\\nparte 13..........................................................49\\nparte 14..........................................................50\\nparte 15..........................................................50\\nCapítulo 8.........................................................59 \\nCapítulo 9.........................................................71\\nCapítulo 10.......................................................97\\ncaos do passado sendo vivido no futuro editável.indd   11caos do passado sendo vivido no futuro editável.indd   11 28/03/2022   14:53:3728/03/2022   14:53:37",
      "position": 11960,
      "chapter": 1,
      "page": 11,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 23.97335223245925,
      "complexity_metrics": {
        "word_count": 83,
        "sentence_count": 34,
        "paragraph_count": 1,
        "avg_sentence_length": 2.4411764705882355,
        "avg_word_length": 27.03614457831325,
        "unique_word_ratio": 0.5662650602409639,
        "avg_paragraph_length": 83.0,
        "punctuation_density": 22.02409638554217,
        "line_break_count": 32,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "parte",
          "capítulo",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "sumário",
          "caos"
        ],
        "entities": [
          [
            "1",
            "CARDINAL"
          ],
          [
            "15",
            "CARDINAL"
          ],
          [
            "2",
            "CARDINAL"
          ],
          [
            "1",
            "CARDINAL"
          ],
          [
            "25",
            "CARDINAL"
          ],
          [
            "2",
            "CARDINAL"
          ],
          [
            "28",
            "CARDINAL"
          ],
          [
            "3",
            "CARDINAL"
          ],
          [
            "4",
            "CARDINAL"
          ],
          [
            "41",
            "CARDINAL"
          ]
        ],
        "readability_score": 90.6685683912119,
        "semantic_density": 0,
        "word_count": 83,
        "unique_words": 47,
        "lexical_diversity": 0.5662650602409639
      },
      "preservation_score": 0.0004264585225037074
    },
    {
      "id": 1,
      "text": "Capítulo 11.......................................................99\\nCapítulo 12.......................................................123\\nparte 1............................................................123\\nparte 2............................................................125\\nparte 3............................................................127\\nCapítulo 13.......................................................131\\nparte 1............................................................132\\nPosfácio.............................................................177\\ncaos do passado sendo vivido no futuro editável.indd   12caos do passado sendo vivido no futuro editável.indd   12 28/03/2022   14:53:3728/03/2022   14:53:37",
      "position": 14410,
      "chapter": 11,
      "page": 12,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 22.8825974025974,
      "complexity_metrics": {
        "word_count": 35,
        "sentence_count": 11,
        "paragraph_count": 1,
        "avg_sentence_length": 3.1818181818181817,
        "avg_word_length": 19.457142857142856,
        "unique_word_ratio": 0.6571428571428571,
        "avg_paragraph_length": 35.0,
        "punctuation_density": 13.485714285714286,
        "line_break_count": 8,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "parte",
          "capítulo",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "posfácio",
          "caos"
        ],
        "entities": [
          [
            "11",
            "CARDINAL"
          ],
          [
            "12",
            "CARDINAL"
          ],
          [
            "1",
            "CARDINAL"
          ],
          [
            "2",
            "CARDINAL"
          ],
          [
            "125",
            "CARDINAL"
          ],
          [
            "3",
            "CARDINAL"
          ],
          [
            "13",
            "CARDINAL"
          ],
          [
            "131",
            "CARDINAL"
          ],
          [
            "1",
            "CARDINAL"
          ],
          [
            "177",
            "CARDINAL"
          ]
        ],
        "readability_score": 92.57194805194806,
        "semantic_density": 0,
        "word_count": 35,
        "unique_words": 23,
        "lexical_diversity": 0.6571428571428571
      },
      "preservation_score": 2.752850418787608e-05
    },
    {
      "id": 1,
      "text": "— 13 —Capítulo 1\\nO início! \\nNo início dos tempos, quais eram as necessidades que o ser hu -\\nmano precisava para sobreviver? A espécie humana não tinha \\numa linha de raciocínio óbvia, ela só sabia sentir a necessidade \\nde algo, comida, reprodução da espécie, se proteger dos preda -\\ndores (pois em força, agilidade e instinto de predador, nós so -\\nmos inferiores à maioria). O que era necessário para sobreviver \\nvocê sendo inferior as demais espécies? Inteligência.\\nFoi quando a espécie humana começou a usar o que nenhum \\noutro animal usava: ferramentas, fogo, adaptação corporal para \\ncomer carne, a partir desse momento, o ser humano começou \\na perceber que poderia ter e ser mais, criando necessidades “su -\\npérfluas” , transformando o necessário em desnecessário, pois \\ncomeçamos a viver com mais facilidade, criando tempo vago, \\npercebendo a energia que ronda o mundo, assim criando mais \\ntempo para se pensar em viver, ao invés de sobreviver!\\nNo decorrer de milênios, quantas necessidades viraram desne -\\ncessárias? Nesse contexto, começamos a valorizar a necessidade \\nsexual, mais importante que a necessidade de sobreviver, pois \\ncomeçamos a dar mais valor ao sentimento, devido a termos \\numa maior percepção da energia gerada na criação, com a ne -\\ncessidade de comer deixando de ser prioridade e criando es -\\npaço para pensarmos nos “excessos” , nos criando desejos que \\nnão tínhamos, nos transformando em animais egocêntricos, \\nprepotentes, egoístas, gananciosos, ambiciosos e nos exaltando \\ncomo melhores que outros. \\ncaos do passado sendo vivido no futuro editável.indd   13caos do passado sendo vivido no futuro editável.indd   13 28/03/2022   14:53:3728/03/2022   14:53:37",
      "position": 15248,
      "chapter": 1,
      "page": 13,
      "segment_type": "page",
      "themes": {},
      "difficulty": 28.681818181818183,
      "complexity_metrics": {
        "word_count": 264,
        "sentence_count": 11,
        "paragraph_count": 1,
        "avg_sentence_length": 24.0,
        "avg_word_length": 5.303030303030303,
        "unique_word_ratio": 0.6439393939393939,
        "avg_paragraph_length": 264.0,
        "punctuation_density": 0.17045454545454544,
        "line_break_count": 27,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "criando",
          "sobreviver",
          "necessidades",
          "espécie",
          "necessidade",
          "pois",
          "sendo",
          "começamos",
          "início",
          "humana",
          "necessário",
          "começou",
          "comer",
          "transformando",
          "viver",
          "tempo",
          "energia",
          "passado",
          "vivido"
        ],
        "entities": [
          [
            "13",
            "CARDINAL"
          ],
          [
            "ser hu -\\nmano",
            "PERSON"
          ],
          [
            "para sobreviver",
            "PERSON"
          ],
          [
            "ela só sabia",
            "PERSON"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "sobreviver",
            "GPE"
          ],
          [
            "Foi",
            "PERSON"
          ],
          [
            "humana",
            "ORG"
          ],
          [
            "adaptação corporal",
            "ORG"
          ],
          [
            "humano começou",
            "PERSON"
          ]
        ],
        "readability_score": 86.4090909090909,
        "semantic_density": 0,
        "word_count": 264,
        "unique_words": 170,
        "lexical_diversity": 0.6439393939393939
      },
      "preservation_score": 1.1810428173823954e-05
    },
    {
      "id": 1,
      "text": "— 14 —\\ncaos do passado sendo vivido no futuro editável.indd   14caos do passado sendo vivido no futuro editável.indd   14 28/03/2022   14:53:3728/03/2022   14:53:37",
      "position": 17051,
      "chapter": 1,
      "page": 14,
      "segment_type": "page",
      "themes": {},
      "difficulty": 20.91449275362319,
      "complexity_metrics": {
        "word_count": 23,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 7.666666666666667,
        "avg_word_length": 5.826086956521739,
        "unique_word_ratio": 0.6086956521739131,
        "avg_paragraph_length": 23.0,
        "punctuation_density": 0.2608695652173913,
        "line_break_count": 1,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "caos"
        ],
        "entities": [
          [
            "14",
            "CARDINAL"
          ],
          [
            "editável.indd",
            "CARDINAL"
          ],
          [
            "14caos",
            "CARDINAL"
          ],
          [
            "sendo vivido",
            "PERSON"
          ],
          [
            "editável.indd",
            "CARDINAL"
          ],
          [
            "14",
            "CARDINAL"
          ],
          [
            "14:53:3728/03/2022   14:53:37",
            "MONEY"
          ]
        ],
        "readability_score": 94.41884057971015,
        "semantic_density": 0,
        "word_count": 23,
        "unique_words": 14,
        "lexical_diversity": 0.6086956521739131
      },
      "preservation_score": 5.8323102092957795e-08
    },
    {
      "id": 1,
      "text": "— 15 —Capítulo 2\\nCriação do “monstro” \\nParte 1\\nO homem, no início, era o caçador para a família, ele tinha que \\nficar focado para ter o que comer para a sua própria sobrevivên -\\ncia, gerando uma característica de se penetrar no que é neces -\\nsário, assim criou a característica marcante do homem em ter \\nmais força e ser mais penetrado em sua necessidade perante a \\nsua própria vida. Com os hormônios do homem sendo hormô -\\nnios de força, e a todo momento o próprio homem tentando se \\nconter, pois não precisava se esforçar tanto para caçar, começou \\na usar a sua força, os seus desejos, para ser exaltado dentro da \\nsua convivência na sua própria espécie, criando a sua própria \\nruína, pois ele criou um superego perante o seu próprio seme -\\nlhante, criando, assim, o desejo de ser dominante, o desejo de \\nconquistar a melhor fêmea, o desejo de conquistar algo que o \\npróprio semelhante não conseguiria ter, pois o desejo de ter \\nmais, ser mais, condiz com a aceitação perante os seus seme -\\nlhantes, pois quanto mais você tem, mais aceitação terá, tendo \\nmais aceitação, uma melhor vida terá. Terá as melhores comi -\\ndas, as melhores fêmeas, as melhores casas, uma vida melhor \\nque qualquer outro. Em questão de evolução, essa aquisição \\nde ser melhor que o seu semelhante foi necessária, porém por \\nqual motivo esse fator evolutivo não deixou de existir, por qual \\nmotivo esse fator evolutivo não evoluiu no termo de se viver \\nmelhor em sociedade? Pelo simples fato de sermos egoístas ao \\nponto de não perceber a frequência que é necessária para se ter \\numa vida digna e mais próxima de ser plena. Como assim? É \\ncaos do passado sendo vivido no futuro editável.indd   15caos do passado sendo vivido no futuro editável.indd   15 28/03/2022   14:53:3728/03/2022   14:53:37",
      "position": 17330,
      "chapter": 2,
      "page": 15,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 33.090770901194354,
      "complexity_metrics": {
        "word_count": 307,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 34.111111111111114,
        "avg_word_length": 4.687296416938111,
        "unique_word_ratio": 0.5407166123778502,
        "avg_paragraph_length": 307.0,
        "punctuation_density": 0.13680781758957655,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "melhor",
          "homem",
          "própria",
          "vida",
          "pois",
          "desejo",
          "assim",
          "força",
          "perante",
          "sendo",
          "próprio",
          "aceitação",
          "terá",
          "melhores",
          "característica",
          "criou",
          "seus",
          "criando",
          "seme"
        ],
        "entities": [
          [
            "15",
            "CARDINAL"
          ],
          [
            "monstro",
            "PRODUCT"
          ],
          [
            "1",
            "CARDINAL"
          ],
          [
            "própria sobrevivên -\\ncia",
            "PERSON"
          ],
          [
            "tanto",
            "GPE"
          ],
          [
            "para caçar",
            "PERSON"
          ],
          [
            "para ser",
            "PERSON"
          ],
          [
            "desejo de ser dominante",
            "ORG"
          ],
          [
            "desejo de \\nconquistar",
            "ORG"
          ],
          [
            "desejo de conquistar",
            "ORG"
          ]
        ],
        "readability_score": 81.538255519363,
        "semantic_density": 0,
        "word_count": 307,
        "unique_words": 166,
        "lexical_diversity": 0.5407166123778502
      },
      "preservation_score": 1.061480458091832e-05
    },
    {
      "id": 1,
      "text": "— 16 —você conseguir controlar as próprias características evolutivas e \\nde captação da energia, não tendo oscilações comportamentais \\nnem sentimentais que possam vir a te prejudicar futuramente.\\n \\nParte 2 \\nAs mulheres evoluíram em cuidar da caça e da cria, fazendo \\nelas ficarem atentas a um contexto e não a um foco, criando \\numa quantidade maior de neurônios para trabalhar em mais \\nfunções do que as do homem. A evolução das mulheres foi \\npara ser mais “fraca” , porém aprendeu a ser mais forte, através \\nda sedução e da necessidade de cuidar (afeto de mãe e esposa). \\nPor outro lado, no decorrer dos anos, isso foi prejudicial para \\nas próprias mulheres, pois os homens viram o ego de ser “me -\\nlhor” sobressair, transformando durante milênios a submissão \\ndas próprias mulheres para serem relativamente mais fracas \\n(força, músculo, testosterona), transformando essa evolução \\nem uma guerra de preconceitos pelo próprio ser humano, in -\\ncapaz de enxergar que o processo evolutivo depende de todos \\nnós, pois a sua fraqueza é a força do outro. Se juntarmos a ne -\\ncessidade de um ser humano que o outro tem mais capacidade \\ndevido à evolução exigir que ele se aprimore na sua necessida -\\nde, nós seriamos seres muito mais evoluídos. \\ncaos do passado sendo vivido no futuro editável.indd   16caos do passado sendo vivido no futuro editável.indd   16 28/03/2022   14:53:3728/03/2022   14:53:37",
      "position": 19218,
      "chapter": 1,
      "page": 16,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 34.82439427312775,
      "complexity_metrics": {
        "word_count": 227,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 28.375,
        "avg_word_length": 5.039647577092511,
        "unique_word_ratio": 0.6607929515418502,
        "avg_paragraph_length": 227.0,
        "punctuation_density": 0.1145374449339207,
        "line_break_count": 22,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "mulheres",
          "próprias",
          "evolução",
          "outro",
          "cuidar",
          "pois",
          "transformando",
          "força",
          "humano",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "você",
          "conseguir",
          "controlar",
          "características"
        ],
        "entities": [
          [
            "16",
            "CARDINAL"
          ],
          [
            "nem sentimentais",
            "PERSON"
          ],
          [
            "possam vir",
            "PERSON"
          ],
          [
            "2",
            "CARDINAL"
          ],
          [
            "cuidar da caça",
            "PERSON"
          ],
          [
            "elas ficarem atentas",
            "PERSON"
          ],
          [
            "para trabalhar",
            "PERSON"
          ],
          [
            "para ser mais",
            "PERSON"
          ],
          [
            "afeto de mãe",
            "ORG"
          ],
          [
            "para serem",
            "PERSON"
          ]
        ],
        "readability_score": 84.30060572687225,
        "semantic_density": 0,
        "word_count": 227,
        "unique_words": 150,
        "lexical_diversity": 0.6607929515418502
      },
      "preservation_score": 6.415541230225359e-06
    },
    {
      "id": 1,
      "text": "— 17 —Capítulo 3 \\nFogo\\nO fogo foi a evolução para a nossa forma de viver o hoje, pois \\no fogo nos fez ter tempo para sentir a propagação da energia, \\nnos tornando pessoas com mais sentimento, com mais sensibi -\\nlidade à energia das pessoas em sua volta.\\nO fogo nos fez ter conforto na vida, devido ao fogo, nós cria -\\nmos laços familiares, proteção contra outros animais por eles \\ntemerem ao fogo (único ser vivo que não teme ao fogo é o ser \\nhumano), facilidade em comer uma comida por ter mais ca -\\npacidade em mastigar, aquecer o corpo perto do fogo, criando \\naproximação entre os semelhantes e ficando com mais tempo \\nobsoleto para ter novas ideias, conseguir captar e absorver as \\nenergias que envolvem o universo e o mundo, as canalizando \\nde uma forma necessária para a sua tribo, povo, colônia, cida -\\ndes, estados, países, as fazendo criar conexões com a energia \\nque captava, gerando uma necessidade de si próprio ou uma \\nnecessidade para um bem maior.\\nO fogo nos fez enxergar a primeira forma de se estudar a ener -\\ngia, pois energia é quente e o fogo é a primeira energia que \\nconseguimos “controlar” para o nosso próprio benefício, nos \\nfazendo criar ferramentas para melhor vivermos e armas para \\ncaçar melhor, nos dando imaginação de como usar o fogo de \\noutras formas!!\\ncaos do passado sendo vivido no futuro editável.indd   17caos do passado sendo vivido no futuro editável.indd   17 28/03/2022   14:53:3728/03/2022   14:53:37",
      "position": 20729,
      "chapter": 3,
      "page": 17,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.4052,
      "complexity_metrics": {
        "word_count": 250,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 41.666666666666664,
        "avg_word_length": 4.684,
        "unique_word_ratio": 0.6,
        "avg_paragraph_length": 250.0,
        "punctuation_density": 0.124,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "fogo",
          "energia",
          "mais",
          "forma",
          "pois",
          "tempo",
          "pessoas",
          "fazendo",
          "criar",
          "necessidade",
          "próprio",
          "primeira",
          "melhor",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "capítulo"
        ],
        "entities": [
          [
            "17",
            "CARDINAL"
          ],
          [
            "nós cria -\\nmos laços familiares",
            "ORG"
          ],
          [
            "contra",
            "NORP"
          ],
          [
            "outros animais",
            "PERSON"
          ],
          [
            "temerem ao fogo",
            "PERSON"
          ],
          [
            "único ser vivo que",
            "ORG"
          ],
          [
            "novas",
            "GPE"
          ],
          [
            "universo e o mundo",
            "ORG"
          ],
          [
            "colônia",
            "GPE"
          ],
          [
            "cida -\\ndes",
            "PERSON"
          ]
        ],
        "readability_score": 77.76146666666666,
        "semantic_density": 0,
        "word_count": 250,
        "unique_words": 150,
        "lexical_diversity": 0.6
      },
      "preservation_score": 7.348710863712682e-06
    },
    {
      "id": 1,
      "text": "— 18 —\\ncaos do passado sendo vivido no futuro editável.indd   18caos do passado sendo vivido no futuro editável.indd   18 28/03/2022   14:53:3728/03/2022   14:53:37",
      "position": 22287,
      "chapter": 1,
      "page": 18,
      "segment_type": "page",
      "themes": {},
      "difficulty": 20.91449275362319,
      "complexity_metrics": {
        "word_count": 23,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 7.666666666666667,
        "avg_word_length": 5.826086956521739,
        "unique_word_ratio": 0.6086956521739131,
        "avg_paragraph_length": 23.0,
        "punctuation_density": 0.2608695652173913,
        "line_break_count": 1,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "caos"
        ],
        "entities": [
          [
            "18",
            "CARDINAL"
          ],
          [
            "editável.indd   18caos",
            "QUANTITY"
          ],
          [
            "sendo vivido",
            "PERSON"
          ],
          [
            "editável.indd",
            "CARDINAL"
          ],
          [
            "18",
            "CARDINAL"
          ],
          [
            "14:53:3728/03/2022   14:53:37",
            "MONEY"
          ]
        ],
        "readability_score": 94.41884057971015,
        "semantic_density": 0,
        "word_count": 23,
        "unique_words": 14,
        "lexical_diversity": 0.6086956521739131
      },
      "preservation_score": 5.8323102092957795e-08
    },
    {
      "id": 1,
      "text": "— 19 —Capítulo 4 \\nAlimentação\\nConseguir manusear o fogo foi peça fundamental para uma \\nevolução mais rápida cerebral, pois criamos conforto cerebral, \\npercepção da energia, laços familiares, ingerimos mais carne, \\nfazendo o nosso cérebro ter mais energia para pensar e menos \\nobrigações a fazer, gerando uma evolução pelas necessidades \\nda ganância. O comer bem chega a ser uma conexão com os \\ndeuses... O êxtase de sensação, ao se alimentar de uma boa ali -\\nmentação, é a sua conexão em agregar a energia universal ao \\nseu mundo físico!!\\nA alimentação nos fez ter outros desejos, outros prazeres, ou -\\ntras necessidades perante eu quero comer melhor para sempre \\nter um êxtase, criando conflitos, criando guerras, criando inte -\\nresses maiores que o seu necessário, perante um estado de se \\nviver em harmonia com os nossos semelhantes. Caos gera mais \\ncaos!!! Para toda ação há uma reação, se algo oscila ou tem uma \\nação sobre, gera uma onda proporcional à ação exercida sobre \\nesse algo, gerando ondas e afetando a propagação da energia, \\nafetando a propagação da energia, cria mais MASSA ESCURA \\n(matéria escura é algo palpável, massa é sentido o deslocamen -\\nto da massa), criando mais sensação da massa escura, a energia \\nse torna mais difícil de se propagar e automaticamente de se \\ncaptar. Criando escassez de energia, gerando uma menor cap -\\ntação de ondas de energia emitidas pelo nosso próprio mundo \\n(natureza), pela própria ganância do homem em ter mais que \\no necessário da natureza, perante o manter a harmonia entre \\na energia consumida (alimentos são formados de átomos) e \\ncaos do passado sendo vivido no futuro editável.indd   19caos do passado sendo vivido no futuro editável.indd   19 28/03/2022   14:53:3728/03/2022   14:53:37",
      "position": 22566,
      "chapter": 4,
      "page": 19,
      "segment_type": "page",
      "themes": {},
      "difficulty": 33.356654888103655,
      "complexity_metrics": {
        "word_count": 283,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 31.444444444444443,
        "avg_word_length": 5.07773851590106,
        "unique_word_ratio": 0.6113074204946997,
        "avg_paragraph_length": 283.0,
        "punctuation_density": 0.14840989399293286,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "mais",
          "criando",
          "massa",
          "gerando",
          "perante",
          "caos",
          "ação",
          "algo",
          "escura",
          "alimentação",
          "evolução",
          "cerebral",
          "nosso",
          "necessidades",
          "ganância",
          "comer",
          "conexão",
          "êxtase",
          "sensação"
        ],
        "entities": [
          [
            "19",
            "CARDINAL"
          ],
          [
            "evolução mais rápida cerebral",
            "ORG"
          ],
          [
            "ingerimos mais",
            "PERSON"
          ],
          [
            "para pensar",
            "PERSON"
          ],
          [
            "alimentar de uma",
            "ORG"
          ],
          [
            "outros desejos",
            "PERSON"
          ],
          [
            "eu quero",
            "PERSON"
          ],
          [
            "seu necessário",
            "GPE"
          ],
          [
            "gera mais",
            "PERSON"
          ],
          [
            "ação sobre",
            "PERSON"
          ]
        ],
        "readability_score": 82.75445622300745,
        "semantic_density": 0,
        "word_count": 283,
        "unique_words": 173,
        "lexical_diversity": 0.6113074204946997
      },
      "preservation_score": 1.1227197152894378e-05
    },
    {
      "id": 1,
      "text": "— 20 —energia necessária para o seu corpo físico!!!\\ncaos do passado sendo vivido no futuro editável.indd   20caos do passado sendo vivido no futuro editável.indd   20 28/03/2022   14:53:3728/03/2022   14:53:37",
      "position": 24429,
      "chapter": 1,
      "page": 20,
      "segment_type": "page",
      "themes": {},
      "difficulty": 20.664655172413795,
      "complexity_metrics": {
        "word_count": 29,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 7.25,
        "avg_word_length": 5.9655172413793105,
        "unique_word_ratio": 0.7241379310344828,
        "avg_paragraph_length": 29.0,
        "punctuation_density": 0.3103448275862069,
        "line_break_count": 1,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "energia",
          "necessária",
          "corpo",
          "físico",
          "caos"
        ],
        "entities": [
          [
            "20",
            "CARDINAL"
          ],
          [
            "editável.indd",
            "CARDINAL"
          ],
          [
            "20caos",
            "CARDINAL"
          ],
          [
            "sendo vivido",
            "PERSON"
          ],
          [
            "editável.indd   20",
            "CARDINAL"
          ],
          [
            "14:53:3728/03/2022   14:53:37",
            "MONEY"
          ]
        ],
        "readability_score": 94.58534482758621,
        "semantic_density": 0,
        "word_count": 29,
        "unique_words": 21,
        "lexical_diversity": 0.7241379310344828
      },
      "preservation_score": 8.019426537781696e-08
    },
    {
      "id": 1,
      "text": "— 21 —Capítulo 5 \\nSexo\\nCom o nosso excesso de tempo, começamos a perceber melhor \\na energia emitida pelo corpo, nos fazendo ter uma conexão \\nmelhor com a nossa parceira, fazendo termos uma conexão \\nentre o mundo físico e o da energia!!!\\nComo seria essa sensação sexual? Por qual motivo não temos \\nesse controle sobre o desejo do sexo? Por que damos tanta im -\\nportância?\\nPrimeiro, nós não tínhamos muitos momentos de “lazer” , sem -\\npre estávamos atentos e tensos à nossa necessidade de sobrevi -\\nver, pois nós somos animais e animal tem seu instinto natural \\n(DNA), esse instinto natural nos faz ter pré princípio genético \\nou um pré princípio de sobrevivência. Nós evoluímos essa ne -\\ncessidade de DNA genética e instinto de sobrevivência de acor -\\ndo com o caos (massa escura) gerado, criando uma necessidade \\nde se adaptar à energia local (tribo, comunidade, cidade, esta -\\ndo, pais), perdendo a percepção da energia envolto do mundo.\\nPerae, como assim? O que isso têm a ver com o sexo? Nós co -\\nmeçamos a fazer sexo pela necessidade reprodutiva, igual a \\nqualquer outro animal.\\nAnalogia  \\nEntre os macacos japoneses, a disputa pelas fêmeas é grande na \\népoca de acasalamento. Isso porque os machos, além de com -\\npetir entre si, também precisam competir com outras fêmeas \\nna hora de encontrar uma parceira. Entre elas, o comporta -\\nmento homossexual é a norma e os casais podem durar uma \\ncaos do passado sendo vivido no futuro editável.indd   21caos do passado sendo vivido no futuro editável.indd   21 28/03/2022   14:53:3728/03/2022   14:53:37",
      "position": 24753,
      "chapter": 5,
      "page": 21,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 25.910673546985333,
      "complexity_metrics": {
        "word_count": 263,
        "sentence_count": 14,
        "paragraph_count": 1,
        "avg_sentence_length": 18.785714285714285,
        "avg_word_length": 4.821292775665399,
        "unique_word_ratio": 0.6653992395437263,
        "avg_paragraph_length": 263.0,
        "punctuation_density": 0.1444866920152091,
        "line_break_count": 27,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "sexo",
          "energia",
          "entre",
          "necessidade",
          "instinto",
          "melhor",
          "fazendo",
          "conexão",
          "nossa",
          "parceira",
          "mundo",
          "como",
          "essa",
          "esse",
          "animal",
          "natural",
          "princípio",
          "sobrevivência",
          "caos",
          "isso"
        ],
        "entities": [
          [
            "21",
            "CARDINAL"
          ],
          [
            "excesso de tempo",
            "PERSON"
          ],
          [
            "perceber melhor",
            "ORG"
          ],
          [
            "pelo corpo",
            "PERSON"
          ],
          [
            "Como",
            "ORG"
          ],
          [
            "desejo",
            "ORG"
          ],
          [
            "Primeiro",
            "ORG"
          ],
          [
            "nós somos animais",
            "ORG"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "princípio genético \\n",
            "PERSON"
          ]
        ],
        "readability_score": 89.16075502444323,
        "semantic_density": 0,
        "word_count": 263,
        "unique_words": 175,
        "lexical_diversity": 0.6653992395437263
      },
      "preservation_score": 1.1219906765132756e-05
    },
    {
      "id": 1,
      "text": "— 22 —semana inteira, indo muito além do sexo: quando não estão \\nacasalando, as fêmeas dormem juntinhas e protegem-se contra \\nrivais em potencial.\\nO leão briga com um bando para poder ter o privilégio de se \\nfazer o sexo com a fêmea, além dele brigar com o bando por \\nele ser forte, ele gera uma juba mais bonita e melhor, assim \\natraindo a fêmea.\\nSe você reparar nos dois textos, nós vemos que temos períodos \\npara acasalar, devido à fêmea estar em um processo de ovu -\\nlação, exalando hormônios (energia), atraindo o macho mais \\nforte, mais bonito, o instinto provocador, o instinto da sedu -\\nção. Mas temos um problema com o ser humano, ele conse -\\nguiu canalizar e “interpretar” a energia do sexo, o fazendo per -\\nder a noção da necessidade e focando no prazer do ato sexual. \\nO sexo virou um ciclo infinito de desejo pela energia recebida \\ndo ato sexual, gerando uma necessidade fisiológica e corpórea \\ndiante dos hormônios gerados pela frequência de se fazer o \\nato, tornando o humano dependente do sexo!!!\\nSe você reparar, têm um padrão de comportamento perante ao \\nsexo. Temos que conquistar a fêmea, como conquisto a fêmea \\nmais cobiçada ou a melhor fêmea?\\nAssim começamos a criar os conflitos, o homem querendo ser \\nmais homem para conquistar a melhor mulher, a mulher que -\\nrendo ter o melhor homem. Tanto o homem (caçador) quanto \\na mulher (dona de casa) evoluíram as suas próprias caracte -\\nrísticas e começaram a se adaptar, como, por exemplo usaram \\num ciclo de si próprio perante a minha necessidade de ter ou \\nser melhor, com fatores de DNA e fatores de ter ou ser melhor \\nna comunidade, criando a ganância de ter ou ser melhor que \\no outro na propagação de si próprio, de vontade de ter ou ser \\nmais que a todos em sua volta, gerando mais massa escura em \\ncaos do passado sendo vivido no futuro editável.indd   22caos do passado sendo vivido no futuro editável.indd   22 28/03/2022   14:53:3728/03/2022   14:53:37",
      "position": 26420,
      "chapter": 1,
      "page": 22,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 33.044782140935986,
      "complexity_metrics": {
        "word_count": 338,
        "sentence_count": 11,
        "paragraph_count": 1,
        "avg_sentence_length": 30.727272727272727,
        "avg_word_length": 4.6301775147929,
        "unique_word_ratio": 0.5680473372781065,
        "avg_paragraph_length": 338.0,
        "punctuation_density": 0.12721893491124261,
        "line_break_count": 31,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "melhor",
          "sexo",
          "fêmea",
          "homem",
          "temos",
          "energia",
          "necessidade",
          "mulher",
          "além",
          "bando",
          "fazer",
          "forte",
          "assim",
          "atraindo",
          "você",
          "reparar",
          "hormônios",
          "instinto",
          "humano"
        ],
        "entities": [
          [
            "22",
            "CARDINAL"
          ],
          [
            "semana inteira",
            "PERSON"
          ],
          [
            "quando não estão \\nacasalando",
            "PERSON"
          ],
          [
            "bando",
            "ORG"
          ],
          [
            "privilégio",
            "GPE"
          ],
          [
            "de se \\nfazer",
            "PERSON"
          ],
          [
            "juba mais bonita",
            "PERSON"
          ],
          [
            "atraindo",
            "ORG"
          ],
          [
            "mais bonito",
            "PERSON"
          ],
          [
            "Mas",
            "PERSON"
          ]
        ],
        "readability_score": 83.24731038192577,
        "semantic_density": 0,
        "word_count": 338,
        "unique_words": 192,
        "lexical_diversity": 0.5680473372781065
      },
      "preservation_score": 1.3560121236612687e-05
    },
    {
      "id": 1,
      "text": "— 23 —torno de um todo em sua volta.\\nSexo foi necessário para evoluirmos o conforto do humano, \\npois o ato sexual nos ensinou a sentir prazer e felicidade com o \\noutro, criando laços de energia focados no outro semelhante. \\nSem a energia emitida no ato sexual, nós não teríamos senti -\\nmentos pelo nosso semelhante, nos tornando pessoas só com o \\ninstinto de sobrevivência, sendo assim um animal irracional!!\\ncaos do passado sendo vivido no futuro editável.indd   23caos do passado sendo vivido no futuro editável.indd   23 28/03/2022   14:53:3728/03/2022   14:53:37",
      "position": 28466,
      "chapter": 1,
      "page": 23,
      "segment_type": "page",
      "themes": {},
      "difficulty": 24.21666666666667,
      "complexity_metrics": {
        "word_count": 90,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 15.0,
        "avg_word_length": 5.166666666666667,
        "unique_word_ratio": 0.7444444444444445,
        "avg_paragraph_length": 90.0,
        "punctuation_density": 0.16666666666666666,
        "line_break_count": 7,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "sendo",
          "sexual",
          "outro",
          "energia",
          "semelhante",
          "passado",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "torno",
          "todo",
          "volta",
          "sexo",
          "necessário",
          "evoluirmos",
          "conforto",
          "humano",
          "pois",
          "ensinou"
        ],
        "entities": [
          [
            "23",
            "CARDINAL"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "para evoluirmos",
            "PRODUCT"
          ],
          [
            "laços de",
            "PERSON"
          ],
          [
            "mentos pelo",
            "PERSON"
          ],
          [
            "editável.indd",
            "CARDINAL"
          ],
          [
            "23caos",
            "CARDINAL"
          ],
          [
            "sendo vivido",
            "PERSON"
          ],
          [
            "editável.indd   23",
            "CARDINAL"
          ],
          [
            "14:53:3728/03/2022   14:53:37",
            "MONEY"
          ]
        ],
        "readability_score": 90.95,
        "semantic_density": 0,
        "word_count": 90,
        "unique_words": 67,
        "lexical_diversity": 0.7444444444444445
      },
      "preservation_score": 9.185888579640854e-07
    },
    {
      "id": 1,
      "text": "— 24 —\\ncaos do passado sendo vivido no futuro editável.indd   24caos do passado sendo vivido no futuro editável.indd   24 28/03/2022   14:53:3728/03/2022   14:53:37",
      "position": 29147,
      "chapter": 1,
      "page": 24,
      "segment_type": "page",
      "themes": {},
      "difficulty": 20.91449275362319,
      "complexity_metrics": {
        "word_count": 23,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 7.666666666666667,
        "avg_word_length": 5.826086956521739,
        "unique_word_ratio": 0.6086956521739131,
        "avg_paragraph_length": 23.0,
        "punctuation_density": 0.2608695652173913,
        "line_break_count": 1,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "caos"
        ],
        "entities": [
          [
            "24",
            "CARDINAL"
          ],
          [
            "editável.indd",
            "CARDINAL"
          ],
          [
            "24caos",
            "CARDINAL"
          ],
          [
            "sendo vivido",
            "PERSON"
          ],
          [
            "editável.indd",
            "CARDINAL"
          ],
          [
            "24",
            "CARDINAL"
          ],
          [
            "14:53:3728/03/2022   14:53:37",
            "MONEY"
          ]
        ],
        "readability_score": 94.41884057971015,
        "semantic_density": 0,
        "word_count": 23,
        "unique_words": 14,
        "lexical_diversity": 0.6086956521739131
      },
      "preservation_score": 5.8323102092957795e-08
    },
    {
      "id": 1,
      "text": "— 25 —Capítulo 6 \\nReligião \\nParte 1\\nEste capítulo é o capítulo!!!\\nIsso aqui interpreta nossa captação de energia coletiva e pes -\\nsoal, inteligência emocional, afetiva, coletiva e muitas outras.\\nComo começamos a ter a necessidade de termos religiosos?\\nQuando começamos a criar conexão de energia e a melhor \\nqualidade de vida, começamos a construir tribos e, nessas tri -\\nbos, começamos a não conseguir administrar a quantidade \\nde energia consumida (alimentos, fogo incontrolável, retirar \\nrochas, contaminando rios, destruindo a camada de ozônio), \\ncriando desestabilidade na propagação da energia do mundo, \\npois se criava mais massa escura, criando interferência na pro -\\npagação da energia de um bem de um todo, gerando falta de \\ncaptação da energia do mundo, perante a necessidade de se \\nadaptar devido a estar com mais massa escura, criando menos \\nrota da propagação da sua própria energia (Deus, Buda, Ala, \\nRá, Zeus etc.).\\nCada tribo, bairro, cidade, estado, país criou um campo mag -\\nnético (pirâmides, canalização de energia e estabilidade do \\ncaos criado pela própria região) com uma energia dominante \\nde percepção e interpretativa perante a uma necessidade de \\num contexto mútuo, nos fazendo criar as primeiras religiões, \\nque foram as religiões politeístas.\\nEssas religiões tinham como referência a dor da sua necessida -\\ncaos do passado sendo vivido no futuro editável.indd   25caos do passado sendo vivido no futuro editável.indd   25 28/03/2022   14:53:3728/03/2022   14:53:37",
      "position": 29426,
      "chapter": 6,
      "page": 25,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 29.564444444444444,
      "complexity_metrics": {
        "word_count": 230,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 25.555555555555557,
        "avg_word_length": 5.4,
        "unique_word_ratio": 0.6391304347826087,
        "avg_paragraph_length": 230.0,
        "punctuation_density": 0.1782608695652174,
        "line_break_count": 26,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "começamos",
          "capítulo",
          "necessidade",
          "criando",
          "religiões",
          "captação",
          "coletiva",
          "como",
          "criar",
          "propagação",
          "mundo",
          "mais",
          "massa",
          "escura",
          "perante",
          "própria",
          "caos",
          "passado",
          "sendo"
        ],
        "entities": [
          [
            "25",
            "CARDINAL"
          ],
          [
            "6",
            "CARDINAL"
          ],
          [
            "1",
            "CARDINAL"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "criava",
            "CARDINAL"
          ],
          [
            "massa escura",
            "PERSON"
          ],
          [
            "mais massa escura",
            "PERSON"
          ],
          [
            "da propagação da sua própria",
            "ORG"
          ],
          [
            "Deus, Buda, Ala",
            "ORG"
          ],
          [
            "Rá",
            "ORG"
          ]
        ],
        "readability_score": 85.60222222222222,
        "semantic_density": 0,
        "word_count": 230,
        "unique_words": 147,
        "lexical_diversity": 0.6391304347826087
      },
      "preservation_score": 1.0235704417314092e-05
    },
    {
      "id": 1,
      "text": "— 26 —de perante a comunidade que eu vivo. Mas como assim? Vamos \\nvoltar na ganância de ter mais do que o necessário, criando \\nmais massa escura e criando um menor caminho de propa -\\ngação da energia, nos tornando com dificuldades de captar a \\nenergia necessária para vivermos em um todo com o mundo \\ne universo, nos limitando em algumas pessoas terem uma \\nsensibilidade melhor para conseguir acessar essa frequência \\nde energia de um bem para um todo, fazendo termos pessoas \\ncom status  de sabedoria, intelectual, vidência e milagrosa..\\nAs tribos continham algumas pessoas com uma maior cap -\\ntação dessa energia, os pajés (religiosidade), curandeiros(as) \\n(vida), mago (cientista), feiticeiro (alquimia), mago e feiticeiro \\nsão as mesmas coisas? Não, um consegue captar a ciência e o \\nmilagre (mago, Buda, Jesus) o outro consegue captar e inter -\\npretar a energia para o físico (feiticeiro, Leonardo da Vinci, \\nTesla, Einstein).\\nAs religiões vieram como uma divindade (energia captada), \\nessa divindade era o caos gerado e a percepção da desestabi -\\nlidade da energia diante do necessário para vivermos em uma \\nsintonia com o todo, nos fazendo dar nomes e símbolos espe -\\ncíficos diante da necessidade de se melhorar aquele aspecto na \\ntribo.\\nExemplos\\nTupã, é o grande criador da vida. Além de dar origem ao mar, \\ncéus e terra, ele também ajudou o povo humano a plantar, fa -\\nzer artesanato e caçar. Para os pajés, ele concedeu algumas ha -\\nbilidades extras sobre plantas, ervas medicinais e curas. \\nJaci é a deusa filha de Tupã. Ela é a grande representante da \\nnoite e guardiã do luar. Ela é responsável pela reprodução. Os \\ncaos do passado sendo vivido no futuro editável.indd   26caos do passado sendo vivido no futuro editável.indd   26 28/03/2022   14:53:3728/03/2022   14:53:37",
      "position": 31035,
      "chapter": 1,
      "page": 26,
      "segment_type": "page",
      "themes": {
        "ciencia": 56.52173913043479,
        "arte": 43.47826086956522
      },
      "difficulty": 26.36360544217687,
      "complexity_metrics": {
        "word_count": 294,
        "sentence_count": 15,
        "paragraph_count": 1,
        "avg_sentence_length": 19.6,
        "avg_word_length": 4.989795918367347,
        "unique_word_ratio": 0.6258503401360545,
        "avg_paragraph_length": 294.0,
        "punctuation_density": 0.14965986394557823,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "captar",
          "todo",
          "algumas",
          "pessoas",
          "mago",
          "feiticeiro",
          "como",
          "mais",
          "necessário",
          "criando",
          "vivermos",
          "essa",
          "fazendo",
          "pajés",
          "vida",
          "consegue",
          "divindade",
          "caos",
          "diante"
        ],
        "entities": [
          [
            "26",
            "CARDINAL"
          ],
          [
            "eu vivo",
            "PERSON"
          ],
          [
            "Vamos",
            "PERSON"
          ],
          [
            "ganância de ter mais",
            "PERSON"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "mais massa escura",
            "PERSON"
          ],
          [
            "para vivermos",
            "PERSON"
          ],
          [
            "terem uma \\nsensibilidade melhor",
            "PERSON"
          ],
          [
            "para conseguir",
            "PERSON"
          ],
          [
            "acessar essa",
            "ORG"
          ]
        ],
        "readability_score": 88.7030612244898,
        "semantic_density": 0,
        "word_count": 294,
        "unique_words": 184,
        "lexical_diversity": 0.6258503401360545
      },
      "preservation_score": 1.458806591100107e-05
    },
    {
      "id": 1,
      "text": "— 27 —povos indígenas contam que ela planta a saudade no coração \\ndos caçadores, para que eles voltem para suas esposas e cuidem \\nda sua família. \\nAnhangá é o protetor dos animais e dos caçadores, porém, ele \\né a representação do mal. Ele é o arqui-inimigo de Tupã e é \\nsempre associado às dimensões infernais. Seu espírito anda li -\\nvre por aí, se transformando em animal selvagem no meio da \\nmata.\\nAkuanduba, enquanto toca a sua flauta, traz harmonia para o \\nmundo. Conta-se que ele jogou uma tribo inteira para dentro \\ndo mar para ver se aprendiam as virtudes da obediência. Ela \\nsobreviveu e deu um novo rumo para a sua existência.\\nSe você reparar, os deuses de tribos são sempre relativos ao caos \\nda própria tribo, quando o caos sobrepõe ao outro caos, se cria \\num outro Deus ou um outro “inimigo” para combater o caos \\ngerado pelo outro Deus...\\nIsso me faz perceber a propagação da massa escura e uma me -\\nnor propagação da energia, sendo feita por nós mesmos sem \\nperceber diante da nossa própria necessidade de se ter mais, \\nde viver um estilo de vida, de se viver melhor perante nós mes -\\nmos, criando grandes condutores de energia, sendo eles pajés, \\nmagos, feiticeiros, profetas, messias, gênios, sendo aquele que \\nmelhor interpreta a necessidade de um todo diante da sua for -\\nma de interpretar de uma tribo, povoado, comunidade, bair -\\nros, cidades, estado, país, mundo e universo!!!\\nDevido a necessidade de se usar referências para se ter uma \\nmelhor compreensão de direcionamento para uma melhor in -\\nterpretação da teoria escrita nesse livro, usarei alguns textos \\ncom algumas modificações retirados do Wikipédia (enciclopé -\\ncaos do passado sendo vivido no futuro editável.indd   27caos do passado sendo vivido no futuro editável.indd   27 28/03/2022   14:53:3728/03/2022   14:53:37",
      "position": 32937,
      "chapter": 1,
      "page": 27,
      "segment_type": "page",
      "themes": {
        "filosofia": 53.57142857142857,
        "ciencia": 46.42857142857144
      },
      "difficulty": 31.12991169977925,
      "complexity_metrics": {
        "word_count": 302,
        "sentence_count": 12,
        "paragraph_count": 1,
        "avg_sentence_length": 25.166666666666668,
        "avg_word_length": 4.877483443708609,
        "unique_word_ratio": 0.6158940397350994,
        "avg_paragraph_length": 302.0,
        "punctuation_density": 0.15562913907284767,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "caos",
          "sendo",
          "outro",
          "melhor",
          "tribo",
          "necessidade",
          "caçadores",
          "eles",
          "inimigo",
          "sempre",
          "mundo",
          "própria",
          "deus",
          "perceber",
          "propagação",
          "energia",
          "diante",
          "viver",
          "passado",
          "vivido"
        ],
        "entities": [
          [
            "27",
            "CARDINAL"
          ],
          [
            "povos indígenas contam",
            "ORG"
          ],
          [
            "para suas esposas e",
            "PERSON"
          ],
          [
            "de Tupã",
            "PERSON"
          ],
          [
            "Seu",
            "ORG"
          ],
          [
            "li -\\nvre",
            "PERSON"
          ],
          [
            "Akuanduba",
            "GPE"
          ],
          [
            "traz",
            "NORP"
          ],
          [
            "harmonia",
            "GPE"
          ],
          [
            "Conta-se",
            "PERSON"
          ]
        ],
        "readability_score": 85.95342163355409,
        "semantic_density": 0,
        "word_count": 302,
        "unique_words": 186,
        "lexical_diversity": 0.6158940397350994
      },
      "preservation_score": 1.2896695950305296e-05
    },
    {
      "id": 1,
      "text": "— 28 —dia livre) só para termos uma base em uma linha de raciocínio, \\nlembrando que é só para referência do estudo de cada texto, \\ncada tópico foi muito mais amplo que “apenas” o que se en -\\ncontra escrito no texto, essa necessidade de se usar os textos é \\npara se ter uma facilidade em compreender o direcionamento \\na qual o livro quer passar.\\nPrimeira religião monoteísta1\\nParte 2\\nZoroastro, também chamado Zaratustra, foi um líder religioso \\nque viveu na região onde hoje se localizam o Irã e o Afeganis -\\ntão. Não existe um consenso sobre em que século teria vivido, \\nporém é provável que tenha vivido por volta do século VII a.C. \\nO zoroastrismo é uma religião persa. Os seguidores do zoroas -\\ntrismo deveriam “fazer sempre o bem” e prestar culto a Ormu -\\nzd, pois assim estariam fortalecendo o lado do bem no grande \\nconflito entre o bem e o mal.\\nOs seguidores do zoroastrismo acreditam na ressurreição, bem \\ncomo no paraíso, no purgatório e no inferno, tal como é prega -\\ndo no cristianismo. Da mesma forma, essa religião acredita na \\nprofecia do fim dos tempos.\\nA primeira religião monoteísta (religião que acredita em um \\nsó Deus) é muito semelhante a religião cristã, por quê? \\nAproximadamente 500 d.C. “foi o começo de um dos piores \\nperíodos, senão o pior” para estar vivo.\\nNaquele ano, uma misteriosa névoa cobriu Europa, Oriente \\n1.  Texto baseado em https://pt.m.wikipedia.org/wiki/Zara tustra .\\ncaos do passado sendo vivido no futuro editável.indd   28caos do passado sendo vivido no futuro editável.indd   28 28/03/2022   14:53:3728/03/2022   14:53:37",
      "position": 34852,
      "chapter": 1,
      "page": 28,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 23.188498098859313,
      "complexity_metrics": {
        "word_count": 263,
        "sentence_count": 20,
        "paragraph_count": 1,
        "avg_sentence_length": 13.15,
        "avg_word_length": 4.8783269961977185,
        "unique_word_ratio": 0.6387832699619772,
        "avg_paragraph_length": 263.0,
        "punctuation_density": 0.1482889733840304,
        "line_break_count": 26,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "religião",
          "vivido",
          "texto",
          "cada",
          "muito",
          "essa",
          "primeira",
          "século",
          "zoroastrismo",
          "seguidores",
          "como",
          "acredita",
          "passado",
          "sendo",
          "futuro",
          "editável",
          "indd",
          "livre",
          "termos",
          "base"
        ],
        "entities": [
          [
            "28",
            "CARDINAL"
          ],
          [
            "dia",
            "ORG"
          ],
          [
            "para referência",
            "PERSON"
          ],
          [
            "de cada",
            "PERSON"
          ],
          [
            "cada",
            "GPE"
          ],
          [
            "foi muito mais amplo",
            "PERSON"
          ],
          [
            "essa necessidade de se usar",
            "PERSON"
          ],
          [
            "para se",
            "PERSON"
          ],
          [
            "2",
            "CARDINAL"
          ],
          [
            "Zoroastro",
            "GPE"
          ]
        ],
        "readability_score": 91.96150190114068,
        "semantic_density": 0,
        "word_count": 263,
        "unique_words": 168,
        "lexical_diversity": 0.6387832699619772
      },
      "preservation_score": 1.0425254499116206e-05
    },
    {
      "id": 1,
      "text": "— 29 —Médio e partes da Ásia por 18 meses. O sol perdeu a intensida -\\nde do brilho e as temperaturas caíram até 2,5 graus, iniciando \\na década mais fria dos últimos anos.\\nNesse mesmo período, foi quando surgiram grandes profetas \\ne messias, o cataclismo gerou muita energia se propagando \\npara todos os lados em ondas como se fossem tsunami, crian -\\ndo grandes condutores de energia. Zaratustra foi o primeiro a \\nrelatar essa captação de energia divina semelhante a de Jesus, \\ndevido a ele viver em uma quantidade de pessoas e espaço ter -\\nritorial grande (tamanho de dois países), a captação da onda \\nde energia em volta é escassa por ter muita massa escura, se \\ntornando mais perceptível uma frequência pela canalização do \\ncaos para si próprio, ocorrendo uma canalização de energia de -\\nvido ao caos sempre estar com mais frequência do que a ener -\\ngia, tornando ter mais acesso à onda por ter menos quantidade \\nde ondas de energia presente.\\nAnalogia\\nFrequências semelhantes a de uma estação de rádio. Temos 100 \\npessoas ouvindo rádio, para essas 100 pessoas, temos 10 rádios \\ndiferentes, temos uma frequência específica de uma rádio que \\nvibra em uma frequência, com hertz que só uma pessoa a cada \\n100 escuta com clareza, o deixando o mais tempo escutando \\naquela estação, pois estava em uma frequência que ele esta -\\nva como se estivesse hipnotizado, satisfeito, êxtase, feliz e uma \\nenergia indescritível.\\nAgora vamos melhorar isso aí, tiramos todos as rádios do ar, \\ndeu uma pane elétrica e só ficou aquela, pois ela trabalhava em \\numa frequência muito baixa, porém poucos conseguem en -\\ntender e compreender de tantas informações que continham \\nnaquela frequência, mas tinha aquele um que conseguia captar \\ncom perfeição aquela frequência, conseguindo fazer a todos \\ncaos do passado sendo vivido no futuro editável.indd   29caos do passado sendo vivido no futuro editável.indd   29 28/03/2022   14:53:3728/03/2022   14:53:37",
      "position": 36535,
      "chapter": 1,
      "page": 29,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 34.27589098532495,
      "complexity_metrics": {
        "word_count": 318,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 35.333333333333336,
        "avg_word_length": 4.9937106918239,
        "unique_word_ratio": 0.6069182389937107,
        "avg_paragraph_length": 318.0,
        "punctuation_density": 0.11635220125786164,
        "line_break_count": 31,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "frequência",
          "energia",
          "mais",
          "todos",
          "pessoas",
          "caos",
          "rádio",
          "temos",
          "aquela",
          "grandes",
          "muita",
          "ondas",
          "como",
          "captação",
          "quantidade",
          "onda",
          "tornando",
          "canalização",
          "estação",
          "rádios"
        ],
        "entities": [
          [
            "29",
            "CARDINAL"
          ],
          [
            "Ásia",
            "GPE"
          ],
          [
            "18",
            "CARDINAL"
          ],
          [
            "2,5",
            "CARDINAL"
          ],
          [
            "década mais",
            "PERSON"
          ],
          [
            "últimos anos",
            "PERSON"
          ],
          [
            "Nesse",
            "ORG"
          ],
          [
            "foi quando",
            "PERSON"
          ],
          [
            "gerou muita",
            "PERSON"
          ],
          [
            "propagando",
            "GPE"
          ]
        ],
        "readability_score": 80.83522012578617,
        "semantic_density": 0,
        "word_count": 318,
        "unique_words": 193,
        "lexical_diversity": 0.6069182389937107
      },
      "preservation_score": 1.0848096989290151e-05
    },
    {
      "id": 1,
      "text": "— 30 —em sua volta compreender aquela frequência que eles sabiam \\nque estavam ali, porém não compreendia e nem entendiam, só \\nsentiam que tinha algo.\\nTeoria\\nAssim é o mundo quântico (vejo como mundo, pois é uma \\ndimensão desconhecida), energia contínua sem existência de \\ntempo, ali a energia só existe se propagando constantemen -\\nte, sem tempo para medir e nem para colocar um término de \\ncomo ela se propaga, pois o nosso planeta passou por uma \\ngrande energia para ser criado e essa energia se mantém, não \\nimporta como ela foi criada, pois nós temos uma relevância no \\ncomportamento do universo, galáxias, sistemas solares e plane -\\ntas e o que acontece a um planeta afeta ao outro, que afeta a um \\nsistema, afetando o sistema afeta a galáxia, afetando a galáxia \\nafeta o universo, virando um único ciclo de energia dentro da \\nmassa escura, as conduzindo como rotas da energia, em uma \\nconstância de movimento de ondas contínua, sem propagação \\nde tempo simplesmente um vácuo de luz!!\\nComo assim nós afetamos o universo? \\nNós temos um planeta com várias engrenagens: atmosfera, \\ncrosta, manto superior, manto, núcleo externo e núcleo inter -\\nno, nessas camadas, temos peso sobre elas, mantendo em um \\njogo de engrenagens de peso e contrapeso e tornando necessá -\\nrio manter o mesmo peso exercido sobre a camada. \\nNessas camadas, temos na atmosfera a camada de ozônio, que \\né formada através de oxigênio e dióxido de carbono, elas têm \\nque se manter em um nível de estabilidade para manter um \\nclima na terra favorável, se aumentar a quantidade de dióxido \\nde carbono na camada de ozônio, nós aumentamos o calor na \\nTerra, aumentando o calor na Terra estamos afetando a camada \\nda crosta terrestre, afetando a crosta terrestre com o degelo das \\ncaos do passado sendo vivido no futuro editável.indd   30caos do passado sendo vivido no futuro editável.indd   30 28/03/2022   14:53:3728/03/2022   14:53:37",
      "position": 38583,
      "chapter": 1,
      "page": 30,
      "segment_type": "page",
      "themes": {
        "filosofia": 53.57142857142857,
        "ciencia": 46.42857142857144
      },
      "difficulty": 45.06435331230284,
      "complexity_metrics": {
        "word_count": 317,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 45.285714285714285,
        "avg_word_length": 4.914826498422713,
        "unique_word_ratio": 0.583596214511041,
        "avg_paragraph_length": 317.0,
        "punctuation_density": 0.138801261829653,
        "line_break_count": 31,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "como",
          "temos",
          "afeta",
          "afetando",
          "camada",
          "pois",
          "tempo",
          "planeta",
          "universo",
          "crosta",
          "peso",
          "manter",
          "terra",
          "assim",
          "mundo",
          "contínua",
          "sistema",
          "galáxia",
          "engrenagens"
        ],
        "entities": [
          [
            "30",
            "CARDINAL"
          ],
          [
            "aquela frequência",
            "PERSON"
          ],
          [
            "nem entendiam",
            "PERSON"
          ],
          [
            "só \\nsentiam que",
            "PERSON"
          ],
          [
            "Teoria\\nAssim",
            "ORG"
          ],
          [
            "vejo como mundo",
            "ORG"
          ],
          [
            "nem para",
            "PERSON"
          ],
          [
            "ela se propaga",
            "PERSON"
          ],
          [
            "essa",
            "GPE"
          ],
          [
            "importa",
            "NORP"
          ]
        ],
        "readability_score": 75.88269490761604,
        "semantic_density": 0,
        "word_count": 317,
        "unique_words": 185,
        "lexical_diversity": 0.583596214511041
      },
      "preservation_score": 1.1752105071730996e-05
    },
    {
      "id": 1,
      "text": "— 31 —geleiras tanto no polo norte e polo sul, desbalanceado o peso \\nnos dois polos da crosta terrestre, mais o consumo excessivo de \\nágua dos lençóis freáticos, rios, nascentes, petróleo, os tirando \\nde um lado da crosta para o oceano ou para consumo, alteran -\\ndo ainda mais o peso na crosta terrestre. Logo abaixo da crosta, \\ntemos a camada do manto superior, que é formada de magma \\njunto com placas tectônicas se mexendo em uma sincronia \\ncom o peso da crosta, que, com a ausência de peso e contrape -\\nso corretamente, altera o eixo vertical da Terra modificando o \\nclima no planeta, criando mais terremotos, tendo mais vulcões \\nativos, pois o magma perdeu o equilíbrio com a crosta, assim \\nque ele localizar uma saída (vulcão), ele irá expelir, mais fura -\\ncões, pois temos mais dióxido de carbono na camada da Terra, \\ndeixando-a mais quente, interferindo na atmosfera junto com \\na crosta, deixando com muita diferença de temperatura, crian -\\ndo mais furacões.\\nMudando o eixo da Terra, nós mudamos o eixo gravitacional \\ndo sistema solar, mudando o eixo gravitacional do sistema so -\\nlar, mudamos o eixo gravitacional da galáxia, mudando o eixo \\ngravitacional da galáxia, mudamos o eixo gravitacional do uni -\\nverso.\\nAssim eu vejo o dano colateral em grande escala, porém, a \\nnossa energia exercida é muito pequena para o universo, pois, \\nassim como o universo tem o caos “massa escura” dele, o pró -\\nprio caos dele faz a massa escura se expandir, assim fazendo o \\nuniverso sempre expandir devido ao próprio movimento. Ele \\ntambém têm a energia que se propaga na direção de manter o \\nuniverso em constante sincronia como uma energia, que não \\nse propaga e, sim, se mantém em constância e a todo espaço \\ntempo!!\\ncaos do passado sendo vivido no futuro editável.indd   31caos do passado sendo vivido no futuro editável.indd   31 28/03/2022   14:53:3728/03/2022   14:53:37",
      "position": 40604,
      "chapter": 1,
      "page": 31,
      "segment_type": "page",
      "themes": {},
      "difficulty": 39.40981012658228,
      "complexity_metrics": {
        "word_count": 316,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 39.5,
        "avg_word_length": 4.841772151898734,
        "unique_word_ratio": 0.5632911392405063,
        "avg_paragraph_length": 316.0,
        "punctuation_density": 0.1550632911392405,
        "line_break_count": 30,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "crosta",
          "eixo",
          "gravitacional",
          "peso",
          "assim",
          "universo",
          "terra",
          "pois",
          "mudando",
          "mudamos",
          "energia",
          "caos",
          "polo",
          "terrestre",
          "consumo",
          "temos",
          "camada",
          "magma",
          "junto"
        ],
        "entities": [
          [
            "31",
            "CARDINAL"
          ],
          [
            "da crosta terrestre",
            "PERSON"
          ],
          [
            "freáticos",
            "GPE"
          ],
          [
            "lado da crosta",
            "PERSON"
          ],
          [
            "ainda mais",
            "PERSON"
          ],
          [
            "crosta terrestre",
            "PERSON"
          ],
          [
            "da crosta",
            "PERSON"
          ],
          [
            "placas",
            "GPE"
          ],
          [
            "mexendo em uma sincronia \\n",
            "ORG"
          ],
          [
            "da crosta",
            "PERSON"
          ]
        ],
        "readability_score": 78.79746835443038,
        "semantic_density": 0,
        "word_count": 316,
        "unique_words": 178,
        "lexical_diversity": 0.5632911392405063
      },
      "preservation_score": 1.3778832869461282e-05
    },
    {
      "id": 1,
      "text": "— 32 —Religião moderna\\nParte 3\\nCom o aumento do caos, o nosso costume de vivermos em \\ncaos e a necessidade de sempre nos adaptarmos ao caos pela \\nnecessidade de sobrevivência de uma espécie receptiva a enten -\\nder e interpretar as energias, diante de manter uma harmonia \\nentre o viver energia e físico, tivemos pessoas receptivas a uma \\nenergia de ensinamento, de um melhor para se viver em har -\\nmonia dentro de um conjunto de pessoas e local, de comer o \\nque é necessário, amar ao próximo como a si mesmo e outros \\ndirecionamentos de sempre se viver em uma harmonia.\\nAí vem outros problemas catastróficos, perante receber a ener -\\ngia e interpretar diante de si próprio como razão, perante a \\nnecessidade de outras pessoas de qual energia era “certa” , de \\nqual religião é a “certa” , qual Deus era mais “forte” . Só existe \\n“um” criador.\\nReligião e o caos criado ao decorrer dos tempos\\nParte 4\\nNo decorrer dos tempos, tivemos muitas guerras de objetivos \\nmonetários, sobrevivência, ganância, mulher e, na maioria das \\nvezes, levavam a religião como estímulo para atrair o maior \\nnúmero de pessoas que vão lutar pelo mesmo propósito, trans -\\nformando no primeiro marketing da história de recrutamento \\nperante uma causa maior que a sua própria vida, pois sua vida \\nserá eterna diante do seu sacrifício para um bem maior. Irei ci -\\ntar algumas guerras que, ao meu ver, tiveram muitos soldados \\ncaos do passado sendo vivido no futuro editável.indd   32caos do passado sendo vivido no futuro editável.indd   32 28/03/2022   14:53:3728/03/2022   14:53:37",
      "position": 42592,
      "chapter": 1,
      "page": 32,
      "segment_type": "page",
      "themes": {
        "filosofia": 42.857142857142854,
        "arte": 57.14285714285714
      },
      "difficulty": 35.303530689842475,
      "complexity_metrics": {
        "word_count": 263,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 37.57142857142857,
        "avg_word_length": 4.821292775665399,
        "unique_word_ratio": 0.6045627376425855,
        "avg_paragraph_length": 263.0,
        "punctuation_density": 0.11406844106463879,
        "line_break_count": 26,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "caos",
          "religião",
          "pessoas",
          "necessidade",
          "diante",
          "viver",
          "energia",
          "como",
          "perante",
          "qual",
          "maior",
          "parte",
          "sempre",
          "sobrevivência",
          "interpretar",
          "harmonia",
          "tivemos",
          "mesmo",
          "outros",
          "certa"
        ],
        "entities": [
          [
            "32",
            "CARDINAL"
          ],
          [
            "3",
            "CARDINAL"
          ],
          [
            "diante de manter",
            "PERSON"
          ],
          [
            "físico",
            "GPE"
          ],
          [
            "tivemos pessoas",
            "ORG"
          ],
          [
            "monia dentro de um conjunto de pessoas e local",
            "ORG"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "amar",
            "PERSON"
          ],
          [
            "catastróficos",
            "PRODUCT"
          ],
          [
            "diante de si próprio como razão",
            "PERSON"
          ]
        ],
        "readability_score": 79.7678978815861,
        "semantic_density": 0,
        "word_count": 263,
        "unique_words": 159,
        "lexical_diversity": 0.6045627376425855
      },
      "preservation_score": 8.529753681095077e-06
    },
    {
      "id": 1,
      "text": "— 33 —em prol da mesma causa, em nome de alguma divindade como \\nimpulso, junto com a necessidade de ter mais terras, mais re -\\ncursos, mais luxo, mais conquista, mais necessidade diante do \\noutro, minha vida vale mais que a sua.\\nEgito2 \\nDesde 5000 a.C., o Egito era habitado por povos que viviam \\nem clãs, chamados nomos. Esses nomos eram independentes \\nuns dos outros, mas cooperavam entre si quando tinham pro -\\nblemas em comum. Essas relações evoluíram e levaram a for -\\nmação de dois reinos independentes:\\n• Reino do Baixo Egito união dos nomos do Norte.\\n• Reino do Alto Egito união dos nomos do Sul.\\nPor volta de 3200 a.C., esses dois reinos foram unificados por \\nMenés, que se tornou o primeiro faraó, considerado um ver -\\ndadeiro Deus na Terra. O faraó usava uma coroa dupla para \\ndemonstrar que era o rei do Alto e Baixo Egito.\\nNo meio desse período, teve um outro fator histórico que foi \\na fuga dos hebreus da Mesopotâmia para Canaã (Palestina, Je -\\nrusalém, faixa de Gaza), comandada por Abraão a mando de \\nDeus.\\nChegando na Palestina, os hebreus tiveram que enfrentar ou -\\ntros povos que já habitavam a região, os cananeus e os filisteus. \\nDepois de algumas lutas, os hebreus acabaram conquistando \\numa parte da Palestina para si e se fixaram na terra que Deus \\nprometeu para eles. \\nPorém, na “Terra Prometida” , a agricultura não era muito fértil, \\n2.  Texto baseado em https://pt.m.wikipedia.org/wiki/Antigo _Egito .\\ncaos do passado sendo vivido no futuro editável.indd   33caos do passado sendo vivido no futuro editável.indd   33 28/03/2022   14:53:3728/03/2022   14:53:37",
      "position": 44260,
      "chapter": 1,
      "page": 33,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 22.741922946941536,
      "complexity_metrics": {
        "word_count": 269,
        "sentence_count": 22,
        "paragraph_count": 1,
        "avg_sentence_length": 12.227272727272727,
        "avg_word_length": 4.821561338289963,
        "unique_word_ratio": 0.6654275092936803,
        "avg_paragraph_length": 269.0,
        "punctuation_density": 0.18587360594795538,
        "line_break_count": 27,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "egito",
          "nomos",
          "deus",
          "terra",
          "hebreus",
          "palestina",
          "necessidade",
          "outro",
          "povos",
          "esses",
          "independentes",
          "dois",
          "reinos",
          "reino",
          "baixo",
          "união",
          "alto",
          "faraó",
          "passado"
        ],
        "entities": [
          [
            "33",
            "CARDINAL"
          ],
          [
            "mais luxo",
            "PERSON"
          ],
          [
            "mais conquista",
            "PERSON"
          ],
          [
            "Egito",
            "GPE"
          ],
          [
            "outros",
            "GPE"
          ],
          [
            "si quando tinham pro -\\nblemas",
            "ORG"
          ],
          [
            "Essas",
            "GPE"
          ],
          [
            "Baixo Egito",
            "ORG"
          ],
          [
            "Norte",
            "PERSON"
          ],
          [
            "Alto Egito",
            "ORG"
          ]
        ],
        "readability_score": 92.43989523487664,
        "semantic_density": 0,
        "word_count": 269,
        "unique_words": 179,
        "lexical_diversity": 0.6654275092936803
      },
      "preservation_score": 1.220410911295142e-05
    },
    {
      "id": 1,
      "text": "— 34 —eles passaram por uma época de seca. Por isso, mais tarde Jacó \\nconvidou os hebreus para migrarem para a Civilização Egípcia. \\nNo Egito, eles encontraram condições favoráveis para se esta -\\nbelecerem. Sua chegada à região coincidiu com o período de \\ndominação dos hicsos, que haviam derrubado o faraó, impon -\\ndo-se no poder. \\nApós a expulsão dos hicsos, derrotados por volta de 1600 a.C., \\nos hebreus começaram a ser perseguidos e obrigados a pagar \\naltos impostos até serem escravizados. \\nE foi a partir disso que Moisés liderou o processo chamado \\nÊxodo do Egito.\\nBabilônia x Jerusalém3\\nA primeira destruição ocorreu na terceira deportação pelos \\nbabilônios no ano 586 a.C., pelos exércitos da Babilônia, co -\\nmandados pelo rei Nabucodonosor II, sitiou Jerusalém pela \\nprimeira vez. O profeta Daniel viveu durante todo o período \\nem que os babilônios dominavam sobre o povo judeu e ficou \\naté o início do domínio Persa. Por volta do 19º ano de Nabu -\\ncodonosor em 587 a.C., Jerusalém foi destruída no seu terceiro \\nsítio. Tanto as muralhas da cidade quanto o templo de Jerusa -\\nlém (cuja construção era atribuída ao rei Salomão e que por \\nisso era chamado de O Templo de Salomão) foram destruídos. \\nO resto da cidade ficou em ruínas durante pouco mais de um \\nséculo até a reconstrução da cidade. Essa foi a primeira e do -\\nlorosa destruição tanto do templo como de Jerusalém que o \\npovo judeu sofreu. \\n3.  Texto baseado em  https://pt.m.wikipedia.org/wiki/Destrui%C3%A7% -\\nC3%A3o_de_Jerusal% C3%A9m .\\ncaos do passado sendo vivido no futuro editável.indd   34caos do passado sendo vivido no futuro editável.indd   34 28/03/2022   14:53:3728/03/2022   14:53:37",
      "position": 45963,
      "chapter": 1,
      "page": 34,
      "segment_type": "page",
      "themes": {},
      "difficulty": 23.919344308827704,
      "complexity_metrics": {
        "word_count": 271,
        "sentence_count": 26,
        "paragraph_count": 1,
        "avg_sentence_length": 10.423076923076923,
        "avg_word_length": 5.051660516605166,
        "unique_word_ratio": 0.6531365313653137,
        "avg_paragraph_length": 271.0,
        "punctuation_density": 0.14760147601476015,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "primeira",
          "jerusalém",
          "cidade",
          "templo",
          "eles",
          "isso",
          "mais",
          "hebreus",
          "egito",
          "período",
          "hicsos",
          "volta",
          "chamado",
          "babilônia",
          "destruição",
          "pelos",
          "babilônios",
          "durante",
          "povo",
          "judeu"
        ],
        "entities": [
          [
            "34",
            "CARDINAL"
          ],
          [
            "para migrarem",
            "PERSON"
          ],
          [
            "para se esta -\\nbelecerem",
            "PERSON"
          ],
          [
            "Sua",
            "PERSON"
          ],
          [
            "Após",
            "PERSON"
          ],
          [
            "Moisés",
            "ORG"
          ],
          [
            "liderou o",
            "PERSON"
          ],
          [
            "Egito",
            "PERSON"
          ],
          [
            "Babilônia",
            "PERSON"
          ],
          [
            "terceira deportação pelos",
            "PERSON"
          ]
        ],
        "readability_score": 93.27296338347999,
        "semantic_density": 0,
        "word_count": 271,
        "unique_words": 177,
        "lexical_diversity": 0.6531365313653137
      },
      "preservation_score": 1.061480458091832e-05
    },
    {
      "id": 1,
      "text": "— 35 —Antes de Roma tomar a Palestina, ia nascer o messias do he -\\nbreus Jesus de Nazaré, Jesus nada mais nada menos é a energia \\nfísica que mais se propagou até hoje, nosso calendário junto ao \\nnosso tempo de vida é marcado devido ao nascimento de Jesus \\nde Nazaré, o “verdadeiro filho de Deus” .\\nRoma x Jerusalém\\nCom a derrota da Grande Revolta Judaica contra o domínio \\nromano, em 70, Jerusalém foi tomada pelas forças do coman -\\ndante romano, Tito. Outra vez, as muralhas e o Templo de Je -\\nrusalém foram destruídos e o resto da cidade voltou a ficar em \\nruínas. A destruição de Jerusalém, também conhecida como \\nCerco de Jerusalém.\\nRoma x Jerusalém segunda derrota4\\nEm 135, o imperador Adriano mandou arrasar a cidade, ao \\ncabo da revolta judaica liderada por Simão Barcoquebas. Sobre \\nos restos de Jerusalém, edificou-se uma cidade helênica e sobre \\no monte onde se erguera o santuário de Javé, erigiu-se um tem -\\nplo dedicado a Júpiter Capitolino.\\nEssa foi a última destruição que colocou um fim de vez em al -\\nguma tentativa de reerguer o templo. Popularmente conheci -\\ndo como o muro das lamentações. Os judeus foram proibidos \\nde viver próximo a Jerusalém e cerca de 900 aldeias judaicas \\nna Judeia foram completamente destruídas e seus moradores \\nmortos, escravizados ou banidos da região.\\nReligião oriente\\n4.  Texto baseado em https://pt.m.wikipedia.org/wiki/Destrui%C3%A7% -\\nC3%A3o_de_Jerusal% C3%A9m .\\ncaos do passado sendo vivido no futuro editável.indd   35caos do passado sendo vivido no futuro editável.indd   35 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 47745,
      "chapter": 1,
      "page": 35,
      "segment_type": "page",
      "themes": {},
      "difficulty": 24.182284541723668,
      "complexity_metrics": {
        "word_count": 258,
        "sentence_count": 17,
        "paragraph_count": 1,
        "avg_sentence_length": 15.176470588235293,
        "avg_word_length": 5.01937984496124,
        "unique_word_ratio": 0.6744186046511628,
        "avg_paragraph_length": 258.0,
        "punctuation_density": 0.13565891472868216,
        "line_break_count": 27,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "jerusalém",
          "roma",
          "jesus",
          "cidade",
          "nazaré",
          "nada",
          "mais",
          "nosso",
          "revolta",
          "judaica",
          "romano",
          "templo",
          "destruição",
          "como",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd"
        ],
        "entities": [
          [
            "35",
            "CARDINAL"
          ],
          [
            "Antes de Roma",
            "PERSON"
          ],
          [
            "Jesus de Nazaré",
            "PERSON"
          ],
          [
            "Jesus nada",
            "PERSON"
          ],
          [
            "nada",
            "GPE"
          ],
          [
            "propagou até hoje",
            "ORG"
          ],
          [
            "de Jesus \\nde Nazaré",
            "PERSON"
          ],
          [
            "filho de Deus",
            "PERSON"
          ],
          [
            "contra",
            "NORP"
          ],
          [
            "70",
            "DATE"
          ]
        ],
        "readability_score": 90.90595075239398,
        "semantic_density": 0,
        "word_count": 258,
        "unique_words": 174,
        "lexical_diversity": 0.6744186046511628
      },
      "preservation_score": 9.448342539059164e-06
    },
    {
      "id": 1,
      "text": "— 36 —Não tenho muitos relatos e muitos estudos, pois me parece \\nque não se têm muitas escritas e além de não se ter muitas \\nescritas, a cultura chinesa, japonesa, a cultura oriental é muito \\nfechada, dificultando um estudo mais profundo sobre as guer -\\nras, os profetas, os messias, os mensageiros, os condutores de \\nenergia perante a percepção para um valor de necessidade lo -\\ncal, cidade, estado e país.\\nPorém, não irei deixar de mostrar que a onda de energia que se \\npropagou no ocidente também se propagou no oriente!!\\nA dinastia Xia é algo mítico. A tradição chinesa diz que os hu -\\nmanos têm a sua origem nos parasitas do corpo do criador, \\nPangu. A seguir ao seu óbito, governantes sábios introduziram \\nas invenções e instituições fundamentais da sociedade huma -\\nna. O primeiro governante chamava-se Fuxi, que domesticou \\nos animais e instituiu o casamento. Depois foi Shennong, que \\nintroduziu a agricultura, a medicina e o comércio. Mais tarde \\nveio Huangdi, o Imperador Amarelo, a quem foi atribuída a \\ninvenção da escrita, da cerâmica e do calendário. Séculos mais \\ntarde surgiu o imperador Yao, que governou sabiamente e in -\\ntroduziu o controle de cheias. O seu feito mais notório foi a \\nsua decisão de não eleger o filho como futuro imperador, por \\nnão o considerar digno, mas um sábio humilde de nome Shun. \\nOs reinados de Shun e Yao seriam mais tarde admirados como \\numa idade dourada. Voltando ao tema, Shun nomeou por sua \\nvez o seu fiel ministro Yu como sucessor. O reinado de Yu teve \\ninício aproximadamente em 2200 a.C., Yu terá alegadamente \\nfundado a Dinastia Xia, a primeira das três dinastias da China \\nantiga: Xia, Shang e Zhou.\\ncaos do passado sendo vivido no futuro editável.indd   36caos do passado sendo vivido no futuro editável.indd   36 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 49433,
      "chapter": 1,
      "page": 36,
      "segment_type": "page",
      "themes": {},
      "difficulty": 25.0640522875817,
      "complexity_metrics": {
        "word_count": 306,
        "sentence_count": 18,
        "paragraph_count": 1,
        "avg_sentence_length": 17.0,
        "avg_word_length": 4.8431372549019605,
        "unique_word_ratio": 0.6470588235294118,
        "avg_paragraph_length": 306.0,
        "punctuation_density": 0.16339869281045752,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "tarde",
          "imperador",
          "como",
          "futuro",
          "shun",
          "muitos",
          "muitas",
          "escritas",
          "cultura",
          "chinesa",
          "energia",
          "propagou",
          "dinastia",
          "passado",
          "sendo",
          "vivido",
          "editável",
          "indd",
          "tenho"
        ],
        "entities": [
          [
            "36",
            "CARDINAL"
          ],
          [
            "têm muitas escritas e além de não se",
            "ORG"
          ],
          [
            "muito \\nfechada",
            "PERSON"
          ],
          [
            "guer -\\nras",
            "ORG"
          ],
          [
            "condutores de \\nenergia",
            "PERSON"
          ],
          [
            "Porém",
            "ORG"
          ],
          [
            "deixar de mostrar",
            "PERSON"
          ],
          [
            "Xia",
            "PERSON"
          ],
          [
            "Pangu",
            "GPE"
          ],
          [
            "governantes",
            "ORG"
          ]
        ],
        "readability_score": 90.04705882352941,
        "semantic_density": 0,
        "word_count": 306,
        "unique_words": 198,
        "lexical_diversity": 0.6470588235294118
      },
      "preservation_score": 1.1839589724870433e-05
    },
    {
      "id": 1,
      "text": "— 37 —Budismo5\\nO budismo é uma religião indiana baseada nos ensinamentos \\nde Sidarta Gautama, conhecido como o Buda mais famoso. De \\ncaráter filosófico e não teísta!!\\nComo expresso nas Quatro Nobres Verdades do Buda, a meta \\ndo budismo é a superação do sofrimento causado pelo desejo e \\npela ignorância em relação à verdadeira natureza da realidade. \\nA maioria das tradições budistas se concentram na superação \\ndo eu individual através da conquista do nirvana (meditação) \\nou da busca do caminho de Buda, o que leva ao fim do ciclo de \\nmorte e renascimento. As bases de todas as tradições e práticas \\nsão as Três Joias: o Buda (captador, messias), o dharma (propa -\\ngador, profeta) e a sangha (povo, civilização). Outras práticas \\nincluem a renúncia à vida secular para se tornar um monge \\nou monja, a meditação e o cultivo da dor do próximo nos faz \\ninterpretar melhor um viver.\\nA uma singularidade de comportamento diante do caos, e essa \\nsingularidade ocorreu devido aos seres humanos ocasionar \\nmuito caos com guerras, interpretação (pessoas) incorreta da \\nenergia sentida, excessos de si próprio. Como assim? Todos nós \\nqueremos um estilo de vida, um conforto de vida, qual é o \\nconforto de vida que você deseja para si próprio? Assim, conti -\\nnuamos a retirar mais do que o necessário, afetando a balança \\npara um lado a mais que o outro, ocasionando desbalancea -\\nmento territorial, cultural, religioso (energia), necessidade de \\ncada um, interpretação de sua própria necessidade como mais \\nrelevante, querer ser melhor para ter mais status  social para \\nconquistar as melhores mulheres. Assim, o ser humano come -\\nçou a vida moderna em que hoje nos encontramos.\\n5.  Texto baseado em https://pt.m.wikipedia.org/wiki/B udismo .\\ncaos do passado sendo vivido no futuro editável.indd   37caos do passado sendo vivido no futuro editável.indd   37 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 51363,
      "chapter": 1,
      "page": 37,
      "segment_type": "page",
      "themes": {},
      "difficulty": 24.622511724856697,
      "complexity_metrics": {
        "word_count": 303,
        "sentence_count": 19,
        "paragraph_count": 1,
        "avg_sentence_length": 15.947368421052632,
        "avg_word_length": 5.145214521452146,
        "unique_word_ratio": 0.6501650165016502,
        "avg_paragraph_length": 303.0,
        "punctuation_density": 0.1551155115511551,
        "line_break_count": 30,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "vida",
          "como",
          "buda",
          "caos",
          "assim",
          "budismo",
          "superação",
          "tradições",
          "meditação",
          "práticas",
          "melhor",
          "singularidade",
          "interpretação",
          "energia",
          "próprio",
          "conforto",
          "necessidade",
          "passado",
          "sendo"
        ],
        "entities": [
          [
            "37",
            "CARDINAL"
          ],
          [
            "indiana baseada",
            "PERSON"
          ],
          [
            "Quatro Nobres",
            "FAC"
          ],
          [
            "Buda",
            "PERSON"
          ],
          [
            "pelo desejo e",
            "PERSON"
          ],
          [
            "pela ignorância em relação",
            "PERSON"
          ],
          [
            "verdadeira natureza",
            "PERSON"
          ],
          [
            "do eu",
            "PERSON"
          ],
          [
            "nirvana (meditação) \\nou da busca",
            "ORG"
          ],
          [
            "de Buda",
            "PERSON"
          ]
        ],
        "readability_score": 90.48275143303803,
        "semantic_density": 0,
        "word_count": 303,
        "unique_words": 197,
        "lexical_diversity": 0.6501650165016502
      },
      "preservation_score": 1.4216256135158465e-05
    },
    {
      "id": 1,
      "text": "— 38 —Se você vê as datas de grandes receptores de energia, evolução \\ndo comportamento humano, ele se transforma proporcional à \\ndata do cataclismo.\\nAntes de ocorrer o cataclismo (apocalipse), como o mundo \\nestava? Ele estava, no termo religioso cristão, uma Sodoma e \\nGomorra... kkkkkkkk E assim os povos, as cidades, os países \\nforam afunilando mais ainda a energia vital do nosso planeta, \\ngerando um quasar. O que seria um quasar?\\nNão temos um estudo de ter um entendimento sobre, mas vou \\ntentar explicar como eu vejo.\\nQuasar é a massa da energia sendo concentrada e comprimida \\npor um buraco negro e expelido quando o próprio buraco ne -\\ngro não consegue conter, expelindo energia (quasar), como se \\nfosse a teoria do Big Bang  e assim funciona o nosso planeta Ter -\\nra. Nós vamos comprimindo a energia através do nosso caos, \\ngerando caminhos de energia mais concentrados e receptivos \\ndiante de sua própria interpretação pela mesma energia emiti -\\nda. Antes de acontecer o cataclismo, nós estávamos com muita \\nmassa negra em nossa volta, com poucos vórtices de energia \\nem nosso planeta, com uma sensação de caos e necessidade de \\nconter o cataclismo que ia vir futuramente, ocasionando uma \\nmaior captação da frequência da energia diante da necessidade \\ndo nosso planeta Terra, sendo interpretada como necessária e \\nrelativa para cada local, tribo, cidade, estado, país para um bem \\nmaior de um planeta Terra (relação de balanceamento).\\nBuraco negro – É igual ao nosso corpo humano aprendendo \\na viver a vida. Como assim? Nós nascemos sem saber nada e, \\nno decorrer da vida, nós vivemos e aprendemos, geramos caos \\ne nos adaptamos ao caos, ou geramos energia e nos adaptamos \\nà energia, ambos em combinação um com o outro e ambos \\nprecisando um do outro para evoluir. Assim é o universo em \\ncaos do passado sendo vivido no futuro editável.indd   38caos do passado sendo vivido no futuro editável.indd   38 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 53370,
      "chapter": 1,
      "page": 38,
      "segment_type": "page",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 29.293478260869566,
      "complexity_metrics": {
        "word_count": 322,
        "sentence_count": 15,
        "paragraph_count": 1,
        "avg_sentence_length": 21.466666666666665,
        "avg_word_length": 4.978260869565218,
        "unique_word_ratio": 0.6149068322981367,
        "avg_paragraph_length": 322.0,
        "punctuation_density": 0.14285714285714285,
        "line_break_count": 31,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "nosso",
          "como",
          "planeta",
          "caos",
          "cataclismo",
          "assim",
          "quasar",
          "sendo",
          "buraco",
          "humano",
          "antes",
          "estava",
          "mais",
          "gerando",
          "massa",
          "negro",
          "conter",
          "diante",
          "necessidade"
        ],
        "entities": [
          [
            "38",
            "CARDINAL"
          ],
          [
            "Ele estava",
            "PERSON"
          ],
          [
            "Sodoma",
            "LOC"
          ],
          [
            "mais ainda",
            "PERSON"
          ],
          [
            "mas vou \\ntentar",
            "PERSON"
          ],
          [
            "como eu vejo",
            "PERSON"
          ],
          [
            "buraco negro",
            "ORG"
          ],
          [
            "expelido quando",
            "PERSON"
          ],
          [
            "buraco",
            "NORP"
          ],
          [
            "Big Bang",
            "GPE"
          ]
        ],
        "readability_score": 87.7731884057971,
        "semantic_density": 0,
        "word_count": 322,
        "unique_words": 198,
        "lexical_diversity": 0.6149068322981367
      },
      "preservation_score": 1.2882115174782053e-05
    },
    {
      "id": 1,
      "text": "— 39 —expansão!! Ele está em adaptação diante da sua própria vida, \\npois assim como nós temos uma marcação de tempo para a \\nnossa própria energia chamada idade, o universo, sistema so -\\nlar, Terra têm um tempo de existência da sua própria energia, \\ndessa forma se adaptando a energia do universo gerada pela \\nprópria evolução do próprio universo. Caos gerado para adap -\\ntação da própria energia. \\ncaos do passado sendo vivido no futuro editável.indd   39caos do passado sendo vivido no futuro editável.indd   39 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 55442,
      "chapter": 1,
      "page": 39,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 26.051136363636363,
      "complexity_metrics": {
        "word_count": 88,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 14.666666666666666,
        "avg_word_length": 5.170454545454546,
        "unique_word_ratio": 0.7386363636363636,
        "avg_paragraph_length": 88.0,
        "punctuation_density": 0.17045454545454544,
        "line_break_count": 7,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "própria",
          "energia",
          "universo",
          "tempo",
          "caos",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "expansão",
          "está",
          "adaptação",
          "diante",
          "vida",
          "pois",
          "assim",
          "como",
          "temos"
        ],
        "entities": [
          [
            "39",
            "CARDINAL"
          ],
          [
            "diante da sua própria",
            "PERSON"
          ],
          [
            "nós temos uma marcação de tempo",
            "ORG"
          ],
          [
            "dessa forma",
            "PERSON"
          ],
          [
            "universo gerada pela",
            "ORG"
          ],
          [
            "para adap -\\ntação da própria",
            "PERSON"
          ],
          [
            "editável.indd",
            "CARDINAL"
          ],
          [
            "editável.indd",
            "CARDINAL"
          ],
          [
            "39",
            "CARDINAL"
          ],
          [
            "14:53:3828/03/2022",
            "CARDINAL"
          ]
        ],
        "readability_score": 91.1155303030303,
        "semantic_density": 0,
        "word_count": 88,
        "unique_words": 65,
        "lexical_diversity": 0.7386363636363636
      },
      "preservation_score": 9.696215722954234e-07
    },
    {
      "id": 1,
      "text": "— 40 —\\ncaos do passado sendo vivido no futuro editável.indd   40caos do passado sendo vivido no futuro editável.indd   40 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 56112,
      "chapter": 2,
      "page": 40,
      "segment_type": "page",
      "themes": {},
      "difficulty": 20.91449275362319,
      "complexity_metrics": {
        "word_count": 23,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 7.666666666666667,
        "avg_word_length": 5.826086956521739,
        "unique_word_ratio": 0.6086956521739131,
        "avg_paragraph_length": 23.0,
        "punctuation_density": 0.2608695652173913,
        "line_break_count": 1,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "caos"
        ],
        "entities": [
          [
            "40",
            "CARDINAL"
          ],
          [
            "editável.indd   40caos",
            "CARDINAL"
          ],
          [
            "sendo vivido",
            "PERSON"
          ],
          [
            "editável.indd   40",
            "CARDINAL"
          ],
          [
            "14:53:3828/03/2022",
            "CARDINAL"
          ],
          [
            "14:53:38",
            "TIME"
          ]
        ],
        "readability_score": 94.41884057971015,
        "semantic_density": 0,
        "word_count": 23,
        "unique_words": 14,
        "lexical_diversity": 0.6086956521739131
      },
      "preservation_score": 5.8323102092957795e-08
    },
    {
      "id": 1,
      "text": "— 41 —Capítulo 7\\nFilosofia, sabedoria e inteligência\\nAntes de termos o cataclismo (apocalipse), tivemos um grande \\naumento de grandes filósofos em uma linha de raciocínio se -\\nmelhante à propagação da energia, grandes sábios e cientistas \\naumentando conceituadamente a quantidade de pessoas que \\npoderiam fazer algo melhor para o nosso planeta, mesmo as -\\nsim, foi inevitável.\\nParte 1 – Mileto6\\nConsiderado o primeiro filósofo ocidental, Tales de Mileto \\nnasceu na Turquia e, na época, era uma colônia grega. Em uma \\nvisita ao Egito, através da observação e da dedução, teve im -\\nportante influência das condições de tempo nas colheitas de \\nalimentos.\\nAtribui-se a ele a primeira previsão ocidental do eclipse total \\ndo sol, pois o filósofo também se interessava por astronomia. \\nEle acreditava no monismo, teoria que tudo no universo pode -\\nria ser reduzido, e era originado de uma matéria principal, no \\ncaso, a água (degelo e consumo em excesso de água). \\nFundou a Escola de Tales, que foi a primeira e mais importante \\nescola de conhecimento Grega.\\n6.  Texto baseado em https://pt.m.wikipedia.org/wiki/Tales_de_ Mileto .\\ncaos do passado sendo vivido no futuro editável.indd   41caos do passado sendo vivido no futuro editável.indd   41 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 56391,
      "chapter": 7,
      "page": 41,
      "segment_type": "page",
      "themes": {
        "filosofia": 39.473684210526315,
        "ciencia": 34.21052631578947,
        "arte": 26.31578947368421
      },
      "difficulty": 25.854020100502513,
      "complexity_metrics": {
        "word_count": 199,
        "sentence_count": 14,
        "paragraph_count": 1,
        "avg_sentence_length": 14.214285714285714,
        "avg_word_length": 5.346733668341709,
        "unique_word_ratio": 0.7185929648241206,
        "avg_paragraph_length": 199.0,
        "punctuation_density": 0.1708542713567839,
        "line_break_count": 22,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "grandes",
          "filósofo",
          "ocidental",
          "tales",
          "mileto",
          "grega",
          "primeira",
          "água",
          "escola",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "capítulo",
          "filosofia",
          "sabedoria",
          "inteligência",
          "antes"
        ],
        "entities": [
          [
            "41",
            "CARDINAL"
          ],
          [
            "Antes de termos",
            "ORG"
          ],
          [
            "poderiam fazer",
            "PERSON"
          ],
          [
            "algo melhor",
            "ORG"
          ],
          [
            "1",
            "CARDINAL"
          ],
          [
            "Considerado",
            "FAC"
          ],
          [
            "primeiro filósofo",
            "ORG"
          ],
          [
            "Tales de Mileto",
            "PERSON"
          ],
          [
            "Egito",
            "GPE"
          ],
          [
            "nas colheitas de \\nalimentos",
            "PERSON"
          ]
        ],
        "readability_score": 91.28883704235463,
        "semantic_density": 0,
        "word_count": 199,
        "unique_words": 143,
        "lexical_diversity": 0.7185929648241206
      },
      "preservation_score": 7.217483884003528e-06
    },
    {
      "id": 1,
      "text": "— 42 —Parte 2 – Anaximandro7\\nDiscípulo e assessor de Tales de Mileto, Anaximandro também \\nnasceu em Mileto e frequentou a Escola de Mileto, fundada \\npelo primeiro filósofo ocidental para procurar uma razão es -\\ntrutural para o mundo. \\n Anaximandro acreditava que o nosso mundo era apenas um \\nentre vários outros, que se desenvolviam, evoluíam e destruíam, \\nem um processo infinito e inevitável (Stephen Hopkins, moti -\\nvo de outros seres não terem chegados ao planeta Terra).\\nPara Anaximandro, tudo tinha início no que ele chamava de \\nApeiron, algo que não tem fim, nem começo (quântico, início \\nde tudo é o primeiro movimento), e é a origem de todas as coi -\\nsas. Ele também acreditava que o sol agia sobre a água, criando \\nseres que evoluíam para várias coisas que conhecemos hoje.\\nParte 3 – Pitágoras, primeiro matemático8\\nNascido na ilha de Samos, Grécia, Pitágoras chegou a estudar \\nna Escola de Mileto também, mas seus conhecimentos eram \\nmais avançados que os de seu mestre, fazendo ele ser mais que \\no seu mestre e automaticamente criar as suas próprias criações.\\nEle era um matemático brilhante, Pitágoras afinou o seu co -\\nnhecimento matemático quando se fixou por aproximada -\\nmente vinte anos no Egito, examinando os cálculos africanos. \\ncriou o Teorema de Pitágoras.\\nPitágoras via nas proporções geométricas explicações para \\ntudo que acontecia na natureza. Os números explicavam desde \\npor que uma música é agradável aos ouvidos (tudo têm um pa -\\n7.  Texto baseado em https://pt.m.wikipedia.org/wiki/Anaxi mandro .\\n8.  Texto baseado em https://pt.m.wikipedia.org/wiki/Pit%C3%A 1goras .\\ncaos do passado sendo vivido no futuro editável.indd   42caos do passado sendo vivido no futuro editável.indd   42 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 57788,
      "chapter": 2,
      "page": 42,
      "segment_type": "page",
      "themes": {
        "filosofia": 42.857142857142854,
        "arte": 57.14285714285714
      },
      "difficulty": 25.29798136645963,
      "complexity_metrics": {
        "word_count": 276,
        "sentence_count": 21,
        "paragraph_count": 1,
        "avg_sentence_length": 13.142857142857142,
        "avg_word_length": 5.278985507246377,
        "unique_word_ratio": 0.6594202898550725,
        "avg_paragraph_length": 276.0,
        "punctuation_density": 0.16304347826086957,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "pitágoras",
          "mileto",
          "tudo",
          "anaximandro",
          "também",
          "primeiro",
          "parte",
          "escola",
          "mundo",
          "acreditava",
          "outros",
          "evoluíam",
          "seres",
          "início",
          "mais",
          "mestre",
          "matemático",
          "texto",
          "baseado",
          "https"
        ],
        "entities": [
          [
            "42",
            "CARDINAL"
          ],
          [
            "2",
            "CARDINAL"
          ],
          [
            "de Tales de Mileto",
            "PERSON"
          ],
          [
            "Anaximandro",
            "ORG"
          ],
          [
            "Mileto",
            "GPE"
          ],
          [
            "fundada \\n",
            "PERSON"
          ],
          [
            "pelo primeiro",
            "PERSON"
          ],
          [
            "para procurar uma",
            "PERSON"
          ],
          [
            "Anaximandro",
            "ORG"
          ],
          [
            "outros",
            "GPE"
          ]
        ],
        "readability_score": 91.84487577639752,
        "semantic_density": 0,
        "word_count": 276,
        "unique_words": 182,
        "lexical_diversity": 0.6594202898550725
      },
      "preservation_score": 1.1839589724870433e-05
    },
    {
      "id": 1,
      "text": "— 43 —drão de aceitação) a, por exemplo, o funcionamento dos seres \\nvivos, plantas etc. Inclusive, ele acreditava que o ser humano \\ntinha ciclos.\\nParte 4 – Heráclito9 \\nNascido em uma família nobre em Éfeso, Heráclito é conheci -\\ndo por afirmar que tudo estava em constante estado de trans -\\nformação. Suas ideias eram de interpretação do padrão com -\\nportamental através da observação e da sensibilidade humana.\\nAo contrário de outros, o filósofo foi autodidata, aprendendo \\nsozinho sobre as questões de ciência, teologia e relações hu -\\nmanas. O movimento (primeira energia gerada no universo) \\nera para ele o principal fundamento da natureza, a verdade \\nentão seria dialética, sempre com dois opostos (ação e reação) \\nse relacionando. \\nO fogo é o elemento fundador da natureza para o filósofo, con -\\nsiderando que o tempo todo se movimenta (primeira energia \\nfoi o movimento),se transforma e origina toda a natureza\\nParte 5 – Parmênides10 \\nParmênides nasceu na colônia grega de Eleia, no litoral su -\\ndoeste da atual Itália, na Magna Grécia. Frequentou a escola \\nque Pitágoras fundou na Itália. \\nEle concluiu que o mundo era uma ilusão (holograma), basea -\\ndo em suas ideias do que era o ser. Não há nada além do ser \\n(nosso próprio pensamento), pois tudo o que existe é, e tudo \\n9.  Texto baseado em https://pt.m.wikipedia.org/wiki/Her%C3%A 1clito .\\n10.  Texto baseado em https://pt.m.wikipedia.org/wiki/Parm%C3%A Anides .\\ncaos do passado sendo vivido no futuro editável.indd   43caos do passado sendo vivido no futuro editável.indd   43 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 59660,
      "chapter": 2,
      "page": 43,
      "segment_type": "page",
      "themes": {
        "filosofia": 31.25,
        "ciencia": 27.083333333333336,
        "arte": 41.66666666666667
      },
      "difficulty": 22.405450923578414,
      "complexity_metrics": {
        "word_count": 251,
        "sentence_count": 22,
        "paragraph_count": 1,
        "avg_sentence_length": 11.409090909090908,
        "avg_word_length": 5.2151394422310755,
        "unique_word_ratio": 0.6733067729083665,
        "avg_paragraph_length": 251.0,
        "punctuation_density": 0.1752988047808765,
        "line_break_count": 26,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "tudo",
          "natureza",
          "parte",
          "suas",
          "ideias",
          "filósofo",
          "movimento",
          "primeira",
          "energia",
          "itália",
          "texto",
          "baseado",
          "https",
          "wikipedia",
          "wiki",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável"
        ],
        "entities": [
          [
            "43",
            "CARDINAL"
          ],
          [
            "drão de aceitação",
            "ORG"
          ],
          [
            "Éfeso",
            "NORP"
          ],
          [
            "Heráclito",
            "GPE"
          ],
          [
            "contrário de outros",
            "ORG"
          ],
          [
            "questões de ciência",
            "PERSON"
          ],
          [
            "relações hu -\\nmanas",
            "PERSON"
          ],
          [
            "movimento),se",
            "PERSON"
          ],
          [
            "5",
            "CARDINAL"
          ],
          [
            "colônia grega de Eleia",
            "PERSON"
          ]
        ],
        "readability_score": 92.73091271278523,
        "semantic_density": 0,
        "word_count": 251,
        "unique_words": 169,
        "lexical_diversity": 0.6733067729083665
      },
      "preservation_score": 1.2131205235335221e-05
    },
    {
      "id": 1,
      "text": "— 44 —que o existe não é. A natureza para Parmênides era imóvel, não \\nse dividia, não se transformava e estava presente em tudo, ela \\nsimplesmente “era” . Se “tudo” era composto pelo ser, que não se \\nalterava, mas claramente o mundo que via com os seus olhos \\nmudava, então esse “tudo” se tratava de uma mentira (viver é \\naceitar, pois o que for para ser, será).\\nParte 6 – Demócrito11 \\nNascido em Abdera, Demócrito foi quem desenvolveu a teoria \\ndo pensador Leucipo sobre o atomismo. São conhecidos como \\nos pais da física por descobrirem o átomo. \\nSendo muito rico, Demócrito usava o seu dinheiro em expe -\\ndições, principalmente para países africanos como o Egito e a \\nEtiópia, na época eram mais avançados na tecnologia devido \\nao caos que continham. Ao voltar para a Grécia, em Atenas, \\nnão foi muito notado.\\nEra interessado por várias áreas de conhecimento e tinha uma \\nvisão materialista, onde tudo era formado pelo átomo. Assim, \\npara ele, quando o corpo humano perecia, a alma permanecia, \\nformada por átomos (tudo é energia).\\nParte 7 – Sócrates12 \\nO homem que revolucionou a filosofia grega nasceu em Ate -\\nnas. Chegou a tentar carreira política (gostava de debater) \\nquando jovem, mas não teve ideias “bem aceitas” . Serviu o exér -\\ncito por um tempo e, depois de aposentado, se dedicou à car -\\nreira de educador. \\n11.  Texto baseado em https://pt.m.wikipedia.org/wiki/Dem%C3%B 3crito .\\n12.  Texto baseado em https://pt.m.wikipedia.org/wiki/S%C3%B3 crates .\\ncaos do passado sendo vivido no futuro editável.indd   44caos do passado sendo vivido no futuro editável.indd   44 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 61358,
      "chapter": 2,
      "page": 44,
      "segment_type": "page",
      "themes": {
        "filosofia": 21.126760563380284,
        "ciencia": 36.61971830985916,
        "arte": 28.169014084507044,
        "tecnologia": 14.084507042253522
      },
      "difficulty": 24.87590909090909,
      "complexity_metrics": {
        "word_count": 264,
        "sentence_count": 25,
        "paragraph_count": 1,
        "avg_sentence_length": 10.56,
        "avg_word_length": 5.053030303030303,
        "unique_word_ratio": 0.6931818181818182,
        "avg_paragraph_length": 264.0,
        "punctuation_density": 0.19696969696969696,
        "line_break_count": 27,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "tudo",
          "sendo",
          "pelo",
          "parte",
          "demócrito",
          "como",
          "átomo",
          "muito",
          "caos",
          "quando",
          "texto",
          "baseado",
          "https",
          "wikipedia",
          "wiki",
          "passado",
          "vivido",
          "futuro",
          "editável",
          "indd"
        ],
        "entities": [
          [
            "44",
            "CARDINAL"
          ],
          [
            "Parmênides",
            "ORG"
          ],
          [
            "ela",
            "PERSON"
          ],
          [
            "pelo ser",
            "PERSON"
          ],
          [
            "mas claramente",
            "PERSON"
          ],
          [
            "tratava de uma mentira",
            "ORG"
          ],
          [
            "6",
            "CARDINAL"
          ],
          [
            "Demócrito",
            "PERSON"
          ],
          [
            "quem",
            "GPE"
          ],
          [
            "da física",
            "PERSON"
          ]
        ],
        "readability_score": 93.20409090909091,
        "semantic_density": 0,
        "word_count": 264,
        "unique_words": 183,
        "lexical_diversity": 0.6931818181818182
      },
      "preservation_score": 1.4172513808588745e-05
    },
    {
      "id": 1,
      "text": "— 45 —É sua a famosa frase “Só sei que nada sei” .\\nAtravés de sua representação nos diálogos (político) de seus \\nestudantes, Sócrates tornou-se renomado por sua contribuição \\nno campo da ética e é esse Sócrates que legou seu nome a con -\\nceitos como a ironia socrática e o método socrático. Até hoje \\na técnica utilizada numa ampla gama de discussões, e consis -\\nte de um tipo peculiar de pedagogia (nossos porquês, nossos \\nquestionamentos) no qual uma série de questões são feitas, \\nnão apenas para obter respostas específicas, mas para encora -\\njar também uma compreensão clara e fundamental do assunto \\nsendo discutido. Foi o Sócrates de Platão que fez contribuições \\nimportantes e duradouras aos campos da epistemologia e da \\nlógica.\\nParte 8 – Platão13 \\nPlatão era um racionalista, realista, idealista e dualista. Foi o \\ninovador do diálogo (mesma conduta de Sócrates) escrito e \\ndas formas dialéticas da filosofia (quanto mais se pratica, mais \\nconhecimento se adquiri). Sua mais famosa contribuição leva \\nseu nome, platonismo, a direção pela razão pura para fornecer \\numa solução realista para os problemas universais. Ele também \\né o epônimo do amor platônico e dos sólidos platônicos. A fi -\\nlosofia agrega uma continuidade de um pensamento filosófico \\nque pode ser visto desde o Egito Antigo. Alegam que seu corpo \\ntextual contém fragmentos de doutrinas não escritas que eram \\nlecionadas oralmente (debate) na sua Academia (Sócrates). \\n13.  Texto baseado em https://pt.m.wikipedia.org/wiki/Plat% C3%A3o .\\ncaos do passado sendo vivido no futuro editável.indd   45caos do passado sendo vivido no futuro editável.indd   45 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 63098,
      "chapter": 2,
      "page": 45,
      "segment_type": "page",
      "themes": {
        "filosofia": 79.64601769911503,
        "ciencia": 11.504424778761061,
        "arte": 8.849557522123893
      },
      "difficulty": 26.902478632478633,
      "complexity_metrics": {
        "word_count": 260,
        "sentence_count": 18,
        "paragraph_count": 1,
        "avg_sentence_length": 14.444444444444445,
        "avg_word_length": 5.323076923076923,
        "unique_word_ratio": 0.7076923076923077,
        "avg_paragraph_length": 260.0,
        "punctuation_density": 0.12307692307692308,
        "line_break_count": 26,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "sócrates",
          "sendo",
          "mais",
          "famosa",
          "contribuição",
          "nome",
          "nossos",
          "também",
          "platão",
          "realista",
          "passado",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "frase",
          "nada",
          "através",
          "representação",
          "diálogos"
        ],
        "entities": [
          [
            "45",
            "CARDINAL"
          ],
          [
            "Através de sua",
            "ORG"
          ],
          [
            "Sócrates",
            "GPE"
          ],
          [
            "Sócrates",
            "GPE"
          ],
          [
            "utilizada",
            "NORP"
          ],
          [
            "gama de discussões",
            "PERSON"
          ],
          [
            "mas",
            "PERSON"
          ],
          [
            "também uma compreensão",
            "PERSON"
          ],
          [
            "Sócrates de Platão",
            "ORG"
          ],
          [
            "8",
            "CARDINAL"
          ]
        ],
        "readability_score": 91.1808547008547,
        "semantic_density": 0,
        "word_count": 260,
        "unique_words": 184,
        "lexical_diversity": 0.7076923076923077
      },
      "preservation_score": 1.0046154335511981e-05
    },
    {
      "id": 1,
      "text": "— 46 —Parte 9 – Aristóteles14 \\nFoi um filósofo grego durante o período clássico na Grécia \\nAntiga, fundador da escola peripatética e do Liceu, além de ter \\nsido aluno de Platão e professor de Alexandre, o Grande. Seus \\nescritos vieram de uma evolução filosófica em quase todas as \\náreas que afeta a mente humana a física, a metafísica, a música, \\na lógica, o debate, o governo, a ética, a política, a economia. \\nAristóteles é visto como um dos fundadores da filosofia oci -\\ndental. Em 343 a.C., torna-se tutor de Alexandre da Macedô -\\nnia, na época com 13 anos de idade. Alexandre assume o trono \\ne Aristóteles volta para Atenas onde funda o Liceu.\\nParte 10 – Alexandre, o Grande15\\nBuscando alcançar a glória, invadiu a Índia em 326 a.C., mas \\nfoi forçado a voltar pela demanda de suas tropas. Alexandre \\nmorreu na Babilônia em 323 a.C. Nos anos seguintes à sua \\nmorte, uma série de guerras civis rasgou seu império em peda -\\nços, com a perda de um grande líder resultou em vários estados \\ngovernados pelos diádicos, sobreviventes e herdeiros generais \\nde Alexandre.\\nSeu legado inclui a difusão cultural que suas conquistas gera -\\nram, como o greco-budismo. Fundou cerca de 20 cidades que \\nlevavam o seu nome, principalmente Alexandria, no Egito. \\nSeus assentamentos de colonos gregos e a propagação resultan -\\nte da cultura grega no leste resultou em uma nova civilização \\nhelenística, o tornando uma lenda através do “caos da filosofia” . \\nTornou-se exemplo para os líderes militares, e academias mili -\\ntares em todo o mundo ainda ensinam suas táticas. \\n14.  Texto baseado em https://pt.m.wikipedia.org/wiki/Arist%C3%B 3teles .\\n15.  Texto baseado em https://pt.m.wikipedia.org/wiki/Alexandre,_o_ Grande .\\ncaos do passado sendo vivido no futuro editável.indd   46caos do passado sendo vivido no futuro editável.indd   46 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 64884,
      "chapter": 2,
      "page": 46,
      "segment_type": "page",
      "themes": {
        "filosofia": 81.81818181818183,
        "arte": 18.181818181818183
      },
      "difficulty": 21.704666666666668,
      "complexity_metrics": {
        "word_count": 300,
        "sentence_count": 30,
        "paragraph_count": 1,
        "avg_sentence_length": 10.0,
        "avg_word_length": 5.126666666666667,
        "unique_word_ratio": 0.68,
        "avg_paragraph_length": 300.0,
        "punctuation_density": 0.2,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "alexandre",
          "grande",
          "suas",
          "parte",
          "liceu",
          "seus",
          "aristóteles",
          "como",
          "filosofia",
          "anos",
          "resultou",
          "caos",
          "texto",
          "baseado",
          "https",
          "wikipedia",
          "wiki",
          "passado",
          "sendo",
          "vivido"
        ],
        "entities": [
          [
            "46",
            "CARDINAL"
          ],
          [
            "9",
            "CARDINAL"
          ],
          [
            "grego durante",
            "PERSON"
          ],
          [
            "Grécia \\nAntiga",
            "PERSON"
          ],
          [
            "Liceu",
            "GPE"
          ],
          [
            "de Alexandre",
            "PERSON"
          ],
          [
            "metafísica",
            "GPE"
          ],
          [
            "343 a.C.",
            "QUANTITY"
          ],
          [
            "de Alexandre da Macedô",
            "PERSON"
          ],
          [
            "13",
            "CARDINAL"
          ]
        ],
        "readability_score": 93.462,
        "semantic_density": 0,
        "word_count": 300,
        "unique_words": 204,
        "lexical_diversity": 0.68
      },
      "preservation_score": 1.5433750891348957e-05
    },
    {
      "id": 1,
      "text": "— 47 —Parte 11 – Cleópatra16\\nAí sim, vimos como o homem ainda era refém dos seus pró -\\nprios instintos primatas.\\nCleópatra VII Filopátor nasceu em meados de agosto de 30 \\na.C., foi a última governante ativa do Reino Ptolemaico do \\nEgito. Como membro da dinastia ptolemaica, foi descendente \\nde Ptolemeu I Sóter, um general greco-macedônio e compa -\\nnheiro de Alexandre, o Grande. Após sua morte, o Egito tor -\\nnou-se uma província do Império Romano, marcando o fim \\ndo Período Helenístico.\\nBem provável que Cleópatra acompanhou e aprendeu com \\nseu pai Ptolemeu XII. durante seu exílio em Roma, depois que \\numa revolta no Egito permitiu que sua filha mais velha, Be -\\nrenice IV , reivindicasse o trono. Quando morreu em 51 a.C., \\nPtolemeu XII foi sucedido por Cleópatra e seu irmão mais \\nnovo, Ptolemeu XIII, como governantes conjuntos, mas um \\ndesentendimento entre ambos levou ao início da guerra civil \\n(ganância). Depois de perder a Batalha de Farsalos na Grécia \\ncontra seu rival Júlio César durante a Segunda Guerra Civil, o \\nestadista romano Pompeu fugiu para o Egito. Ptolemeu XIII \\nmatou Pompeu enquanto César ocupava Alexandria em busca \\ndo próprio Pompeu. César, um cônsul da República Roma -\\nna, tentou reconciliar Ptolemeu XIII com sua irmã Cleópatra. \\nPotino, o conselheiro-chefe do faraó, considerou os termos \\ndo cônsul favoráveis à rainha, não satisfeito com os termos, \\nocasionando mais guerras que fizeram o comando cair sob o \\ncontrole de sua irmã mais nova, Arsínoe IV , cercaram César \\ne Cleópatra. Após o cerco no início de 47 a.C o governante \\negípcio morreu pouco depois na Batalha do Nilo. Arsínoe IV \\nfoi exilada em Éfeso e César, primeiro ditador eleito não origi -\\n16.  Texto baseado em https://pt.m.wikipedia.org/wiki/Cle%C3%B 3patra .\\ncaos do passado sendo vivido no futuro editável.indd   47caos do passado sendo vivido no futuro editável.indd   47 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 66864,
      "chapter": 2,
      "page": 47,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 22.91193548387097,
      "complexity_metrics": {
        "word_count": 310,
        "sentence_count": 25,
        "paragraph_count": 1,
        "avg_sentence_length": 12.4,
        "avg_word_length": 5.106451612903226,
        "unique_word_ratio": 0.6516129032258065,
        "avg_paragraph_length": 310.0,
        "punctuation_density": 0.17096774193548386,
        "line_break_count": 31,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "ptolemeu",
          "cleópatra",
          "césar",
          "egito",
          "mais",
          "como",
          "depois",
          "xiii",
          "pompeu",
          "governante",
          "após",
          "romano",
          "durante",
          "roma",
          "morreu",
          "início",
          "guerra",
          "civil",
          "batalha",
          "cônsul"
        ],
        "entities": [
          [
            "47",
            "CARDINAL"
          ],
          [
            "11",
            "CARDINAL"
          ],
          [
            "homem ainda",
            "PERSON"
          ],
          [
            "Cleópatra VII Filopátor",
            "PERSON"
          ],
          [
            "de agosto de 30",
            "PERSON"
          ],
          [
            "Reino Ptolemaico",
            "FAC"
          ],
          [
            "Egito",
            "PERSON"
          ],
          [
            "nheiro de Alexandre",
            "PERSON"
          ],
          [
            "Após",
            "PERSON"
          ],
          [
            "Egito",
            "GPE"
          ]
        ],
        "readability_score": 92.26806451612903,
        "semantic_density": 0,
        "word_count": 310,
        "unique_words": 202,
        "lexical_diversity": 0.6516129032258065
      },
      "preservation_score": 1.4916133360273956e-05
    },
    {
      "id": 1,
      "text": "— 48 —nário de uma cadeia familiar, declarou Cleópatra e seu irmão \\nmais novo Ptolemeu XIV como governantes conjuntos. O di -\\ntador manteve um caso com a rainha, que gerou um filho, Ce -\\nsarião. Após os assassinatos de César e Ptolemeu XIV esse que \\na própria Cleópatra mandou matar em 44 a.C., tentou dar um \\ngolpe de estado para fazer de Cesarião o herdeiro de seu pai, \\nmas o título foi para Otaviano, sobrinho-neto de César.\\nNa Guerra Civil dos Libertadores entre 43-42 a.C., Cleópatra \\nsempre com fome de ter mais poder ficou ao lado do Segundo \\nTriunvirato formado por Otaviano, Marco Antônio e Lépido. \\nApós um encontro em Tarso, em 41 a.C., a rainha teve um \\ncaso com Antônio para conseguir manipular. Ele realizou a \\nexecução de Arsínoe a pedido dela para conseguir concentrar \\no poder, e ele por sua vez tornou-se cada vez mais dependente \\ndela para financiamento e ajuda militar durante suas invasões \\ndo Império Parta e do Reino da Armênia. Os filhos de Alexan -\\ndria fizeram um legado Alexandre Hélio, Cleópatra Selene II \\ne Ptolemeu Filadelfo, viraram governantes de vários territórios \\nantigos. Esses acontecimentos mais seu casamento e o divórcio \\nde Marco Antônio da irmã de Otaviano, Otávia, a Jovem, leva -\\nram à Última Guerra Civil da República Romana. Otaviano se \\nengajou numa guerra “familiar” , forçou os aliados de Antônio \\nno Senado a fugir de Roma em 32 a.C. e declarou guerra à \\nCleópatra. Depois de derrotar a frota naval de ambos na Ba -\\ntalha de Áccio, em 31 a.C., as forças de Otaviano invadiram o \\nEgito em 30 a.C. com a derrota e o egocentrismo de Antônio, o \\nlevou a cometer suicídio. Quando a rainha soube que o gover -\\nnante romano planejava fazer de toda a sua vida uma procissão \\ntriunfal, cometeu suicídio por envenenamento. \\nSeu legado sobrevive em numerosas obras de arte, sua beleza \\ne seus encantos tanto antigas quanto modernas. Nas artes vi -\\nsuais, representações antigas de Cleópatra incluem os desejos \\ncaos do passado sendo vivido no futuro editável.indd   48caos do passado sendo vivido no futuro editável.indd   48 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 68901,
      "chapter": 2,
      "page": 48,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 25.265938410320434,
      "complexity_metrics": {
        "word_count": 356,
        "sentence_count": 27,
        "paragraph_count": 1,
        "avg_sentence_length": 13.185185185185185,
        "avg_word_length": 4.837078651685394,
        "unique_word_ratio": 0.6235955056179775,
        "avg_paragraph_length": 356.0,
        "punctuation_density": 0.14887640449438203,
        "line_break_count": 32,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "cleópatra",
          "otaviano",
          "antônio",
          "mais",
          "guerra",
          "ptolemeu",
          "rainha",
          "familiar",
          "declarou",
          "governantes",
          "caso",
          "após",
          "césar",
          "fazer",
          "civil",
          "poder",
          "marco",
          "conseguir",
          "dela",
          "legado"
        ],
        "entities": [
          [
            "48",
            "CARDINAL"
          ],
          [
            "Cleópatra",
            "PERSON"
          ],
          [
            "Ptolemeu XIV",
            "PERSON"
          ],
          [
            "Após os assassinatos de César e Ptolemeu XIV",
            "PERSON"
          ],
          [
            "Cleópatra",
            "PERSON"
          ],
          [
            "44 a.C.",
            "PERCENT"
          ],
          [
            "para fazer de Cesarião",
            "PERSON"
          ],
          [
            "Libertadores",
            "PERSON"
          ],
          [
            "43-42 a.C.,",
            "QUANTITY"
          ],
          [
            "Cleópatra",
            "PERSON"
          ]
        ],
        "readability_score": 91.95628381190178,
        "semantic_density": 0,
        "word_count": 356,
        "unique_words": 222,
        "lexical_diversity": 0.6235955056179775
      },
      "preservation_score": 1.563059136091269e-05
    },
    {
      "id": 1,
      "text": "— 49 —a ganância romana e ptolemaica. Foi tema de muitas obras de \\narte renascentista e barroca, devido a sua vida ter tido muito \\npoder, sexo, guerras, conflitos, luxúria, desejos acima da nor -\\nmalidade as pinturas, poesia, dramas teatrais... nós tempos mo -\\ndernos ela é referência de poder e sedução!!\\nParte 12 – Epicuro17 \\nNascido na ilha de Samos, Epicuro teve Sócrates e Aristóteles \\ncomo professores, mas inaugurou uma nova forma de pensa -\\nmento que condizia com o contexto social da época, chamada \\nEpicurismo. \\nEle acreditava que o sentido da vida era satisfazer prazeres, mas \\nsó os que não eram impostos pela sociedade e, sim, os prazeres \\nsimples, como beber água quando se está com sede. Isso seria a \\nchave para uma vida feliz. \\nComo um bom materialista, ele acreditava também que, como \\ntudo era feito de átomos, não era preciso temer a morte, que \\nera apenas uma fase de transição, de transformação natural da \\nvida.\\nParte 13 – Zenão de Cítio18 \\nOutro nome importante da era helenista foi Zenão de Cítio, \\nque nasceu na ilha de Chipre. Era um comerciante que, atraído \\npelos ensinamentos de Sócrates, foi parar em Atenas. \\nFundador da escola filosófica estoica, Zenão discordava de Epi -\\n17.  Texto baseado em https://pt.m.wikipedia.org/wiki/E picuro .\\n18.  Texto baseado em https://pt.m.wikipedia.org/wiki/Zen%C3%A3o_de_C% -\\nC3%ADtio .\\ncaos do passado sendo vivido no futuro editável.indd   49caos do passado sendo vivido no futuro editável.indd   49 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 71125,
      "chapter": 2,
      "page": 49,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 23.133453784709015,
      "complexity_metrics": {
        "word_count": 239,
        "sentence_count": 22,
        "paragraph_count": 1,
        "avg_sentence_length": 10.863636363636363,
        "avg_word_length": 5.2175732217573225,
        "unique_word_ratio": 0.7154811715481172,
        "avg_paragraph_length": 239.0,
        "punctuation_density": 0.22594142259414227,
        "line_break_count": 26,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "vida",
          "como",
          "zenão",
          "poder",
          "parte",
          "ilha",
          "sócrates",
          "acreditava",
          "prazeres",
          "texto",
          "baseado",
          "https",
          "wikipedia",
          "wiki",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd"
        ],
        "entities": [
          [
            "49",
            "CARDINAL"
          ],
          [
            "Foi tema de muitas",
            "ORG"
          ],
          [
            "de \\narte",
            "PERSON"
          ],
          [
            "tido muito",
            "PERSON"
          ],
          [
            "desejos acima da nor -\\n",
            "PERSON"
          ],
          [
            "poesia",
            "GPE"
          ],
          [
            "dramas teatrais",
            "PERSON"
          ],
          [
            "nós tempos mo -\\ndernos",
            "PERSON"
          ],
          [
            "referência de",
            "PERSON"
          ],
          [
            "12",
            "CARDINAL"
          ]
        ],
        "readability_score": 93.00290985165462,
        "semantic_density": 0,
        "word_count": 239,
        "unique_words": 171,
        "lexical_diversity": 0.7154811715481172
      },
      "preservation_score": 1.1562554989928884e-05
    },
    {
      "id": 1,
      "text": "— 50 —curo e achava que o homem tinha que desprezar qualquer tipo \\nde prazer e problema. O importante do homem era adquirir a \\nsabedoria necessária para entender o cosmos pois através dos \\ncosmos enxergamos o nosso próprio movimento. Tal pensa -\\nmento se relaciona ao contexto social em que vivemos até hoje \\nonde o homem já não estava preso à Terra, à cidade grega eram \\npessoas sem raízes, um peso para o mundo.\\nParte 14 – Pirro de Élis19\\nPirro nasceu na cidade de Élis, ou Élida, e pouco se sabe so -\\nbre a sua infância. Na juventude, acompanhou o explorador \\nAlexandre em sua jornada pelo Oriente, onde se deparou com \\nculturas e costumes muito diferentes, e percebeu que não con -\\nseguiria determinar o que era certo e errado, justo ou injusto, \\nbem ou mal. \\nA sua filosofia era: se você quer ser um sábio, não dá para ter \\ncerteza de nada. Viver feliz era viver na suspensão do juízo, \\nporque são inúmeras as possibilidades de verdade, variando \\nconforme o local, as pessoas, etc. A isso deu-se o nome de ce -\\nticismo. Pirro, então, foi o primeiro filósofo cético da história. \\nParte 15 – Cesar20\\nEm 49 a.C., César assumiu o comando em Roma em um golpe \\nde estado e assumiu como um ditador absoluto. Ele iniciou \\nentão uma série de reformas sociais e políticas, incluindo a \\ncriação do calendário juliano. Continuou a centralizar o po -\\n19.  Texto baseado em https://pt.m.wikipedia.org/wiki/Pirro_de_%C3 %89lis .\\n20.  Texto baseado em https://pt.m.wikipedia.org/wiki/J%C3%BAlio_C% -\\nC3%A9sar .\\ncaos do passado sendo vivido no futuro editável.indd   50caos do passado sendo vivido no futuro editável.indd   50 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 72752,
      "chapter": 2,
      "page": 50,
      "segment_type": "page",
      "themes": {
        "filosofia": 42.857142857142854,
        "arte": 57.14285714285714
      },
      "difficulty": 21.935451505016722,
      "complexity_metrics": {
        "word_count": 276,
        "sentence_count": 26,
        "paragraph_count": 1,
        "avg_sentence_length": 10.615384615384615,
        "avg_word_length": 4.913043478260869,
        "unique_word_ratio": 0.6920289855072463,
        "avg_paragraph_length": 276.0,
        "punctuation_density": 0.18115942028985507,
        "line_break_count": 27,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "homem",
          "pirro",
          "cosmos",
          "onde",
          "cidade",
          "pessoas",
          "parte",
          "viver",
          "então",
          "assumiu",
          "texto",
          "baseado",
          "https",
          "wikipedia",
          "wiki",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável"
        ],
        "entities": [
          [
            "50",
            "CARDINAL"
          ],
          [
            "qualquer tipo",
            "PERSON"
          ],
          [
            "que vivemos até hoje",
            "PERSON"
          ],
          [
            "Terra",
            "ORG"
          ],
          [
            "nasceu na cidade de Élis",
            "PERSON"
          ],
          [
            "Élida",
            "ORG"
          ],
          [
            "Alexandre",
            "PERSON"
          ],
          [
            "jornada pelo Oriente",
            "PERSON"
          ],
          [
            "muito",
            "PERSON"
          ],
          [
            "primeiro",
            "ORG"
          ]
        ],
        "readability_score": 93.21839464882943,
        "semantic_density": 0,
        "word_count": 276,
        "unique_words": 191,
        "lexical_diversity": 0.6920289855072463
      },
      "preservation_score": 1.1613587704260222e-05
    },
    {
      "id": 1,
      "text": "— 51 —der, pois a ganância de ser mais devido a não ter vindo da rea -\\nleza, foi eliminando o sistema burocrático de Roma, dando a si \\nmesmo grande autoridade. Porém a ferida da guerra civil ainda \\nestava aberta e a oposição política em Roma começou a cons -\\npirar para derrubá-lo do poder. As conspirações culminaram \\nnos Idos de Março em 44 a.C. com o assassinato de César por \\num grupo de senadores aristocratas liderados por Marco Júnio \\nBruto. Sua morte precipitaria uma nova guerra civil, devido ao \\npoder ser enraizado em famílias da realeza causando um mal -\\n-estar em quem era contra o poder de Cesar assim, o governo \\nconstitucional republicano nunca foi totalmente restaurado. \\nO seu sobrinho-neto, Caio Otaviano, foi feito seu herdeiro em \\ntestamento. Em 27 a.C., o jovem passaria para a história como \\nAugusto, devido a ele ter vindo de uma família de realeza ele \\nquis se desfazer do seu nome de origem “plebeia” .\\nEu interpreto o entendimento que o caos faz você criar o caos. \\nAnalogia\\nVingadores, quem assistiu ao filme dos vingadores sabe quem \\né o Thanos, ele é um cara que vê o caos no universo e quer \\nestabilizá-lo, fazendo pensar diferente de todos para um bem \\n“maior” , para não ter uma destruição, e sim, colocar o universo \\nem equilíbrio antes que não tenha solução.\\nNessa mesma analogia, irei colocar uma linha de raciocínio \\nperante os acontecimentos de um seguimento da propagação \\nda energia em escala de tempo. Tales de Mileto, ele conseguiu \\ninterpretar a energia em uma direção científica e filosófica, \\napós ele mostrar um “novo mundo” de se interpretar a energia \\nperante a necessidade de se manter uma balança entre o físico \\ne a energia.\\nAnaximandro já interpretou em uma forma científica seme -\\nlhante ao Mileto, porém a forma de se colocar em entendi -\\ncaos do passado sendo vivido no futuro editável.indd   51caos do passado sendo vivido no futuro editável.indd   51 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 74525,
      "chapter": 2,
      "page": 51,
      "segment_type": "page",
      "themes": {},
      "difficulty": 28.269893048128342,
      "complexity_metrics": {
        "word_count": 330,
        "sentence_count": 17,
        "paragraph_count": 1,
        "avg_sentence_length": 19.41176470588235,
        "avg_word_length": 4.821212121212121,
        "unique_word_ratio": 0.6151515151515151,
        "avg_paragraph_length": 330.0,
        "punctuation_density": 0.11818181818181818,
        "line_break_count": 31,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "caos",
          "energia",
          "devido",
          "poder",
          "quem",
          "colocar",
          "vindo",
          "roma",
          "porém",
          "guerra",
          "civil",
          "realeza",
          "analogia",
          "vingadores",
          "universo",
          "perante",
          "mileto",
          "interpretar",
          "científica",
          "forma"
        ],
        "entities": [
          [
            "51",
            "CARDINAL"
          ],
          [
            "sistema burocrático de Roma",
            "PERSON"
          ],
          [
            "estava aberta e",
            "PERSON"
          ],
          [
            "Roma",
            "ORG"
          ],
          [
            "nos Idos de Março",
            "ORG"
          ],
          [
            "44 a.C.",
            "PERCENT"
          ],
          [
            "assassinato de César",
            "ORG"
          ],
          [
            "Marco Júnio \\nBruto",
            "PERSON"
          ],
          [
            "Sua",
            "PERSON"
          ],
          [
            "nova",
            "LOC"
          ]
        ],
        "readability_score": 88.84775401069518,
        "semantic_density": 0,
        "word_count": 330,
        "unique_words": 203,
        "lexical_diversity": 0.6151515151515151
      },
      "preservation_score": 1.2656113154171841e-05
    },
    {
      "id": 1,
      "text": "— 52 —mento para civilização foi em forma de energia (Deus), onde \\ntudo é energia.\\nPitágoras conseguiu transformar a energia que ele captava em \\nmatemática.\\nVocê captar a energia (física) e falar sobre é diferente de achar \\num padrão. O achar padrão é matemática e não sentir algo \\nque você sabe dizer porém não compreender é sentimento, o \\nentender padrão é diferente de sentir.\\nHeráclito, esse cara é a chave para o entendimento da propa -\\ngação da energia, pois, mesmo ele não sendo de uma escola de \\nfilósofos, sem alguém para ensinar a decifrar aquela energia \\nque ele sentia, ele conseguiu interpretar a energia em forma de \\ncalor, colocando o fogo e a natureza em uma forma de direcio -\\nnamento de sentir a energia, que de certa forma não deixa de \\nser uma energia onipresente, Deus.\\nParmênides, o que esse filósofo falou é lindo!!! Ele simples -\\nmente reduziu uma interpretação de um contexto para si pró -\\nprio, e isso faz com que todos façam o melhor para todos. Na \\nfísica, é um padrão de energia captada e interpretada diante do \\nseu próprio pensamento, meio que você vive e forma que você \\ninterpreta a sua vida.\\nDemócrito confirmou para o mundo físico que existia o mun -\\ndo da energia, que Heráclito já tinha descoberto porém não \\ncomprovado.\\nSócrates foi a transição da filosofia sem caos para uma filosofia \\nde que se adaptar ao caos é necessário. Só sei que nada sei. Por \\nqual motivo ele falou isso? Falando isso, ele criava o caos por \\nmostrar entender, compreender e acontecer coisas que ele não \\nsabia entender e compreender, por isso o seu método de ensi -\\nno eram os questionamentos e não a certeza.\\ncaos do passado sendo vivido no futuro editável.indd   52caos do passado sendo vivido no futuro editável.indd   52 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 76590,
      "chapter": 2,
      "page": 52,
      "segment_type": "page",
      "themes": {
        "filosofia": 69.76744186046511,
        "ciencia": 30.232558139534888
      },
      "difficulty": 27.753969869706843,
      "complexity_metrics": {
        "word_count": 307,
        "sentence_count": 16,
        "paragraph_count": 1,
        "avg_sentence_length": 19.1875,
        "avg_word_length": 4.723127035830619,
        "unique_word_ratio": 0.5472312703583062,
        "avg_paragraph_length": 307.0,
        "punctuation_density": 0.1270358306188925,
        "line_break_count": 30,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "forma",
          "você",
          "padrão",
          "isso",
          "caos",
          "sentir",
          "compreender",
          "entender",
          "sendo",
          "deus",
          "conseguiu",
          "matemática",
          "física",
          "diferente",
          "achar",
          "porém",
          "heráclito",
          "esse",
          "falou"
        ],
        "entities": [
          [
            "52",
            "CARDINAL"
          ],
          [
            "Deus",
            "PERSON"
          ],
          [
            "Pitágoras",
            "PERSON"
          ],
          [
            "Você",
            "ORG"
          ],
          [
            "matemática e não",
            "ORG"
          ],
          [
            "diferente de sentir",
            "PERSON"
          ],
          [
            "Heráclito",
            "GPE"
          ],
          [
            "mesmo ele não sendo de uma escola de \\nfilósofos",
            "ORG"
          ],
          [
            "para ensinar",
            "PERSON"
          ],
          [
            "forma de \\ncalor",
            "PERSON"
          ]
        ],
        "readability_score": 88.98931188925081,
        "semantic_density": 0,
        "word_count": 307,
        "unique_words": 168,
        "lexical_diversity": 0.5472312703583062
      },
      "preservation_score": 1.115429327527818e-05
    },
    {
      "id": 1,
      "text": "— 53 —Platão conseguiu ser o primeiro a juntar as ideias religiosas \\ncom as ideias filosóficas. Ele era um seguidor de Sócrates, logo \\nele percebeu o caos do mundo diante do pensamento de si \\npróprio, perante uma necessidade de ter o caos controlado pe -\\nrante a si e um contexto de massa e energia, por isso temos a \\nexpressão “amor platônico”!!!\\nAristóteles, sendo aluno de Platão, ele simplesmente foi o cara \\nque viu padrão em tudo que nós vivemos. Ele foi a pessoa que \\ndirecionou o Alexandre, o Grande, a ser grande, ele conseguiu \\ntrazer os estudos da filosofia em um padrão comportamental, \\nmúsica, necessidade, enxergando o movimento de energia pa -\\ndrão entre seres, terra e universo. Conseguiu interpretar o caos, \\nver a necessidade do caos e trabalhar com o caos.\\nAlexandre, o Grande, foi o marco de que a filosofia mudou de \\npaz para o caos. \\nFrases\\nVence o medo e vencerás a morte. \\nNada é impossível para aquele que persiste.\\nA sorte favorece os destemidos. \\nNem o céu admite dois sóis, nem a terra dois senhores.               \\nNas frases que ele diz, você vê a discrepância de interpretação \\ndo caos como necessidade para um bem maior, ele percebeu \\nque não poderia lutar com várias religiões e pensamentos di -\\nferentes (provavelmente ideia de Aristóteles), criou um segui -\\nmento filosófico (energia), junto a religião (massa, pessoas) \\npara se ganhar todas as batalhas que se disputou. Juntou o be -\\nnefício da quantidade religiosa e o benefício de interpretação \\nda energia filosófica.\\ncaos do passado sendo vivido no futuro editável.indd   53caos do passado sendo vivido no futuro editável.indd   53 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 78486,
      "chapter": 2,
      "page": 53,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 26.67919708029197,
      "complexity_metrics": {
        "word_count": 274,
        "sentence_count": 15,
        "paragraph_count": 1,
        "avg_sentence_length": 18.266666666666666,
        "avg_word_length": 4.930656934306569,
        "unique_word_ratio": 0.6058394160583942,
        "avg_paragraph_length": 274.0,
        "punctuation_density": 0.14963503649635038,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "caos",
          "necessidade",
          "energia",
          "conseguiu",
          "sendo",
          "grande",
          "platão",
          "ideias",
          "percebeu",
          "massa",
          "aristóteles",
          "padrão",
          "alexandre",
          "filosofia",
          "terra",
          "frases",
          "dois",
          "interpretação",
          "passado",
          "vivido"
        ],
        "entities": [
          [
            "53",
            "CARDINAL"
          ],
          [
            "Ele era",
            "DATE"
          ],
          [
            "Ele",
            "PERSON"
          ],
          [
            "Alexandre",
            "PERSON"
          ],
          [
            "música",
            "GPE"
          ],
          [
            "Alexandre",
            "PERSON"
          ],
          [
            "marco de que",
            "ORG"
          ],
          [
            "Frases\\nVence",
            "ORG"
          ],
          [
            "medo",
            "GPE"
          ],
          [
            "Nada",
            "PERSON"
          ]
        ],
        "readability_score": 89.38746958637469,
        "semantic_density": 0,
        "word_count": 274,
        "unique_words": 166,
        "lexical_diversity": 0.6058394160583942
      },
      "preservation_score": 1.1431328010219729e-05
    },
    {
      "id": 1,
      "text": "— 54 —Cleópatra, primeira mulher com muito poder perante aos ho -\\nmens “fracos” , pelo seu próprio instinto. Todos os homens com \\nquem ela teve relacionamento, eram homens de poder, com \\num superego de ter poder, e a Cleópatra era a energia da sabe -\\ndoria (viveu no meio da filosofia) com amor (energia captada \\nperante ao instinto da mulher de sedução) e ódio (sofrer por \\nser mulher, criando o superego de ter mais poder), transfor -\\nmando em mulher icônica e rara, perante uma sociedade em \\nque as mulheres eram inferiores ao homem. Necessário para \\nentendermos a nossa evolução perante os nossos instintos, \\npois mostrou o quanto o homem sábio e forte pode se tornar \\nfraco perante o seu próprio desejo.\\nEpicuro foi o filósofo da mesma escola que Alexandre, porém \\ncom um pensamento de paz. Ele pregou que o maior controle \\ndo ser humano é controlar o seu próprio caos, sem isso, você \\nnão consegue viver em harmonia. Ele vê como necessário con -\\ntrolar os nossos excessos, não deixando de se viver o que te dar \\nprazer. Controlar o seu prazer é controlar a sua ganância, para \\nviver basta viver o necessário dos seus desejos!!\\nDesejo é a causa de todos os males!!!\\nZenão de Cítio, ao meu ver, não soube lidar com a sabedoria, \\ngeneralizando tudo e todos pelos seus próprios erros. Foram \\ntantos erros (isolamento do mundo) cometidos por ele mesmo \\nque entrou em uma bolha de si próprio, deixando de ver valo -\\nres em se viver uma vida em balanço com a energia e o físico. \\nNão deixando de canalizar uma energia de entendimento so -\\nbre si próprio perante a desistência de controlar o seu próprio \\ncaos, cometeu suicídio.\\nPirro de Élida viveu com Alexandre, o Grande viveu muitas \\nhistórias boas e ruins sem saber discernir o que era certo ou \\nerrado diante de um viver de cada pessoa, local, região, cidades, \\ncaos do passado sendo vivido no futuro editável.indd   54caos do passado sendo vivido no futuro editável.indd   54 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 80265,
      "chapter": 2,
      "page": 54,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 28.543841642228738,
      "complexity_metrics": {
        "word_count": 341,
        "sentence_count": 14,
        "paragraph_count": 1,
        "avg_sentence_length": 24.357142857142858,
        "avg_word_length": 4.703812316715543,
        "unique_word_ratio": 0.5953079178885631,
        "avg_paragraph_length": 341.0,
        "punctuation_density": 0.12903225806451613,
        "line_break_count": 31,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "perante",
          "próprio",
          "viver",
          "mulher",
          "poder",
          "energia",
          "controlar",
          "todos",
          "viveu",
          "necessário",
          "caos",
          "deixando",
          "cleópatra",
          "instinto",
          "homens",
          "eram",
          "superego",
          "homem",
          "nossos",
          "desejo"
        ],
        "entities": [
          [
            "Cleópatra",
            "PERSON"
          ],
          [
            "muito poder",
            "PERSON"
          ],
          [
            "aos ho -\\nmens “fracos”",
            "PERSON"
          ],
          [
            "pelo seu",
            "PERSON"
          ],
          [
            "Cleópatra",
            "LOC"
          ],
          [
            "da mulher de sedução",
            "PERSON"
          ],
          [
            "Necessário",
            "GPE"
          ],
          [
            "tornar \\nfraco perante",
            "ORG"
          ],
          [
            "desejo",
            "PERSON"
          ],
          [
            "Alexandre",
            "PERSON"
          ]
        ],
        "readability_score": 86.41028487641391,
        "semantic_density": 0,
        "word_count": 341,
        "unique_words": 203,
        "lexical_diversity": 0.5953079178885631
      },
      "preservation_score": 1.4012125277833111e-05
    },
    {
      "id": 1,
      "text": "— 55 —pois ele percebeu que, por mais sabedoria que ele tivesse, não \\nsão todos que iriam compreender, entender o que é viver, pois \\ncada um tem a sua linha de tempo de raciocínio.\\nNa Bíblia, temos o “número 666” , de acordo com os estudiosos \\nde simbologia acredita-se que quer dizer Cesar. “Quem tiver \\ndiscernimento, calcule o número da besta, pois é número de \\nhomem, e seu número é 666... ” Na Antiguidade, usar números \\npara disfarçar um nome era necessário. Nos alfabetos grego e \\nhebraico, toda letra tem um número correspondente, então, \\nse você somasse todas as letras do seu nome, você tinha um \\ncódigo numérico que, interpretando, dava o nome do Cesar.\\nCesar teve uma vida de guerreiro com um pensamento filosó -\\nfico muito aflorado, tudo em sua vida sempre foi muita luta, \\no tornando uma pessoa calculista e metódica, o prejudicando \\nem fazer alianças. A extravagância de Cesar e a prepotência \\nde eu posso eu consigo, pela vida dele sempre ter muita luta, \\nsaindo de uma vida inferior e chegando no mais alto escalão \\nda sociedade, o fez querer brigar por guerras através da sua \\nprópria ganância.\\nFrases\\nSabe o porquê tem muita gente odiando? Simples, odiar é fácil \\ne não exige força. Agora, tente amar! Amar, não raramente, é \\ndar as mãos ao sofrimento.\\nNão julgue alguém pela aparência no primeiro encontro, pois \\nnão percebemos as qualidades da alma logo de cara.\\nReligião aliada à política é uma arma perfeita pra escravizar \\nignorantes.\\nQuando nos acomodamos à rotina da vida, perdemos, pouco \\ncaos do passado sendo vivido no futuro editável.indd   55caos do passado sendo vivido no futuro editável.indd   55 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 82353,
      "chapter": 2,
      "page": 55,
      "segment_type": "page",
      "themes": {},
      "difficulty": 26.226258992805754,
      "complexity_metrics": {
        "word_count": 278,
        "sentence_count": 16,
        "paragraph_count": 1,
        "avg_sentence_length": 17.375,
        "avg_word_length": 4.920863309352518,
        "unique_word_ratio": 0.6798561151079137,
        "avg_paragraph_length": 278.0,
        "punctuation_density": 0.17985611510791366,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "número",
          "vida",
          "pois",
          "cesar",
          "nome",
          "muita",
          "mais",
          "você",
          "sempre",
          "luta",
          "pela",
          "amar",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "percebeu",
          "sabedoria"
        ],
        "entities": [
          [
            "55",
            "CARDINAL"
          ],
          [
            "que iriam compreender",
            "PERSON"
          ],
          [
            "Na Bíblia",
            "ORG"
          ],
          [
            "estudiosos \\nde simbologia",
            "ORG"
          ],
          [
            "Cesar",
            "ORG"
          ],
          [
            "número da besta",
            "PERSON"
          ],
          [
            "número de \\nhomem",
            "PERSON"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "666",
            "CARDINAL"
          ],
          [
            "números",
            "PRODUCT"
          ]
        ],
        "readability_score": 89.83624100719425,
        "semantic_density": 0,
        "word_count": 278,
        "unique_words": 189,
        "lexical_diversity": 0.6798561151079137
      },
      "preservation_score": 1.1839589724870433e-05
    },
    {
      "id": 1,
      "text": "— 56 —a pouco, o pulso de nós mesmos, deixando o nosso processo \\nde crescimento à mercê das influências e das circunstâncias \\nexternas.\\nSanto Agostinho21\\nEle foi a peça de encaixe para a evolução da propagação da ener -\\ngia, encaixando o seu comportamento e suas ideias de uma for -\\nma de constância de ciclo comportamental, de pré-cataclismo \\nperante a um sentimento diante de um período Pré-Idade das \\nTrevas “massa escura” , da forma de onda da propagação da ener -\\ngia, entre a massa escura e a captação de sentimento evolutivo, \\napós grandes captadores de energia em forma de caos, o Santo \\nAgostinho veio na forma de amar, pois ele canalizou a energia \\ndevido à massa escura está “dominando” , só sentia a energia, \\npois teve muito caos e, em algum momento, essa energia seria \\nem forma da bondade!!!\\nNa Igreja Católica e na Comunhão Anglicana, Agostinho é ve -\\nnerado como um santo, o patrono dos agostinianos. Sua festa \\né celebrada no dia de sua morte, 28 de agosto. Muitos protes -\\ntantes, consideram Agostinho como um dos “pais teológicos” \\nda Reforma Protestante por causa de suas doutrinas sobre a \\nsalvação e graça divina.\\nA “Bondade” captada de Santo Agostinho gerou o caos nova -\\nmente, pois, durante um bom período, a forma de interpretar \\na bondade foi destoando. Foi o marco de transição de forma \\nde pensar na dor e começar a pensar a viver novamente, seme -\\nlhante à era dos primeiros filósofos a aparecer e os primeiros \\nprofetas em forma de pensar perante ao caos.\\n21.  Texto baseado em https://pt.m.wikipedia.org/wiki/Agostinho_de_ Hipona .\\ncaos do passado sendo vivido no futuro editável.indd   56caos do passado sendo vivido no futuro editável.indd   56 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 84141,
      "chapter": 2,
      "page": 56,
      "segment_type": "page",
      "themes": {},
      "difficulty": 28.203125,
      "complexity_metrics": {
        "word_count": 288,
        "sentence_count": 15,
        "paragraph_count": 1,
        "avg_sentence_length": 19.2,
        "avg_word_length": 4.899305555555555,
        "unique_word_ratio": 0.6076388888888888,
        "avg_paragraph_length": 288.0,
        "punctuation_density": 0.14583333333333334,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "forma",
          "caos",
          "santo",
          "energia",
          "agostinho",
          "massa",
          "escura",
          "pois",
          "bondade",
          "pensar",
          "propagação",
          "ener",
          "suas",
          "perante",
          "sentimento",
          "período",
          "como",
          "primeiros",
          "passado",
          "sendo"
        ],
        "entities": [
          [
            "56",
            "CARDINAL"
          ],
          [
            "de nós mesmos",
            "PERSON"
          ],
          [
            "deixando o",
            "ORG"
          ],
          [
            "encaixando o",
            "ORG"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "ma de constância de ciclo",
            "PERSON"
          ],
          [
            "Trevas",
            "ORG"
          ],
          [
            "da forma de onda da propagação",
            "PERSON"
          ],
          [
            "forma de caos",
            "ORG"
          ],
          [
            "teve muito caos e",
            "PERSON"
          ]
        ],
        "readability_score": 88.93020833333333,
        "semantic_density": 0,
        "word_count": 288,
        "unique_words": 175,
        "lexical_diversity": 0.6076388888888888
      },
      "preservation_score": 1.2451982296846492e-05
    },
    {
      "id": 1,
      "text": "— 57 —Durante esse período, tivemos o surgimento de grandes impé -\\nrios em nome de alguma divindade, gerando caos novamente \\nda minha energia ser mais importante que a sua energia, surgiu \\nnovamente o extremismo, ganância, sexo, excessos, megaloma -\\nníaco devido à Terra voltar ao seu eixo perante o universo, para \\ntornar o nosso planeta melhor habitável novamente, gerando \\nmais recursos da Terra, gerando um ciclo vicioso da propaga -\\nção da energia diante da massa escura gerado por nós mesmos. \\nPeste negra22 \\nA “cereja do bolo perante o caos e devido a ter uma passagem \\nbíblica apocalíptica” também conhecida como Grande Peste, \\nPeste ou Praga, foi a pandemia mais devastadora registada na \\nhistória humana, tendo resultado na morte de 75 a 200 mi -\\nlhões de pessoas na Eurásia, atingindo o pico na Europa en -\\ntre os anos de 1347 e 1351. Acredita-se que a bactéria Yersi-\\nnia pestis , que resulta em várias formas de peste (septicémica, \\npneumônica e, a mais comum, bubônica), tenha sido a causa. \\nA Peste Negra foi o primeiro grande surto europeu de peste e a \\nsegunda pandemia da doença. A pandemia que estamos viven -\\ndo mostra o caos criado pela ausência de mão de obra, matéria \\nprima, distribuição de alimentos e etc.\\nA Peste Negra provavelmente teve a sua origem na Ásia Cen -\\ntral ou na Ásia Oriental, de onde viajou ao longo da Rota da \\nSeda, atingindo a Crimeia por volta de 1340. De lá, era prova -\\nvelmente transportada por pulgas que viviam nos ratos que \\nviajavam em navios mercantes genoveses, espalhando-se por \\ntoda a bacia do Mediterrâneo, atingindo o resto da Europa \\natravés da península italiana.\\n22.  Texto baseado em https://pt.m.wikipedia.org/wiki/Peste _Negra .\\ncaos do passado sendo vivido no futuro editável.indd   57caos do passado sendo vivido no futuro editável.indd   57 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 85978,
      "chapter": 2,
      "page": 57,
      "segment_type": "page",
      "themes": {},
      "difficulty": 26.85200868621064,
      "complexity_metrics": {
        "word_count": 307,
        "sentence_count": 15,
        "paragraph_count": 1,
        "avg_sentence_length": 20.466666666666665,
        "avg_word_length": 4.95114006514658,
        "unique_word_ratio": 0.6579804560260586,
        "avg_paragraph_length": 307.0,
        "punctuation_density": 0.1465798045602606,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "peste",
          "caos",
          "mais",
          "gerando",
          "novamente",
          "energia",
          "pandemia",
          "atingindo",
          "devido",
          "terra",
          "perante",
          "grande",
          "europa",
          "negra",
          "ásia",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável"
        ],
        "entities": [
          [
            "57",
            "CARDINAL"
          ],
          [
            "Durante",
            "ORG"
          ],
          [
            "tivemos o",
            "ORG"
          ],
          [
            "universo",
            "ORG"
          ],
          [
            "para \\ntornar",
            "PERSON"
          ],
          [
            "mesmos",
            "PERSON"
          ],
          [
            "também conhecida",
            "PERSON"
          ],
          [
            "Praga",
            "PERSON"
          ],
          [
            "mais devastadora registada na \\nhistória humana",
            "PERSON"
          ],
          [
            "200",
            "CARDINAL"
          ]
        ],
        "readability_score": 88.28132464712269,
        "semantic_density": 0,
        "word_count": 307,
        "unique_words": 202,
        "lexical_diversity": 0.6579804560260586
      },
      "preservation_score": 1.3108117195392267e-05
    },
    {
      "id": 1,
      "text": "— 58 —Estima-se que a Peste Negra tenha matado entre 30% a 60% \\nda população da Europa. Se a população atual não está sendo \\nbem distribuída, imagina sem os recursos que nós temos hoje \\ne se não tivesse ocorrido essa quantidade de mortes, consegui -\\nríamos ter alimento para toda a população? Será que conse -\\nguiríamos sobreviver entre nós? A peste retornou várias vezes \\ncomo surtos até ao início do século XX.\\nÁsia Central ou na Ásia Oriental teve o início da peste negra. \\nNaquele ano, uma misteriosa (vulcão) névoa cobriu a Europa, \\nOriente Médio e partes da Ásia por quase 2 anos. O sol perdeu \\na intensidade do brilho e as temperaturas caíram até 2,5 graus, \\niniciando a década mais fria dos últimos 2.300 anos. Faça as \\nsuas próprias conclusões sobre a coincidência de acontecimen -\\ntos. Os nossos ciclos são constante, os nossos erros são um ciclo \\nconstante, a nossa vida é um ciclo constante, a Terra gira cons -\\ntantemente, o sol gira constantemente e nós giramos entorno \\ndo sol constantemente, o sol gira entorno de um buraco negro \\nconstantemente e as galáxias têm um movimento (deve ser al -\\ngum padrão que ainda não identificamos) constante.\\nA energia não se propaga, ela é um movimento constante e \\ntudo o que é, é tudo que é para ser.\\nCuriosidade\\nQuais são os territórios que mais continham pessoas nesse pe -\\nríodo? \\ncaos do passado sendo vivido no futuro editável.indd   58caos do passado sendo vivido no futuro editável.indd   58 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 87945,
      "chapter": 2,
      "page": 58,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 25.032941176470587,
      "complexity_metrics": {
        "word_count": 255,
        "sentence_count": 15,
        "paragraph_count": 1,
        "avg_sentence_length": 17.0,
        "avg_word_length": 4.776470588235294,
        "unique_word_ratio": 0.6588235294117647,
        "avg_paragraph_length": 255.0,
        "punctuation_density": 0.12156862745098039,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "constante",
          "peste",
          "população",
          "sendo",
          "ásia",
          "gira",
          "constantemente",
          "negra",
          "entre",
          "europa",
          "início",
          "anos",
          "mais",
          "nossos",
          "ciclo",
          "entorno",
          "movimento",
          "tudo",
          "passado",
          "vivido"
        ],
        "entities": [
          [
            "58",
            "CARDINAL"
          ],
          [
            "Estima",
            "PERSON"
          ],
          [
            "Negra",
            "PERSON"
          ],
          [
            "matado",
            "GPE"
          ],
          [
            "30%",
            "PERCENT"
          ],
          [
            "60%",
            "PERCENT"
          ],
          [
            "Europa",
            "LOC"
          ],
          [
            "imagina sem",
            "PERSON"
          ],
          [
            "essa quantidade de mortes",
            "PERSON"
          ],
          [
            "XX",
            "GPE"
          ]
        ],
        "readability_score": 90.06705882352941,
        "semantic_density": 0,
        "word_count": 255,
        "unique_words": 168,
        "lexical_diversity": 0.6588235294117647
      },
      "preservation_score": 7.69864947627043e-06
    },
    {
      "id": 1,
      "text": "— 59 —Capítulo 8\\nIdade Média pós-cataclismo (apocalipse)\\nEsse capítulo está mais para um seguimento de linha do tem -\\npo, perante a energia se propagando levando a uma simetria \\nda energia em linha de tempo, pois mostra o quanto foi de \\ninsignificância comparando com outros momentos históricos \\npara o mundo espiritual, filosófico e científico, não tendo fre -\\nquência receptiva no mundo para se captar, levando as pessoas \\nviverem A IDADE DAS TREVAS!!!\\nSanto Tomás de Aquino23\\nPrimeira pessoa a voltar a sentir a energia e interpretar de al -\\nguma forma a prosperidade de harmonia do físico para o es -\\npiritual.\\nAos 5 anos de idade, começou a estudar em Monte Cassino, \\nmas, depois que o conflito militar entre o Imperador Frederi -\\nco II e o Papa Gregório IX chegou à abadia por volta de 1240, \\na Universidade em Nápoles, recém-criada por Frederico em \\nNápoles. Foi provavelmente lá que Tomás foi introduzido aos \\nestudos filosóficos, grande influência para sua filosofia teoló -\\ngica. Na universidade ele conheceu um pregador dominicano \\nque era parte do grande esforço empreendido pela Ordem \\ndos Pregadores para recrutar seguidores. Aos 19, Tomás resol -\\nveu se juntar à ordem, o que não agradou sua família. Numa \\n23.  Texto baseado em https://pt.m.wikipedia.org/wiki/Tom%C3%A1s_de_\\nAquino .\\ncaos do passado sendo vivido no futuro editável.indd   59caos do passado sendo vivido no futuro editável.indd   59 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 89554,
      "chapter": 8,
      "page": 59,
      "segment_type": "page",
      "themes": {
        "filosofia": 60.0,
        "arte": 40.0
      },
      "difficulty": 24.98805418719212,
      "complexity_metrics": {
        "word_count": 232,
        "sentence_count": 14,
        "paragraph_count": 1,
        "avg_sentence_length": 16.571428571428573,
        "avg_word_length": 5.198275862068965,
        "unique_word_ratio": 0.7025862068965517,
        "avg_paragraph_length": 232.0,
        "punctuation_density": 0.14224137931034483,
        "line_break_count": 25,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "idade",
          "energia",
          "tomás",
          "capítulo",
          "linha",
          "levando",
          "mundo",
          "universidade",
          "nápoles",
          "grande",
          "ordem",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "média",
          "cataclismo",
          "apocalipse"
        ],
        "entities": [
          [
            "59",
            "CARDINAL"
          ],
          [
            "8",
            "CARDINAL"
          ],
          [
            "Idade Média",
            "FAC"
          ],
          [
            "mostra",
            "LOC"
          ],
          [
            "quanto foi de \\ninsignificância comparando",
            "PERSON"
          ],
          [
            "outros momentos",
            "PERSON"
          ],
          [
            "históricos \\npara o mundo espiritual",
            "ORG"
          ],
          [
            "filosófico e científico",
            "PERSON"
          ],
          [
            "Tomás de Aquino23\\nPrimeira",
            "PERSON"
          ],
          [
            "interpretar de al -\\nguma forma",
            "PERSON"
          ]
        ],
        "readability_score": 90.15480295566502,
        "semantic_density": 0,
        "word_count": 232,
        "unique_words": 163,
        "lexical_diversity": 0.7025862068965517
      },
      "preservation_score": 8.383945925862683e-06
    },
    {
      "id": 1,
      "text": "— 60 —tentativa de impedir que sua mãe influenciasse a escolha de \\nTomás, os dominicanos arranjaram para que ele se mudasse \\npara Roma e, de lá, para Paris. Porém, durante a viagem para \\nRoma, seus irmãos o capturaram ele a mando de sua mãe, seus \\npais o deixaram preso em Monte San Giovanni. Ficou preso \\npor cerca de um ano nos castelos da família em Monte San \\nGiovanni. Desesperados com a teimosia de Tomás, dois de seus \\nirmãos chegaram a ponto de contratarem uma prostituta para \\nseduzi-lo. De acordo com a lenda, Tomás a expulsou com um \\nferro em brasa e, durante a noite, “dois anjos apareceram para \\nele enquanto ele dormia para fortalecer sua determinação de \\npermanecer celibatário” . Concentração em querer algo, nos faz \\ncriar sonhos e realidades distintas para o nosso próprio “bem” . \\nEm 1244, sua família percebeu que era desnecessário aquele \\nesforço, Tomás seguiu primeiro para Nápoles e, depois, para \\nRoma, onde se encontrou com o mestre-geral da Ordem dos \\nPregadores.\\nEle começou a sentir a penitência pelos seus pecados, come -\\nçou a se flagelar figurativamente pelos outros e por si próprio, \\ncom frases de impacto de falta de entendimento perante ao \\nerro dos outros, chegando a sentir dor sentimental!!\\nFrases\\nDê-me, Senhor, agudeza para entender, capacidade para reter, \\nmétodo e faculdade para aprender, sutileza para interpretar, \\ngraça e abundância para falar, acerto ao começar, direção ao \\nprogredir e perfeição ao concluir.\\nA ninguém te mostres muito íntimo, pois familiaridade exces -\\nsiva gera desprezo.\\nUm homem é chamado paciente não porque foge do mal, mas \\ncaos do passado sendo vivido no futuro editável.indd   60caos do passado sendo vivido no futuro editável.indd   60 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 91126,
      "chapter": 3,
      "page": 60,
      "segment_type": "page",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 29.380196399345337,
      "complexity_metrics": {
        "word_count": 282,
        "sentence_count": 13,
        "paragraph_count": 1,
        "avg_sentence_length": 21.692307692307693,
        "avg_word_length": 5.113475177304965,
        "unique_word_ratio": 0.6595744680851063,
        "avg_paragraph_length": 282.0,
        "punctuation_density": 0.16312056737588654,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "tomás",
          "seus",
          "roma",
          "durante",
          "irmãos",
          "preso",
          "monte",
          "giovanni",
          "família",
          "dois",
          "próprio",
          "sentir",
          "pelos",
          "outros",
          "frases",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável"
        ],
        "entities": [
          [
            "60",
            "CARDINAL"
          ],
          [
            "Paris",
            "GPE"
          ],
          [
            "para \\nRoma",
            "PERSON"
          ],
          [
            "Monte San Giovanni",
            "PERSON"
          ],
          [
            "Monte San \\n",
            "PERSON"
          ],
          [
            "Giovanni",
            "GPE"
          ],
          [
            "De",
            "PERSON"
          ],
          [
            "Tomás",
            "PERSON"
          ],
          [
            "sua determinação de \\npermanecer celibatário",
            "ORG"
          ],
          [
            "faz",
            "ORG"
          ]
        ],
        "readability_score": 87.61980360065466,
        "semantic_density": 0,
        "word_count": 282,
        "unique_words": 186,
        "lexical_diversity": 0.6595744680851063
      },
      "preservation_score": 1.2051010969957405e-05
    },
    {
      "id": 1,
      "text": "— 61 —porque aguenta um mal presente de forma honrosa, isto é, sem \\nficar indevidamente triste por isso.\\nA beleza é a marca do que é bem-feito, seja um universo, seja \\num objeto.\\nPeríodos de guerra\\nIslã: nascido na Península Arábica, conseguiu expandir-se em \\ndireção ao norte africano, ao Oriente Médio e ao sul europeu.\\nImpério Mongol: nascido no Extremo Oriente, ao norte da \\nChina, conseguiu construir o império com a maior extensão \\nterritorial de toda a história, que abrangia quase toda a Ásia \\n(incluindo a Rússia), a Indochina e o leste europeu.\\nImpério Bizantino: remanescente da Antiguidade, resistiu até \\no ano de 1453, quando seu centro, Constantinopla, foi invadi -\\ndo e submetido pelos muçulmanos.\\nCristianismo cruzada: muitas derivações e muitos conflitos em \\npaíses e reinos diferentes, propagação da energia cristã foi mais \\nsignificativa, irei interpretar diante da necessidade da linha de \\ntempo da energia perante ao caos que nos ronda.\\nIslã24\\nAntes do advento do Islã, os árabes não formavam uma unida -\\nde política coerente. No início do século VI, a Arábia posicio -\\nna-se em torno de dois impérios que se defrontam. A oeste, Bi -\\nzâncio, cristã e herdeira de Roma, dominava o norte de África, \\n24.  Texto baseado em https://pt.m.wikipedia.org/wiki/Isl%C3%A3o#:~:tex -\\nt=Isl%C3%A3o%20ou%20isl%C3%A3%20(em%20%C3%A1rabe,suna%2C%20\\nparte%20do%20h%C3%A1dice )%20de .\\ncaos do passado sendo vivido no futuro editável.indd   61caos do passado sendo vivido no futuro editável.indd   61 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 92994,
      "chapter": 3,
      "page": 61,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 24.02426948051948,
      "complexity_metrics": {
        "word_count": 231,
        "sentence_count": 16,
        "paragraph_count": 1,
        "avg_sentence_length": 14.4375,
        "avg_word_length": 5.6017316017316015,
        "unique_word_ratio": 0.6926406926406926,
        "avg_paragraph_length": 231.0,
        "punctuation_density": 0.21212121212121213,
        "line_break_count": 26,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "norte",
          "império",
          "seja",
          "islã",
          "nascido",
          "conseguiu",
          "oriente",
          "europeu",
          "toda",
          "energia",
          "cristã",
          "caos",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "porque",
          "aguenta"
        ],
        "entities": [
          [
            "61",
            "CARDINAL"
          ],
          [
            "de forma",
            "PERSON"
          ],
          [
            "Islã",
            "PERSON"
          ],
          [
            "Península Arábica",
            "PERSON"
          ],
          [
            "norte africano",
            "PERSON"
          ],
          [
            "Oriente Médio",
            "PERSON"
          ],
          [
            "Império Mongol",
            "PERSON"
          ],
          [
            "Extremo Oriente",
            "PERSON"
          ],
          [
            "China",
            "GPE"
          ],
          [
            "história",
            "GPE"
          ]
        ],
        "readability_score": 91.10073051948052,
        "semantic_density": 0,
        "word_count": 231,
        "unique_words": 160,
        "lexical_diversity": 0.6926406926406926
      },
      "preservation_score": 1.1941655153533109e-05
    },
    {
      "id": 1,
      "text": "— 62 —a Palestina, a Síria, a Anatólia, a Grécia e o Sul da Itália. \\nImpério Mongol25\\nO Império Mongol dos séculos XIII e XIV foi o maior impé -\\nrio de terras contíguas da história e o segundo maior império \\nem área. Originário da Mongólia no Leste Asiático, o Império \\nMongol chegou a se estender da Europa Oriental e partes da \\nEuropa Central até o Mar do Japão, além de também para o \\nnorte, em partes do Ártico; para o leste e para o sul no subcon -\\ntinente indiano, no sudeste da Ásia continental e no planalto \\niraniano; e para o oeste até o Levante e as montanhas dos Cár -\\npatos. O Império Mongol surgiu da unificação de várias tribos \\nnômades na pátria mongol sob a liderança de Genghis Khan \\na quem um conselho proclamou como o governante de todos \\nos mongóis aproximadamente 1200. O império cresceu rapi -\\ndamente enviavam exércitos invasores em todas as direções. \\nO vasto império transcontinental conectou o Oriente com o \\nOcidente, o Pacífico com o Mediterrâneo, permitindo a disse -\\nminação e troca de comércio, tecnologias, mercadorias e ideo -\\nlogias em toda a Eurásia.\\nImpério Bizantino26\\nO Império Romano e o Império Bizantino não é possível atri -\\nbuir uma data de separação. Muitos conflitos do século IV ao \\nséculo VI marcaram o período de transição durante o qual as \\nmetades oriental e ocidental do Império Romano se dividi -\\n25.  Texto baseado em https://pt.m.wikipedia.org/wiki/Imp%C3%A9rio_\\nMongol .\\n26.  Texto baseado em https://pt.m.wikipedia.org/wiki/Imp%C3%A9rio_Bi -\\nzantino .\\ncaos do passado sendo vivido no futuro editável.indd   62caos do passado sendo vivido no futuro editável.indd   62 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 94653,
      "chapter": 3,
      "page": 62,
      "segment_type": "page",
      "themes": {
        "ciencia": 30.232558139534888,
        "arte": 46.51162790697674,
        "tecnologia": 23.25581395348837
      },
      "difficulty": 23.518454545454546,
      "complexity_metrics": {
        "word_count": 275,
        "sentence_count": 20,
        "paragraph_count": 1,
        "avg_sentence_length": 13.75,
        "avg_word_length": 4.9781818181818185,
        "unique_word_ratio": 0.6,
        "avg_paragraph_length": 275.0,
        "punctuation_density": 0.13818181818181818,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "império",
          "mongol",
          "maior",
          "leste",
          "europa",
          "oriental",
          "partes",
          "romano",
          "século",
          "texto",
          "baseado",
          "https",
          "wikipedia",
          "wiki",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd"
        ],
        "entities": [
          [
            "62",
            "CARDINAL"
          ],
          [
            "Síria",
            "GPE"
          ],
          [
            "Anatólia",
            "GPE"
          ],
          [
            "Grécia",
            "PERSON"
          ],
          [
            "Itália",
            "GPE"
          ],
          [
            "Império Mongol25\\nO",
            "PERSON"
          ],
          [
            "XIII",
            "ORG"
          ],
          [
            "XIV",
            "ORG"
          ],
          [
            "da história",
            "PERSON"
          ],
          [
            "Mongólia",
            "GPE"
          ]
        ],
        "readability_score": 91.63154545454546,
        "semantic_density": 0,
        "word_count": 275,
        "unique_words": 165,
        "lexical_diversity": 0.6
      },
      "preservation_score": 1.0002412008942265e-05
    },
    {
      "id": 1,
      "text": "— 63 —ram. Em 285, o Imperador Diocleciano dividiu a governança \\nem duas metades. Entre 324 e 330, Constantino transferiu a \\ncapital principal de Roma para Bizâncio, conhecida mais tarde \\ncomo Constantinopla e Nova Roma. Sob Teodósio I o cristia -\\nnismo tornou-se a religião oficial do império e, com sua morte, \\no Estado romano dividiu-se definitivamente em duas metades, \\ncada qual controlada por um de seus filhos. E finalmente, sob \\no reinado de Heráclio, a governança e as forças armadas do \\nimpério foram reestruturadas e o grego foi adotado em lugar \\ndo latim. O Império Bizantino se distingue da Roma Antiga \\nna medida em que foi orientado à cultura grega em e caracte -\\nrizou-se pelo cristianismo ortodoxo.\\nAs fronteiras do império mudaram muito ao longo de sua exis -\\ntência, alcançou sua maior extensão após reconquistar muito \\ndos territórios mediterrâneos antes pertencentes à porção oci -\\ndental do Império Romano, incluindo o norte da África, pe -\\nnínsula Itálica e parte da Península Ibérica. Perderam muitos \\nterritórios durante as invasões muçulmanas do século VII. \\nA ausência de captação de energia fez grandes religiões caírem \\ne surgirem impérios, pois com a ausência de energia como te -\\nríamos novos profetas, filósofos, novos pajés, novos captores \\nde energia para dar uma direção espiritual, ao invés de uma \\ndireção material (caos, guerras, impérios).\\nCristianismo cruzada27\\nCruzada é um termo utilizado para designar qualquer dos mo -\\nvimentos militares de inspiração cristã, que partiram da Euro -\\npa Ocidental em direção à Terra Santa e à cidade de Jerusalém \\ncom o intuito de conquistá-las, ocupá-las e mantê-las sob do -\\n27.  Texto baseado em https://pt.m.wikipedia.org/wiki/C ruzada .\\ncaos do passado sendo vivido no futuro editável.indd   63caos do passado sendo vivido no futuro editável.indd   63 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 96434,
      "chapter": 3,
      "page": 63,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 27.376490528414756,
      "complexity_metrics": {
        "word_count": 295,
        "sentence_count": 17,
        "paragraph_count": 1,
        "avg_sentence_length": 17.352941176470587,
        "avg_word_length": 5.274576271186441,
        "unique_word_ratio": 0.6813559322033899,
        "avg_paragraph_length": 295.0,
        "punctuation_density": 0.13898305084745763,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "império",
          "roma",
          "energia",
          "novos",
          "direção",
          "dividiu",
          "governança",
          "duas",
          "metades",
          "como",
          "romano",
          "cristianismo",
          "muito",
          "territórios",
          "ausência",
          "impérios",
          "caos",
          "passado",
          "sendo",
          "vivido"
        ],
        "entities": [
          [
            "63",
            "CARDINAL"
          ],
          [
            "285",
            "CARDINAL"
          ],
          [
            "Imperador Diocleciano",
            "PERSON"
          ],
          [
            "Entre 324",
            "ORG"
          ],
          [
            "330",
            "CARDINAL"
          ],
          [
            "Constantino",
            "ORG"
          ],
          [
            "Bizâncio",
            "GPE"
          ],
          [
            "Constantinopla",
            "ORG"
          ],
          [
            "Nova Roma",
            "GPE"
          ],
          [
            "Sob Teodósio",
            "PERSON"
          ]
        ],
        "readability_score": 89.74115653040877,
        "semantic_density": 0,
        "word_count": 295,
        "unique_words": 201,
        "lexical_diversity": 0.6813559322033899
      },
      "preservation_score": 1.2685274705218321e-05
    },
    {
      "id": 1,
      "text": "— 64 —mínio cristão. Essas guerras estenderam-se entre os séculos XI \\ne XIII, as Cruzadas foram chamadas de “invasões francas” , os \\ncruzados vinha dos territórios do antigo Império Carolíngio e \\nse autodenominavam “francos” .\\nO termo Cruzada não era conhecido no tempo histórico, o \\nnome dado era peregrinação e guerra santa. O termo Cruza -\\nda surgiu porque seus participantes se consideravam soldados \\nde Cristo, e por sempre cometerem muitos pecados, a cruzada \\nvirou uma forma de dívida divina para o própria necessidade \\nda igreja.\\nPor volta do ano 1000, aumentou muito a peregrinação de cris -\\ntãos para Jerusalém, por causa do misticismo do fim do mundo, \\ndevido a não ter captação de energia por causa do cataclisma \\nque os humanos causaram, e o planeta Terra para regularizar \\no seu próprio eixo, precisa esfriar o seu corpo e desacelerar, \\ncriando a falta de energia, criando uma sensação de ausência, \\nfazendo o humano fazer autoflagelação.\\nAqui que entra o Santo Agostinho!!!! É união de Roma, Bi -\\nzantino e várias outras regiões que foram na mesma forma de \\npensar, do melhor para se viver, em uma forma de ver a vida, \\ndiante de uma energia que tinha sido captada (Santo Agosti -\\nnho) é destoada (ganância de si próprio) ao ver, diante da sua \\nimportância perante a uma energia que outra pessoa (Santo \\nAgostinho), sentiu e emitiu e por quem aceitou, destoando va -\\nlores e princípios ao seu próprio ver. O início da Idade Média \\né 476, marco do último imperador romano do Ocidente. O \\ntérmino da idade média tem muitas advertências, todas elas \\npor volta de 1500.\\nForam mil anos de Idade Média, dois filósofos e religiosos com \\nlinha de raciocínio extremista, perante a energia cristã (Deus), \\nque se propagou até os dias de hoje, como a maior religião do \\ncaos do passado sendo vivido no futuro editável.indd   64caos do passado sendo vivido no futuro editável.indd   64 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 98424,
      "chapter": 3,
      "page": 64,
      "segment_type": "page",
      "themes": {},
      "difficulty": 29.96656346749226,
      "complexity_metrics": {
        "word_count": 323,
        "sentence_count": 12,
        "paragraph_count": 1,
        "avg_sentence_length": 26.916666666666668,
        "avg_word_length": 4.8885448916408665,
        "unique_word_ratio": 0.653250773993808,
        "avg_paragraph_length": 323.0,
        "punctuation_density": 0.13622291021671826,
        "line_break_count": 31,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "forma",
          "próprio",
          "santo",
          "idade",
          "média",
          "termo",
          "cruzada",
          "peregrinação",
          "volta",
          "causa",
          "criando",
          "agostinho",
          "diante",
          "perante",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável"
        ],
        "entities": [
          [
            "64",
            "CARDINAL"
          ],
          [
            "mínio cristão",
            "PERSON"
          ],
          [
            "XIII",
            "GPE"
          ],
          [
            "Cruzadas",
            "ORG"
          ],
          [
            "Império Carolíngio",
            "PERSON"
          ],
          [
            "francos",
            "GPE"
          ],
          [
            "Cruzada",
            "ORG"
          ],
          [
            "histórico",
            "PERSON"
          ],
          [
            "de Cristo",
            "ORG"
          ],
          [
            "cometerem muitos",
            "PERSON"
          ]
        ],
        "readability_score": 85.07510319917441,
        "semantic_density": 0,
        "word_count": 323,
        "unique_words": 211,
        "lexical_diversity": 0.653250773993808
      },
      "preservation_score": 1.4464129319053534e-05
    },
    {
      "id": 1,
      "text": "— 65 —mundo!!! A importância desses dois filósofos, Santo Augusti -\\nnho e o Santo Tomás de Aquino, foi necessária para a propa -\\ngação da energia, em forma de pensamento e semelhança de \\ncaos que se viviam nas regiões, ocorrendo uniões em grandes \\ngrupos com o término dos dois grandes impérios, Romano \\n(transição de monarquia para império) e Bizantino com a \\nforça da energia dos dois últimos grandes captores de ener -\\ngia, se propagando durante 1000 anos após o pior cataclismo \\nque sofremos, dando a discrepância na religião cristã perante \\nao mundo e transformando a Europa no velho continente e \\nsendo o “centro do mundo” , pois de lá saiu a última grande \\nenergia captada antes do cataclismo, deixando o mundo ape -\\nnas com massa escura, até conseguir se recuperar do grande \\ncataclismo ocorrido, por não controlarmos as nossas próprias \\nfalhas, gerando massa negra por não conseguir sentir a energia \\nde um bem melhor para um todo, fazendo da sua ganância \\ndiante de um viver melhor, retirando mais do que o necessá -\\nrio do planeta Terra, tirando o nosso próprio planeta do eixo, \\nredirecionando a energia do planeta para si próprio, para se \\nmanter em harmonia com o universo!!!\\nNesse mesmo período, surgiu o início da pior característica \\nque um ser humano criou por outro, o preconceito racial!!!\\nPreconceito racial\\nSurgiu através de uma crença religiosa e interpretativa, para \\no bem de uma aparência diferente, separando o mundo em \\nnegros e brancos.\\nApós o dilúvio, que daria fim ao caos em que se encontrava a \\nhumanidade, os filhos de Noé, Cam, Sem e Jafé, foram os res -\\nponsáveis por repovoar a terra com seus descendentes. Cada \\num cuidou de repovoar cada continente dos três conhecidos \\nno velho mundo. Sem repovoou a Ásia. Jafé a Europa e Cam \\ncaos do passado sendo vivido no futuro editável.indd   65caos do passado sendo vivido no futuro editável.indd   65 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 100470,
      "chapter": 3,
      "page": 65,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.66645962732919,
      "complexity_metrics": {
        "word_count": 322,
        "sentence_count": 10,
        "paragraph_count": 1,
        "avg_sentence_length": 32.2,
        "avg_word_length": 4.888198757763975,
        "unique_word_ratio": 0.6024844720496895,
        "avg_paragraph_length": 322.0,
        "punctuation_density": 0.13975155279503104,
        "line_break_count": 31,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mundo",
          "energia",
          "dois",
          "caos",
          "grandes",
          "cataclismo",
          "sendo",
          "planeta",
          "santo",
          "após",
          "pior",
          "europa",
          "velho",
          "continente",
          "grande",
          "massa",
          "conseguir",
          "melhor",
          "terra",
          "próprio"
        ],
        "entities": [
          [
            "65",
            "CARDINAL"
          ],
          [
            "Tomás de Aquino",
            "PERSON"
          ],
          [
            "semelhança de \\ncaos",
            "PERSON"
          ],
          [
            "nas regiões",
            "PERSON"
          ],
          [
            "Romano",
            "PERSON"
          ],
          [
            "para império",
            "PERSON"
          ],
          [
            "gia",
            "GPE"
          ],
          [
            "1000",
            "CARDINAL"
          ],
          [
            "anos após",
            "PERSON"
          ],
          [
            "que sofremos",
            "PERSON"
          ]
        ],
        "readability_score": 82.4335403726708,
        "semantic_density": 0,
        "word_count": 322,
        "unique_words": 194,
        "lexical_diversity": 0.6024844720496895
      },
      "preservation_score": 1.2882115174782053e-05
    },
    {
      "id": 1,
      "text": "— 66 —a África. O fato que justificou a inferioridade dos africanos foi \\numa passagem bíblica em que Cam, seu filho Canaã e toda \\nsua descendência foram amaldiçoados por Noé. No capítulo \\n9, versículos 18-27 do Gênesis diz: após beber vinho, Noé fi -\\ncou nu dentro de sua tenda, dormindo. Cam, pai de Canaã, \\nviu a nudez de seu pai e chamou os dois irmão, Sem e Jafé, \\nque tomaram um manto e o cobriram. Ao acordar, Noé soube \\ndo acontecido e pronunciou o terrível veredicto: “maldito seja \\nCanaã, que ele seja para seus irmãos o último dos escravos. \\nBendito seja Javé, o Deus de Sem, e que Canaã seja seu escravo \\ne que Deus dilate a Jafé, e que Canaã seja seu escravo. ”\\nEssa passagem da Bíblia era usada na Cruzada para necessidade \\nde se ter mão de obra escrava, devido a eu ser melhor que você \\nperante a Deus, impedindo do ser humano como qualquer \\num outro ser humano, ter tempo para evoluir em um todo \\nna vida mental, pois não tinham descanso mental pelo corpo \\nfísico sempre estar em tensão, pela forma que se vivia uma vida \\ndiante da minha cor e aceitação, diante de se caminhar na rua \\ncomo inferior. \\nFamília, pois não tinha o necessário para se viver e sendo im -\\npedido de evoluir por não poder evoluir, dentro daquele local, \\nEstado, cidade, país.\\nFísico, parte que o negro evoluiu mais do que o branco, devido \\na sofrer e ter que se adaptar, devido à necessidade de sobrevi -\\nvência, tornando o corpo mais resistente (esporte de corrida, \\ntrabalho).\\nArte para Negros\\nDevido a viver em constante caos, a arte dos negros evoluiu \\nlogo após o mundo “acabar com a escravidão” , tornando-a arte \\ncaos do passado sendo vivido no futuro editável.indd   66caos do passado sendo vivido no futuro editável.indd   66 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 102509,
      "chapter": 9,
      "page": 66,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 29.45448717948718,
      "complexity_metrics": {
        "word_count": 312,
        "sentence_count": 12,
        "paragraph_count": 1,
        "avg_sentence_length": 26.0,
        "avg_word_length": 4.57051282051282,
        "unique_word_ratio": 0.6185897435897436,
        "avg_paragraph_length": 312.0,
        "punctuation_density": 0.15384615384615385,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "canaã",
          "seja",
          "devido",
          "deus",
          "evoluir",
          "sendo",
          "arte",
          "passagem",
          "após",
          "dentro",
          "jafé",
          "escravo",
          "necessidade",
          "humano",
          "como",
          "vida",
          "mental",
          "pois",
          "corpo",
          "físico"
        ],
        "entities": [
          [
            "66",
            "CARDINAL"
          ],
          [
            "África",
            "ORG"
          ],
          [
            "Cam",
            "ORG"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "Canaã",
            "ORG"
          ],
          [
            "Noé",
            "ORG"
          ],
          [
            "9",
            "CARDINAL"
          ],
          [
            "18-27",
            "CARDINAL"
          ],
          [
            "Noé",
            "ORG"
          ],
          [
            "dentro de sua",
            "ORG"
          ]
        ],
        "readability_score": 85.62884615384615,
        "semantic_density": 0,
        "word_count": 312,
        "unique_words": 193,
        "lexical_diversity": 0.6185897435897436
      },
      "preservation_score": 1.2896695950305296e-05
    },
    {
      "id": 1,
      "text": "— 67 —em uma forma de protesto com diversão Como assim?\\nSe você vive no caos sendo escravo por quase 700 anos, como \\nvocê conseguiria ser feliz? O que te faz feliz? Como você pensa -\\nria em ser feliz? Assim eu vejo a ascensão da música.\\nA música preta28 ou black music , também conhecida como \\nmúsica afro-brasileira no Brasil, e música afro-americana nos \\nEstados Unidos, é um termo dado a todo um grupo de gêneros \\nmusicais que emergiram ou foram influenciados pela cultura \\nde descendentes africanos em países colonizados por um siste -\\nma agrícola baseado na utilização de mão de obra escrava.\\nAs músicas africanas foram trazidas pelos escravos para os paí -\\nses americanos, onde se desenvolveram novas técnicas com \\nnovos instrumentos, formando variados gêneros musicais que \\ncaracterizaram a vida de negros norte-americanos antes da \\nguerra civil americana. A música foi usada como uma forma \\nde expressar desejos e necessidades que foram ignoradas de -\\nvido a climas raciais e políticas adversas. O termo também é \\nusado, às vezes, para abranger qualquer gênero musical com \\numa grande proporção de artistas negros, ou de uma forma \\nmuito estreita para significa urbana ou música. “O sofrimento \\ndos negros foi tão significante, hoje temos mais negros na mú -\\nsica que brancos. ”\\nO termo não é de caráter segregativo, porque todas as origens \\npodem tanto apreciar a mesma música, mesmo se eles não \\ntêm mais nada em comum. Foi uma maneira que os primei -\\nros escravos podiam expressar-se e comunicar-se quando eles \\nestavam sendo realocados (única forma de ser feliz). Em um \\ntempo em que o seu mundo sociocultural estava sendo renega -\\ndo, a música serviu como uma fuga, forma de expressão e sutis \\n28.  Texto baseado em  https://pt.m.wikipedia.org/wiki/M%C3%BAsica _negra .\\ncaos do passado sendo vivido no futuro editável.indd   67caos do passado sendo vivido no futuro editável.indd   67 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 104391,
      "chapter": 3,
      "page": 67,
      "segment_type": "page",
      "themes": {},
      "difficulty": 24.496904761904762,
      "complexity_metrics": {
        "word_count": 315,
        "sentence_count": 20,
        "paragraph_count": 1,
        "avg_sentence_length": 15.75,
        "avg_word_length": 5.073015873015873,
        "unique_word_ratio": 0.6507936507936508,
        "avg_paragraph_length": 315.0,
        "punctuation_density": 0.12063492063492064,
        "line_break_count": 30,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "música",
          "como",
          "forma",
          "sendo",
          "feliz",
          "negros",
          "você",
          "termo",
          "assim",
          "caos",
          "também",
          "afro",
          "americana",
          "gêneros",
          "musicais",
          "baseado",
          "escravos",
          "americanos",
          "expressar",
          "mais"
        ],
        "entities": [
          [
            "67",
            "CARDINAL"
          ],
          [
            "diversão Como",
            "ORG"
          ],
          [
            "Se",
            "PERSON"
          ],
          [
            "700",
            "CARDINAL"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "Assim eu",
            "PERSON"
          ],
          [
            "vejo",
            "ORG"
          ],
          [
            "da música",
            "PERSON"
          ],
          [
            "também conhecida como \\nmúsica afro-brasileira",
            "PERSON"
          ],
          [
            "Brasil",
            "PERSON"
          ]
        ],
        "readability_score": 90.60309523809524,
        "semantic_density": 0,
        "word_count": 315,
        "unique_words": 205,
        "lexical_diversity": 0.6507936507936508
      },
      "preservation_score": 1.2247851439521137e-05
    },
    {
      "id": 1,
      "text": "— 68 —formas de protesto social para comunidades negras iniciais. A \\nmúsica negra no Brasil se iniciou no final da década de 60, \\ncom os bailes black , festas onde tocavam discos de funk e soul. \\nDitadura militar, o que impossibilitou não só a música mas \\na arte em geral. Com esse pequeno avanço cultural os negros \\ncomeçaram a ganhar “mais espaço” , tivemos os grandes festivais \\ntrazendo Elza Soares, Mussum, Jair Rodrigues, Tony Tornado, \\nGilberto Gil e muitos outros. Nos bailes black , que eram fre -\\nquentados por pessoas das favelas, havia as equipes de som, a \\nFuracão 2000, Pipos, Cash Box. As festas que aconteciam em \\nSão Paulo, onde era mais tocado o rap Racionais, RZO, Mv Bill \\nresultado do movimento hip-hop vieram se transformar nos \\ndias de hoje, em um movimento de muita expressão e poder \\npara os negros em ganhar uma estrutura familiar.\\nNo final do século 19, temos uma captação sentimental peran -\\nte o meu caos.\\nQuando “deixamos de ter escravos” , começamos a ter mais voz \\nperante o mundo, assim, começamos a “evolução” artística e \\nser tratado como sempre deveria ter sido tratado, como ser hu -\\nmano!!!\\nOs negros, por sempre viverem no caos, quando podem exaltar \\na energia captada, foi exaltada através do amor, música, mani -\\nfestação, protesto diante do caos e dor (amor) em comum dos \\nsemelhantes.\\nArte é a expressão do sentimento!!! \\nA expressão do negro é o sentimento do caos vivido, assim se \\ntornando mais aceito diante dos seres humanos, pois nós vive -\\nmos em caos, sobrevivemos ao caos e estamos nos adaptando \\nao caos. temos uma vida de caos, como iremos interpretar o \\ncaos?\\ncaos do passado sendo vivido no futuro editável.indd   68caos do passado sendo vivido no futuro editável.indd   68 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 106446,
      "chapter": 3,
      "page": 68,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 28.511666666666667,
      "complexity_metrics": {
        "word_count": 300,
        "sentence_count": 15,
        "paragraph_count": 1,
        "avg_sentence_length": 20.0,
        "avg_word_length": 4.816666666666666,
        "unique_word_ratio": 0.67,
        "avg_paragraph_length": 300.0,
        "punctuation_density": 0.18,
        "line_break_count": 30,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "caos",
          "mais",
          "música",
          "negros",
          "expressão",
          "como",
          "vivido",
          "protesto",
          "final",
          "bailes",
          "black",
          "festas",
          "onde",
          "arte",
          "ganhar",
          "movimento",
          "temos",
          "quando",
          "começamos",
          "assim"
        ],
        "entities": [
          [
            "68",
            "CARDINAL"
          ],
          [
            "formas de protesto social para comunidades negras iniciais",
            "ORG"
          ],
          [
            "Brasil",
            "PERSON"
          ],
          [
            "discos de funk e soul",
            "ORG"
          ],
          [
            "Ditadura",
            "PERSON"
          ],
          [
            "tivemos",
            "PERSON"
          ],
          [
            "Elza Soares",
            "PERSON"
          ],
          [
            "Mussum",
            "PERSON"
          ],
          [
            "Jair Rodrigues",
            "PERSON"
          ],
          [
            "Tony Tornado",
            "PERSON"
          ]
        ],
        "readability_score": 88.555,
        "semantic_density": 0,
        "word_count": 300,
        "unique_words": 201,
        "lexical_diversity": 0.67
      },
      "preservation_score": 1.5309814299401422e-05
    },
    {
      "id": 1,
      "text": "— 69 —Quando os negros começaram a ter voz, tudo era melhor do \\nque tinha lembrança do que já tinha vivido antes, nesse afeto \\nde uma falsa liberdade, falsa felicidade dos negros, começaram \\na exaltar o caos vivido em forma de felicidade e amor, pois os \\nnegros já tinham vivido muito o caos, e falar de amor quando \\nsó se viveu o caos é fácil, interpretar o seu caos diante do caos \\nque eu vivi toda a minha vida, seus problemas, seu caos não \\nera nada diante do que eu vivi toda a minha vida, mostrando \\ne direcionando a felicidade em cantar, dançar, brincar e sorrir \\ncom o pouco que se viveu e do que tinha, tudo era melhor do \\nque eu já vivi!!!\\ncaos do passado sendo vivido no futuro editável.indd   69caos do passado sendo vivido no futuro editável.indd   69 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 108333,
      "chapter": 3,
      "page": 69,
      "segment_type": "page",
      "themes": {},
      "difficulty": 33.137499999999996,
      "complexity_metrics": {
        "word_count": 144,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 36.0,
        "avg_word_length": 4.486111111111111,
        "unique_word_ratio": 0.5416666666666666,
        "avg_paragraph_length": 144.0,
        "punctuation_density": 0.1527777777777778,
        "line_break_count": 11,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "caos",
          "vivido",
          "negros",
          "tinha",
          "felicidade",
          "vivi",
          "quando",
          "começaram",
          "tudo",
          "melhor",
          "falsa",
          "amor",
          "viveu",
          "diante",
          "toda",
          "minha",
          "vida",
          "passado",
          "sendo",
          "futuro"
        ],
        "entities": [
          [
            "69",
            "CARDINAL"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "forma de felicidade",
            "ORG"
          ],
          [
            "tinham vivido muito o",
            "ORG"
          ],
          [
            "interpretar o seu",
            "ORG"
          ],
          [
            "que eu vivi",
            "PERSON"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "que eu vivi",
            "PERSON"
          ],
          [
            "que eu já vivi",
            "PERSON"
          ],
          [
            "editável.indd   69caos",
            "QUANTITY"
          ]
        ],
        "readability_score": 80.65416666666667,
        "semantic_density": 0,
        "word_count": 144,
        "unique_words": 78,
        "lexical_diversity": 0.5416666666666666
      },
      "preservation_score": 1.9246623690676078e-06
    },
    {
      "id": 1,
      "text": "— 70 —\\ncaos do passado sendo vivido no futuro editável.indd   70caos do passado sendo vivido no futuro editável.indd   70 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 109255,
      "chapter": 3,
      "page": 70,
      "segment_type": "page",
      "themes": {},
      "difficulty": 20.91449275362319,
      "complexity_metrics": {
        "word_count": 23,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 7.666666666666667,
        "avg_word_length": 5.826086956521739,
        "unique_word_ratio": 0.6086956521739131,
        "avg_paragraph_length": 23.0,
        "punctuation_density": 0.2608695652173913,
        "line_break_count": 1,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "caos"
        ],
        "entities": [
          [
            "70",
            "CARDINAL"
          ],
          [
            "editável.indd   70caos",
            "QUANTITY"
          ],
          [
            "editável.indd",
            "CARDINAL"
          ],
          [
            "70",
            "CARDINAL"
          ],
          [
            "14:53:3828/03/2022",
            "CARDINAL"
          ],
          [
            "14:53:38",
            "TIME"
          ]
        ],
        "readability_score": 94.41884057971015,
        "semantic_density": 0,
        "word_count": 23,
        "unique_words": 14,
        "lexical_diversity": 0.6086956521739131
      },
      "preservation_score": 5.8323102092957795e-08
    },
    {
      "id": 1,
      "text": "— 71 —Capítulo 9\\nIdade Moderna\\nFilosofia moderna\\nÉ toda a filosofia que se desenvolveu durante os séculos XV , \\nXVI, XVII, XVIII, XIX; começando pelo fim da “adaptação” da \\nenergia da terra, e se estendendo até meados do século XIX.\\nFilosofia do Renascimento\\nA filosofia do Renascimento foi o período da história da filo -\\nsofia na qual é o aparecimento de “novas energias” , reaparecen -\\ndo novos captadores de energia por isso o nome filosofia do \\nRenascimento cultural estão o Renascimento da educação e \\ncivilização clássica e um retorno parcial à autoridade de Platão \\nsobre Aristóteles.\\nO período foi marcado por transformações em muitas áreas, \\nocasionando muitas guerras e conflitos por territórios, para \\nse ter o que plantar para comer e sobreviver, esse período de \\ntransição entre Idade Média e o início da Idade Moderna teve \\nmuitos conflitos religiosos aumentando as riquezas territo -\\nriais, assim criando mais países e aumentando a quantidade de \\nrecursos territoriais pela própria ganância. Apesar dessas trans -\\nformações serem bem evidentes na cultura, sociedade, econo -\\nmia, política e religião, caracterizando a transição do feudalis -\\nmo para o capitalismo\\ncaos do passado sendo vivido no futuro editável.indd   71caos do passado sendo vivido no futuro editável.indd   71 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 109534,
      "chapter": 9,
      "page": 71,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 35.17807017543859,
      "complexity_metrics": {
        "word_count": 209,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 34.833333333333336,
        "avg_word_length": 5.315789473684211,
        "unique_word_ratio": 0.6650717703349283,
        "avg_paragraph_length": 209.0,
        "punctuation_density": 0.11483253588516747,
        "line_break_count": 23,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "filosofia",
          "renascimento",
          "idade",
          "moderna",
          "período",
          "energia",
          "muitas",
          "conflitos",
          "transição",
          "aumentando",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "capítulo",
          "toda",
          "desenvolveu",
          "durante"
        ],
        "entities": [
          [
            "71",
            "CARDINAL"
          ],
          [
            "9",
            "CARDINAL"
          ],
          [
            "Idade",
            "GPE"
          ],
          [
            "Moderna",
            "PERSON"
          ],
          [
            "XV",
            "PERSON"
          ],
          [
            "XVII",
            "ORG"
          ],
          [
            "XVIII",
            "ORG"
          ],
          [
            "XIX",
            "ORG"
          ],
          [
            "começando pelo fim da “",
            "PERSON"
          ],
          [
            "XIX",
            "ORG"
          ]
        ],
        "readability_score": 80.98859649122807,
        "semantic_density": 0,
        "word_count": 209,
        "unique_words": 139,
        "lexical_diversity": 0.6650717703349283
      },
      "preservation_score": 6.036441066621133e-06
    },
    {
      "id": 1,
      "text": "— 72 —Filósofos\\nNicolau Maquiavel29\\nEsse aqui eu faço questão de falar, pois captou uma energia \\napós um cataclismo e soube explicar o caos vivido na massa \\nescura. \\nNicolau Maquiavel nasceu em Florença, 3 de maio de 1469 \\n— Florença, 21 de junho de 1527 foi um filósofo, historiador, \\npoeta, diplomata e músico de origem florentina do Renasci -\\nmento. É reconhecido como fundador do pensamento e da \\nciência política moderna, pelo fato de ter sentido todo o caos \\nque vínhamos vivendo, e interpretar de uma forma explicativa, \\nsobre o Estado e o governo como realmente são, e não como \\ndeveriam ser.\\n Com o choque de realidade causado pelas suas ideias sobre \\na dinâmica do poder, seus textos geraram uma ameaça aos va -\\nlores cristãos, os mesmos que vieram de uma conquista terri -\\ntorial, principalmente devido às análises do poder político da \\nigreja católica, pois o seu pensamento era totalmente contra -\\nditório a doutrina religiosa. Já na literatura e teatro ingleses do \\nséculo 17, foi associado diretamente ao Diabo, pelo seu pen -\\nsamento contraditório de entender que a visão “enganosa” do \\nhumano era o normal da vida. \\nMaquiavel viveu em República Florentina durante o governo \\nde Lourenço de Médici. Entrou para a política aos 29 anos de \\nidade no cargo de Secretário da Segunda Chancelaria. Nesse \\ncargo, Maquiavel observava tudo de ruim do poder humano \\npois o comportamento de grandes nomes da época o fazia ter \\n29. \\ncaos do passado sendo vivido no futuro editável.indd   72caos do passado sendo vivido no futuro editável.indd   72 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 110986,
      "chapter": 3,
      "page": 72,
      "segment_type": "page",
      "themes": {
        "ciencia": 56.52173913043479,
        "historia": 43.47826086956522
      },
      "difficulty": 30.453396029258098,
      "complexity_metrics": {
        "word_count": 261,
        "sentence_count": 11,
        "paragraph_count": 1,
        "avg_sentence_length": 23.727272727272727,
        "avg_word_length": 4.996168582375479,
        "unique_word_ratio": 0.6551724137931034,
        "avg_paragraph_length": 261.0,
        "punctuation_density": 0.11877394636015326,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "pois",
          "caos",
          "vivido",
          "maquiavel",
          "como",
          "poder",
          "nicolau",
          "florença",
          "florentina",
          "pensamento",
          "política",
          "pelo",
          "governo",
          "humano",
          "cargo",
          "passado",
          "sendo",
          "futuro",
          "editável",
          "indd"
        ],
        "entities": [
          [
            "72",
            "CARDINAL"
          ],
          [
            "Nicolau Maquiavel",
            "ORG"
          ],
          [
            "Florença",
            "ORG"
          ],
          [
            "3 de maio de 1469",
            "QUANTITY"
          ],
          [
            "Florença",
            "ORG"
          ],
          [
            "21",
            "CARDINAL"
          ],
          [
            "1527",
            "DATE"
          ],
          [
            "diplomata e músico de origem florentina",
            "ORG"
          ],
          [
            "Renasci",
            "GPE"
          ],
          [
            "da \\nciência política moderna",
            "PERSON"
          ]
        ],
        "readability_score": 86.63751306165099,
        "semantic_density": 0,
        "word_count": 261,
        "unique_words": 171,
        "lexical_diversity": 0.6551724137931034
      },
      "preservation_score": 8.369365150339445e-06
    },
    {
      "id": 1,
      "text": "— 73 —experiências para melhor explicar a ganância do humano. e \\na partir dessa experiência retirou alguns postulados para sua \\nobra. Depois de servir em Florença durante catorze anos, foi \\nafastado e escreveu suas principais obras. \\nFrases \\nHá três espécies de cérebros: uns entendem por si próprios; \\nos outros discernem o que os primeiros entendem; e os ter -\\nceiros não entendem nem por si próprios nem pelos outros; \\nos primeiros são excelentíssimos; os segundos excelentes; e os \\nterceiros totalmente inúteis.\\nNunca se deve deixar que aconteça uma desordem para evitar \\numa guerra, pois ela é inevitável, mas, sendo protelada, resulta \\nem tua desvantagem.\\nOs que vencem, não importa como vençam, nunca conquis -\\ntam a vergonha.\\nQuem seja a causa de alguém se tornar poderoso, desgraça-se a \\nsi próprio: pois esse poder é produzido por si quer através de \\nengenho quer de força; e ambos são suspeitos para aquele que \\nsubiu à posição de poder.\\nOs homens devem ser adulados ou destruídos, pois podem \\nvingar-se das ofensas leves, não das graves; de modo que a ofen -\\nsa que se faz ao homem deve ser de tal ordem que não se tema \\na vingança.\\nOs pensamentos dele sempre eram de exaltar o caos perante \\nos ignorantes que proporcionavam o mesmo caos que viviam, \\ncausando um impacto maquiavélico perante ao próprio caos \\nque pairou por toda a Idade Média, exaltando os problemas \\nque a civilização pensava que era certo, dentro de um contexto \\ncaos do passado sendo vivido no futuro editável.indd   73caos do passado sendo vivido no futuro editável.indd   73 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 112694,
      "chapter": 3,
      "page": 73,
      "segment_type": "page",
      "themes": {},
      "difficulty": 28.54089180781196,
      "complexity_metrics": {
        "word_count": 263,
        "sentence_count": 11,
        "paragraph_count": 1,
        "avg_sentence_length": 23.90909090909091,
        "avg_word_length": 4.984790874524715,
        "unique_word_ratio": 0.6615969581749049,
        "avg_paragraph_length": 263.0,
        "punctuation_density": 0.13688212927756654,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "caos",
          "entendem",
          "pois",
          "sendo",
          "próprios",
          "outros",
          "primeiros",
          "nunca",
          "deve",
          "próprio",
          "poder",
          "quer",
          "perante",
          "passado",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "experiências",
          "melhor"
        ],
        "entities": [
          [
            "73",
            "CARDINAL"
          ],
          [
            "para sua",
            "PERSON"
          ],
          [
            "Florença",
            "ORG"
          ],
          [
            "catorze anos",
            "PERSON"
          ],
          [
            "entendem",
            "ORG"
          ],
          [
            "outros discernem",
            "PERSON"
          ],
          [
            "entendem nem",
            "PERSON"
          ],
          [
            "nem pelos outros",
            "PERSON"
          ],
          [
            "Nunca",
            "ORG"
          ],
          [
            "para evitar",
            "PERSON"
          ]
        ],
        "readability_score": 86.55001728309713,
        "semantic_density": 0,
        "word_count": 263,
        "unique_words": 174,
        "lexical_diversity": 0.6615969581749049
      },
      "preservation_score": 8.777626864990149e-06
    },
    {
      "id": 1,
      "text": "— 74 —de visão de simplesmente perguntar o porquê dos ignorantes, \\nexaltando os próprios erros cometidos diante de nós mesmos. \\nMarsílio Ficino30\\nNasceu em Figline Valdarno, 19 de outubro de 1433.\\nA parte mais substancial da obra filosófica de Marsílio Ficino \\nfoi completada entre 1458 e 1493. Sua Theologia platonica  ou \\nDe immortalitate animarum , dedicada a Lourenço de Médicis, \\num provável direcionador de Maquiavel é considerada a sín -\\ntese do seu pensamento hermético e filosófico. Caos religioso \\ndirecionado a adaptação filosófica no qual procura conciliar o \\nplatonismo e o cristianismo.\\nSeu pensamento propõe uma visão do Homem com forte afi -\\nnidade cósmica e mágica, no centro de uma animada e alta -\\nmente espiritualizada, porque ele pensava que o ser humano \\ntêm que movimentar-se A função principal do pensamento \\nhumano seria a de atingir – através de uma iluminação racio -\\nnal de movimentar os pensamentos (ação e reação)intelectuais \\ne fantasiosa que o próprio homem para atingir uma imortali -\\ndade era de ser divino para ele mesmo junto a uma intelectua -\\nlidade.\\nExistiria, segundo Ficino, uma antiga e consistente tradição \\nteológica desde Hermes Trimegisto até Platão, passando por \\nZoroastro, Orfeu, Pitágoras e outros que se propõe a subtrair \\na alma do engano dos sentidos e da fantasia, para conduzi-la à \\nmente, ele interpretou uma ordem dentro do caos que percebe \\na verdade e a ordem de todas as coisas que existem em Deus ou \\nque emanam de Deus. \\n30.  Texto baseado em https://pt.m.wikipedia.org/wiki/Mars%C3%ADlio_\\nFicino .\\ncaos do passado sendo vivido no futuro editável.indd   74caos do passado sendo vivido no futuro editável.indd   74 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 114410,
      "chapter": 3,
      "page": 74,
      "segment_type": "page",
      "themes": {
        "filosofia": 60.0,
        "arte": 40.0
      },
      "difficulty": 26.71333333333333,
      "complexity_metrics": {
        "word_count": 270,
        "sentence_count": 15,
        "paragraph_count": 1,
        "avg_sentence_length": 18.0,
        "avg_word_length": 5.266666666666667,
        "unique_word_ratio": 0.6666666666666666,
        "avg_paragraph_length": 270.0,
        "punctuation_density": 0.11851851851851852,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "ficino",
          "pensamento",
          "caos",
          "visão",
          "marsílio",
          "filosófica",
          "propõe",
          "homem",
          "mente",
          "humano",
          "movimentar",
          "atingir",
          "ordem",
          "deus",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd"
        ],
        "entities": [
          [
            "74",
            "CARDINAL"
          ],
          [
            "diante de nós mesmos",
            "PERSON"
          ],
          [
            "Marsílio Ficino30\\nNasceu",
            "PERSON"
          ],
          [
            "Figline Valdarno",
            "PERSON"
          ],
          [
            "19",
            "CARDINAL"
          ],
          [
            "1458 e 1493",
            "DATE"
          ],
          [
            "Sua Theologia",
            "PERSON"
          ],
          [
            "de Maquiavel",
            "ORG"
          ],
          [
            "sín",
            "ORG"
          ],
          [
            "tese",
            "NORP"
          ]
        ],
        "readability_score": 89.42,
        "semantic_density": 0,
        "word_count": 270,
        "unique_words": 180,
        "lexical_diversity": 0.6666666666666666
      },
      "preservation_score": 9.302534783826768e-06
    },
    {
      "id": 1,
      "text": "— 75 —Dentro de uma visão cíclica da história, marcada pelo mito do \\nretorno platônico. Sua ideia animadora é a exaltação do ho -\\nmem como microcosmo, aqui o sentimento dele foi quântico \\nperante a uma importância de si próprio. Outra ideia que o \\ninspirava é a da continuidade do desenvolvimento religioso, \\ndesde os antigos sábios e filósofos Zoroastro, Orfeu, Pitágoras, \\nPlatão até o cristianismo, ele interpretou a propagação da ener -\\ngia de conter o caos.\\nWilliam Shakespeare31\\nCoisa de louco como ele se dava com a energia dele capta -\\nda. Ele era tão sentimental ao ponto de sentir dor no amor. A \\nenergia que ele captava e propagava era semelhante a de Jesus \\ne Sidarta Gautama  um filósofo com essa capacidade de com -\\npreender a dor, com o lado da necessidade de amar perante a \\ndor.\\nWilliam Shakespeare nasceu 1564 foi um poeta, dramaturgo \\ne ator inglês, tido como o maior escritor do idioma inglês e o \\nmais influente dramaturgo do mundo. Suas peças foram tra -\\nduzidas para todas as principais línguas modernas e são mais \\nencenadas que as de qualquer outro dramaturgo. Semelhante \\nas palavras de jesus que se propagou de uma forma acima da \\nmédia.\\nCasou aos 18 anos e teve teve 3 filhos Shakespeare começou \\numa carreira bem-sucedida em Londres como ator, escritor e \\num dos proprietários da companhia de teatro chamada Lord \\nChamberlain’s Men, mais tarde conhecida como King’s Men.\\nSuas primeiras peças eram principalmente comédias e obras \\n31.  Texto baseado em https://pt.m.wikipedia.org/wiki/William_Shake speare .\\ncaos do passado sendo vivido no futuro editável.indd   75caos do passado sendo vivido no futuro editável.indd   75 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 116243,
      "chapter": 3,
      "page": 75,
      "segment_type": "page",
      "themes": {},
      "difficulty": 24.24740470397405,
      "complexity_metrics": {
        "word_count": 274,
        "sentence_count": 18,
        "paragraph_count": 1,
        "avg_sentence_length": 15.222222222222221,
        "avg_word_length": 5.083941605839416,
        "unique_word_ratio": 0.6642335766423357,
        "avg_paragraph_length": 274.0,
        "punctuation_density": 0.12408759124087591,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "como",
          "dramaturgo",
          "mais",
          "ideia",
          "dele",
          "perante",
          "caos",
          "william",
          "energia",
          "semelhante",
          "jesus",
          "shakespeare",
          "ator",
          "inglês",
          "escritor",
          "suas",
          "peças",
          "teve",
          "passado",
          "sendo"
        ],
        "entities": [
          [
            "75",
            "CARDINAL"
          ],
          [
            "Dentro de uma visão",
            "ORG"
          ],
          [
            "da história",
            "PERSON"
          ],
          [
            "marcada pelo mito",
            "PERSON"
          ],
          [
            "ho -\\nmem como microcosmo",
            "PERSON"
          ],
          [
            "Outra",
            "ORG"
          ],
          [
            "Zoroastro",
            "GPE"
          ],
          [
            "Orfeu",
            "PERSON"
          ],
          [
            "Pitágoras",
            "PERSON"
          ],
          [
            "Platão",
            "ORG"
          ]
        ],
        "readability_score": 90.86370640713706,
        "semantic_density": 0,
        "word_count": 274,
        "unique_words": 182,
        "lexical_diversity": 0.6642335766423357
      },
      "preservation_score": 8.981757722315501e-06
    },
    {
      "id": 1,
      "text": "— 76 —baseadas em eventos e personagens históricos, ao estudar mui -\\nto e ter uma vida confortável, A partir de um momento perce -\\nbeu o caos desnecessário, e começou a interpretar o amor atra -\\nvés da tragédia cotidiana, escreveu Hamlet , Rei Lear  e Macbeth , \\nconsideradas algumas das obras mais importantes na língua \\ninglesa. Na sua última fase, escreveu um conjuntos de peças \\nclassificadas como tragicomédias ou romances.\\nSó viria a atingir o nível em que se encontra hoje no século \\nXIX. O pensamento dele era atemporal para a sua época.\\nComo irei falar de Shakespeare... Todos falaram dele, teve uma \\nvisão sobre ele, tenho até medo de falar sobre...\\nÉ um cara que captou a energia do amor, da vida em êxtase \\nperante o viver uma vida sentimental, perante a dor do amor \\ndo outro, que, a meu ver, não merece sofrer por amor. Vivendo \\ntambém no meio da massa escura, o fez ter palavras de con -\\ntexto proporcional a energia a qual ele vivia, com frases de \\nimpacto com muito sentimento, o ser artista. Foi um choque \\nde realidade após a Idade das Trevas. Foi o resquício do amor \\npuro devido a ter vivido o melhor da família que antes do cata -\\nclismo, foi a energia que sumiu com a essência (DNA) de nos \\nafastar do planeta Terra, por nos aproximar de nós mesmos e \\nesquecendo do valor da energia universal.\\nPor viver com artistas (pessoas mais receptivas a energia sen -\\ntimental), acaba sentindo muita dor perante a energia em sua \\nvolta, exaltando a energia a qual você capta de uma forma se -\\nmelhante a mesma energia captada, quanto mais massa escura \\nvive em seu torno, mais energia ele emite de si próprio... “Bu -\\nraco de minhoca” ...\\ncaos do passado sendo vivido no futuro editável.indd   76caos do passado sendo vivido no futuro editável.indd   76 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 118051,
      "chapter": 3,
      "page": 76,
      "segment_type": "page",
      "themes": {},
      "difficulty": 27.04629049111808,
      "complexity_metrics": {
        "word_count": 319,
        "sentence_count": 15,
        "paragraph_count": 1,
        "avg_sentence_length": 21.266666666666666,
        "avg_word_length": 4.598746081504702,
        "unique_word_ratio": 0.6300940438871473,
        "avg_paragraph_length": 319.0,
        "punctuation_density": 0.1536050156739812,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "amor",
          "mais",
          "vida",
          "perante",
          "vivido",
          "caos",
          "escreveu",
          "como",
          "dele",
          "falar",
          "viver",
          "massa",
          "escura",
          "qual",
          "passado",
          "sendo",
          "futuro",
          "editável",
          "indd"
        ],
        "entities": [
          [
            "76",
            "CARDINAL"
          ],
          [
            "históricos",
            "ORG"
          ],
          [
            "Hamlet",
            "ORG"
          ],
          [
            "Rei Lear  ",
            "ORG"
          ],
          [
            "consideradas algumas das",
            "PERSON"
          ],
          [
            "de Shakespeare",
            "PERSON"
          ],
          [
            "tenho",
            "ORG"
          ],
          [
            "medo de",
            "PERSON"
          ],
          [
            "outro",
            "PERSON"
          ],
          [
            "meio da massa escura",
            "PERSON"
          ]
        ],
        "readability_score": 87.98704284221526,
        "semantic_density": 0,
        "word_count": 319,
        "unique_words": 201,
        "lexical_diversity": 0.6300940438871473
      },
      "preservation_score": 1.32685057261479e-05
    },
    {
      "id": 1,
      "text": "— 77 —Frases \\nNem tudo que reluz é ouro.\\nO Inferno está vazio e todos os demônios estão aqui.\\nAme a todos, confie em poucos e não faça mal a ninguém.\\nEsses prazeres violentos têm finais violentos.\\nParece-me que a dama faz demasiados protestos.\\nA concisão é a alma do espírito.\\nPesada sempre se encontra a fronte coroada.\\nAgora é o inverno do nosso descontentamento.\\nRomeu, Romeu! Ah! Por que és tu Romeu?\\nRenascimento, o próprio nome já diz... É a energia voltando a \\nser sentida, diferente do que a idade média vinha trazendo, isso \\naqui é o certo. Começaram a ter questionamentos, conflitos \\nreligiosos diante da sua própria crença e o que sentia pelo seu \\npróprio semelhante, perante a um contexto de fazer o bem, pe -\\nrante uma propagação de algo que todos pregavam como deve \\nser a forma certa de seguir, baseada nos textos antes cataclismo, \\njunto com a sua crença a qual você foi criado e captação de \\nenergia.\\nFilosofia do século XVII32\\nBarroco é o estilo artístico que floresceu entre o final do sé -\\nculo XVI e meados do século XVIII, inicialmente na Itália, di -\\nfundindo-se em seguida pelos países católicos da Europa e da \\nAmérica\\n32.  Texto baseado em https://pt.m.wikipedia.org/wiki/B arroco .\\ncaos do passado sendo vivido no futuro editável.indd   77caos do passado sendo vivido no futuro editável.indd   77 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 119975,
      "chapter": 3,
      "page": 77,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 21.77774703557312,
      "complexity_metrics": {
        "word_count": 230,
        "sentence_count": 22,
        "paragraph_count": 1,
        "avg_sentence_length": 10.454545454545455,
        "avg_word_length": 4.8652173913043475,
        "unique_word_ratio": 0.7304347826086957,
        "avg_paragraph_length": 230.0,
        "punctuation_density": 0.17391304347826086,
        "line_break_count": 25,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "todos",
          "romeu",
          "aqui",
          "violentos",
          "próprio",
          "energia",
          "crença",
          "século",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "frases",
          "tudo",
          "reluz",
          "ouro",
          "inferno",
          "está"
        ],
        "entities": [
          [
            "todos",
            "CARDINAL"
          ],
          [
            "confie em poucos",
            "ORG"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "concisão",
            "ORG"
          ],
          [
            "Pesada",
            "GPE"
          ],
          [
            "Agora",
            "PERSON"
          ],
          [
            "certo",
            "NORP"
          ],
          [
            "da sua própria crença e o que sentia",
            "ORG"
          ],
          [
            "pelo seu",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ]
        ],
        "readability_score": 93.31316205533597,
        "semantic_density": 0,
        "word_count": 230,
        "unique_words": 168,
        "lexical_diversity": 0.7304347826086957
      },
      "preservation_score": 8.566205619903178e-06
    },
    {
      "id": 1,
      "text": "— 78 —Considerado como o estilo correspondente ao Absolutismo \\ne à Contrarreforma, distingue-se pelo esplendor exuberante. \\nFoi a transição do renascimento para algo, foi o trajeto natu -\\nral da evolução em se adaptar ao próprio caos, criando novos \\npensamentos fora da doutrina religiosa, devido a captação da \\nenergia ser científica. \\nPara diversos pesquisadores, o Barroco constitui não apenas \\num estilo artístico, mas todo um período histórico e um mo -\\nvimento sociocultural, onde se formularam novos modos de \\nentender o mundo, o homem e Deus. \\nFilósofos \\nO Maneirismo foi um estilo e um movimento artístico que se \\ndesenvolveu na Europa, aproximadamente entre 1515 e 1600, \\nfoi uma evolução interpretativa do clero da sociedade, em tra -\\nzer a cultura na obra de arte, pois se caracterizou pela sofis -\\nticação da própria interpretação do artista as tornando obras \\nartificiais muito contraditória e com muitos conflitos por ser \\ninterpretativa não do sentimento do ser humano e sim a inter -\\npretação do humano. \\nMichelangelo33\\nMichelangelo nasceu em Caprese, 6 de março de 1475, foi um \\npintor, escultor, poeta, anatomista e arquiteto italiano, conside -\\nrado um dos maiores criadores da história da arte do ocidente.\\nEle viveu em Florença e Roma, onde viveram seus grandes me -\\ncenas, a família Medici de Florença. Tendo o seu talento logo \\nreconhecido, tornou-se um protegido dos Medici, para quem \\n33.  Texto baseado em https://pt.m.wikipedia.org/wiki/Michel angelo .\\ncaos do passado sendo vivido no futuro editável.indd   78caos do passado sendo vivido no futuro editável.indd   78 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 121456,
      "chapter": 3,
      "page": 78,
      "segment_type": "page",
      "themes": {
        "ciencia": 39.3939393939394,
        "arte": 60.60606060606061
      },
      "difficulty": 25.791219649915302,
      "complexity_metrics": {
        "word_count": 253,
        "sentence_count": 14,
        "paragraph_count": 1,
        "avg_sentence_length": 18.071428571428573,
        "avg_word_length": 5.375494071146245,
        "unique_word_ratio": 0.691699604743083,
        "avg_paragraph_length": 253.0,
        "punctuation_density": 0.15810276679841898,
        "line_break_count": 27,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "estilo",
          "evolução",
          "caos",
          "novos",
          "artístico",
          "onde",
          "interpretativa",
          "arte",
          "humano",
          "florença",
          "medici",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "considerado",
          "como",
          "correspondente"
        ],
        "entities": [
          [
            "78",
            "CARDINAL"
          ],
          [
            "Considerado",
            "FAC"
          ],
          [
            "Absolutismo",
            "PRODUCT"
          ],
          [
            "Contrarreforma",
            "GPE"
          ],
          [
            "pelo",
            "PERSON"
          ],
          [
            "fora da doutrina religiosa",
            "ORG"
          ],
          [
            "Para",
            "PRODUCT"
          ],
          [
            "Barroco",
            "PRODUCT"
          ],
          [
            "artístico",
            "ORG"
          ],
          [
            "artístico",
            "ORG"
          ]
        ],
        "readability_score": 89.35163749294185,
        "semantic_density": 0,
        "word_count": 253,
        "unique_words": 175,
        "lexical_diversity": 0.691699604743083
      },
      "preservation_score": 1.0038863947750362e-05
    },
    {
      "id": 1,
      "text": "— 79 —realizou várias obras. Mais um que pode ter influenciado a for -\\nmar Maquiavel, fixou-se em Roma, onde deixou a maior parte \\nde suas obras mais representativas. Sua carreira se desenvolveu \\nna transição do Renascimento para o Maneirismo, ele conse -\\nguiu conciliar a arte com ganância e sofisticação junto ao sofri -\\nmento. Várias de suas criações estão entre as mais célebres da \\narte do ocidente, destacando-se na escultura o Baco, a Pietà, o \\nDavid, as duas tumbas Medici e o Moisés; na pintura, o vasto \\nciclo do teto da Capela Sistina e o Juízo Final no mesmo local, \\ne dois afrescos na Capela Paulina.\\nAinda em vida, foi considerado o maior artista de seu tempo; \\nchamavam-no de o Divino, a facilidade em propagar a sua obra \\npor viver no clero o facilitou em ser reconhecido e trabalhar \\nmais a sua própria arte com o estudo sobre o caos vivido, pe -\\nrante ao que ele vivia em sua vida artística. Foi um dos primei -\\nros artistas ocidentais a ter sua biografia publicada ainda em \\nvida. Sua fama era tamanha que, como nenhum artista ante -\\nrior ou contemporâneo seu, sobrevivem registros numerosos \\nsobre sua carreira e personalidade. Michelangelo permanece \\ncomo um dos poucos artistas que foram capazes de expressar a \\nexperiência do belo, do trágico e do sublime numa dimensão \\ncósmica e universal.\\nAinda bebê, dormindo no mesmo berço de um irmão, esse \\ncontraiu grave doença contagiosa, da qual faleceu, mas Miche -\\nlangelo milagrosamente não foi contaminado. Era para ser o \\nque ele tinha que ser, nós nascemos já com um DNA e esse \\nDNA têm uma forma de propagar a energia do seu “entorno” \\nem forma de conter o caos de maior ação no espaço territorial \\ndo planeta Terra (predestinado). Sua família era antiga e per -\\ntencia à nobreza, o que era aceito como um fato na época em \\nque viveu. Seria descendente dos condes de Canossa, da região \\nde Reggio Emilia. entre seus ancestrais a célebre Matilde de \\ncaos do passado sendo vivido no futuro editável.indd   79caos do passado sendo vivido no futuro editável.indd   79 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 123209,
      "chapter": 3,
      "page": 79,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 28.38935574229692,
      "complexity_metrics": {
        "word_count": 357,
        "sentence_count": 15,
        "paragraph_count": 1,
        "avg_sentence_length": 23.8,
        "avg_word_length": 4.742296918767507,
        "unique_word_ratio": 0.6106442577030813,
        "avg_paragraph_length": 357.0,
        "punctuation_density": 0.11764705882352941,
        "line_break_count": 32,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "maior",
          "arte",
          "ainda",
          "vida",
          "caos",
          "vivido",
          "como",
          "várias",
          "obras",
          "suas",
          "carreira",
          "entre",
          "capela",
          "mesmo",
          "artista",
          "propagar",
          "artistas",
          "esse",
          "forma"
        ],
        "entities": [
          [
            "79",
            "CARDINAL"
          ],
          [
            "mais representativas",
            "PERSON"
          ],
          [
            "Sua carreira se desenvolveu",
            "PERSON"
          ],
          [
            "Renascimento",
            "ORG"
          ],
          [
            "Maneirismo",
            "GPE"
          ],
          [
            "Várias de suas criações estão",
            "PERSON"
          ],
          [
            "mais célebres da \\narte",
            "PERSON"
          ],
          [
            "Baco",
            "PERSON"
          ],
          [
            "Pietà",
            "PERSON"
          ],
          [
            "David",
            "PERSON"
          ]
        ],
        "readability_score": 86.67731092436975,
        "semantic_density": 0,
        "word_count": 357,
        "unique_words": 218,
        "lexical_diversity": 0.6106442577030813
      },
      "preservation_score": 1.376425209393804e-05
    },
    {
      "id": 1,
      "text": "— 80 —Canossa, e ligados pelo sangue a imperadores. Um membro da \\nfamília, Simone da Canoss.\\nGiambologna34\\nGiambologna nasceu em Douai, Flandres em 1529, considera -\\ndo o mais perfeito representante do Maneirismo e seu renome \\nvem de suas obras cheias de movimento, com um precioso po -\\nlimento de superfície. O excesso do perfeccionismo, a melhor \\nforma de interpretar o luxo com sentimento. A divulgação \\nde suas grandes obras em cópias reduzidas em bronze fez sua \\nfama se espalhar pela Europa.\\nNascido em uma família de classe média, seus pais queriam \\nfazer dele um notário, mas seu talento foi percebido e ele foi \\naceito como aprendiz no ateliê do escultor e arquiteto Jacques \\ndu Broeucq.\\nDepois de terminar seu aprendizado, transferiu-se para a Itália \\nem torno de 1550, fixando-se em Roma, onde ele percebeu a \\nsua conexão com a energia de Michelangelo e também e com \\nGuglielmo della Porta, com quem teria aprendido a técnica \\nda escultura em bronze, fazendo ele propagar a energia em \\nevolução do luxo.\\nAqui é a luxúria da energia (sentimento carnal, espiritual, in -\\ntelectual, científico, filosófico). O sentir a arte, o fazer arte, é \\nsentir um contexto da energia semelhante à minha, perante \\nminha necessidade do meio em que eu vivo, a uma empatia de \\nenergia de sentir o conforto local, comunidade, cidade, Estado, \\npaís e mundo. Assim funciona o sentimento pela música que \\nalimenta uma maior quantidade de pessoas, sentimento da \\n34.  Texto baseado em https://pt.m.wikipedia.org/wiki/Giamb ologna .\\ncaos do passado sendo vivido no futuro editável.indd   80caos do passado sendo vivido no futuro editável.indd   80 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 125403,
      "chapter": 4,
      "page": 80,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 24.50095090667846,
      "complexity_metrics": {
        "word_count": 266,
        "sentence_count": 17,
        "paragraph_count": 1,
        "avg_sentence_length": 15.647058823529411,
        "avg_word_length": 5.1992481203007515,
        "unique_word_ratio": 0.6578947368421053,
        "avg_paragraph_length": 266.0,
        "punctuation_density": 0.17669172932330826,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "sentimento",
          "sentir",
          "família",
          "suas",
          "obras",
          "luxo",
          "bronze",
          "pela",
          "fazer",
          "arte",
          "minha",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "canossa",
          "ligados"
        ],
        "entities": [
          [
            "Canossa",
            "PERSON"
          ],
          [
            "pelo",
            "PERSON"
          ],
          [
            "Simone da Canoss",
            "PERSON"
          ],
          [
            "Giambologna",
            "PERSON"
          ],
          [
            "Douai",
            "ORG"
          ],
          [
            "Flandres",
            "PERSON"
          ],
          [
            "1529",
            "DATE"
          ],
          [
            "mais perfeito",
            "PERSON"
          ],
          [
            "Maneirismo e seu",
            "ORG"
          ],
          [
            "forma de interpretar",
            "ORG"
          ]
        ],
        "readability_score": 90.61669615214507,
        "semantic_density": 0,
        "word_count": 266,
        "unique_words": 175,
        "lexical_diversity": 0.6578947368421053
      },
      "preservation_score": 1.1431328010219729e-05
    },
    {
      "id": 1,
      "text": "— 81 —energia semelhante a minha, o meu caos é semelhante ao seu \\ncaos. Então, quando nos nós empatizamos por uma arte (algo \\nque tenha sentimento incluso), nós estamos sendo empático \\ncom aquele sentimento, levando a luxúria de se ter mais senti -\\nmento (arte) em sua volta, gerando a ganância do sentir com \\na ganância de ter mais. Os filósofos gerado dessa geração, foi \\nfruto do meio de uma ideia em comum perante a uma energia \\ncontextual de outros.\\nFilosofia século XVIII\\nRevolução filosófica científica35 \\nO Iluminismo, também conhecido como Século das Luzes e \\nIlustração, foi um movimento intelectual e filosófico que do -\\nminou o mundo das ideias na Europa durante o século XVIII, \\n“O Século da Filosofia” .\\nO Iluminismo incluiu uma série de ideias centradas na razão \\ncomo a principal fonte de autoridade e legitimidade e defen -\\ndia ideais como liberdade, progresso, tolerância, fraternidade, \\ngoverno constitucional e separação Igreja-Estado. Na França, \\nas doutrinas centrais dos filósofos do Iluminismo eram a li -\\nberdade individual e a tolerância religiosa, muitas variações de \\ncaptação de energia desde religiosa e filosófica, e condutores de \\nenergia com uma má interpretação da mesma. em oposição a \\numa monarquia absoluta e aos dogmas fixos da Igreja Católica \\nRomana. \\n Com o início da Revolução Científica do período, circularam \\namplamente suas ideias através de encontros em academias \\n35.  Texto baseado em https://pt.m.wikipedia.org/wiki/Ilum inismo .\\ncaos do passado sendo vivido no futuro editável.indd   81caos do passado sendo vivido no futuro editável.indd   81 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 127194,
      "chapter": 4,
      "page": 81,
      "segment_type": "page",
      "themes": {
        "filosofia": 69.23076923076923,
        "arte": 30.76923076923077
      },
      "difficulty": 25.089774236387782,
      "complexity_metrics": {
        "word_count": 251,
        "sentence_count": 15,
        "paragraph_count": 1,
        "avg_sentence_length": 16.733333333333334,
        "avg_word_length": 5.410358565737051,
        "unique_word_ratio": 0.6772908366533864,
        "avg_paragraph_length": 251.0,
        "punctuation_density": 0.14342629482071714,
        "line_break_count": 27,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "século",
          "caos",
          "sendo",
          "iluminismo",
          "como",
          "ideias",
          "semelhante",
          "arte",
          "sentimento",
          "mais",
          "ganância",
          "filósofos",
          "filosofia",
          "xviii",
          "revolução",
          "filosófica",
          "tolerância",
          "igreja",
          "religiosa"
        ],
        "entities": [
          [
            "81",
            "CARDINAL"
          ],
          [
            "quando",
            "PERSON"
          ],
          [
            "nós empatizamos",
            "ORG"
          ],
          [
            "incluso",
            "PERSON"
          ],
          [
            "nós estamos",
            "ORG"
          ],
          [
            "sendo empático",
            "FAC"
          ],
          [
            "meio de uma ideia",
            "PERSON"
          ],
          [
            "Filosofia",
            "PERSON"
          ],
          [
            "Iluminismo",
            "ORG"
          ],
          [
            "Século",
            "ORG"
          ]
        ],
        "readability_score": 90.01022576361221,
        "semantic_density": 0,
        "word_count": 251,
        "unique_words": 170,
        "lexical_diversity": 0.6772908366533864
      },
      "preservation_score": 9.645183008622898e-06
    },
    {
      "id": 1,
      "text": "— 82 —científicas, lojas maçônicas, salões literários, cafés e em livros \\nimpressos e panfletos. Continua a captação de energia sendo \\npropagada através do clero. As ideias do Iluminismo minaram \\na autoridade da monarquia e da Igreja e prepararam o cami -\\nnho para as revoluções políticas dos séculos XVIII e XIX. \\nTentaram aplicar o pensamento iluminista sobre a tolerância \\nreligiosa e a política, o que se tornou conhecido como “absolu -\\ntismo esclarecido” . \\nA publicação mais influente do Iluminismo foi Enciclopédia. \\nPublicado entre 1751 e 1772 em 35 volumes, foi compilado \\npor um grupo de 150 cientistas e filósofos. As ideias do Ilumi -\\nnismo desempenharam um papel importante na inspiração da \\nRevolução Francesa, que começou em 1789. Aqui foi a grande \\ndemonstração do erro de interpretar a energia para a sua pró -\\npria ganância, mostrando o quanto a religião estava perdendo \\ndinheiro devido a perder seguidores. Após a Revolução, o Ilu -\\nminismo foi seguido pelo movimento intelectual conhecido \\ncomo romantismo.\\nFilósofos \\nFrancis Bacon, 1° Visconde de Alban, nasceu em Londres, 22 \\nde janeiro de 1561 foi um político, filósofo, cientista, também \\nem 1621, Bacon foi acusado de corrupção. Condenado ao pa -\\ngamento de pesada multa, foi também proibido de exercer car -\\ngos públicos.\\nComo filósofo, destacou-se com uma obra onde a ciência era \\nexaltada como benéfica para o homem. Todo grande caos vi -\\nvido e bem interpretado se gera evolução da energia captada. \\nEm suas investigações, ocupou-se especialmente da metodolo -\\ngia científica e do empirismo, sendo muitas vezes chamado de \\ncaos do passado sendo vivido no futuro editável.indd   82caos do passado sendo vivido no futuro editável.indd   82 28/03/2022   14:53:3828/03/2022   14:53:38",
      "position": 128946,
      "chapter": 4,
      "page": 82,
      "segment_type": "page",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 25.29105215827338,
      "complexity_metrics": {
        "word_count": 278,
        "sentence_count": 16,
        "paragraph_count": 1,
        "avg_sentence_length": 17.375,
        "avg_word_length": 5.241007194244604,
        "unique_word_ratio": 0.6798561151079137,
        "avg_paragraph_length": 278.0,
        "punctuation_density": 0.1366906474820144,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "sendo",
          "como",
          "energia",
          "ideias",
          "iluminismo",
          "conhecido",
          "filósofos",
          "revolução",
          "grande",
          "bacon",
          "filósofo",
          "também",
          "caos",
          "passado",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "científicas",
          "lojas"
        ],
        "entities": [
          [
            "82",
            "CARDINAL"
          ],
          [
            "lojas maçônicas",
            "PERSON"
          ],
          [
            "propagada",
            "ORG"
          ],
          [
            "Iluminismo",
            "PRODUCT"
          ],
          [
            "Igreja",
            "ORG"
          ],
          [
            "políticas",
            "GPE"
          ],
          [
            "XVIII e XIX",
            "PERSON"
          ],
          [
            "pensamento",
            "GPE"
          ],
          [
            "Iluminismo foi Enciclopédia",
            "ORG"
          ],
          [
            "1751 e 1772",
            "DATE"
          ]
        ],
        "readability_score": 89.74019784172663,
        "semantic_density": 0,
        "word_count": 278,
        "unique_words": 189,
        "lexical_diversity": 0.6798561151079137
      },
      "preservation_score": 1.1205325989609518e-05
    },
    {
      "id": 1,
      "text": "— 83 —“fundador da ciência moderna” . \\nFrancis Bacon foi um dos mais conhecidos e influentes rosa -\\n-cruzes e também um alquimista, tendo ocupado o posto mais \\nelevado da Ordem Rosacruz, o de Imperator. \\nCatarina II36 \\nNasceu em Estetino, 2 de maio de 1729 Catarina, a Grande, foi \\na Imperatriz da Rússia, nascida como princesa, Sofia se conver -\\nteu para a Igreja Ortodoxa Russa, assumiu o nome de Catarina \\nAlexeievna e se casou com o grão-duque Pedro Feodorovich, \\nela organizou um golpe de estado que o tirou do trono, com \\nPedro morrendo alguns dias depois supostamente assassinado.\\nDurante o seu reinado, o Império Russo melhorou a sua ad -\\nministração e continuou a modernizar-se. Uma pessoa que vi -\\nveu em uma família e país sem tantos preconceitos em termos \\nde “mulher ser mulher, em um país com os homens vivendo \\ncomo homens e mulheres sendo mulheres” . O reinado de Ca -\\ntarina revitalizou a Rússia, que cresceu com ainda mais força e \\ntornou conhecida como uma das maiores potências europeias. \\nOs seus sucessos dentro da complexa política externa e as suas \\nrepresálias por vezes brutas aos movimentos revolucionários \\n O seu reinado foi a doutrinação da nobreza russa perante a \\numa forma de pensar em um todo. Pedro III, sob pressão da \\nmesma nobreza. Catarina com os intelectuais do iluminismo \\nna Europa Ocidental, a imperatriz não considerava prático me -\\nlhorar as condições de vida dos seus súbditos mais pobres, pois \\no maior conflito que ela sofria, era o corpo a corpo contra os \\nhomens que continham mais poder. As distinções entre os di -\\n36.  Texto baseado em https://pt.m.wikipedia.org/wiki/Catarina_II_da_R% -\\nC3% BAssia .\\ncaos do passado sendo vivido no futuro editável.indd   83caos do passado sendo vivido no futuro editável.indd   83 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 130821,
      "chapter": 4,
      "page": 83,
      "segment_type": "page",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 27.295127748068925,
      "complexity_metrics": {
        "word_count": 297,
        "sentence_count": 17,
        "paragraph_count": 1,
        "avg_sentence_length": 17.470588235294116,
        "avg_word_length": 5.0033670033670035,
        "unique_word_ratio": 0.6498316498316499,
        "avg_paragraph_length": 297.0,
        "punctuation_density": 0.12794612794612795,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "catarina",
          "como",
          "pedro",
          "reinado",
          "homens",
          "sendo",
          "imperatriz",
          "rússia",
          "russa",
          "país",
          "mulher",
          "mulheres",
          "seus",
          "nobreza",
          "corpo",
          "passado",
          "vivido",
          "futuro",
          "editável"
        ],
        "entities": [
          [
            "83",
            "CARDINAL"
          ],
          [
            "da ciência moderna",
            "PERSON"
          ],
          [
            "Francis Bacon",
            "PERSON"
          ],
          [
            "Ordem Rosacruz",
            "ORG"
          ],
          [
            "Nasceu",
            "GPE"
          ],
          [
            "Estetino",
            "GPE"
          ],
          [
            "2",
            "CARDINAL"
          ],
          [
            "Grande",
            "ORG"
          ],
          [
            "a Imperatriz da Rússia",
            "PERSON"
          ],
          [
            "Sofia",
            "GPE"
          ]
        ],
        "readability_score": 89.76369578134285,
        "semantic_density": 0,
        "word_count": 297,
        "unique_words": 193,
        "lexical_diversity": 0.6498316498316499
      },
      "preservation_score": 1.1628168479783462e-05
    },
    {
      "id": 1,
      "text": "— 84 —reitos dos camponeses, desapareceram virtualmente na lei e na \\nprática durante o seu reinado.\\nEm 1785, Catarina conferiu à nobreza a Carta Régia da No -\\nbreza, aumentando ainda mais o poder dos senhores de terra. \\nTrouxe o capitalismo Russo para o seu lado aumentando o seu \\nnetwork . Os nobres em cada distrito elegiam um marechal da \\nnobreza que falava em seu nome para arrecadar mais impostos.\\nEsse ponto é chave para a teoria de Darwin (irei falar mais \\na frente), “evolução diante da liberdade de expressão” . Mulhe -\\nres com poder, podendo exaltar a sua própria interpretação de \\nenergia diante de uma nação.\\nBenjamin Franklin37\\nBenjamin Franklin nasceu em Boston, 17 de janeiro de 1706, \\nfoi um estudioso da história americana. Foi um dos líderes da \\nRevolução Americana, conhecido por suas citações e experiên -\\ncias com a eletricidade. Foi ainda o primeiro embaixador dos \\nEstados Unidos na França. Nesse momento de sua vida, foi \\nquando a interpretação de vida dos seus estudos, a um estilo \\nde vida americano, o fez propagar a captação da energia do \\ncaos europeu em uma forma de adaptação na cultura América.\\nReligioso, calvinista, e uma figura representativa do iluminis -\\nmo. Franklin tornou-se o primeiro-ministro dos correios dos \\nEstados Unidos. Assim foi agregando outras culturas pelo \\nmundo, e modificando a sua forma de interpretar uma energia \\npara um bem maior dos EUA.\\n37.  Texto baseado em https://pt.m.wikipedia.org/wiki/Benjamin_Fr anklin .\\ncaos do passado sendo vivido no futuro editável.indd   84caos do passado sendo vivido no futuro editável.indd   84 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 132747,
      "chapter": 4,
      "page": 84,
      "segment_type": "page",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 24.79347985347985,
      "complexity_metrics": {
        "word_count": 260,
        "sentence_count": 21,
        "paragraph_count": 1,
        "avg_sentence_length": 12.380952380952381,
        "avg_word_length": 5.184615384615385,
        "unique_word_ratio": 0.6269230769230769,
        "avg_paragraph_length": 260.0,
        "punctuation_density": 0.15,
        "line_break_count": 26,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "energia",
          "vida",
          "nobreza",
          "aumentando",
          "ainda",
          "poder",
          "diante",
          "interpretação",
          "benjamin",
          "franklin",
          "americana",
          "primeiro",
          "estados",
          "unidos",
          "caos",
          "forma",
          "passado",
          "sendo",
          "vivido"
        ],
        "entities": [
          [
            "84",
            "CARDINAL"
          ],
          [
            "1785",
            "DATE"
          ],
          [
            "Catarina",
            "ORG"
          ],
          [
            "Carta",
            "GPE"
          ],
          [
            "ainda mais",
            "PERSON"
          ],
          [
            "Trouxe",
            "ORG"
          ],
          [
            "Russo",
            "NORP"
          ],
          [
            "teoria de Darwin",
            "PERSON"
          ],
          [
            "Mulhe",
            "NORP"
          ],
          [
            "podendo exaltar",
            "ORG"
          ]
        ],
        "readability_score": 92.2541391941392,
        "semantic_density": 0,
        "word_count": 260,
        "unique_words": 163,
        "lexical_diversity": 0.6269230769230769
      },
      "preservation_score": 9.667054171907756e-06
    },
    {
      "id": 1,
      "text": "— 85 —Thomas Jefferson38\\nThomas Jefferson nasceu em Shadwell, 13 de abril de 1743 foi \\no terceiro presidente dos Estados Unidos e o principal autor da \\ndeclaração de independência dos Estados Unidos. \\nComo filósofo político, foi um homem do Iluminismo, Ben -\\njamin Franklin veio abrindo as portas para Thomas Jefferson \\nevoluir e propagar a energia de um direcionamento de se viver \\nmelhor em um contexto territorial, esse mesmo que conhe -\\nceu diversos dos grandes líderes intelectuais da Grã-Bretanha e \\nFrança de seu tempo. Apoiava a separação entre Igreja e Estado \\ne foi o autor do Estatuto da Virgínia para Liberdade Religiosa, \\nmesmo Com esse pensamento “contraditório” para a maioria, \\nmesmo assim proporcionou o efeito fã (idolatrar outra pessoa \\nmais que a si mesmo) em grande maioria dos americanos. ele \\ndominou foi cofundador e líder do Partido Democrata-Repu -\\nblicano, que dominou a política dos Estados Unidos por 25 \\nanos. \\nComo presidente, Thomas Jefferson defendeu os interesses co -\\nmerciais e marítimos da nação contra os Piratas da Barbária \\ne as políticas comerciais britânicas agressivas. Começando em \\n1803, Jefferson ainda promoveu uma política expansionista \\npara o oeste, organizando a Compra da Luisiana que, de uma \\nvez só dobrou o tamanho do país, fazendo da Europa uma \\nescola para se expandir e se adaptar ao próprio caos de sua \\nprópria ganância, da mesma forma que a humanidade vem fa -\\nzendo em toda sua existência. Para abrir espaço para reassen -\\ntamento de pessoas para o oeste, Jefferson começou um con -\\ntroverso processo de remoção indígena dos novos territórios \\nadquiridos. Jefferson assinou uma lei que proibia a importação \\nde escravos do exterior.\\n38.  Texto baseado em https://pt.m.wikipedia.org/wiki/Thomas_Jeff erson .\\ncaos do passado sendo vivido no futuro editável.indd   85caos do passado sendo vivido no futuro editável.indd   85 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 134493,
      "chapter": 4,
      "page": 85,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 28.097,
      "complexity_metrics": {
        "word_count": 300,
        "sentence_count": 16,
        "paragraph_count": 1,
        "avg_sentence_length": 18.75,
        "avg_word_length": 5.323333333333333,
        "unique_word_ratio": 0.6333333333333333,
        "avg_paragraph_length": 300.0,
        "punctuation_density": 0.11333333333333333,
        "line_break_count": 31,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "jefferson",
          "thomas",
          "mesmo",
          "estados",
          "unidos",
          "presidente",
          "autor",
          "como",
          "esse",
          "maioria",
          "dominou",
          "política",
          "oeste",
          "caos",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd"
        ],
        "entities": [
          [
            "85",
            "CARDINAL"
          ],
          [
            "Thomas Jefferson38\\nThomas Jefferson",
            "PERSON"
          ],
          [
            "Shadwell",
            "ORG"
          ],
          [
            "13",
            "CARDINAL"
          ],
          [
            "1743",
            "DATE"
          ],
          [
            "terceiro presidente",
            "GPE"
          ],
          [
            "Estados Unidos",
            "ORG"
          ],
          [
            "Estados Unidos",
            "ORG"
          ],
          [
            "Como",
            "ORG"
          ],
          [
            "Iluminismo",
            "PERSON"
          ]
        ],
        "readability_score": 89.028,
        "semantic_density": 0,
        "word_count": 300,
        "unique_words": 190,
        "lexical_diversity": 0.6333333333333333
      },
      "preservation_score": 1.1074099009900364e-05
    },
    {
      "id": 1,
      "text": "— 86 —Jefferson se destacou, entre outras coisas, como horticultor, lí -\\nder político, arquiteto, arqueólogo, paleontólogo, músico, in -\\nventor e fundador da Universidade da Virgínia. \\nEsse século... Imagina a quantidade de frequência de energia \\nque estava presente na terra, energia limpa, energia receptivo \\na todos. Porém, temos um problema e uma evolução diante \\ndo necessário para se viver melhor sabendo usar a sabedoria \\nda energia. Ocorreram muitos conflitos de pensamentos sobre \\no certo e o errado? O existe ou não existe? O bom e o ruim? \\nCriando uma interpretação mútua de si próprio entre as ener -\\ngias, devido à percepção pela mesma ser semelhante em cons -\\ntante evolução de um bem maior.\\nFilosofia século XVIII\\nFilosofia virando amor\\nNo século XVIII, em que as filosofias do Iluminismo come -\\nçaram a ter um efeito dramático, com grande influência de \\nShakespeare no surgimento de novos filósofos do século XIX. \\nRomantismo buscou combinar a racionalidade formal do pas -\\nsado, a ampliação do caos fez surgir contextos de percepção, \\nevolutivo e interpretativo, criando uma rede quântica de cap -\\ntação de energia. Ideias fundamentais que reluzem esta mu -\\ndança são a Evolução e Darwin. Pressões para igualitarismo e \\nmudanças rápidas e forçosas, culminaram em um período de \\nrevolução e turbulência, que fariam com que a filosofia mu -\\ndasse de uma forma proveitosa, devido ao período anterior ter \\ncaptado muitas correntes de energia (semelhante às correntes \\nmarítimas).\\nCorrentes de energia são as correntes que trafegam pela massa \\ncaos do passado sendo vivido no futuro editável.indd   86caos do passado sendo vivido no futuro editável.indd   86 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 136534,
      "chapter": 4,
      "page": 86,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 25.645555555555553,
      "complexity_metrics": {
        "word_count": 270,
        "sentence_count": 15,
        "paragraph_count": 1,
        "avg_sentence_length": 18.0,
        "avg_word_length": 5.262962962962963,
        "unique_word_ratio": 0.6592592592592592,
        "avg_paragraph_length": 270.0,
        "punctuation_density": 0.14814814814814814,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "século",
          "correntes",
          "evolução",
          "filosofia",
          "entre",
          "existe",
          "criando",
          "devido",
          "percepção",
          "pela",
          "semelhante",
          "xviii",
          "caos",
          "período",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável"
        ],
        "entities": [
          [
            "86",
            "CARDINAL"
          ],
          [
            "Jefferson",
            "PERSON"
          ],
          [
            "outras coisas",
            "PERSON"
          ],
          [
            "músico",
            "GPE"
          ],
          [
            "Imagina a quantidade de frequência de energia",
            "PERSON"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "melhor sabendo",
            "GPE"
          ],
          [
            "percepção pela",
            "PERSON"
          ],
          [
            "Filosofia",
            "PERSON"
          ],
          [
            "Iluminismo",
            "PRODUCT"
          ]
        ],
        "readability_score": 89.42111111111112,
        "semantic_density": 0,
        "word_count": 270,
        "unique_words": 178,
        "lexical_diversity": 0.6592592592592592
      },
      "preservation_score": 1.0818935438243673e-05
    },
    {
      "id": 1,
      "text": "— 87 —escura em movimento de propagação com oscilação em on -\\ndas contínuas, voltando para si próprio. Antes do cataclismo, \\ntínhamos poucas correntes de energia trafegando pela Terra, \\npois tínhamos muita massa escura e quem as captava, as exal -\\ntava (pajé, mago, feiticeiro, profetas, messias, filósofos). Nesse \\nperíodo, tinha muitas correntes de diferentes interpretação, \\nnessas interpretações venho a matemática sobre as frequências \\nexistente que circulam pelo mundo, amenizando a quantidade \\nde seguidores perante a um ser, pois a ciência começou a expli -\\ncar o inexplicável, afetando a filosofia e ampliando a filosofia \\npara ciências.\\nNesse período, você começa a enxergar uma singularidade \\nna propagação da energia, a energia saindo do centro do ca -\\ntaclismo e se propagando de uma forma inerente, para todos \\nas regiões do mundo (Rússia e Estados Unidos), aumentando \\na quantidade de energia focado em regiões, retirando mais re -\\ncursos do planeta, afetando novamente o eixo central da ter -\\nra, aumentando a massa escura concentrado a propagação da \\nenergia, em menor quantidade de frequência porém continua \\ne retilínea, com absorção perante ao seu próprio entendimen -\\nto ao meio em que eu vivo.\\nFilosofia da Ciência Moderna \\nNessa época, se cria uma nova forma de interpretação da ener -\\ngia, pois a massa escura não estava conseguindo conter a ener -\\ngia, pois a Terra estava saindo do caos e entrando em um novo \\nciclo de energia, essa energia captada por receptores que já ti -\\nnham outras referências históricas filosóficas, interpretativa de \\nvárias formas de ver e entender o fazer o bem para um bem \\nmaior, juntando a necessidade do corpo físico perante a for -\\nma de se viver com mais conforto, diante da necessidade que \\ncaos do passado sendo vivido no futuro editável.indd   87caos do passado sendo vivido no futuro editável.indd   87 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 138362,
      "chapter": 4,
      "page": 87,
      "segment_type": "page",
      "themes": {
        "filosofia": 53.57142857142857,
        "ciencia": 46.42857142857143
      },
      "difficulty": 36.524755700325734,
      "complexity_metrics": {
        "word_count": 307,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 43.857142857142854,
        "avg_word_length": 5.136807817589577,
        "unique_word_ratio": 0.5993485342019544,
        "avg_paragraph_length": 307.0,
        "punctuation_density": 0.13029315960912052,
        "line_break_count": 30,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "escura",
          "pois",
          "propagação",
          "massa",
          "quantidade",
          "perante",
          "filosofia",
          "próprio",
          "tínhamos",
          "correntes",
          "terra",
          "nesse",
          "período",
          "interpretação",
          "mundo",
          "ciência",
          "afetando",
          "saindo",
          "forma"
        ],
        "entities": [
          [
            "87",
            "CARDINAL"
          ],
          [
            "das contínuas",
            "PRODUCT"
          ],
          [
            "massa escura e quem",
            "PERSON"
          ],
          [
            "circulam pelo mundo",
            "PERSON"
          ],
          [
            "ciência começou",
            "PERSON"
          ],
          [
            "Nesse",
            "ORG"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "eu",
            "PERSON"
          ],
          [
            "Filosofia da Ciência Moderna",
            "PERSON"
          ],
          [
            "Nessa",
            "PERSON"
          ]
        ],
        "readability_score": 76.5303862261517,
        "semantic_density": 0,
        "word_count": 307,
        "unique_words": 184,
        "lexical_diversity": 0.5993485342019544
      },
      "preservation_score": 1.246656307236973e-05
    },
    {
      "id": 1,
      "text": "— 88 —fomos criando com o nosso próprio caos perante a uma neces -\\nsidade do caos coletivo, mútuo e conjunto de se conter o caos \\npara um viver melhor em um conjunto de energia boa para si \\npróprio. Movimento é a energia inicial de toda existência, tudo \\ne qualquer coisa que você pensa ou faça, existe um movimen -\\nto de ação, reação, ação, reação quântico. Quando entramos \\nem contato com uma nova energia, criamos uma lembrança \\n(quântico) diante dessa nova interação, revivida quando se têm \\na necessidade de uso da mesma, nossos corpos (universo, galá -\\nxias, sistemas, Terra, nós) precisam se movimentar para viver. O \\ncaos é necessário ter para movimentar-se e adaptar-se, criando \\num sistema de movimento constante de ação e reação propor -\\ncional ao sentir do “corpo” , o saber movimentar-se é a raciona -\\nlidade de um viver melhor com todos no amanhã. Calcular o \\nimpacto da ação perante a outra ação e calcular a reação futura, \\né preservar o caos colateral.\\nFilósofo inventor39 \\nLeonardo da Vinci nasceu em Anchiano, 15 de abril de 1452, \\nfoi o cara!!! uma das figuras mais importantes do Alto Renas -\\ncimento foi cientista, matemático, engenheiro, inventor, ana -\\ntomista, pintor, escultor, arquiteto, botânico, poeta e músico. \\nPor ter muitos dons e se destacar em tudo que fazia, se transfor -\\nmou em um paradigma para todos, alguém cuja curiosidade \\ninsaciável era igualada apenas pela sua capacidade de invenção. \\nNascido como filho ilegítimo de um notário e de uma cam -\\nponesa, foi educado no ateliê do renomado pintor trabalhou \\nem Milão, Veneza, Roma e Bolonha. O desenho do Homem \\nVitruviano, é a medida mais próxima da perfeição do corpo \\n39.  Texto baseado em https://pt.m.wikipedia.org/wiki/Leonardo_da _Vinci .\\ncaos do passado sendo vivido no futuro editável.indd   88caos do passado sendo vivido no futuro editável.indd   88 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 140385,
      "chapter": 4,
      "page": 88,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 31.74303605313093,
      "complexity_metrics": {
        "word_count": 310,
        "sentence_count": 17,
        "paragraph_count": 1,
        "avg_sentence_length": 18.235294117647058,
        "avg_word_length": 5.025806451612903,
        "unique_word_ratio": 0.635483870967742,
        "avg_paragraph_length": 310.0,
        "punctuation_density": 0.18064516129032257,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "caos",
          "ação",
          "reação",
          "viver",
          "energia",
          "movimentar",
          "criando",
          "próprio",
          "perante",
          "conjunto",
          "melhor",
          "movimento",
          "tudo",
          "quântico",
          "quando",
          "nova",
          "corpo",
          "todos",
          "calcular",
          "mais"
        ],
        "entities": [
          [
            "88",
            "CARDINAL"
          ],
          [
            "de se",
            "PERSON"
          ],
          [
            "que",
            "CARDINAL"
          ],
          [
            "reação",
            "GPE"
          ],
          [
            "ação",
            "GPE"
          ],
          [
            "reação quântico",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "nova",
            "LOC"
          ],
          [
            "nova",
            "LOC"
          ],
          [
            "revivida quando",
            "PERSON"
          ]
        ],
        "readability_score": 89.3746110056926,
        "semantic_density": 0,
        "word_count": 310,
        "unique_words": 197,
        "lexical_diversity": 0.635483870967742
      },
      "preservation_score": 1.6068014626609876e-05
    },
    {
      "id": 1,
      "text": "— 89 —humano, foi feito por um desafio de provar que o homem era \\no “centro do mundo” , ele teve a ideia de pegar os extremos do \\ncírculo e fazer um quadrado dentro para conseguir ter uma \\nbase de proporção, com isso teve que colocar o pé de lado para \\nconseguir encaixar dentro do círculo. Não conseguia parar de \\ncriar devido a um viver muito intenso, gerando interpretação \\nde energia de adaptação do caos vivido, Leonardo vivia uma \\nvida de muito sexo, drogas, religiosidade e tudo que o melhor \\nele podia aproveitar dentro da sua própria realidade de vida. \\nTeve ideias muito à frente de seu tempo, como um protótipo \\nde helicóptero, um tanque de guerra, o uso da energia solar, \\numa calculadora, o casco duplo nas embarcações, e uma teoria \\nrudimentar das placas tectônicas. \\nFrase\\nQuando você tiver provado a sensação de voar, andará na terra \\ncom seus olhos voltados ao céu, pois lá você esteve e para lá \\ndesejará retornar.\\nEsse cara é um dos caras. Ele captou a energia em forma de \\nmatemática e a energia da aerodinâmica em matemática, con -\\nseguiu interpretar o seu mundo dentro das próprias “loucuras” \\ndo seu próprio mundo, ele era capaz de ter a sensibilidade de \\nentender e compreender a energia, e recriar aquela sensação \\nna sensação física e para o mundo físico, para que nós pudés -\\nsemos entender que o mundo da energia é o mesmo mundo \\nque nós vivemos. \\nAnalogia\\nMessias em criar a energia em matéria!!!\\ncaos do passado sendo vivido no futuro editável.indd   89caos do passado sendo vivido no futuro editável.indd   89 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 142394,
      "chapter": 4,
      "page": 89,
      "segment_type": "page",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 32.07140221402214,
      "complexity_metrics": {
        "word_count": 271,
        "sentence_count": 10,
        "paragraph_count": 1,
        "avg_sentence_length": 27.1,
        "avg_word_length": 4.7380073800738005,
        "unique_word_ratio": 0.6014760147601476,
        "avg_paragraph_length": 271.0,
        "punctuation_density": 0.12546125461254612,
        "line_break_count": 27,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "mundo",
          "dentro",
          "teve",
          "muito",
          "vivido",
          "sensação",
          "círculo",
          "conseguir",
          "criar",
          "caos",
          "vida",
          "você",
          "matemática",
          "entender",
          "passado",
          "sendo",
          "futuro",
          "editável",
          "indd"
        ],
        "entities": [
          [
            "89",
            "CARDINAL"
          ],
          [
            "foi feito",
            "PERSON"
          ],
          [
            "pé de lado",
            "ORG"
          ],
          [
            "encaixar dentro",
            "PERSON"
          ],
          [
            "Leonardo",
            "PERSON"
          ],
          [
            "vida de muito sexo",
            "ORG"
          ],
          [
            "drogas",
            "GPE"
          ],
          [
            "podia aproveitar",
            "ORG"
          ],
          [
            "dentro da sua própria",
            "ORG"
          ],
          [
            "Teve",
            "PERSON"
          ]
        ],
        "readability_score": 85.02859778597787,
        "semantic_density": 0,
        "word_count": 271,
        "unique_words": 163,
        "lexical_diversity": 0.6014760147601476
      },
      "preservation_score": 8.267299721676767e-06
    },
    {
      "id": 1,
      "text": "— 90 —Galileo di Vincenzo Bonaulti de Galilei40\\nGalileu Galilei nasceu em Pisa, 15 de fevereiro de 1564 foi um \\nastrônomo, físico e engenheiro florentino, mais um cheios de \\ndons. Pai da ciência moderna, estudou o princípio da relativi -\\ndade e fenômenos como a rapidez e a velocidade, a gravida -\\nde e a queda livre, a inércia e o movimento de projéteis. Era \\numa pessoa caótica, vivia debatendo com tudo e com todos, \\nera extremista em sua ideologia de vida, era matemático. Mas \\ntambém trabalhou em ciência e tecnologia aplicadas, inventou \\no termos copio e várias bússolas militares, e usou o telescópio \\npara observações científicas de objetos celestes. \\nFoi julgado pela igreja católica por não seguir uma doutrina, \\nforçado a se retratar, e passou o resto de sua vida em prisão \\ndomiciliar. \\nEsse é o gênio da matemática diante da energia gravitacional. \\nTudo que ele via era a massa da energia que causava no corpo \\nfísico, visual e no mundo material. O que é a matemática? Ma -\\ntemática é exatidão da física. Ter tese, teoria é uma coisa total -\\nmente diferente da matemática. Matemática é você encontrar \\no padrão da energia e colocar em fórmula para que todos pos -\\nsam entender.\\nAnalogia\\nProfeta da energia!!!\\nIsaac Newton41\\nIsaac Newton nasceu em Colsterworth, 25 de dezembro de \\n1642 foi um matemático, físico, astrônomo, teólogo e autor \\n40.  Texto baseado em https://pt.m.wikipedia.org/wiki/Galileu_G alilei .\\n41.  Texto baseado em https://pt.m.wikipedia.org/wiki/Isaac_ Newton .\\ncaos do passado sendo vivido no futuro editável.indd   90caos do passado sendo vivido no futuro editável.indd   90 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 144092,
      "chapter": 4,
      "page": 90,
      "segment_type": "page",
      "themes": {
        "ciencia": 83.87096774193549,
        "tecnologia": 16.129032258064516
      },
      "difficulty": 23.950000000000003,
      "complexity_metrics": {
        "word_count": 264,
        "sentence_count": 25,
        "paragraph_count": 1,
        "avg_sentence_length": 10.56,
        "avg_word_length": 5.166666666666667,
        "unique_word_ratio": 0.6515151515151515,
        "avg_paragraph_length": 264.0,
        "punctuation_density": 0.19318181818181818,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "matemática",
          "energia",
          "físico",
          "nasceu",
          "astrônomo",
          "ciência",
          "tudo",
          "todos",
          "vida",
          "matemático",
          "isaac",
          "newton",
          "texto",
          "baseado",
          "https",
          "wikipedia",
          "wiki",
          "passado",
          "sendo",
          "vivido"
        ],
        "entities": [
          [
            "90",
            "CARDINAL"
          ],
          [
            "Galileo",
            "PRODUCT"
          ],
          [
            "Bonaulti de Galilei40\\n",
            "PERSON"
          ],
          [
            "Pisa",
            "ORG"
          ],
          [
            "15",
            "CARDINAL"
          ],
          [
            "físico",
            "GPE"
          ],
          [
            "engenheiro florentino",
            "PERSON"
          ],
          [
            "ciência moderna",
            "PERSON"
          ],
          [
            "movimento de projéteis",
            "ORG"
          ],
          [
            "todos",
            "CARDINAL"
          ]
        ],
        "readability_score": 93.17,
        "semantic_density": 0,
        "word_count": 264,
        "unique_words": 172,
        "lexical_diversity": 0.6515151515151515
      },
      "preservation_score": 1.1839589724870433e-05
    },
    {
      "id": 1,
      "text": "— 91 —inglês as suas ideias ao observar as coisas básicas da vida e ques -\\ntionar o início do movimento da ação, fez ele ser uma pessoa \\nchave na Revolução Científica. \\nCaptou as primeiras leis do movimento e da gravitação uni -\\nversal que criaram o ponto de vista científico dominante até \\nserem substituídas pela teoria da relatividade de Albert Eins -\\ntein. Newton usou sua descrição matemática da gravidade para \\nprovar as leis de movimento planetário, explicar as marés, as \\ntrajetórias dos cometas. Demonstrou que o movimento dos \\nobjetos na Terra e nos corpos celestes poderia ser explicado \\npelos mesmos princípios. \\nNewton construiu o primeiro telescópio refletor prático e de -\\nsenvolveu uma teoria sofisticada da cor com base na observa -\\nção de que um prisma separa a luz branca nas cores do espec -\\ntro visível. O olhar em seu entorno o que você enxerga? Como \\ninterpretamos o que olhamos? Até que ponto o observar o \\n“básico” é possível evoluirmos e criarmos? Fez o primeiro cál -\\nculo teórico da velocidade do som e introduziu a noção de um \\nfluido newtoniano. \\nFoi um cristão devoto, mas pouco ortodoxo, que rejeitava, em \\nparticular, a doutrina da Trindade. Ele captava a energia “di -\\nvina” em movimento, tudo que ele enxergava no movimento \\nreligioso era a pureza e não o lado da ganância. Se recusava a \\nreceber ordens da Igreja da Inglaterra dedicou grande parte de \\nseu tempo ao estudo da alquimia e da cronologia bíblica. \\nNewton agregou, evoluiu a energia que Galileu Galilei cap -\\ntou... Ele captou a mesma frequência com o conhecimento \\nque ele já tinha de outros sobre aquela energia, com mais re -\\ncursos evolutivo que ele mesmo criou o telescópio newtonia -\\nno, conseguindo ter uma melhor percepção de como a energia \\n(luz) se propaga diante dos nossos olhos.\\ncaos do passado sendo vivido no futuro editável.indd   91caos do passado sendo vivido no futuro editável.indd   91 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 145860,
      "chapter": 4,
      "page": 91,
      "segment_type": "page",
      "themes": {
        "ciencia": 72.22222222222221,
        "arte": 27.77777777777778
      },
      "difficulty": 34.13793847814355,
      "complexity_metrics": {
        "word_count": 327,
        "sentence_count": 17,
        "paragraph_count": 1,
        "avg_sentence_length": 19.235294117647058,
        "avg_word_length": 4.871559633027523,
        "unique_word_ratio": 0.6422018348623854,
        "avg_paragraph_length": 327.0,
        "punctuation_density": 0.10091743119266056,
        "line_break_count": 31,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "movimento",
          "energia",
          "newton",
          "observar",
          "captou",
          "leis",
          "ponto",
          "teoria",
          "primeiro",
          "telescópio",
          "como",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "inglês",
          "suas",
          "ideias"
        ],
        "entities": [
          [
            "91",
            "CARDINAL"
          ],
          [
            "coisas básicas da vida",
            "PERSON"
          ],
          [
            "da ação",
            "PERSON"
          ],
          [
            "Captou",
            "GPE"
          ],
          [
            "leis",
            "PERSON"
          ],
          [
            "ponto de vista científico",
            "ORG"
          ],
          [
            "dominante até \\nserem substituídas pela",
            "PERSON"
          ],
          [
            "teoria da relatividade de Albert Eins -\\n",
            "PERSON"
          ],
          [
            "Newton",
            "ORG"
          ],
          [
            "matemática da gravidade",
            "PERSON"
          ]
        ],
        "readability_score": 88.92088505126821,
        "semantic_density": 0,
        "word_count": 327,
        "unique_words": 210,
        "lexical_diversity": 0.6422018348623854
      },
      "preservation_score": 1.1752105071730996e-05
    },
    {
      "id": 1,
      "text": "— 92 —Segundo Profeta da energia!!\\nIdade Moderna e as guerras\\nAs guerras nesta idade, foram exaltados os próprios interesses \\ndiante da “minha necessidade, voltando ao ciclo da ganância \\nda minha própria “necessidade” .\\nA Guerra dos 80 anos42\\nA Guerra dos 80 anos ou Revolta Holandesa de 1568 a 1648, \\nfoi a guerra de secessão na qual as Províncias Unidas se torna -\\nram independente da Espanha.\\nDurante essa guerra, as Províncias Unidas se tornaram, por um \\ncurto período histórico, uma potência mundial, com grande \\npoder naval, além de se beneficiarem de um crescimento eco -\\nnómico, científico e cultural sem precedentes.\\nOs Países Baixos pertenciam ao Império Espanhol, mas o \\nConselho de Regência. Devido a altos impostos, desemprego \\ne temores da perseguição católica contra os calvinistas cria -\\nram uma perigosa oposição, destruído pelo duque de Alba. \\nGuilherme, o Taciturno, que evitou batalhas campais com as \\nforças espanholas, explorando estrategicamente seu conheci -\\nmento da região, levou a uma união temporária de todos os \\nPaíses Baixos na pacificação de Gante. Os excessos calvinistas \\nlogo levaram as províncias do sul a formarem a União de Ar -\\nras (1579) e a fazer as pazes com a Espanha. As províncias do \\nnorte formaram a União de Utrecht e a guerra tornou-se uma \\nluta religiosa pela independência. As Províncias Unidas salva -\\n42.  Texto baseado em https://pt.m.wikipedia.org/wiki/Guerra_dos_Oiten -\\nta_Anos .\\ncaos do passado sendo vivido no futuro editável.indd   92caos do passado sendo vivido no futuro editável.indd   92 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 147921,
      "chapter": 4,
      "page": 92,
      "segment_type": "page",
      "themes": {},
      "difficulty": 24.006945428773918,
      "complexity_metrics": {
        "word_count": 249,
        "sentence_count": 17,
        "paragraph_count": 1,
        "avg_sentence_length": 14.647058823529411,
        "avg_word_length": 5.317269076305221,
        "unique_word_ratio": 0.6666666666666666,
        "avg_paragraph_length": 249.0,
        "punctuation_density": 0.15261044176706828,
        "line_break_count": 27,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "guerra",
          "províncias",
          "unidas",
          "união",
          "idade",
          "guerras",
          "minha",
          "necessidade",
          "espanha",
          "países",
          "baixos",
          "calvinistas",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "segundo",
          "profeta"
        ],
        "entities": [
          [
            "92",
            "CARDINAL"
          ],
          [
            "Idade",
            "GPE"
          ],
          [
            "Moderna",
            "PERSON"
          ],
          [
            "Guerra",
            "ORG"
          ],
          [
            "80",
            "CARDINAL"
          ],
          [
            "Guerra",
            "ORG"
          ],
          [
            "80",
            "CARDINAL"
          ],
          [
            "Revolta Holandesa de 1568",
            "ORG"
          ],
          [
            "1648",
            "DATE"
          ],
          [
            "guerra de secessão",
            "ORG"
          ]
        ],
        "readability_score": 91.08128986534373,
        "semantic_density": 0,
        "word_count": 249,
        "unique_words": 166,
        "lexical_diversity": 0.6666666666666666
      },
      "preservation_score": 1.0432544886877827e-05
    },
    {
      "id": 1,
      "text": "— 93 —ram-se pelo compromisso de guerra da Espanha com a França, \\nInglaterra e Turquia. \\nA Guerra Imjin43\\nA Guerra Imjin foi um conflito armado travado entre 1592 e \\n1598 na qual se envolveram três países asiáticos: Japão, China \\ne Coreia. Uma guerra originária devido a eu precisar de mais \\nrecursos para viver, no intuito de querer se aliar para conquis -\\ntar mais territórios para ter uma maior quantidade de produ -\\nção (alimentos, ganância), para a minha necessidade de viver \\nmelhor que a sua. Japão queria se unir a Coreia para invadir \\na China e não foi atendido, gerando uma guerra generalizada \\nentre eles.\\nDepois de um rápido e eficaz avanço das tropas japonesas pelo \\nterritório coreano, a campanha naval do Almirante Yi cortou \\no fornecimento de recursos para os invasores, obrigando-os a \\nparar seu avanço. A milícia coreana, junto com a intervenção \\ndo exército chinês, obrigou o governo japonês a iniciar rela -\\nções de paz com a China em 1593. Após os pedidos de Hi -\\ndeyoshi terem sido negados, a guerra entrou em uma nova fase \\nem 1597, quando se retomaram as hostilidades. O confronto \\nterminou em 1598 com a retirada total das tropas invasoras \\nseguinte a morte de Hideyoshi.\\nEsse acontecimento foi o primeiro na Ásia a utilizar exércitos \\ncom números elevados de soldados portando armas modernas \\ne representou um dano severo para a Coreia. Esse país sofreu \\na perda de 66% de suas terras cultiváveis e a extração forçada \\nde artesões e acadêmicos ao Japão, levando ao desenvolvimen -\\nto da ciência naquele país. Devido a todo esse caos, perdemos \\n43.  Texto baseado em https://pt.m.wikipedia.org/wiki/Guerra _Imjin .\\ncaos do passado sendo vivido no futuro editável.indd   93caos do passado sendo vivido no futuro editável.indd   93 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 149630,
      "chapter": 4,
      "page": 93,
      "segment_type": "page",
      "themes": {
        "ciencia": 56.52173913043479,
        "arte": 43.47826086956522
      },
      "difficulty": 24.782879818594104,
      "complexity_metrics": {
        "word_count": 294,
        "sentence_count": 18,
        "paragraph_count": 1,
        "avg_sentence_length": 16.333333333333332,
        "avg_word_length": 5.017006802721088,
        "unique_word_ratio": 0.6598639455782312,
        "avg_paragraph_length": 294.0,
        "punctuation_density": 0.12585034013605442,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "guerra",
          "japão",
          "china",
          "coreia",
          "esse",
          "pelo",
          "entre",
          "devido",
          "mais",
          "recursos",
          "viver",
          "avanço",
          "tropas",
          "país",
          "caos",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável"
        ],
        "entities": [
          [
            "93",
            "CARDINAL"
          ],
          [
            "França",
            "GPE"
          ],
          [
            "Guerra Imjin43",
            "ORG"
          ],
          [
            "Guerra Imjin",
            "GPE"
          ],
          [
            "conflito",
            "GPE"
          ],
          [
            "1592 e \\n1598",
            "DATE"
          ],
          [
            "Japão",
            "GPE"
          ],
          [
            "China",
            "GPE"
          ],
          [
            "Coreia",
            "ORG"
          ],
          [
            "eu precisar de mais",
            "PERSON"
          ]
        ],
        "readability_score": 90.328231292517,
        "semantic_density": 0,
        "word_count": 294,
        "unique_words": 194,
        "lexical_diversity": 0.6598639455782312
      },
      "preservation_score": 1.0148219764174657e-05
    },
    {
      "id": 1,
      "text": "— 94 —grande parte de captadores de energia da história da China \\nmuitos registros foram queimados junto com vários palácios \\nimperiais em Seul. Devido a guerra precisar de muitos recur -\\nsos a dinastia Ming ficou sem recursos para se sustentar contra \\noutros inimigos. Isto facilitaria a ascensão ao poder da dinastia \\nQing.\\nTratado de Tordesilhas44\\nAssinado na povoação castelhana de Tordesilhas em 7 de junho \\nde 1494, foi um tratado celebrado entre o Reino de Portugal e \\na Coroa de Castela para dividir as terras “descobertas e por des -\\ncobrir” por ambas as Coroas fora da Europa. A necessidade de \\nse ter mais, fez o humano entrar em “ desespero” pela própria \\nganância, gerando expedições marítimas para se conquistar \\nmais recursos para um “viver melhor” . Esse tratado surgiu na \\nsequência da contestação portuguesa às pretensões da Coroa \\nde Castela, resultantes da viagem de Cristóvão Colombo, que \\num ano e meio antes chegara ao ”Novo Mundo” .\\nO tratado definia como linha de demarcação o meridiano 370 \\nléguas a oeste da ilha de Santo Antão no arquipélago de Cabo \\nVerde. Esta linha estava situada a meio caminho entre estas \\nilhas (eram de Portugal) e as ilhas das Caraíbas descobertas por \\nColombo, no tratado referidas como “Cipango” e Antília. Os \\nterritórios a leste desse meridiano pertenceriam a Portugal e os \\nterritórios a oeste, a Castela “ O surrealismo do poder humano” . \\nMesma coisa que a religião fez, só que de uma forma direcio -\\nnada e não “manipulada” . Devido a ocorrer outras questões ao \\ndecorrer dos anos da chamada “questão das Molucas” , o outro \\n44.  Texto baseado em https://pt.m.wikipedia.org/wiki/Tratado_de_Tor -\\ndesilhas .\\ncaos do passado sendo vivido no futuro editável.indd   94caos do passado sendo vivido no futuro editável.indd   94 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 151542,
      "chapter": 4,
      "page": 94,
      "segment_type": "page",
      "themes": {
        "ciencia": 72.22222222222221,
        "arte": 27.77777777777778
      },
      "difficulty": 24.74249249249249,
      "complexity_metrics": {
        "word_count": 296,
        "sentence_count": 18,
        "paragraph_count": 1,
        "avg_sentence_length": 16.444444444444443,
        "avg_word_length": 5.0675675675675675,
        "unique_word_ratio": 0.652027027027027,
        "avg_paragraph_length": 296.0,
        "punctuation_density": 0.10472972972972973,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "tratado",
          "portugal",
          "castela",
          "muitos",
          "devido",
          "dinastia",
          "recursos",
          "poder",
          "entre",
          "coroa",
          "descobertas",
          "mais",
          "humano",
          "colombo",
          "meio",
          "como",
          "linha",
          "meridiano",
          "oeste",
          "ilhas"
        ],
        "entities": [
          [
            "94",
            "CARDINAL"
          ],
          [
            "de captadores de energia",
            "ORG"
          ],
          [
            "da história da",
            "PERSON"
          ],
          [
            "China",
            "GPE"
          ],
          [
            "Seul",
            "PERSON"
          ],
          [
            "Devido",
            "PERSON"
          ],
          [
            "para se sustentar",
            "PERSON"
          ],
          [
            "contra \\noutros inimigos",
            "PERSON"
          ],
          [
            "Qing",
            "DATE"
          ],
          [
            "Tratado",
            "GPE"
          ]
        ],
        "readability_score": 90.25750750750751,
        "semantic_density": 0,
        "word_count": 296,
        "unique_words": 193,
        "lexical_diversity": 0.652027027027027
      },
      "preservation_score": 1.1628168479783462e-05
    },
    {
      "id": 1,
      "text": "— 95 —lado da Terra seria dividido, assumindo como linha de demar -\\ncação, a leste, o antimeridiano correspondente ao meridiano \\nde Tordesilhas, pelo Tratado de Saragoça, a 22 de abril de 1529.\\nPara as negociações do Tratado e a sua assinatura, D. João II de \\nPortugal (1477, 1481-1495) designou como embaixador a sua \\nprima de Castela (filha de uma infanta portuguesa) a D. Rui \\nde Sousa. \\nEsse período foi crucial para evolução da propagação da ener -\\ngia, diante de um caos gerado universalmente por nós mes -\\nmos. Propagação da energia fizeram outros sentirem uma \\nenergia semelhante, em alguns casos se propagou ao ponto de \\ncriar novos “profetas” da energia, pois assim como a energia \\nse propaga, a massa escura se expande com o caos gerado pela \\nprópria interpretação da energia, que se propagou em uma in -\\nterpretação errada, diante da própria situação da necessidade \\nde si próprio, pensando que era um bem maior para um local, \\ncidade, Estado, país e mundo.\\ncaos do passado sendo vivido no futuro editável.indd   95caos do passado sendo vivido no futuro editável.indd   95 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 153482,
      "chapter": 4,
      "page": 95,
      "segment_type": "page",
      "themes": {},
      "difficulty": 26.88726726726727,
      "complexity_metrics": {
        "word_count": 185,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 20.555555555555557,
        "avg_word_length": 4.994594594594594,
        "unique_word_ratio": 0.6594594594594595,
        "avg_paragraph_length": 185.0,
        "punctuation_density": 0.15675675675675677,
        "line_break_count": 17,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "como",
          "caos",
          "tratado",
          "propagação",
          "diante",
          "gerado",
          "propagou",
          "própria",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "lado",
          "terra",
          "seria",
          "dividido",
          "assumindo"
        ],
        "entities": [
          [
            "95",
            "CARDINAL"
          ],
          [
            "de demar -\\ncação",
            "PERSON"
          ],
          [
            "pelo Tratado de Saragoça",
            "ORG"
          ],
          [
            "22",
            "CARDINAL"
          ],
          [
            "Tratado",
            "GPE"
          ],
          [
            "D. João II de \\nPortugal",
            "PERSON"
          ],
          [
            "1477",
            "DATE"
          ],
          [
            "1481-1495",
            "DATE"
          ],
          [
            "de Castela",
            "PERSON"
          ],
          [
            "D. Rui \\nde Sousa",
            "PERSON"
          ]
        ],
        "readability_score": 88.22384384384384,
        "semantic_density": 0,
        "word_count": 185,
        "unique_words": 122,
        "lexical_diversity": 0.6594594594594595
      },
      "preservation_score": 5.205336861796483e-06
    },
    {
      "id": 1,
      "text": "— 96 —\\ncaos do passado sendo vivido no futuro editável.indd   96caos do passado sendo vivido no futuro editável.indd   96 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 154724,
      "chapter": 4,
      "page": 96,
      "segment_type": "page",
      "themes": {},
      "difficulty": 20.91449275362319,
      "complexity_metrics": {
        "word_count": 23,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 7.666666666666667,
        "avg_word_length": 5.826086956521739,
        "unique_word_ratio": 0.6086956521739131,
        "avg_paragraph_length": 23.0,
        "punctuation_density": 0.2608695652173913,
        "line_break_count": 1,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "caos"
        ],
        "entities": [
          [
            "96",
            "CARDINAL"
          ],
          [
            "editável.indd   96caos",
            "QUANTITY"
          ],
          [
            "sendo vivido",
            "PERSON"
          ],
          [
            "editável.indd   96",
            "DATE"
          ],
          [
            "28/03/2022",
            "DATE"
          ],
          [
            "14:53:3928/03/2022",
            "CARDINAL"
          ],
          [
            "14:53:39",
            "PERSON"
          ]
        ],
        "readability_score": 94.41884057971015,
        "semantic_density": 0,
        "word_count": 23,
        "unique_words": 14,
        "lexical_diversity": 0.6086956521739131
      },
      "preservation_score": 5.8323102092957795e-08
    },
    {
      "id": 1,
      "text": "— 97 —Capítulo 10\\nIdade Contemporânea45\\nNessa idade começamos a ter frequência de energia pelo mun -\\ndo todo (correntes de energia semelhante a correntes maríti -\\nma), diante da própria necessidade local, territorial e popula -\\ncional. Nesse período, nós estamos em crescimento para todos \\nos lados, frequência de energia, absorção e captação de energia \\nde várias formas de entendimento diferente, transformando o \\nmundo em um cataclismo das guerras. São guerras por todos \\nos motivos, desde religioso, filosófico, científico, preconceito, \\nliberdade, ganância, necessidade, poder, luxúria etc. Tudo que \\neu quero dentro daquela frequência de um bem em comum \\npara uma população, é melhor para mim do que para você.\\nA Idade Contemporânea, também chamada de Contempora -\\nneidade, é o período atual da história ocidental e cujo início \\nremonta à Revolução Francesa. Marcado pela captação da ener -\\ngia do iluminismo, evolução filosófica que defende o primado \\nda razão e uma maior interpretação da ciência em uma melhor \\nadaptação da ação e reação.\\nEsse período caracteriza-se, pelo desenvolvimento e consoli -\\ndação do capitalismo no ocidente e, consequentemente pelas \\ndisputas das grandes potências europeias por territórios, ma -\\ntérias-primas e mercados consumidores, adaptando-se a sua \\nprópria ganância.\\nApós duas grandes guerras mundiais, teve conflitos filosóficos \\nde enxergar e perceber o quanto nós humanos somos subde -\\n45.  Texto baseado em https://pt.m.wikipedia.org/wiki/Idade_Contempor% -\\nC3%A2nea .\\ncaos do passado sendo vivido no futuro editável.indd   97caos do passado sendo vivido no futuro editável.indd   97 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 155003,
      "chapter": 10,
      "page": 97,
      "segment_type": "page",
      "themes": {
        "filosofia": 53.57142857142857,
        "ciencia": 46.42857142857144
      },
      "difficulty": 27.02285714285714,
      "complexity_metrics": {
        "word_count": 245,
        "sentence_count": 15,
        "paragraph_count": 1,
        "avg_sentence_length": 16.333333333333332,
        "avg_word_length": 5.742857142857143,
        "unique_word_ratio": 0.689795918367347,
        "avg_paragraph_length": 245.0,
        "punctuation_density": 0.17551020408163265,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "idade",
          "frequência",
          "período",
          "guerras",
          "pelo",
          "correntes",
          "própria",
          "necessidade",
          "todos",
          "captação",
          "ganância",
          "melhor",
          "grandes",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd"
        ],
        "entities": [
          [
            "97",
            "CARDINAL"
          ],
          [
            "Idade",
            "GPE"
          ],
          [
            "Nessa",
            "ORG"
          ],
          [
            "pelo mun -\\n",
            "PERSON"
          ],
          [
            "diante da própria",
            "PERSON"
          ],
          [
            "Nesse",
            "ORG"
          ],
          [
            "nós estamos",
            "ORG"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "preconceito",
            "PERSON"
          ],
          [
            "que \\neu",
            "QUANTITY"
          ]
        ],
        "readability_score": 90.11047619047619,
        "semantic_density": 0,
        "word_count": 245,
        "unique_words": 169,
        "lexical_diversity": 0.689795918367347
      },
      "preservation_score": 1.2043720582195786e-05
    },
    {
      "id": 1,
      "text": "— 98 —senvolvidos, nos fazendo perceber o quão “involuídos” nós so -\\nmos. A percepção de que nações consideradas tão avançadas e \\ninstruídas eram de fato capazes de cometer atrocidades devido \\na não conter o seu próprio sentimento.\\nNão sabemos que ponto se iniciou, em qual ponto irá termi -\\nnar e se é que ainda estamos.\\nEssa é a idade a qual nos encontramos, pois o contemporâneo \\né o presente, então, a partir deste ponto, não irei mais colocar \\nem ordem dê uma linha de tempo constante de fato por fato, \\nirei colocar os fatos em que eu irei ver fatores e pessoas sig -\\nnificativas, dentro de uma linha de tempo da propagação da \\nenergia até o nosso viver de hoje.\\ncaos do passado sendo vivido no futuro editável.indd   98caos do passado sendo vivido no futuro editável.indd   98 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 156791,
      "chapter": 4,
      "page": 98,
      "segment_type": "page",
      "themes": {},
      "difficulty": 26.76273726273726,
      "complexity_metrics": {
        "word_count": 143,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 20.428571428571427,
        "avg_word_length": 4.685314685314685,
        "unique_word_ratio": 0.6783216783216783,
        "avg_paragraph_length": 143.0,
        "punctuation_density": 0.1258741258741259,
        "line_break_count": 12,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "fato",
          "ponto",
          "irei",
          "qual",
          "colocar",
          "linha",
          "tempo",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "senvolvidos",
          "fazendo",
          "perceber",
          "quão",
          "involuídos",
          "percepção",
          "nações"
        ],
        "entities": [
          [
            "98",
            "CARDINAL"
          ],
          [
            "fazendo",
            "ORG"
          ],
          [
            "perceber o quão",
            "PERSON"
          ],
          [
            "de fato",
            "PERSON"
          ],
          [
            "irá termi -\\n",
            "PERSON"
          ],
          [
            "ainda estamos",
            "PERSON"
          ],
          [
            "Essa",
            "PERSON"
          ],
          [
            "que eu",
            "PERSON"
          ],
          [
            "dentro de uma",
            "ORG"
          ],
          [
            "editável.indd",
            "CARDINAL"
          ]
        ],
        "readability_score": 88.38011988011988,
        "semantic_density": 0,
        "word_count": 143,
        "unique_words": 97,
        "lexical_diversity": 0.6783216783216783
      },
      "preservation_score": 2.1871163284859175e-06
    },
    {
      "id": 1,
      "text": "— 99 —Capítulo 11\\nKrakatoa o segundo cataclismo46 \\nA erupção do Krakatoa em 1883 ocorreu, em 27 de agosto da -\\nquele ano na ilha de Krakatoa, localizada no estreito de Sunda, \\nentre as ilhas de Sumatra e Java, nas Índias Orientais Holan -\\ndesas (atual Indonésia). A ilha desapareceu quando o vulcão \\nhomônimo, no monte Perboewatan — supostamente extinto \\n— entrou em erupção. Esta é considerada a segunda erupção \\nvulcânica mais fatal da história, a sexta maior erupção do mun -\\ndo, além de o som mais alto já ouvido na História.\\nA caldeira de magma do vulcão era monstruosa, possuía apro -\\nximadamente 16 km de diâmetro. O vulcão não parou de cus -\\npir lava e houve ainda outras erupções durante todo o ano. \\nAntes da erupção, a ilha possuía 882 metros de altitude, mas \\napós a erupção a ilha foi riscada do mapa, tendo-se um lago \\nformado na cratera do vulcão.\\nOlha isso, que término lindo, antes de acontecer o cataclismo, \\naconteceu uma singularidade em uma menor proporção de es -\\npaço tempo perante a um novo “messias” , devido a ser uma ca -\\ntaclismo com uma menor proporção. Anteriormente, tivemos \\npessoas captando a energia proporcional a necessidade em que \\nvivia do tempo em que vivia, fosse ele religioso ou filósofo, a \\nproporção de captadores antes do tempo em que ia ocorrer o \\ncataclismo aconteceu bem antes de esse acontecer. A quantida -\\nde de novos captores antes de acontecer o cataclismo, no que \\n46.  Texto baseado em https://pt.m.wikipedia.org/wiki/Erup%C3%A7% -\\nC3%A3o_do_Krakatoa_em_1883#:~:text=A%20erup%C3%A7%C3%A3o%20\\ndo%20Krakatoa%20em,supostamente%20extinto%20%E2%80%94%20en -\\ntrou%20em%20erup%C3%A7% C3%A3o .\\ncaos do passado sendo vivido no futuro editável.indd   99caos do passado sendo vivido no futuro editável.indd   99 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 157732,
      "chapter": 11,
      "page": 99,
      "segment_type": "page",
      "themes": {},
      "difficulty": 25.50233540925267,
      "complexity_metrics": {
        "word_count": 281,
        "sentence_count": 16,
        "paragraph_count": 1,
        "avg_sentence_length": 17.5625,
        "avg_word_length": 5.320284697508897,
        "unique_word_ratio": 0.6334519572953736,
        "avg_paragraph_length": 281.0,
        "punctuation_density": 0.1494661921708185,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "erupção",
          "antes",
          "ilha",
          "vulcão",
          "krakatoa",
          "acontecer",
          "cataclismo",
          "proporção",
          "tempo",
          "supostamente",
          "mais",
          "história",
          "possuía",
          "aconteceu",
          "menor",
          "vivia",
          "passado",
          "sendo",
          "vivido",
          "futuro"
        ],
        "entities": [
          [
            "99",
            "CARDINAL"
          ],
          [
            "cataclismo46",
            "GPE"
          ],
          [
            "Krakatoa em 1883",
            "GPE"
          ],
          [
            "27",
            "CARDINAL"
          ],
          [
            "de Krakatoa",
            "PERSON"
          ],
          [
            "ilhas de Sumatra",
            "PERSON"
          ],
          [
            "Java",
            "PERSON"
          ],
          [
            "Índias Orientais Holan -\\ndesas",
            "ORG"
          ],
          [
            "Indonésia",
            "PERSON"
          ],
          [
            "quando",
            "PERSON"
          ]
        ],
        "readability_score": 89.62266459074733,
        "semantic_density": 0,
        "word_count": 281,
        "unique_words": 178,
        "lexical_diversity": 0.6334519572953736
      },
      "preservation_score": 1.2896695950305296e-05
    },
    {
      "id": 1,
      "text": "— 100 —antecedeu esse cataclismo, foi entender a energia elétrica em \\nforma física. É o marco zero para uma nova geração diante de \\nmais um cataclismo, a era da energia elétrica. Expelindo massa \\nnegra, canalizando a propagação da energia, ficando mais fácil \\ncaptar, interpretar e direcionar diante da forma a qual você \\ninterpreta seja ela para a religião, filosofia, física, propagação, \\nmatemática, sentimento, empatia, amor, caos. Todos os pensa -\\nmentos foram exaltados diante da necessidade territorial ou \\nmundial, pois a “troca” de energia era algo constante perante \\ntodos os povos, sendo assim a interpretação da energia de cada \\npara si próprio era referente aquilo que ele vivia, de acordo \\ncom o meio e a forma que ele doutrinou a ver tudo e um todo \\na sua volta. Mas, como nem tudo são flores, temos uma grande \\nmassa negra em nossa volta, canalizando a energia e última \\nvez em que aconteceu esse mesmo comportamento, sabemos \\no cataclismo que aconteceu. No decorrer das análises, iremos \\nver as consequências de acordo com os acontecimentos até o \\ndia de hoje.\\nCharles Robert Darwin47\\nDarwin nasceu em Shrewsbury, 12 de fevereiro de 1809 foi \\num naturalista, geólogo e biólogo britânico, célebre por seus \\navanços sobre evolução nas ciências biológicas. Estabeleceu a \\nideia que todos os seres vivos descendem de um ancestral em \\ncomum, evolução devido a necessidade de se adaptar ao caos \\nconsiderado um conceito fundamental no meio científico, e \\npropôs a teoria de que a seleção natural da vida e devido a mo -\\ntivação do sexo e da sobrevivência onde quem sobrevive não é \\no mais forte, e sim aquele que melhor se adapta ao caos. \\n47.  Texto baseado em https://pt.m.wikipedia.org/wiki/Charles_ Darwin .\\ncaos do passado sendo vivido no futuro editável.indd   100caos do passado sendo vivido no futuro editável.indd   100 28/03/2022   14:53:3928/03/2022   14:53:39\\n\\n30/08/2021\\n, \\né 30/08/1986, o Tesla tem estudo e muitas comprovações que",
      "position": 159646,
      "chapter": 5,
      "page": 100,
      "segment_type": "page",
      "themes": {
        "filosofia": 53.57142857142857,
        "ciencia": 46.42857142857144
      },
      "difficulty": 33.44842252396166,
      "complexity_metrics": {
        "word_count": 313,
        "sentence_count": 16,
        "paragraph_count": 2,
        "avg_sentence_length": 19.5625,
        "avg_word_length": 5.140575079872204,
        "unique_word_ratio": 0.6421725239616614,
        "avg_paragraph_length": 156.5,
        "punctuation_density": 0.15654952076677317,
        "line_break_count": 33,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "caos",
          "cataclismo",
          "forma",
          "diante",
          "mais",
          "todos",
          "sendo",
          "esse",
          "elétrica",
          "física",
          "massa",
          "negra",
          "canalizando",
          "propagação",
          "necessidade",
          "acordo",
          "meio",
          "tudo",
          "volta"
        ],
        "entities": [
          [
            "100",
            "CARDINAL"
          ],
          [
            "marco zero",
            "PERSON"
          ],
          [
            "nova",
            "LOC"
          ],
          [
            "diante de \\nmais",
            "PERSON"
          ],
          [
            "diante da forma",
            "PERSON"
          ],
          [
            "ela para",
            "PERSON"
          ],
          [
            "de acordo",
            "PERSON"
          ],
          [
            "Mas",
            "PERSON"
          ],
          [
            "nem tudo são flores",
            "PERSON"
          ],
          [
            "última \\nvez em que",
            "ORG"
          ]
        ],
        "readability_score": 88.67657747603835,
        "semantic_density": 0,
        "word_count": 313,
        "unique_words": 201,
        "lexical_diversity": 0.6421725239616614
      },
      "preservation_score": 2.6464107574679605e-05
    },
    {
      "id": 1,
      "text": "— 101 —Seu livro de 1859, A Origem das Espécies , consolidou a seleção \\nnatural como o mecanismo básico da evolução. A teoria de \\nDarwin é considerada o mecanismo unificador para explicar a \\nvida e a diversidade na Terra.\\nEm sua vida focou-se em pesquisar sobre animais invertebra -\\ndos. Pela Universidade de Cambridge (Christ’s College), ele to -\\nmou a iniciativa pelas ciências naturais e viajou durante cinco \\nanos. Intrigado com a distribuição geográfica da vida selvagem \\ne dos fósseis coletados durante sua viagem, Darwin começou \\ninvestigações detalhadas e, em 1838, concebeu a teoria da se -\\nleção natural, captando, sentindo e percebendo a necessidade \\nevolutiva de adaptação, ao caos, de cada espécie.\\nConsagrada a publicação, a teoria evolutiva darwiniana deter -\\nminou drasticamente o cenário da ciências biológicas, tornan -\\ndo-se a explicação dominante sobre o porquê da diversidade \\nnatural do planeta. Após estudar o comportamento evolutivo \\nde cada espécie perante a própria necessidade sexual, após um \\nperíodo Darwin volta a publicar livros, desta vez falando sobre \\na sexualidade humana e sua descendência. \\nCara, esse é o cara que dimensionou a energia propagada em \\naparência. Veja uma dança com uma música semelhante ao \\nque se está ouvindo, analisa a expressão corporal das pessoas \\nperante a um contexto de música. Isso se chama energia diante \\nda minha evolução, necessidade, vontade, somos uma energia \\ndê ciclos de adaptação diante da situação, evoluímos na mes -\\nma proporção que destruímos, pois se estamos vivos é pelo \\nmesmo motivo que ainda não morremos... Porém, nem tudo \\nsão flores. Temos que nos preocupar, pois não sabemos qual é \\no tamanho do próximo cataclismo que possa vir por nós mes -\\nmos não estarmos em harmonia com o mundo que queremos \\nviver. É complicado sermos egoístas com nós mesmos, porém \\ncaos do passado sendo vivido no futuro editável.indd   101caos do passado sendo vivido no futuro editável.indd   101 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 161747,
      "chapter": 5,
      "page": 101,
      "segment_type": "page",
      "themes": {
        "filosofia": 16.129032258064516,
        "ciencia": 83.87096774193549
      },
      "difficulty": 34.17310126582279,
      "complexity_metrics": {
        "word_count": 316,
        "sentence_count": 15,
        "paragraph_count": 1,
        "avg_sentence_length": 21.066666666666666,
        "avg_word_length": 5.243670886075949,
        "unique_word_ratio": 0.6613924050632911,
        "avg_paragraph_length": 316.0,
        "punctuation_density": 0.13924050632911392,
        "line_break_count": 31,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "natural",
          "teoria",
          "darwin",
          "vida",
          "necessidade",
          "energia",
          "mecanismo",
          "evolução",
          "diversidade",
          "ciências",
          "durante",
          "evolutiva",
          "adaptação",
          "caos",
          "cada",
          "espécie",
          "após",
          "perante",
          "cara",
          "música"
        ],
        "entities": [
          [
            "101",
            "CARDINAL"
          ],
          [
            "1859",
            "DATE"
          ],
          [
            "A Origem das Espécies",
            "ORG"
          ],
          [
            "básico da evolução",
            "PERSON"
          ],
          [
            "teoria de \\nDarwin",
            "PERSON"
          ],
          [
            "Pela Universidade de Cambridge",
            "PERSON"
          ],
          [
            "Christ’s College",
            "ORG"
          ],
          [
            "geográfica da vida",
            "PERSON"
          ],
          [
            "sua viagem",
            "PERSON"
          ],
          [
            "Darwin",
            "PERSON"
          ]
        ],
        "readability_score": 87.89356540084388,
        "semantic_density": 0,
        "word_count": 316,
        "unique_words": 209,
        "lexical_diversity": 0.6613924050632911
      },
      "preservation_score": 1.3108117195392265e-05
    },
    {
      "id": 1,
      "text": "— 102 —necessário para um viver melhor amanhã.\\nEsse cara nos fez enxergar o mundo dessa forma, ele captou \\numa energia e teve uma captação tão sabia, que conseguiu defi -\\nnir perfeitamente o que era para definir, só tenho uma palavra \\npara falar: Gênio!!!\\nFrases\\nUm homem que gasta uma hora não entendeu o significado \\nda vida.\\nA ignorância gera mais confiança do que o conhecimento: são \\nos que sabem pouco, e não aqueles que sabem muito, que afir -\\nmam de uma forma tão categórica que este ou aquele proble -\\nma nunca será resolvido pela ciência.\\nAs amizades de um homem são uma das melhores medidas de \\nseu valor.\\nA compaixão para com os animais é das mais nobres virtudes \\nda natureza humana.\\nPara ser um bom observador é preciso ser um bom teórico.\\nNão estou apto a seguir cegamente o exemplo de outros ho -\\nmens.\\nÉ sempre recomendável perceber claramente a nossa ignorân -\\ncia.\\n... porque o escudo pode ser tão importante para a vitória \\nquanto a espada ou a lança.\\nNão estamos preocupados com esperanças ou medos, somente \\ncom a verdade que nossa razão nos permite descobrir.\\nÉ necessário olhar para a frente da colheita, não importa o \\ncaos do passado sendo vivido no futuro editável.indd   102caos do passado sendo vivido no futuro editável.indd   102 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 163865,
      "chapter": 5,
      "page": 102,
      "segment_type": "page",
      "themes": {
        "filosofia": 53.57142857142857,
        "ciencia": 46.42857142857144
      },
      "difficulty": 24.487428571428573,
      "complexity_metrics": {
        "word_count": 225,
        "sentence_count": 14,
        "paragraph_count": 1,
        "avg_sentence_length": 16.071428571428573,
        "avg_word_length": 4.72,
        "unique_word_ratio": 0.6666666666666666,
        "avg_paragraph_length": 225.0,
        "punctuation_density": 0.13777777777777778,
        "line_break_count": 26,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "necessário",
          "forma",
          "homem",
          "mais",
          "sabem",
          "nossa",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "viver",
          "melhor",
          "amanhã",
          "esse",
          "cara",
          "enxergar",
          "mundo",
          "dessa"
        ],
        "entities": [
          [
            "102",
            "CARDINAL"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "dessa forma",
            "PERSON"
          ],
          [
            "gasta uma hora não",
            "PERSON"
          ],
          [
            "ignorância gera mais",
            "PERSON"
          ],
          [
            "sabem muito",
            "PERSON"
          ],
          [
            "categórica",
            "GPE"
          ],
          [
            "ciência.\\n",
            "PERSON"
          ],
          [
            "das",
            "ORG"
          ],
          [
            "medidas de \\nseu",
            "PERSON"
          ]
        ],
        "readability_score": 90.54828571428571,
        "semantic_density": 0,
        "word_count": 225,
        "unique_words": 150,
        "lexical_diversity": 0.6666666666666666
      },
      "preservation_score": 7.202903108480288e-06
    },
    {
      "id": 1,
      "text": "— 103 —quão distante isso seja, quando uma fruta for colhida, algo \\nbom aconteceu.\\nSem mais!!\\nThomas Alva Edison48\\nO que falar dessa fase pré-cataclismo, só tivemos gênios len -\\ndários que nos proporcionaram sabedoria diferenciada, nos \\ntornando pessoas com uma sabedoria que não existiriam sem \\neles. Se não fosse esse cara, não existia o próximo da lista, por \\nmais que tiveram desentendimentos da maluquice de um e \\nmaluquice do outro, diante do erra com acerto de um, e o erro \\ne o acerto do outro. Então, é um cara que foi fundamental ter \\nganância, para investir em tecnologia, criar e administrar. Eu \\nme pergunto, como ele arrumava tempo para ser gênio e fazer \\nisso tudo? A admiração é de gratidão por todos os erros e acer -\\ntos de cada um desses caras, pois foi necessário para interpre -\\ntar um mundo melhor diante de nossa própria energia e caos \\n(massa escura).\\nThomas Alva Edison nasceu Milan, Ohio, de fevereiro de 1847 \\nfoi um empresário dos Estados Unidos que patenteou e finan -\\nciou o desenvolvimento de muitos dispositivos importantes de \\ngrande interesse industrial. Foi um dos primeiros a aplicar os \\nprincípios da produção maciça ao processo da invenção. Vivia \\nem caos não percebendo o tamanho do próprio caos.\\nEle inventou O fonógrafo, cinematógrafo, a primeira câmera \\ncinematográfica bem-sucedida, aperfeiçoou o telefone, em um \\naparelho que funcionava muito melhor. Fez o mesmo com a \\nmáquina de escrever. Trabalhou em projetos variados, como \\n48.  Texto baseado em https://pt.m.wikipedia.org/wiki/Thomas_ Edison .\\ncaos do passado sendo vivido no futuro editável.indd   103caos do passado sendo vivido no futuro editável.indd   103 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 165284,
      "chapter": 5,
      "page": 103,
      "segment_type": "page",
      "themes": {
        "ciencia": 56.52173913043479,
        "tecnologia": 43.47826086956522
      },
      "difficulty": 26.413333333333334,
      "complexity_metrics": {
        "word_count": 270,
        "sentence_count": 20,
        "paragraph_count": 1,
        "avg_sentence_length": 13.5,
        "avg_word_length": 5.211111111111111,
        "unique_word_ratio": 0.6851851851851852,
        "avg_paragraph_length": 270.0,
        "punctuation_density": 0.16666666666666666,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "caos",
          "isso",
          "mais",
          "thomas",
          "alva",
          "sabedoria",
          "cara",
          "maluquice",
          "outro",
          "diante",
          "acerto",
          "como",
          "melhor",
          "edison",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd"
        ],
        "entities": [
          [
            "103",
            "CARDINAL"
          ],
          [
            "quando",
            "PERSON"
          ],
          [
            "colhida",
            "GPE"
          ],
          [
            "Thomas Alva Edison48\\nO",
            "PERSON"
          ],
          [
            "só tivemos",
            "PERSON"
          ],
          [
            "len -\\n",
            "PERSON"
          ],
          [
            "existiriam sem",
            "PERSON"
          ],
          [
            "não fosse",
            "ORG"
          ],
          [
            "não existia",
            "ORG"
          ],
          [
            "próximo da lista",
            "PERSON"
          ]
        ],
        "readability_score": 91.68666666666667,
        "semantic_density": 0,
        "word_count": 270,
        "unique_words": 185,
        "lexical_diversity": 0.6851851851851852
      },
      "preservation_score": 1.1227197152894378e-05
    },
    {
      "id": 1,
      "text": "— 104 —alimentos empacotados a vácuo, um aparelho de raios X e um \\nsistema de construções mais baratas feitas de concreto. Capta -\\ndor da energia em forma de propagação da mesma. \\nE um dos precursores da revolução tecnológica do século XX. \\nTeve também um papel determinante na indústria do cinema.\\nFrases\\nNossa maior fraqueza está em desistir. O caminho mais certo \\nde vencer é tentar mais uma vez.\\nMuitas das falhas da vida acontecem quando as pessoas não \\npercebem o quão perto estão quando desistem.\\nMostra-me um homem 100% satisfeito e eu mostrar-te-ei um \\nfracassado.\\nTudo alcança aquele que trabalha duro enquanto espera.\\nSe fizéssemos todas as coisas de que somos capazes, nós nos \\nsurpreenderíamos a nós mesmos.\\nPreciso falar mais o quê? Ele pensava em otimizar o tempo, \\nem fazer sempre algo enquanto estivesse com tempo obsoleto, \\ncom aproveitando para fazer algo que o agregava algo na vida. \\nDeterminação é o que descreve, mais a genialidade interpreta -\\ntiva da captação e adaptação da energia em seu envolto, o fez \\nser o que tinha que ser.\\nNikola Tesla49\\nAí... O que falar desse “anjo”? Esse cara é foda pacaralho! Ele é o \\nmotivo de eu estar escrevendo este livro. Ele me fez pensar que \\n49.  Texto baseado em https://pt.m.wikipedia.org/wiki/Nikola _Tesla .\\ncaos do passado sendo vivido no futuro editável.indd   104caos do passado sendo vivido no futuro editável.indd   104 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 167103,
      "chapter": 5,
      "page": 104,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 23.25931330472103,
      "complexity_metrics": {
        "word_count": 233,
        "sentence_count": 25,
        "paragraph_count": 1,
        "avg_sentence_length": 9.32,
        "avg_word_length": 5.064377682403434,
        "unique_word_ratio": 0.6866952789699571,
        "avg_paragraph_length": 233.0,
        "punctuation_density": 0.15879828326180256,
        "line_break_count": 25,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "algo",
          "energia",
          "vida",
          "quando",
          "enquanto",
          "falar",
          "tempo",
          "fazer",
          "nikola",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "alimentos",
          "empacotados",
          "vácuo",
          "aparelho"
        ],
        "entities": [
          [
            "104",
            "CARDINAL"
          ],
          [
            "XX",
            "GPE"
          ],
          [
            "Teve",
            "PERSON"
          ],
          [
            "Nossa",
            "PERSON"
          ],
          [
            "tentar mais uma vez",
            "PERSON"
          ],
          [
            "100%",
            "PERCENT"
          ],
          [
            "eu mostrar-te",
            "PERSON"
          ],
          [
            "Tudo alcança",
            "PERSON"
          ],
          [
            "coisas de que",
            "ORG"
          ],
          [
            "quê",
            "PERSON"
          ]
        ],
        "readability_score": 93.82068669527897,
        "semantic_density": 0,
        "word_count": 233,
        "unique_words": 160,
        "lexical_diversity": 0.6866952789699571
      },
      "preservation_score": 8.383945925862683e-06
    },
    {
      "id": 1,
      "text": "— 105 —o básico é grande. Parei para beber uma cerveja, estava emocio -\\nnado. Me fez dimensionar pequenos ciclos em grandes ciclos \\nde comportamento diante da propagação da energia emitida \\npor cada um de nós, na proporção per capita  de uma rede de \\nproporção perpendiculares de ganho e desgaste físico perante \\na energia do mundo, aumentando a massa escura, diminuin -\\ndo a quantidade da propagação da energia, canalizando menos \\nas frequências existentes proporcional ao desgaste, junto com \\nalguns corpos (semelhante a uma antena) conseguem captar \\numa frequência exclusiva, interpretativa de si, perante a um \\nretorno de energia na mesma proporção emitida, com uma \\nbalança de dois mundos diferentes (físico proporcional à ener -\\ngia), em uma balança constante de certo ou errado, bom ou \\nruim, de quantidade de energia (pessoas) em sua volta, crian -\\ndo um conjunto de energias diferentes, com uma oscilação \\ncomum perante a um lado balancear ao outro, diante de um \\ncontexto de todas as energias em concordância. Sequência in -\\nfinita de dois polos, com o ciclo infinito de dois polos relativo \\na um ao outro, sequência de movimento infinito entre os dois \\npolos. Preciso falar mais alguma coisa sobre esse cara? Ele é um \\nmonstro!!! \\nNikola Tesla nasceu em Smiljan, Império Austríaco, 10 de \\njulho de 1856 foi um inventor, engenheiro eletrotécnico e \\nengenheiro mecânico sérvio, mais conhecido por suas contri -\\nbuições ao projeto do moderno sistema de fornecimento de \\neletricidade em corrente alternada. Duas energias em movi -\\nmentos de concordância uma para com a outra.\\nNascido e criado no Império Austríaco, Tesla estudou enge -\\nnharia e física na década de 1870 sem se formar, e ganhou \\nexperiência prática no início da década de 1880 trabalhando \\nem telefonia e na Continental Edison. Quando trabalhou com \\nEdison, tesla era um inventor sem valor, e a ganância de Edi -\\ncaos do passado sendo vivido no futuro editável.indd   105caos do passado sendo vivido no futuro editável.indd   105 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 168653,
      "chapter": 5,
      "page": 105,
      "segment_type": "page",
      "themes": {},
      "difficulty": 33.32905268490374,
      "complexity_metrics": {
        "word_count": 329,
        "sentence_count": 12,
        "paragraph_count": 1,
        "avg_sentence_length": 27.416666666666668,
        "avg_word_length": 5.124620060790273,
        "unique_word_ratio": 0.60790273556231,
        "avg_paragraph_length": 329.0,
        "punctuation_density": 0.1276595744680851,
        "line_break_count": 32,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "dois",
          "proporção",
          "perante",
          "energias",
          "polos",
          "tesla",
          "ciclos",
          "diante",
          "propagação",
          "emitida",
          "desgaste",
          "físico",
          "quantidade",
          "proporcional",
          "balança",
          "diferentes",
          "outro",
          "concordância",
          "sequência"
        ],
        "entities": [
          [
            "105",
            "CARDINAL"
          ],
          [
            "interpretativa de si",
            "ORG"
          ],
          [
            "balança constante de certo",
            "PERSON"
          ],
          [
            "Sequência",
            "PERSON"
          ],
          [
            "infinito de dois",
            "ORG"
          ],
          [
            "sequência de",
            "PERSON"
          ],
          [
            "Ele",
            "PERSON"
          ],
          [
            "Nikola Tesla",
            "ORG"
          ],
          [
            "Smiljan",
            "GPE"
          ],
          [
            "Império Austríaco",
            "PERSON"
          ]
        ],
        "readability_score": 84.75428064842959,
        "semantic_density": 0,
        "word_count": 329,
        "unique_words": 200,
        "lexical_diversity": 0.60790273556231
      },
      "preservation_score": 1.376425209393804e-05
    },
    {
      "id": 1,
      "text": "— 106 —son, fez enxergar a inteligência de tesla e a importância de usar \\naquela pessoa a seu favor. Emigrou para os Estados Unidos e \\nse naturalizou cidadão americano. Ele trabalhou por um cur -\\nto período na Edison Machine Works, em Nova Iorque, antes \\nde começar por conta própria. Conflitos financeiros o fez ter \\nproblemas a vida toda, desde perder o dinheiro de sua família \\na viver endividado pela sua ganância mental. Com a ajuda de \\nparceiros para financiar e comercializar suas ideias, Tesla mon -\\ntou laboratórios e empresas em Nova Iorque para desenvolver \\numa variedade de dispositivos elétricos e mecânicos ganhando \\nbastante dinheiro.\\nTentando desenvolver invenções que pudesse patentear e co -\\nmercializar, Tesla conduziu uma série de experimentos com \\nosciladores/geradores mecânicos, tubos de descarga elétrica e \\nradiografia. Tesla seguiu suas ideias para iluminação sem fio \\ne distribuição mundial de energia elétrica sem fio em seus \\nexperimentos de alta tensão e alta frequência. Sempre muito \\npolêmico, levantou a possibilidade de comunicação sem fio \\ncom seus dispositivos. Tesla tentou colocar essas ideias em uso \\nprático em seu projeto inacabado da Wardenclyffe Tower, uma \\ntransmissora sem fio intercontinental de comunicações e ener -\\ngia, mas ficou sem dinheiro antes que pudesse concluí-lo.\\nTesla morava em uma série de hotéis de Nova Iorque, deixando \\npara trás contas não pagas. \\nTesla era viciado em jogos de azar, teve uma vez que a mãe \\ndele deu todo o dinheiro para ele e falou: Meu filho, jogue \\ntodo nosso dinheiro. ” Ele foi e jogou todo o seu dinheiro, ele \\nali percebeu o vício dele, pois ele percebeu que a sabedoria de \\nsua mãe, sabia que tinha que fazer aquilo pois era necessário \\nele passar por aquilo ali. Tesla era bom com números, por isso \\ndo vício em jogos, e quando foi trabalhar com energia elétrica, \\ncaos do passado sendo vivido no futuro editável.indd   106caos do passado sendo vivido no futuro editável.indd   106 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 170814,
      "chapter": 5,
      "page": 106,
      "segment_type": "page",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 27.37512899896801,
      "complexity_metrics": {
        "word_count": 323,
        "sentence_count": 15,
        "paragraph_count": 1,
        "avg_sentence_length": 21.533333333333335,
        "avg_word_length": 5.139318885448916,
        "unique_word_ratio": 0.6099071207430341,
        "avg_paragraph_length": 323.0,
        "punctuation_density": 0.11764705882352941,
        "line_break_count": 31,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "tesla",
          "dinheiro",
          "nova",
          "iorque",
          "ideias",
          "elétrica",
          "todo",
          "antes",
          "suas",
          "desenvolver",
          "dispositivos",
          "mecânicos",
          "pudesse",
          "série",
          "experimentos",
          "energia",
          "seus",
          "alta",
          "jogos",
          "dele"
        ],
        "entities": [
          [
            "106",
            "CARDINAL"
          ],
          [
            "aquela pessoa",
            "PERSON"
          ],
          [
            "Estados Unidos",
            "ORG"
          ],
          [
            "Ele trabalhou",
            "PERSON"
          ],
          [
            "Edison Machine Works",
            "ORG"
          ],
          [
            "Nova Iorque",
            "NORP"
          ],
          [
            "conta própria",
            "PERSON"
          ],
          [
            "Conflitos",
            "PERSON"
          ],
          [
            "financeiros",
            "CARDINAL"
          ],
          [
            "dinheiro de sua",
            "ORG"
          ]
        ],
        "readability_score": 87.69153766769865,
        "semantic_density": 0,
        "word_count": 323,
        "unique_words": 197,
        "lexical_diversity": 0.6099071207430341
      },
      "preservation_score": 1.0396092948069726e-05
    },
    {
      "id": 1,
      "text": "— 107 —a visão do cara mudou, tudo foi uma consequência necessária \\nde um loop para o Tesla ser o que deveria ser. Ele conseguiu in -\\nterpretar a propagação da energia (quântica) perante o mundo \\nfísico. Gênio!!! Viveu uma vida do jeito dele, do jeito que que -\\nria viver, sem arrependimentos perante a gastar tudo em suas \\nloucuras ao ponto de não perceber que prejudicava os outros. \\nIsso chega a ser prepotência pelo poder de si próprio. Pessoas \\nque pensam em outras pessoas, não pensariam em dar calote \\nno seu semelhante. Então temos uma falha comportamental \\nruim perante a uma genialidade.\\nFrases \\nDeixem que o futuro diga a verdade e avalie cada um de acor -\\ndo com o seu trabalho e realizações. O presente pertence a eles, \\nmas o futuro pelo qual eu sempre trabalhei pertence a mim.\\nSe você quiser descobrir os segredos do Universo, pense em \\ntermos de energia, frequência e vibração.\\nNossas virtudes e nossos defeitos são inseparáveis, assim como \\na força e a matéria. Quando se separam, o homem deixa de \\nexistir.\\nA ciência é, portanto, uma perversão de si mesma, a menos que \\ntenha como fim último, melhorar a humanidade.\\nA maioria das pessoas está tão absorta na contemplação do \\nmundo exterior que está totalmente alheia ao que está aconte -\\ncendo em si.\\nO dom de poder mental vem de Deus, o Ser Divino e se con -\\ncentrarmos nossas mentes na verdade, ficamos em sintonia \\ncom este grande poder.\\nMeu cérebro é apenas um receptor, no Universo existe um nú -\\ncaos do passado sendo vivido no futuro editável.indd   107caos do passado sendo vivido no futuro editável.indd   107 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 172945,
      "chapter": 5,
      "page": 107,
      "segment_type": "page",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 24.277837089758798,
      "complexity_metrics": {
        "word_count": 281,
        "sentence_count": 18,
        "paragraph_count": 1,
        "avg_sentence_length": 15.61111111111111,
        "avg_word_length": 4.722419928825623,
        "unique_word_ratio": 0.6619217081850534,
        "avg_paragraph_length": 281.0,
        "punctuation_density": 0.1387900355871886,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "futuro",
          "perante",
          "poder",
          "pessoas",
          "está",
          "tudo",
          "energia",
          "mundo",
          "jeito",
          "pelo",
          "verdade",
          "pertence",
          "universo",
          "nossas",
          "como",
          "passado",
          "sendo",
          "vivido",
          "editável",
          "indd"
        ],
        "entities": [
          [
            "107",
            "CARDINAL"
          ],
          [
            "Tesla",
            "ORG"
          ],
          [
            "ser o que deveria ser",
            "ORG"
          ],
          [
            "Ele",
            "PERSON"
          ],
          [
            "Gênio",
            "PERSON"
          ],
          [
            "Viveu",
            "PERSON"
          ],
          [
            "jeito dele",
            "PERSON"
          ],
          [
            "ponto de não perceber que",
            "ORG"
          ],
          [
            "prepotência pelo",
            "PERSON"
          ],
          [
            "de si próprio",
            "PERSON"
          ]
        ],
        "readability_score": 90.77771846579675,
        "semantic_density": 0,
        "word_count": 281,
        "unique_words": 186,
        "lexical_diversity": 0.6619217081850534
      },
      "preservation_score": 1.0002412008942265e-05
    },
    {
      "id": 1,
      "text": "— 108 —cleo a partir do qual obtemos conhecimento, força e inspira -\\nção. Eu não penetrei nos segredos deste núcleo, mas eu sei que \\nele existe.\\nMinha mãe compreendeu bem a natureza humana e nunca \\nrepreendeu ninguém. Ela sabia que o homem não pode ser \\nsalvo de sua própria tolice pelos esforços ou protestos de outra \\npessoa, mas somente com o uso de sua própria vontade.\\n(Quando...) a distância, que é o principal impedimento para \\no progresso da humanidade, for completamente superada, em \\natos e palavras. A humanidade estará unida, as guerras serão \\nimpossíveis, e a paz reinará em todo o planeta.\\nEsteja sozinho, este é o segredo da invenção, estar sozinho, isto \\né quando as ideias nascem.\\nO dinheiro não representa tal valor como os homens coloca -\\nram em cima dele. Todo o meu dinheiro foi investido nas ex -\\nperiências com as quais eu fiz descobertas novas permitindo a \\nhumanidade de ter uma vida um pouco mais fácil.\\nOs cientistas de hoje pensam profundamente ao invés de clara -\\nmente. Você tem que ser são para pensar claramente, mas pode \\npensar profundamente e ser insano.\\nEm todo o espaço, há energia, é (só) uma questão de tempo até \\nque os homens tenham êxito em associar seus mecanismos ao \\naproveitamento desta energia.\\nSem mais!!\\nAlbert Einstein50\\nAgora, vem com menos impacto, pois estou ficando sem pala -\\n50.  Texto baseado em https://pt.m.wikipedia.org/wiki/Albert_Ei nstein .\\ncaos do passado sendo vivido no futuro editável.indd   108caos do passado sendo vivido no futuro editável.indd   108 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 174691,
      "chapter": 5,
      "page": 108,
      "segment_type": "page",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 22.455712769720552,
      "complexity_metrics": {
        "word_count": 257,
        "sentence_count": 22,
        "paragraph_count": 1,
        "avg_sentence_length": 11.681818181818182,
        "avg_word_length": 5.003891050583658,
        "unique_word_ratio": 0.7237354085603113,
        "avg_paragraph_length": 257.0,
        "punctuation_density": 0.17509727626459143,
        "line_break_count": 27,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "humanidade",
          "todo",
          "pode",
          "própria",
          "quando",
          "sozinho",
          "dinheiro",
          "homens",
          "mais",
          "profundamente",
          "pensar",
          "energia",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "cleo",
          "partir"
        ],
        "entities": [
          [
            "108",
            "CARDINAL"
          ],
          [
            "Eu",
            "PERSON"
          ],
          [
            "núcleo",
            "NORP"
          ],
          [
            "mas eu",
            "PERSON"
          ],
          [
            "pelos esforços",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "Esteja",
            "PERSON"
          ],
          [
            "segredo da invenção",
            "PERSON"
          ],
          [
            "estar",
            "PERSON"
          ],
          [
            "quando",
            "PERSON"
          ]
        ],
        "readability_score": 92.65792359391581,
        "semantic_density": 0,
        "word_count": 257,
        "unique_words": 186,
        "lexical_diversity": 0.7237354085603113
      },
      "preservation_score": 1.1023066295569023e-05
    },
    {
      "id": 1,
      "text": "— 109 —vras para descrever esses caras. Quero pular essa parte igual o \\nfilme Click. kkkkkk\\nAlbert Einstein nasceu 14 de março de 1879 em Princeton, \\nfoi um físico teórico alemão que desenvolveu a teoria da re -\\nlatividade geral, um dos pilares da física moderna ao lado da \\nmecânica quântica. Embora mais conhecido por sua fórmula \\nde equivalência massa-energia, E = mc² a equação mais famosa \\ndo mundo.\\nNascido em uma família de judeus (captação da energia de \\nDeus, símbolo estrela de Davi) alemães, mudou-se para a Suí -\\nça ainda jovem e iniciou seus estudos na Escola Politécnica \\nde Zurique. Obteve um cargo no escritório de patentes suíço \\nenquanto ingressava no curso de doutorado da Universidade \\nde Zurique. Em 1905 publicou uma série de artigos acadêmi -\\ncos revolucionários. A sua forma de interpretar a captação da \\nenergia era “pura” , Einstein tinha uma vida com muita satisfa -\\nção, trabalhava com o que gostava e vivia uma rotina padrão \\nconfortável de se viver, com sua família e amigos. Percebeu, no \\nentanto, que o princípio da relatividade também poderia ser \\nestendido para campos gravitacionais, e com a sua posterior \\nteoria da gravitação. Transformou a sua “pequena” forma de \\npensar, em tamanho quântico. publicou um artigo sobre a teo -\\nria da relatividade geral. Enquanto acumulava cargos em uni -\\nversidades e instituições, continuou a lidar com problemas da \\nmecânica estatística e teoria quântica, o que levou às suas expli -\\ncações sobre a teoria das partículas e o movimento browniano. \\nRealizou diversas viagens ao redor do mundo, deu palestras \\npúblicas em conceituadas universidades e conheceu persona -\\nlidades célebres de sua época, tanto na ciência quanto fora do \\nmundo acadêmico. Publicou mais de 300 trabalhos científicos, \\njuntamente com mais de 150 obras não científicas. Suas gran -\\ncaos do passado sendo vivido no futuro editável.indd   109caos do passado sendo vivido no futuro editável.indd   109 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 176370,
      "chapter": 5,
      "page": 109,
      "segment_type": "page",
      "themes": {
        "ciencia": 86.66666666666667,
        "arte": 13.333333333333334
      },
      "difficulty": 39.98443665867601,
      "complexity_metrics": {
        "word_count": 319,
        "sentence_count": 17,
        "paragraph_count": 1,
        "avg_sentence_length": 18.764705882352942,
        "avg_word_length": 5.144200626959248,
        "unique_word_ratio": 0.6614420062695925,
        "avg_paragraph_length": 319.0,
        "punctuation_density": 0.11598746081504702,
        "line_break_count": 31,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "teoria",
          "mais",
          "energia",
          "mundo",
          "publicou",
          "einstein",
          "geral",
          "mecânica",
          "quântica",
          "família",
          "captação",
          "zurique",
          "enquanto",
          "forma",
          "relatividade",
          "suas",
          "passado",
          "sendo",
          "vivido",
          "futuro"
        ],
        "entities": [
          [
            "109",
            "CARDINAL"
          ],
          [
            "Quero",
            "ORG"
          ],
          [
            "pular essa parte",
            "ORG"
          ],
          [
            "Albert Einstein",
            "PERSON"
          ],
          [
            "14",
            "CARDINAL"
          ],
          [
            "de março de 1879",
            "ORG"
          ],
          [
            "Princeton",
            "GPE"
          ],
          [
            "teórico alemão",
            "PERSON"
          ],
          [
            "teoria da re -\\n",
            "PERSON"
          ],
          [
            "lado da \\nmecânica quântica",
            "PERSON"
          ]
        ],
        "readability_score": 89.07438687073575,
        "semantic_density": 0,
        "word_count": 319,
        "unique_words": 211,
        "lexical_diversity": 0.6614420062695925
      },
      "preservation_score": 1.2656113154171841e-05
    },
    {
      "id": 1,
      "text": "— 110 —des conquistas intelectuais e originalidade fizeram da palavra \\n“Einstein” sinônimo de gênio. \\nAlbert Einstein!! Simplesmente não saberíamos que matéria \\ne energia são as mesmas coisas em tamanho, dimensão e pro -\\nporção diferente relativamente, que simplesmente temos parte \\ndo corpo que tem mais energia, do que o outra parte do cor -\\npo, temos átomos diferentes perante uma necessidade mate -\\nrial. Ele mostrou que tempo é relativo a velocidade da energia, \\nmostrando que a energia é onipresente ela sempre está, pois há \\nenergia em tudo e se há energia em tudo, tudo que há energia \\nserá tudo. Assim que pensamos em mundo quântico, pois se a \\num mundo quântico proporcional ao nosso tamanho peran -\\nte ao universo, nós nos movimentamos em Concordância de \\nenergia em via contínua e intermitente com oscilações, vibra -\\nções em frequências receptivas e propagada em proporção de \\ncausa e efeito em escala quântica.\\nEsse é o cara que fez a tecnologia fazer sentido, antes mesmo \\nde fazer sentido.\\nFrases\\nA imaginação é mais importante que o conhecimento.\\nViver é como andar de bicicleta: É preciso estar em constante \\nmovimento para manter o equilíbrio.\\nImaginação é tudo, é a prévia das atrações futuras.\\nSó duas coisas são infinitas, o universo e a estupidez humana, \\nmas não estou seguro sobre o primeiro.\\nEle esqueceu de falar os números.\\nSe você não consegue explicar algo de forma simples, você não \\nentendeu suficientemente bem.\\ncaos do passado sendo vivido no futuro editável.indd   110caos do passado sendo vivido no futuro editável.indd   110 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 178473,
      "chapter": 5,
      "page": 110,
      "segment_type": "page",
      "themes": {
        "ciencia": 30.232558139534888,
        "arte": 46.51162790697674,
        "tecnologia": 23.25581395348837
      },
      "difficulty": 28.23359073359073,
      "complexity_metrics": {
        "word_count": 259,
        "sentence_count": 15,
        "paragraph_count": 1,
        "avg_sentence_length": 17.266666666666666,
        "avg_word_length": 5.111969111969112,
        "unique_word_ratio": 0.6602316602316602,
        "avg_paragraph_length": 259.0,
        "punctuation_density": 0.13513513513513514,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "tudo",
          "einstein",
          "simplesmente",
          "coisas",
          "tamanho",
          "temos",
          "parte",
          "mais",
          "pois",
          "mundo",
          "quântico",
          "universo",
          "fazer",
          "sentido",
          "imaginação",
          "você",
          "passado",
          "sendo",
          "vivido"
        ],
        "entities": [
          [
            "110",
            "CARDINAL"
          ],
          [
            "Albert Einstein",
            "PERSON"
          ],
          [
            "Simplesmente",
            "PERSON"
          ],
          [
            "mesmas coisas",
            "PERSON"
          ],
          [
            "outra",
            "NORP"
          ],
          [
            "cor -\\npo",
            "ORG"
          ],
          [
            "temos átomos",
            "PERSON"
          ],
          [
            "ela sempre está",
            "PERSON"
          ],
          [
            "Concordância de \\nenergia",
            "PERSON"
          ],
          [
            "propagada",
            "GPE"
          ]
        ],
        "readability_score": 89.83307593307593,
        "semantic_density": 0,
        "word_count": 259,
        "unique_words": 171,
        "lexical_diversity": 0.6602316602316602
      },
      "preservation_score": 8.981757722315501e-06
    },
    {
      "id": 1,
      "text": "— 111 —Coincidência é a maneira que Deus encontrou para permane -\\ncer no anonimato.\\nDeus não joga dados com o Universo.\\nEssa última frase, resumiu todo o meu livro!!! Deus e o Univer -\\nso são uma única coisa.\\nKarl Marx51\\nKarl Marx nasceu em Tréveris, 5 de maio de 1818 foi um fi -\\nlósofo, sociólogo, historiador, economista, jornalista e revolu -\\ncionário socialista. Nascido na Prússia, mais tarde se tornou \\napátrida e passou grande parte de sua vida em Londres, no Rei -\\nno Unido. Viveu uma vida de extremos, sem saber direcionar \\num viver para si, A obra de Marx em economia estabeleceu a \\nbase para muito do entendimento atual sobre o trabalho e sua \\nrelação com o capital, por ter vivido uma vida de “caprichos” \\ne não ser feliz com os mesmos, se tornou um pensador contra \\no capitalismo.\\nMarx nasceu numa família de classe média em Tréveris, todo o \\ncaos vivido em um viver “bem” , direcionou os seus pensamen -\\ntos em interpretar o desnecessário, onde todos acham neces -\\nsário ter. Iniciou o seu trabalho na teoria da concepção mate -\\nrialista da história. Devido a ter sido criado com o clero, “ não \\ntinha respeito” pelo poder de quem possuía, sendo interpreta -\\ndo de uma forma extremista contra o sistema em que vivemos. \\nAtravés desse pensamento, ele criou muitos inimigos devido \\nao seu pensamento contraditório perante a uma “ totalidade” . \\nMudou-se para Paris, onde começou a escrever para outros jor -\\nnais radicais e conheceu Friedrich Engels, que se tornaria seu \\n51.  Texto baseado em https://pt.m.wikipedia.org/wiki/Kar l_Marx .\\ncaos do passado sendo vivido no futuro editável.indd   111caos do passado sendo vivido no futuro editável.indd   111 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 180193,
      "chapter": 5,
      "page": 111,
      "segment_type": "page",
      "themes": {
        "ciencia": 39.3939393939394,
        "historia": 30.303030303030305,
        "arte": 30.303030303030305
      },
      "difficulty": 28.1395738481151,
      "complexity_metrics": {
        "word_count": 289,
        "sentence_count": 19,
        "paragraph_count": 1,
        "avg_sentence_length": 15.210526315789474,
        "avg_word_length": 4.85121107266436,
        "unique_word_ratio": 0.6401384083044983,
        "avg_paragraph_length": 289.0,
        "punctuation_density": 0.15570934256055363,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "vivido",
          "deus",
          "marx",
          "vida",
          "sendo",
          "todo",
          "karl",
          "nasceu",
          "tréveris",
          "tornou",
          "viver",
          "trabalho",
          "contra",
          "caos",
          "onde",
          "devido",
          "pensamento",
          "passado",
          "futuro",
          "editável"
        ],
        "entities": [
          [
            "111",
            "CARDINAL"
          ],
          [
            "Coincidência",
            "PRODUCT"
          ],
          [
            "Deus",
            "LOC"
          ],
          [
            "Deus",
            "PERSON"
          ],
          [
            "Universo",
            "GPE"
          ],
          [
            "Essa última",
            "GPE"
          ],
          [
            "Deus",
            "PERSON"
          ],
          [
            "Karl Marx51",
            "PERSON"
          ],
          [
            "Karl Marx",
            "PERSON"
          ],
          [
            "Tréveris",
            "ORG"
          ]
        ],
        "readability_score": 90.93937352030595,
        "semantic_density": 0,
        "word_count": 289,
        "unique_words": 185,
        "lexical_diversity": 0.6401384083044983
      },
      "preservation_score": 1.3472636583473252e-05
    },
    {
      "id": 1,
      "text": "— 112 —amigo de longa data e colaborador. Em 1849, foi exilado e se \\nmudou para Londres juntamente a sua esposa e filhos.\\nAs teorias de Marx sobre a sociedade, a economia e a política \\n— a compreensão coletiva do que é conhecido como o marxis -\\nmo, é devido a sua própria interpretação de viver um melhor \\ndentro de um sistema de direção, sustento de um padrão social \\nquântico. sustentam que as sociedades humanas progridem \\natravés da luta de classes, fazendo um sistema de necessida -\\nde perante a minha própria ganância, em um conflito entre \\numa classe social que controla os meios de produção e a classe \\ntrabalhadora, que fornece a mão de obra para a produção. E \\nque o sistema foi criado para proteger os interesses da classe \\ndominante, embora seja apresentado como um instrumento \\nque representa o interesse comum de todos. Ele argumentava \\nque os antagonismos no sistema capitalista, entre a burguesia \\ne o proletariado, seriam consequência de uma guerra perpétua \\n(ação e reação) entre a primeira e as demais classes ao longo \\nda história. \\nKarl Marx é um dos maiores revolucionários filosófico de toda \\na nossa história. Seus pensamentos até hoje convergem com o \\nnosso viver atual, a sua captação de energia foi atemporal.\\nKarl Marx, captação de energia extrema. Ele nasceu em uma \\nfamília judaica, deve ter sofrido consequências absurdas diante \\nde enxergar o erro e lutar contra ele, generalizando tudo e a to -\\ndos diante de uma certeza dos erros dos outros, pois ele captou \\na energia boa da dor. O caos gerado pelo meio em que ele viveu, \\nse propagou em forma de luta, do extremista contra a ganância \\ndo ser humano, brigando com um sistema enraizado com um \\npensamento de sistema de oportunidades iguais para todos, \\nfazendo com que sua família, sua vida tivesse a carga e o peso \\ndessa captação diante da energia, propagando para si próprio \\ncaos do passado sendo vivido no futuro editável.indd   112caos do passado sendo vivido no futuro editável.indd   112 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 182020,
      "chapter": 5,
      "page": 112,
      "segment_type": "page",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 42.965384615384615,
      "complexity_metrics": {
        "word_count": 338,
        "sentence_count": 13,
        "paragraph_count": 1,
        "avg_sentence_length": 26.0,
        "avg_word_length": 4.884615384615385,
        "unique_word_ratio": 0.5769230769230769,
        "avg_paragraph_length": 338.0,
        "punctuation_density": 0.10946745562130178,
        "line_break_count": 31,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "sistema",
          "energia",
          "marx",
          "entre",
          "classe",
          "captação",
          "diante",
          "como",
          "própria",
          "viver",
          "social",
          "luta",
          "classes",
          "fazendo",
          "ganância",
          "produção",
          "todos",
          "história",
          "karl",
          "família"
        ],
        "entities": [
          [
            "112",
            "CARDINAL"
          ],
          [
            "1849",
            "DATE"
          ],
          [
            "Londres juntamente",
            "PERSON"
          ],
          [
            "sistema de direção",
            "ORG"
          ],
          [
            "sustentam que",
            "PERSON"
          ],
          [
            "da luta de",
            "PERSON"
          ],
          [
            "Ele argumentava \\nque",
            "PERSON"
          ],
          [
            "burguesia",
            "GPE"
          ],
          [
            "seriam consequência de uma",
            "PERSON"
          ],
          [
            "Karl Marx",
            "PERSON"
          ]
        ],
        "readability_score": 85.53461538461539,
        "semantic_density": 0,
        "word_count": 338,
        "unique_words": 195,
        "lexical_diversity": 0.5769230769230769
      },
      "preservation_score": 1.0170090927459515e-05
    },
    {
      "id": 1,
      "text": "— 113 —(família em sua volta) uma massa escura. Como assim? Buraco \\nnegro, canalização da energia (vórtice) “ele está absorvendo a \\nenergia para dentro de si mesmo” , vai concentrando a energia \\npara dentro de si próprio, quando a massa escura não consegue \\nmais conter a energia, expelindo uma energia concentrada de \\nsi próprio, com valores energéticos de várias informações em \\nconjunto, diante daquele padrão que ele mesmo enxerga.\\nCanalizou tanto a energia, que, em seu entorno, era um caos. \\nNão conseguia administrar as suas “loucuras” perante sua famí -\\nlia, o fazendo perder todo o sentimento bom em seu entorno. \\nMuitos filhos morreram e os que sobreviveram não viveram. \\nEsse é o preço de ser um captador de energia em excesso para \\nalgum lado da balança, seja ela sentimental, espiritual, filosófi -\\nco, matemática, científico, material, amor e caos.\\nFrases\\nDe cada um, de acordo com suas habilidades, a cada um, de \\nacordo com suas necessidades.\\nA religião é o ópio do povo.\\nÚltimas palavras são para tolos que não disseram o suficiente.\\nUm espectro assombra a Europa: o espectro do comunismo\\nOs filósofos se limitaram a interpretar o mundo diferentemen -\\nte, cabe transformá-lo.\\nOs homens fazem sua própria história, mas não a fazem como \\nquerem.\\nA história de toda sociedade existente até hoje tem sido a his -\\ntória das lutas de classes.\\nTrabalhadores do mundo, uni-vos, vós não tendes nada a per -\\ncaos do passado sendo vivido no futuro editável.indd   113caos do passado sendo vivido no futuro editável.indd   113 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 184158,
      "chapter": 5,
      "page": 113,
      "segment_type": "page",
      "themes": {},
      "difficulty": 24.608925097276263,
      "complexity_metrics": {
        "word_count": 257,
        "sentence_count": 16,
        "paragraph_count": 1,
        "avg_sentence_length": 16.0625,
        "avg_word_length": 5.0505836575875485,
        "unique_word_ratio": 0.6770428015564203,
        "avg_paragraph_length": 257.0,
        "punctuation_density": 0.17120622568093385,
        "line_break_count": 27,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "caos",
          "suas",
          "massa",
          "escura",
          "como",
          "dentro",
          "mesmo",
          "próprio",
          "entorno",
          "cada",
          "acordo",
          "espectro",
          "mundo",
          "fazem",
          "história",
          "passado",
          "sendo",
          "vivido",
          "futuro"
        ],
        "entities": [
          [
            "113",
            "CARDINAL"
          ],
          [
            "família em sua volta",
            "ORG"
          ],
          [
            "Buraco",
            "NORP"
          ],
          [
            "para dentro de si mesmo",
            "PERSON"
          ],
          [
            "para dentro de si próprio",
            "PERSON"
          ],
          [
            "quando",
            "PERSON"
          ],
          [
            "massa escura",
            "ORG"
          ],
          [
            "concentrada de \\nsi próprio",
            "PERSON"
          ],
          [
            "energéticos de várias",
            "PERSON"
          ],
          [
            "Canalizou",
            "ORG"
          ]
        ],
        "readability_score": 90.45357490272373,
        "semantic_density": 0,
        "word_count": 257,
        "unique_words": 174,
        "lexical_diversity": 0.6770428015564203
      },
      "preservation_score": 1.2007268643387689e-05
    },
    {
      "id": 1,
      "text": "— 114 —der a não ser vossos grilhões.\\nOs ricos farão de tudo pelos pobres, menos descer de suas cos -\\ntas.\\nA produção de um número excessivo de coisas úteis resulta \\nnum número excessivo de pessoas inúteis.\\nSigmund Freud52\\nFrei nasceu em Freiberg in Mähren, 6 de maio de 1856 foi um \\nmédico neurologista e psiquiatra criador da psicanálise. Freud \\nnasceu em uma família judaica, mais um com uma origem \\ncom direcionamento religioso de doutrina e captação da ener -\\ngia do judaísmo.\\nFreud iniciou seus estudos pela utilização da técnica da hip -\\nnose no tratamento de pacientes com histeria, como forma de \\nacesso aos seus conteúdos mentais. Por ele observar os efeitos \\nde pessoas em agir por impulso, e esses impulsos comporta -\\nmentais são involuntários, por muitas vezes causando histeria \\npela falta de controle de conter o próprio caos. \\nFreud acreditava que o desejo sexual era a energia motivacio -\\nnal primária da vida humana.  \\nDe acordo com os seus estudos, nossos desejos em fazer sexo, é \\na causa dos nossos impulsos motivacionais, nos transformando \\nem animais racionais imperfeitos vivendo uma vida contradi -\\ntório por não controlar os nossos próprios impulsos carnais. \\nGerando caos devido a ser contraditório para viver em socie -\\ndade, causando um tormento coletivo devido ao seu próprio \\nimpulso.\\n52.  Texto baseado em https://pt.m.wikipedia.org/wiki/Sigmund _Freud .\\ncaos do passado sendo vivido no futuro editável.indd   114caos do passado sendo vivido no futuro editável.indd   114 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 185848,
      "chapter": 5,
      "page": 114,
      "segment_type": "page",
      "themes": {},
      "difficulty": 25.48278911564626,
      "complexity_metrics": {
        "word_count": 245,
        "sentence_count": 18,
        "paragraph_count": 1,
        "avg_sentence_length": 13.61111111111111,
        "avg_word_length": 5.220408163265306,
        "unique_word_ratio": 0.689795918367347,
        "avg_paragraph_length": 245.0,
        "punctuation_density": 0.1306122448979592,
        "line_break_count": 27,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "freud",
          "seus",
          "impulsos",
          "caos",
          "nossos",
          "número",
          "excessivo",
          "pessoas",
          "sigmund",
          "nasceu",
          "estudos",
          "pela",
          "histeria",
          "mentais",
          "impulso",
          "causando",
          "próprio",
          "vida",
          "devido",
          "passado"
        ],
        "entities": [
          [
            "114",
            "CARDINAL"
          ],
          [
            "farão de tudo pelos pobres",
            "PERSON"
          ],
          [
            "Sigmund Freud52\\n",
            "PERSON"
          ],
          [
            "Freiberg",
            "GPE"
          ],
          [
            "Mähren",
            "GPE"
          ],
          [
            "6 de maio de 1856",
            "QUANTITY"
          ],
          [
            "da técnica da",
            "PERSON"
          ],
          [
            "como forma de \\nacesso aos",
            "PERSON"
          ],
          [
            "impulsos comporta -\\nmentais",
            "PERSON"
          ],
          [
            "falta de controle de conter o próprio caos",
            "ORG"
          ]
        ],
        "readability_score": 91.62832199546486,
        "semantic_density": 0,
        "word_count": 245,
        "unique_words": 169,
        "lexical_diversity": 0.689795918367347
      },
      "preservation_score": 8.070459252113036e-06
    },
    {
      "id": 1,
      "text": "— 115 —Freud tinha autoconhecimento, fazendo ele ter um entendi -\\nmento acima do normal para um entendimento do ser hu -\\nmano. Usava muitas drogas para conseguir se entender e com -\\npreender a histeria de seus pacientes, perdeu amigo por usar \\nexcesso de drogas, e através da mesma, fazendo ele alcançar um \\nestado mental semelhante a de estar em sonhos consciente, ge -\\nrando acesso a sua própria forma de viver e ver a vida do caos \\nonde ele vivia. \\nCom isso Freud ficou conhecido no mundo todo, como um \\nintérprete da noção de inconsciente e transferência.\\nSó pancada no cérebro!!! Esse cara é um “buraco negro gigan -\\nte”! Pensa em como ele canalizava a energia para si próprio. Ele \\nvivia dentro do caos, absorvia as frequências quase inexistente \\n(semelhante a uma baleia, alimenta-se de pequenos animais) \\ndevido a ter muita massa escura entorno, tendo uma quantida -\\nde de massa maior dentro de si próprio, ele conseguia resistir \\nmais tempo e assim conseguia ter uma melhor interpretação \\nda própria energia concentrada que ele mesmo captava, ele \\nconseguia entender o caos que outros viviam, por outros não \\nconseguirem canalizar e entender a energia absorvida.\\nFrases\\nSomos feitos de carne, mas temos de viver como se fôssemos \\nde ferro.\\nComo fica forte uma pessoa quando está segura de ser amada!\\nUm homem que está livre da religião tem uma oportunidade \\nmelhor de viver uma vida mais normal e completa.\\nA felicidade é um problema individual. Aqui, nenhum conse -\\nlho é válido. Cada um deve procurar, por si, tornar-se feliz.\\ncaos do passado sendo vivido no futuro editável.indd   115caos do passado sendo vivido no futuro editável.indd   115 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 187510,
      "chapter": 5,
      "page": 115,
      "segment_type": "page",
      "themes": {},
      "difficulty": 25.357978723404255,
      "complexity_metrics": {
        "word_count": 282,
        "sentence_count": 16,
        "paragraph_count": 1,
        "avg_sentence_length": 17.625,
        "avg_word_length": 4.943262411347518,
        "unique_word_ratio": 0.6382978723404256,
        "avg_paragraph_length": 282.0,
        "punctuation_density": 0.13120567375886524,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "caos",
          "como",
          "entender",
          "viver",
          "energia",
          "conseguia",
          "freud",
          "fazendo",
          "normal",
          "drogas",
          "semelhante",
          "própria",
          "vida",
          "vivia",
          "próprio",
          "dentro",
          "massa",
          "mais",
          "melhor",
          "outros"
        ],
        "entities": [
          [
            "115",
            "CARDINAL"
          ],
          [
            "ser hu -\\nmano",
            "PERSON"
          ],
          [
            "Usava",
            "ORG"
          ],
          [
            "drogas",
            "NORP"
          ],
          [
            "para conseguir",
            "PERSON"
          ],
          [
            "excesso de drogas",
            "PERSON"
          ],
          [
            "ge",
            "ORG"
          ],
          [
            "forma de viver",
            "PERSON"
          ],
          [
            "Freud",
            "PERSON"
          ],
          [
            "buraco",
            "NORP"
          ]
        ],
        "readability_score": 89.70452127659574,
        "semantic_density": 0,
        "word_count": 282,
        "unique_words": 180,
        "lexical_diversity": 0.6382978723404256
      },
      "preservation_score": 1.061480458091832e-05
    },
    {
      "id": 1,
      "text": "— 116 —A nossa civilização é em grande parte responsável pelas nossas \\ndesgraças. Seríamos muito mais felizes se a abandonássemos e \\nretornássemos às condições primitivas.\\nOs judeus admiram mais o espírito do que o corpo. A escolher \\nentre os dois, eu também colocaria em primeiro lugar a inte -\\nligência.\\nIrei colocar dois pensamentos que eu escrevi, como referência \\npara Freud:\\nAmor\\nAmor pode ser a perfeição do sentimento ou a maior decepção \\ndo sentimento.\\nAmor pode ser o seu equilíbrio ou pode ser o seu desequilí -\\nbrio.\\nAmor você não escolhe, amor é o único sentimento que temos \\ncerteza que temos, mas não temos marcação do sentimento de \\namar.\\nAmor você têm que sentir para viver o melhor do amor, mas \\nquando o amor, você sente demais e não é retribuído, você se \\nsente em um vazio.\\nAmor você têm que aprender a lhe dar, pois o amor nos deixa \\ncego diante do que vivemos.\\nAmor é a razão de viver, assim como é razão de não querer \\nviver.\\nAmor você sabe o que é, sente o que é, vive o que é, porém \\nele também te deixa cego diante dos erros do outro que você \\nmesmo ama.\\nAmor é algo inexplicável e muito fácil de explicar.\\nAmor é o sentindo de se viver feliz e o sentido de se viver triste.\\ncaos do passado sendo vivido no futuro editável.indd   116caos do passado sendo vivido no futuro editável.indd   116 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 189323,
      "chapter": 5,
      "page": 116,
      "segment_type": "page",
      "themes": {
        "filosofia": 75.0,
        "arte": 25.0
      },
      "difficulty": 22.868237704918034,
      "complexity_metrics": {
        "word_count": 244,
        "sentence_count": 16,
        "paragraph_count": 1,
        "avg_sentence_length": 15.25,
        "avg_word_length": 4.495901639344262,
        "unique_word_ratio": 0.5532786885245902,
        "avg_paragraph_length": 244.0,
        "punctuation_density": 0.13114754098360656,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "amor",
          "você",
          "viver",
          "sentimento",
          "pode",
          "temos",
          "sente",
          "muito",
          "mais",
          "dois",
          "também",
          "como",
          "deixa",
          "cego",
          "diante",
          "razão",
          "passado",
          "sendo",
          "vivido",
          "futuro"
        ],
        "entities": [
          [
            "116",
            "CARDINAL"
          ],
          [
            "Seríamos muito mais",
            "ORG"
          ],
          [
            "judeus admiram mais",
            "PERSON"
          ],
          [
            "eu também",
            "PERSON"
          ],
          [
            "eu escrevi",
            "PERSON"
          ],
          [
            "Freud",
            "PERSON"
          ],
          [
            "ser o seu",
            "ORG"
          ],
          [
            "único",
            "GPE"
          ],
          [
            "mas não",
            "PERSON"
          ],
          [
            "mas \\nquando",
            "PERSON"
          ]
        ],
        "readability_score": 91.02622950819672,
        "semantic_density": 0,
        "word_count": 244,
        "unique_words": 135,
        "lexical_diversity": 0.5532786885245902
      },
      "preservation_score": 7.348710863712683e-06
    },
    {
      "id": 1,
      "text": "— 117 —Amor e ódio são uma única coisa, pois para você ter ódio de \\nalguém um dia, você já amou esse alguém.\\nAmor as pessoas confundem com eu não gostar de alguém, \\npor uma imagem.\\nAmor você precisa conhecer, sentir, admirar, confiar, abraçar, \\nvalorizar, compreender, brigar, dialogar, ensinar, preocupar \\namor é tudo que é belo, porém, quando você perde algumas \\nbeleza do amor, ele se transforma em “ódio” .\\nAmor não é você viver sempre, amor é caso do acaso, amor é a \\nraridade de se viver a felicidade maior de ser um ser humano.\\nAmor não é amar uma pessoa, amor é reconhecer que aquela \\npessoa te faz ser uma versão melhor de si mesmo.\\nAmor pode ser de mãe, filho, irmão, esposa, amigos, primos, \\ntias, vós, avôs amor é você amar o ser humano que está ali em \\nsua frente, fazendo exaltar o seu sentimento de amar sem você \\nescolher e sim sentir.\\nNão confundam saudade com tesão!!!\\nSaudade você têm daquela pessoa q mesmo longe você lembra \\ncom felicidade, carinho, admiração, sempre quando está jun -\\nto àquela saudade, parece que nem aconteceu simplesmente a \\nhistória continuou de onde parou da última vez.\\nTesão é você perder a noção entre o certo e o errado diante da \\nsua própria necessidade. Tesão você quer fazer sexo com a pes -\\nsoa, mesmo sabendo que não têm afeto quase nenhum.\\nTesão é o homem acordar parecendo um pau-brasil, a mulher \\nacordar toda molhada por uma lembrança sexual e não con -\\ntextual (pode acontecer por amor, têm que se entender).\\nTesão é algo que você sobe pelas paredes e quando você quer \\nfazer... Saí da frente pois você vai dá um jeito de fazer. \\ncaos do passado sendo vivido no futuro editável.indd   117caos do passado sendo vivido no futuro editável.indd   117 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 190800,
      "chapter": 5,
      "page": 117,
      "segment_type": "page",
      "themes": {},
      "difficulty": 26.983946078431373,
      "complexity_metrics": {
        "word_count": 306,
        "sentence_count": 16,
        "paragraph_count": 1,
        "avg_sentence_length": 19.125,
        "avg_word_length": 4.633986928104576,
        "unique_word_ratio": 0.6274509803921569,
        "avg_paragraph_length": 306.0,
        "punctuation_density": 0.1895424836601307,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "amor",
          "tesão",
          "ódio",
          "alguém",
          "quando",
          "amar",
          "pessoa",
          "mesmo",
          "saudade",
          "fazer",
          "pois",
          "sentir",
          "viver",
          "sempre",
          "felicidade",
          "humano",
          "pode",
          "está",
          "frente"
        ],
        "entities": [
          [
            "117",
            "CARDINAL"
          ],
          [
            "para você",
            "PERSON"
          ],
          [
            "dia",
            "ORG"
          ],
          [
            "você já amou",
            "PERSON"
          ],
          [
            "eu não gostar de alguém",
            "PERSON"
          ],
          [
            "ensinar",
            "PERSON"
          ],
          [
            "belo",
            "GPE"
          ],
          [
            "quando você perde algumas",
            "ORG"
          ],
          [
            "Amor",
            "ORG"
          ],
          [
            "que aquela \\npessoa",
            "PERSON"
          ]
        ],
        "readability_score": 89.04730392156863,
        "semantic_density": 0,
        "word_count": 306,
        "unique_words": 192,
        "lexical_diversity": 0.6274509803921569
      },
      "preservation_score": 1.4376644665914097e-05
    },
    {
      "id": 1,
      "text": "— 118 —Tesão não é algo que você não tem que usar e sim saber usar, \\nsuas necessidades corpórea são tão necessária quanto a necessi -\\ndade de comer, dormir, respirar nós humanos precisamos fazer \\nsexo porque o sexo, em toda história evolutiva do humano, \\nsempre foi feito para combater o estresse, o mau humor, libe -\\nrar endorfina, satisfação corporal.\\nNão prejudique alguém pela sua necessidade, não engane al -\\nguém por você precisar acabar com o seu tesão, fale a verdade, \\npois, como você quer, a outra pessoa também quer o acontecer, \\no sentimento, o amar, o se conhecer não é necessariamente res -\\ntrição e sim aprender a apreciar o trajeto, nesse trajeto, tem um \\ninício e muitas vezes, esse mesmo início começa com um tesão \\nfora de controle. Não se priva de fazer, se priva de se entender \\nantes de querer mais e mais.\\nRevolução industrial53\\nÉ uma energia que se propagava ou teve um “Deus” para essa \\nrevolução?\\nA revolução industrial foi uma necessidade de se viver melhor, \\nperante a energia que se estava entre nós. Tivemos grandes filó -\\nsofos, matemáticos, físicos, captadores de energia fora do nor -\\nmal, frequências de energia que eu não sei como explicar que é \\na captação. Porém, temos uma energia dentro de todas as ener -\\ngias, a energia universal de manter um ciclo de propagação de \\nenergia mútua uma com a outra, se mantendo sempre na linha \\nda energia mais forte, como impulsionadora da energia que \\nestá fora de sincronismo.\\nPensando dessa forma, nós estávamos com uma fácil captação \\n53.  Texto baseado em https://pt.m.wikipedia.org/wiki/Revolu%C3%A7% -\\nC3%A3o_Indu strial .\\ncaos do passado sendo vivido no futuro editável.indd   118caos do passado sendo vivido no futuro editável.indd   118 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 192663,
      "chapter": 5,
      "page": 118,
      "segment_type": "page",
      "themes": {},
      "difficulty": 26.35433789954338,
      "complexity_metrics": {
        "word_count": 292,
        "sentence_count": 15,
        "paragraph_count": 1,
        "avg_sentence_length": 19.466666666666665,
        "avg_word_length": 4.958904109589041,
        "unique_word_ratio": 0.6472602739726028,
        "avg_paragraph_length": 292.0,
        "punctuation_density": 0.1678082191780822,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "tesão",
          "você",
          "como",
          "fora",
          "mais",
          "revolução",
          "usar",
          "fazer",
          "sexo",
          "sempre",
          "necessidade",
          "quer",
          "outra",
          "trajeto",
          "início",
          "priva",
          "captação",
          "passado",
          "sendo"
        ],
        "entities": [
          [
            "118",
            "CARDINAL"
          ],
          [
            "Tesão",
            "GPE"
          ],
          [
            "tão necessária quanto",
            "ORG"
          ],
          [
            "respirar nós",
            "ORG"
          ],
          [
            "humanos precisamos",
            "PERSON"
          ],
          [
            "feito",
            "ORG"
          ],
          [
            "mau",
            "ORG"
          ],
          [
            "al -\\n",
            "PERSON"
          ],
          [
            "como você quer",
            "ORG"
          ],
          [
            "outra",
            "NORP"
          ]
        ],
        "readability_score": 88.77899543378996,
        "semantic_density": 0,
        "word_count": 292,
        "unique_words": 189,
        "lexical_diversity": 0.6472602739726028
      },
      "preservation_score": 1.2896695950305296e-05
    },
    {
      "id": 1,
      "text": "— 119 —da energia universal diante de qualquer frequência captada, \\nentão qualquer frequência que você captar tem uma energia \\nde estabilizar o caos, antes ou depois de ocorrer. Sendo assim, \\ncriamos formas de viver melhor em um bem comum para \\ntodos, criando mais conforto em viver o mundo físico, para \\nmelhor conseguir viver em um padrão de energia física e uni -\\nversal.\\nRevolução Industrial foi a transição para novos processos de \\nmanufatura no período entre 1760 a 1840. Esta transformação \\nincluiu a transição de métodos de produção artesanais para \\na produção por máquinas, graças aos grandes captadores de \\nenergia evoluindo um conforto para melhor se viver. Fabrica -\\nção de novos produtos químicos, novos processos de produção \\nde ferro, maior eficiência da energia da água, o uso crescente \\nda energia a vapor e o desenvolvimento das máquinas-ferra -\\nmentas, além da substituição da madeira e de outros biocom -\\nbustíveis pelo carvão. Agravando o caos gerado no mundo, a \\nrevolução teve início na Inglaterra e em poucas décadas se es -\\npalhou para a Europa Ocidental e os Estados Unidos que esse \\nfoi o primeiro país de outro continente a captar a energia do \\nmaior caos no mundo.\\nA Revolução Industrial é um divisor de águas na história e \\nquase todos os aspectos da vida cotidiana da época foram in -\\nfluenciados de alguma forma por esse processo. A população \\ncomeçou a experimentar um crescimento sustentado sem pre -\\ncedentes históricos, com isso criamos um conforto em viver, \\nacontecendo um problema preocupante na história da huma -\\nnidade, que se pensava ser “impossível” de termos, problema \\ncom obesidade (excesso de prazer). boa renda média. Pela pri -\\nmeira vez na história o padrão de vida das pessoas comuns \\ncomeçou a se submeter a um crescimento sustentado Nada \\nremotamente parecido com este comportamento econômico é \\ncaos do passado sendo vivido no futuro editável.indd   119caos do passado sendo vivido no futuro editável.indd   119 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 194542,
      "chapter": 5,
      "page": 119,
      "segment_type": "page",
      "themes": {
        "ciencia": 72.22222222222221,
        "arte": 27.77777777777778
      },
      "difficulty": 37.769000000000005,
      "complexity_metrics": {
        "word_count": 325,
        "sentence_count": 12,
        "paragraph_count": 1,
        "avg_sentence_length": 27.083333333333332,
        "avg_word_length": 5.095384615384615,
        "unique_word_ratio": 0.5846153846153846,
        "avg_paragraph_length": 325.0,
        "punctuation_density": 0.09230769230769231,
        "line_break_count": 32,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "viver",
          "caos",
          "sendo",
          "melhor",
          "conforto",
          "mundo",
          "revolução",
          "novos",
          "produção",
          "história",
          "qualquer",
          "frequência",
          "captar",
          "criamos",
          "todos",
          "padrão",
          "industrial",
          "transição",
          "processos"
        ],
        "entities": [
          [
            "119",
            "CARDINAL"
          ],
          [
            "universal diante de qualquer frequência captada",
            "PERSON"
          ],
          [
            "então qualquer frequência",
            "PERSON"
          ],
          [
            "você captar",
            "ORG"
          ],
          [
            "Sendo",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "para \\nmelhor conseguir",
            "ORG"
          ],
          [
            "Revolução Industrial",
            "PERSON"
          ],
          [
            "processos de \\nmanufatura",
            "ORG"
          ],
          [
            "1760",
            "CARDINAL"
          ]
        ],
        "readability_score": 84.92971794871795,
        "semantic_density": 0,
        "word_count": 325,
        "unique_words": 190,
        "lexical_diversity": 0.5846153846153846
      },
      "preservation_score": 1.0731450785104233e-05
    },
    {
      "id": 1,
      "text": "— 120 —mencionado por economistas clássicos, até mesmo como uma \\npossibilidade teórica.\\nO início e a duração da Revolução Industrial variam de acordo \\ncom diferentes historiadores.  \\nProvavelmente seu início foi por volta de 1780 na Grã-Breta -\\nnha não foi totalmente percebida até por volta de 1840, muitos \\nfalam que o processo de mudança econômica e social ocorreu \\nde forma gradual e que o termo “revolução” é equivocado, fa -\\nzendo ter muitas datas de início e se estendendo até os dias \\natuais. \\nCom a Revolução Industrial ocorreu um crescimento invo -\\nluntário do capitalismo. A revolução impulsionou uma era de \\nforte crescimento econômico nas economias capitalistas é um \\ndivisor na história da humanidade em crescimento de um vi -\\nver melhor, desde a domesticação de animais e a agricultura. \\nA Revolução Industrial se enraizou tanto no nosso cotidiano, \\nque tivemos um processo evolutivo para o nosso viver melhor \\ntão significativo, que virou ganância em se querer viver um \\nmelhor.\\nAnálise\\nNesse período de pré-cataclismo da captação de energia em \\nseu entorno, junto com um entorno de necessidade de uma \\npropagação (proporção de si próprio), com uma percepção \\ne captação da energia universal diante do meio em que você \\nvive, perante a uma necessidade de um bem maior, manten -\\ndo o nosso ciclo junto com ciclo universal (Deus, Ala, Buda, \\nZaratustra) de se viver um padrão em que todos precisam de \\nciclo constante de ação e reação, perante a energia universal e \\na sua própria necessidade da sua própria energia, em um ciclo \\nde necessidade entre o material e o Universo (quântico, mente \\nhumana), porém nem tudo são flores. Eu não sei se estamos \\ncaos do passado sendo vivido no futuro editável.indd   120caos do passado sendo vivido no futuro editável.indd   120 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 196667,
      "chapter": 6,
      "page": 120,
      "segment_type": "page",
      "themes": {
        "historia": 100.0
      },
      "difficulty": 36.6964406779661,
      "complexity_metrics": {
        "word_count": 295,
        "sentence_count": 10,
        "paragraph_count": 1,
        "avg_sentence_length": 29.5,
        "avg_word_length": 5.081355932203389,
        "unique_word_ratio": 0.5728813559322034,
        "avg_paragraph_length": 295.0,
        "punctuation_density": 0.1016949152542373,
        "line_break_count": 31,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "revolução",
          "energia",
          "necessidade",
          "ciclo",
          "início",
          "industrial",
          "crescimento",
          "melhor",
          "nosso",
          "viver",
          "universal",
          "volta",
          "processo",
          "ocorreu",
          "captação",
          "entorno",
          "junto",
          "perante",
          "própria",
          "passado"
        ],
        "entities": [
          [
            "120",
            "CARDINAL"
          ],
          [
            "até mesmo",
            "ORG"
          ],
          [
            "volta de 1780",
            "ORG"
          ],
          [
            "Grã-Breta -\\nnha não",
            "PERSON"
          ],
          [
            "1840",
            "DATE"
          ],
          [
            "falam",
            "GPE"
          ],
          [
            "processo de mudança econômica e social ocorreu \\nde forma",
            "ORG"
          ],
          [
            "história da humanidade",
            "PERSON"
          ],
          [
            "virou ganância",
            "PERSON"
          ],
          [
            "Análise\\nNesse",
            "ORG"
          ]
        ],
        "readability_score": 83.72559322033898,
        "semantic_density": 0,
        "word_count": 295,
        "unique_words": 169,
        "lexical_diversity": 0.5728813559322034
      },
      "preservation_score": 1.0622094968679941e-05
    },
    {
      "id": 1,
      "text": "— 121 —evoluindo proporcional a quantidade da população mundial \\nque cresceu ou se estamos concentrando massa escura nas sur -\\ndinas... Ao mesmo tempo eu vejo que estamos evoluindo em \\nvários aspectos, eu vejo uma “desvolução” em outras, ocorren -\\ndo muita discrepância de valores do material perante ao espi -\\nritual (amor, carinho, compreensão, confiar, admirar, agregar, \\nensinar, evoluir, juntar, sentir). Mas vejo um movimento mun -\\ndial, em um caminho de compreensão perante a necessidade \\nde melhorar, para todos. Esse assunto não é para esta linha de \\ntempo, mais a frente irei falar com mais carinho e explicativo \\nao meu ponto de ver.\\nE repara uma coisa interessante, irei colocar uma frase de \\nFreud para exemplificar: “Os judeus admiram mais o espírito \\ndo que o corpo. A escolher entre os dois, eu também colocaria \\nem primeiro lugar a inteligência. ” Essa frase é o ponto chave \\npara a minha tese, pois ela me ajudou a explicar melhor o que \\né difícil de explicar. Oscilação em grande escala pré-cataclismo \\n(primeiro) Grécia e a religião dominante judaica.\\nSegundo cataclismo Europa ocidental (maioria) e vindo de fa -\\nmília de Judeus.\\nEu vejo que, no próximo cataclismo, vão surgir muitos gênios \\nno México ou Rio de Janeiro, são dois lugares que se têm mui -\\nta energia espalhada de muitas etnias, muita forma de viver \\ndiferente um do outro, acúmulo de muita gente, muito caos \\ngerado entorno de si próprio, países muito livres, menos com -\\nprometimentos em cumprir as regras, mais alegria e mais caos, \\nao mesmo tempo, oscilação de energia variando muito, a mas -\\nsa escura tem uma massa mais pesada que a energia, encurtan -\\ndo o espaço de toda essa oscilação de energia, concentrando e \\ncanalizando em grandes captadores.\\nNota:  o último cataclismo foi o tsunami no Haiti, bem mais \\ncaos do passado sendo vivido no futuro editável.indd   121caos do passado sendo vivido no futuro editável.indd   121 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 198608,
      "chapter": 6,
      "page": 121,
      "segment_type": "page",
      "themes": {},
      "difficulty": 29.031980056980057,
      "complexity_metrics": {
        "word_count": 324,
        "sentence_count": 13,
        "paragraph_count": 1,
        "avg_sentence_length": 24.923076923076923,
        "avg_word_length": 4.978395061728395,
        "unique_word_ratio": 0.6512345679012346,
        "avg_paragraph_length": 324.0,
        "punctuation_density": 0.16049382716049382,
        "line_break_count": 31,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "vejo",
          "cataclismo",
          "energia",
          "tempo",
          "muita",
          "oscilação",
          "muito",
          "caos",
          "evoluindo",
          "estamos",
          "concentrando",
          "massa",
          "escura",
          "mesmo",
          "perante",
          "carinho",
          "compreensão",
          "irei",
          "ponto"
        ],
        "entities": [
          [
            "121",
            "CARDINAL"
          ],
          [
            "concentrando massa escura",
            "PERSON"
          ],
          [
            "eu vejo",
            "PERSON"
          ],
          [
            "eu vejo",
            "PERSON"
          ],
          [
            "compreensão",
            "ORG"
          ],
          [
            "ensinar",
            "GPE"
          ],
          [
            "evoluir",
            "PERSON"
          ],
          [
            "juntar",
            "PERSON"
          ],
          [
            "para todos",
            "PERSON"
          ],
          [
            "admiram mais",
            "PRODUCT"
          ]
        ],
        "readability_score": 86.04494301994302,
        "semantic_density": 0,
        "word_count": 324,
        "unique_words": 211,
        "lexical_diversity": 0.6512345679012346
      },
      "preservation_score": 1.672414952515565e-05
    },
    {
      "id": 1,
      "text": "— 122 —próximo do México e do Brasil, fazendo alguém próximo des -\\nsas regiões ser um bom captador de energia perante a um bem \\nmaior para o nosso mundo.\\ncaos do passado sendo vivido no futuro editável.indd   122caos do passado sendo vivido no futuro editável.indd   122 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 200687,
      "chapter": 6,
      "page": 122,
      "segment_type": "page",
      "themes": {},
      "difficulty": 23.03,
      "complexity_metrics": {
        "word_count": 50,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 12.5,
        "avg_word_length": 5.1,
        "unique_word_ratio": 0.78,
        "avg_paragraph_length": 50.0,
        "punctuation_density": 0.16,
        "line_break_count": 3,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "próximo",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "méxico",
          "brasil",
          "fazendo",
          "alguém",
          "regiões",
          "captador",
          "energia",
          "perante",
          "maior",
          "nosso",
          "mundo",
          "caos"
        ],
        "entities": [
          [
            "122",
            "CARDINAL"
          ],
          [
            "México",
            "GPE"
          ],
          [
            "Brasil",
            "PERSON"
          ],
          [
            "próximo des -\\nsas",
            "ORG"
          ],
          [
            "editável.indd",
            "CARDINAL"
          ],
          [
            "122caos",
            "CARDINAL"
          ],
          [
            "editável.indd",
            "CARDINAL"
          ],
          [
            "122",
            "CARDINAL"
          ],
          [
            "28/03/2022",
            "DATE"
          ],
          [
            "14:53:3928/03/2022",
            "CARDINAL"
          ]
        ],
        "readability_score": 92.22,
        "semantic_density": 0,
        "word_count": 50,
        "unique_words": 39,
        "lexical_diversity": 0.78
      },
      "preservation_score": 2.405827961334509e-07
    },
    {
      "id": 1,
      "text": "— 123 —Capítulo 12\\nInício do novo caos\\nEssa parte, até arrepiou!!! Assim, o que falar da idade média \\nproporcional a nós termos tecnologia, devido a captarmos \\nenergia para viver melhor, gerando uma melhora no caos futu -\\nro. Bem explicativo e curto. Curto e grosso. Kkkkk\\nEsse período foram as guerras das armas criadas pela sabedoria \\ndos sábios, que se tornou a sabedoria da destruição para os \\ntolos (amor é ódio, porém amor e ódio tem que ter um equi -\\nlíbrio)... Pois cataclismo, nossa massa escura paira com uma \\nmassa maior, deixando tudo em seu envolto um caos (Sodoma \\ne Gomorra).\\nParte 1 \\nPrimeira Guerra Mundial54\\nA Primeira Guerra foi um conflito bélico “global” centrado \\nonde mais se teve caos na história da humanidade. Teve seu iní -\\ncio 28 de julho de 1914 e durou até 11 de novembro de 1918. \\nA guerra envolveu as grandes potências, países que mais cau -\\nsaram caos ao decorrer da humanidade, que se organizaram \\nem duas alianças opostas: A guerra era dividida em 2 grupos \\nTríplice Entente entre Reino Unido, França e Rússia e os Impé -\\nrios Centrais, a Alemanha e a Áustria-Hungria. Originalmente \\na Tríplice Aliança era formada pela Alemanha, Áustria-Hun -\\n54.  Texto baseado em https://pt.m.wikipedia.org/wiki/Primeira_Guerra_\\nMundial .\\ncaos do passado sendo vivido no futuro editável.indd   123caos do passado sendo vivido no futuro editável.indd   123 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 201116,
      "chapter": 12,
      "page": 123,
      "segment_type": "page",
      "themes": {
        "ciencia": 30.232558139534888,
        "arte": 46.51162790697674,
        "tecnologia": 23.25581395348837
      },
      "difficulty": 23.42864782276547,
      "complexity_metrics": {
        "word_count": 231,
        "sentence_count": 17,
        "paragraph_count": 1,
        "avg_sentence_length": 13.588235294117647,
        "avg_word_length": 5.0562770562770565,
        "unique_word_ratio": 0.7142857142857143,
        "avg_paragraph_length": 231.0,
        "punctuation_density": 0.16883116883116883,
        "line_break_count": 25,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "caos",
          "guerra",
          "parte",
          "curto",
          "pela",
          "sabedoria",
          "amor",
          "ódio",
          "massa",
          "primeira",
          "mais",
          "teve",
          "humanidade",
          "tríplice",
          "alemanha",
          "áustria",
          "passado",
          "sendo",
          "vivido",
          "futuro"
        ],
        "entities": [
          [
            "123",
            "CARDINAL"
          ],
          [
            "12",
            "CARDINAL"
          ],
          [
            "Essa",
            "PERSON"
          ],
          [
            "captarmos",
            "GPE"
          ],
          [
            "nossa massa escura paira",
            "PERSON"
          ],
          [
            "deixando tudo",
            "PERSON"
          ],
          [
            "Gomorra",
            "GPE"
          ],
          [
            "1",
            "CARDINAL"
          ],
          [
            "Primeira Guerra Mundial54",
            "PERSON"
          ],
          [
            "Primeira Guerra",
            "PERSON"
          ]
        ],
        "readability_score": 91.68899923605807,
        "semantic_density": 0,
        "word_count": 231,
        "unique_words": 165,
        "lexical_diversity": 0.7142857142857143
      },
      "preservation_score": 1.0024283172227121e-05
    },
    {
      "id": 1,
      "text": "— 124 —gria e a Itália; mas como a Áustria-Hungria tinha tomado a \\nofensiva, violando o acordo, a Itália não entrou na guerra pela \\nTríplice Aliança (teve aliança na Segunda Guerra Mundial) Es -\\nsas alianças reorganizaram-se (a Itália lutou pelos Aliados) e \\nexpandiram-se com mais nações que entraram na guerra. Mais \\nde nove milhões de combatentes foram mortos, em grande \\nparte por causa de avanços tecnológicos (captação de energia \\npara combater o caos criando mais caos) que determinaram \\num crescimento enorme na letalidade de armas.\\nOcorreu uma mudança pelo motivo de se ter uma guerra, \\ndescentralizou o foco religioso para, políticas imperialistas \\nestrangeiras das grandes potências da Europa, como o Impé -\\nrio Alemão, o Império Austro-Húngaro, o Império Otomano, \\no Império Russo, o Império Britânico, a Terceira República \\nFrancesa e a Itália. Em 28 de junho de 1914, o assassinato do \\narquiduque Francisco Fernando da Áustria, o herdeiro do tro -\\nno da Áustria-Hungria, pelo nacionalista iugoslavo Gavrilo \\nPrincip, em Sarajevo, na Bósnia, foi a cereja do bolo para se ter \\numa guerra.\\nOs eventos nos conflitos locais eram tão tumultuosos quanto \\nnas grandes frentes de batalha, tentando os participantes mo -\\nbilizar a sua mão de obra e recursos econômicos para lutar \\numa guerra . Quais são os países que tem a economia mais está -\\nvel hoje em dia? Guerra gera trabalho, trabalho melhora a qua -\\nlidade de vida de um coletivo, coletivo vira país. Isso criou um \\npatriotismo preconceituoso o nacionalismo de vários países, a \\ndepressão econômica, as repercussões da derrota da Alemanha \\ne os problemas com o Tratado de Versalhes, que foram fatores \\nque contribuíram para o início da Segunda Guerra Mundial.\\nAntes de um cataclismo, temos uma maior captação da energia \\ne depois do cataclismo, fica a massa escura mantendo o caos \\ncaos do passado sendo vivido no futuro editável.indd   124caos do passado sendo vivido no futuro editável.indd   124 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 202651,
      "chapter": 6,
      "page": 124,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 31.142471590909093,
      "complexity_metrics": {
        "word_count": 320,
        "sentence_count": 11,
        "paragraph_count": 1,
        "avg_sentence_length": 29.09090909090909,
        "avg_word_length": 5.171875,
        "unique_word_ratio": 0.653125,
        "avg_paragraph_length": 320.0,
        "punctuation_density": 0.125,
        "line_break_count": 31,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "guerra",
          "itália",
          "mais",
          "caos",
          "império",
          "áustria",
          "como",
          "hungria",
          "aliança",
          "segunda",
          "mundial",
          "captação",
          "energia",
          "pelo",
          "grandes",
          "países",
          "trabalho",
          "coletivo",
          "cataclismo",
          "passado"
        ],
        "entities": [
          [
            "124",
            "CARDINAL"
          ],
          [
            "Itália",
            "GPE"
          ],
          [
            "Áustria-Hungria",
            "ORG"
          ],
          [
            "acordo",
            "ORG"
          ],
          [
            "Itália",
            "GPE"
          ],
          [
            "Segunda Guerra Mundial",
            "PERSON"
          ],
          [
            "Itália",
            "GPE"
          ],
          [
            "pelos Aliados",
            "PERSON"
          ],
          [
            "de se",
            "PERSON"
          ],
          [
            "para",
            "PRODUCT"
          ]
        ],
        "readability_score": 83.90298295454545,
        "semantic_density": 0,
        "word_count": 320,
        "unique_words": 209,
        "lexical_diversity": 0.653125
      },
      "preservation_score": 1.3334119216002477e-05
    },
    {
      "id": 1,
      "text": "— 125 —até a energia conseguir continuar o fluxo de propagação de \\nciclos infinitos universal, galáxia, sistema solar, terra, nós, den -\\ntro do próprio ciclo infinito universal, galáxia, sistema solar, \\nterra, nós. Com o caos nos parando, evolução no mundo físico, \\nnovas formas de se utilizar a força vital do universo (energia), \\ncom o caos implantado diante de novas tecnologias, nos fazen -\\ndo “evoluir” o caos.\\nOutra vez o caos é onde está o maior caos, diante de nós mes -\\nmos.\\nParte 2\\nA Grande Depressão\\nGeramos caos diante do caos...\\nGeramos uma guerra através da necessidade da ganância mate -\\nrial (a energia era difícil de se captar), nos transformando em \\npessoas materialista em excesso, capitalista em excesso, egocên -\\ntricos em excesso, com a energia espiritual mal interpretada \\nde novo, para o lado sombrio do amor, gerando o amor pelo \\nmundo material maior que o valor da energia universal.\\nA Grande Depressão55\\nA Grande Depressão, também conhecida como Crise de 1929, \\nfoi a maior crise financeira da história dos Estados Unidos, aqui \\nfoi o início de enxergar a necessidade de se existir o capitalis -\\nmo, que teve início em 1929 e persistiu ao longo da década de \\n1930, terminando apenas com a Segunda Guerra Mundial. Os \\n55.  Texto baseado em https://pt.m.wikipedia.org/wiki/Grande_Depres -\\ns%C3%A3o .\\ncaos do passado sendo vivido no futuro editável.indd   125caos do passado sendo vivido no futuro editável.indd   125 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 204771,
      "chapter": 6,
      "page": 125,
      "segment_type": "page",
      "themes": {
        "ciencia": 39.3939393939394,
        "arte": 30.303030303030305,
        "tecnologia": 30.303030303030305
      },
      "difficulty": 29.245535714285715,
      "complexity_metrics": {
        "word_count": 240,
        "sentence_count": 14,
        "paragraph_count": 1,
        "avg_sentence_length": 17.142857142857142,
        "avg_word_length": 5.104166666666667,
        "unique_word_ratio": 0.6291666666666667,
        "avg_paragraph_length": 240.0,
        "punctuation_density": 0.1875,
        "line_break_count": 26,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "caos",
          "energia",
          "universal",
          "diante",
          "maior",
          "grande",
          "excesso",
          "galáxia",
          "sistema",
          "solar",
          "terra",
          "mundo",
          "novas",
          "depressão",
          "geramos",
          "guerra",
          "necessidade",
          "amor",
          "crise",
          "início"
        ],
        "entities": [
          [
            "125",
            "CARDINAL"
          ],
          [
            "fluxo de propagação de \\nciclos",
            "ORG"
          ],
          [
            "universo (energia",
            "ORG"
          ],
          [
            "Outra",
            "ORG"
          ],
          [
            "diante de nós",
            "PERSON"
          ],
          [
            "2",
            "CARDINAL"
          ],
          [
            "Grande Depressão",
            "ORG"
          ],
          [
            "Geramos",
            "PERSON"
          ],
          [
            "capitalista",
            "PERSON"
          ],
          [
            "interpretada \\nde novo",
            "ORG"
          ]
        ],
        "readability_score": 89.89732142857143,
        "semantic_density": 0,
        "word_count": 240,
        "unique_words": 151,
        "lexical_diversity": 0.6291666666666667
      },
      "preservation_score": 1.137300490812677e-05
    },
    {
      "id": 1,
      "text": "— 126 —países que assumiram o controle da Alemanha após o tratado \\nde Versalhes, separaram a Alemanha em duas partes Alemanha \\noriental e Alemanha ocidental, criando uma grande dificulda -\\nde em se viver na Alemanha, com o acontecimento da Grande \\nDepressão, os países com uma maior qualidade de vida perdeu \\numa qualidade de viver, assim os países não conseguiam admi -\\nnistrar a Alemanha, pois todo o dinheiro do país, era direcio -\\nnado para o próprio país, assim abrindo mão de controlar a \\nAlemanha, e o povo alemão acostumado a viver no caos devi -\\ndo ao Tratado de Versalhes, cresceu mais que os outros países \\neconomicamente, criou empregos, fábricas de armas, infraes -\\ntrutura e um líder que sabia direcionar a necessidade do caos \\nvivido, para se viver melhor dentro de sua própria necessidade. \\nconsiderada o pior e o mais longo período de recessão eco -\\nnômica do sistema capitalista do século XX. Este período de \\ndepressão econômica causou altas taxas de desemprego, que -\\ndas drásticas do produto interno bruto de diversos países, bem \\ncomo quedas drásticas na produção industrial, preços de ações, \\ne em praticamente todo o medidor de atividade econômica, \\nem diversos países no mundo.\\nMilhares de acionistas perderam, literalmente da noite para o \\ndia, grandes somas em dinheiro. Muitos perderam tudo o que \\ntinham, fazendo muitas pessoas se matarem. Essa quebra na \\nbolsa de valores de Nova Iorque causou grande deflação e que -\\nda nas taxas de venda de produtos, que por sua vez obrigaram \\nao encerramento de inúmeras empresas comerciais e indus -\\ntriais, elevando assim drasticamente as taxas de desemprego.\\n Em alguns países, a Grande Depressão foi um dos fatores pri -\\nmários que ajudaram a ascensão de regimes ditatoriais, como \\nos nazistas comandados por Adolf Hitler na Alemanha. O iní -\\ncio da Segunda Guerra Mundial terminou com qualquer efei -\\nto remanescente da Grande Depressão.\\ncaos do passado sendo vivido no futuro editável.indd   126caos do passado sendo vivido no futuro editável.indd   126 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 206371,
      "chapter": 6,
      "page": 126,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 33.92867547882385,
      "complexity_metrics": {
        "word_count": 337,
        "sentence_count": 11,
        "paragraph_count": 1,
        "avg_sentence_length": 30.636363636363637,
        "avg_word_length": 5.0652818991097925,
        "unique_word_ratio": 0.6023738872403561,
        "avg_paragraph_length": 337.0,
        "punctuation_density": 0.11869436201780416,
        "line_break_count": 32,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "alemanha",
          "países",
          "grande",
          "viver",
          "depressão",
          "assim",
          "caos",
          "vivido",
          "taxas",
          "tratado",
          "versalhes",
          "qualidade",
          "todo",
          "dinheiro",
          "país",
          "mais",
          "necessidade",
          "período",
          "econômica",
          "causou"
        ],
        "entities": [
          [
            "126",
            "CARDINAL"
          ],
          [
            "de Versalhes",
            "PERSON"
          ],
          [
            "Alemanha",
            "ORG"
          ],
          [
            "Alemanha",
            "ORG"
          ],
          [
            "Alemanha",
            "ORG"
          ],
          [
            "Alemanha",
            "ORG"
          ],
          [
            "nado",
            "ORG"
          ],
          [
            "Alemanha",
            "ORG"
          ],
          [
            "Tratado de Versalhes",
            "FAC"
          ],
          [
            "fábricas de armas",
            "ORG"
          ]
        ],
        "readability_score": 83.16223361208525,
        "semantic_density": 0,
        "word_count": 337,
        "unique_words": 203,
        "lexical_diversity": 0.6023738872403561
      },
      "preservation_score": 1.2597790052078883e-05
    },
    {
      "id": 1,
      "text": "— 127 —Vamos à linha de tempo de propagação da energia. Quando \\nfoi a primeira vez que os Estados Unidos captou a primeira \\nenergia da Europa e trouxe para as Américas?\\nBenjamin Franklin embaixador dos Estados Unidos na França, \\ncaptou a energia da vida em viver melhor em um contexto, \\nlevando nova forma de se viver e evoluir perante a uma na -\\nção. Desde então, os Estados Unidos vieram em uma evolução \\n(território longe dos territórios de onde têm guerra) do mun -\\ndo universal junto ao mundo físico (material), aumentando a \\nmassa escura mais massa escura proporcional a evolução terri -\\ntorial e de qualidade de vida, entrando em um ciclo de ter mais \\npara si próprio, para cada um de nós dentro de um contexto \\nmaior (eu, família, cidade, Estado, país mundo), observação \\ndiante do seu próprio mundo perante a um mundo melhor, \\ncausando mais desequilíbrio do eixo da terra, Trazendo mais \\nrecursos e mais caos.\\nLembre-se, terremoto do Haiti.\\nParte 3 \\nSegunda Guerra Mundial56\\nSe existiu o Diabo, aqui foi a confirmação dele. Adolf Hitler, o \\ncara com o padrão comportamental mais louco e mais aceito \\ndiante da “minha” própria dor. A Alemanha tinha perdido a \\nPrimeira Guerra Mundial, foram obrigados a assinar o tratado \\nde Versalhes, destruindo a Alemanha que já estava destruída \\ndevido a guerra, deixando o povo alemão no caos total após \\num cataclismo, com várias restrições de comércio, não saben -\\ndo o que poderia produzir, tendo que melhorar o conforto de \\n56.  Texto baseado em https://pt.m.wikipedia.org/wiki/Segunda_Guerra_\\nMundial .\\ncaos do passado sendo vivido no futuro editável.indd   127caos do passado sendo vivido no futuro editável.indd   127 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 208556,
      "chapter": 6,
      "page": 127,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 25.89265944645006,
      "complexity_metrics": {
        "word_count": 277,
        "sentence_count": 15,
        "paragraph_count": 1,
        "avg_sentence_length": 18.466666666666665,
        "avg_word_length": 5.086642599277979,
        "unique_word_ratio": 0.6462093862815884,
        "avg_paragraph_length": 277.0,
        "punctuation_density": 0.148014440433213,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "guerra",
          "mundo",
          "energia",
          "primeira",
          "estados",
          "unidos",
          "caos",
          "captou",
          "vida",
          "viver",
          "melhor",
          "contexto",
          "perante",
          "evolução",
          "massa",
          "escura",
          "próprio",
          "diante",
          "alemanha"
        ],
        "entities": [
          [
            "127",
            "CARDINAL"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "Estados Unidos",
            "ORG"
          ],
          [
            "Europa",
            "LOC"
          ],
          [
            "Américas",
            "GPE"
          ],
          [
            "Benjamin Franklin",
            "PERSON"
          ],
          [
            "Estados Unidos",
            "ORG"
          ],
          [
            "França",
            "GPE"
          ],
          [
            "levando",
            "NORP"
          ],
          [
            "nova forma de se",
            "PERSON"
          ]
        ],
        "readability_score": 89.24067388688327,
        "semantic_density": 0,
        "word_count": 277,
        "unique_words": 179,
        "lexical_diversity": 0.6462093862815884
      },
      "preservation_score": 1.1839589724870433e-05
    },
    {
      "id": 1,
      "text": "— 128 —vida da sua nação, sem recursos sem nada, no caos total.\\nApós a perda da Primeira Guerra Mundial, veio a grande que -\\nda, ocasionando um holocausto financeiro no mundo todo, to -\\ndos os países se virando em como viver, vendendo até a “alma” \\npara sustentar a sua própria nação. Nesse momento que apare -\\nce o maior captador de energia perante o amar no caos. Todos \\nque estavam ali na Alemanha, estavam vivendo de uma forma \\nde sobrevivência humana, qualquer “messias” que aparecesse \\ntrazendo comida para a minha casa, é a melhor energia a ser \\nseguida.\\nAdolfo Hitler foi um gênio do mal, pelo seu próprio caos ser \\nsemelhante à sua dor, eu entendo o quanto você está em caos.\\nApós a grande queda, os países que restringiram o comércio \\nalemão, não conseguiram nem resolver os seus próprios pro -\\nblemas, quanto mas observar a Alemanha... Essa brecha foi ne -\\ncessária para a ascensão do “Diabo” .\\nA Segunda Guerra Mundial foi um conflito militar “global” \\nque durou de 1939 a 1945, foi — organizada em duas alianças \\nmilitares opostas: os Aliados e o Eixo. Foi a guerra mais abran -\\ngente da história. O mundo está com uma quantidade de hu -\\nmanos absurdo para se adaptar de um viver com o outro. com \\nmais de 100 milhões de militares mobilizados. Todos os mi -\\nlitares foram captados através do patriotismo pelo país. Com \\numa guerra logo após a qualidade de vida ter uma melhora, \\ndevido a termos vindo de uma Revolução Industrial, avanço \\ntecnológicos, ciências, matemática, “aceitação religiosa” ... Mar -\\ncado por um número significante de ataques contra civis, uso \\npreconceituoso de raça evoluída (Darwin) e religião (judeus), \\nincluindo o Holocausto e a única vez em que armas nucleares \\nforam utilizadas em combate.\\nGeralmente considera-se o ponto inicial da guerra como sen -\\ncaos do passado sendo vivido no futuro editável.indd   128caos do passado sendo vivido no futuro editável.indd   128 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 210385,
      "chapter": 6,
      "page": 128,
      "segment_type": "page",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 26.18544517504887,
      "complexity_metrics": {
        "word_count": 331,
        "sentence_count": 17,
        "paragraph_count": 1,
        "avg_sentence_length": 19.470588235294116,
        "avg_word_length": 4.833836858006042,
        "unique_word_ratio": 0.649546827794562,
        "avg_paragraph_length": 331.0,
        "punctuation_density": 0.1419939577039275,
        "line_break_count": 31,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "caos",
          "guerra",
          "após",
          "vida",
          "nação",
          "mundial",
          "grande",
          "holocausto",
          "mundo",
          "países",
          "como",
          "viver",
          "energia",
          "todos",
          "estavam",
          "alemanha",
          "pelo",
          "quanto",
          "está",
          "militares"
        ],
        "entities": [
          [
            "128",
            "CARDINAL"
          ],
          [
            "sem nada",
            "PERSON"
          ],
          [
            "Após",
            "PERSON"
          ],
          [
            "Primeira Guerra Mundial",
            "PERSON"
          ],
          [
            "para sustentar",
            "PERSON"
          ],
          [
            "sua própria",
            "ORG"
          ],
          [
            "Nesse",
            "ORG"
          ],
          [
            "Alemanha",
            "ORG"
          ],
          [
            "sobrevivência humana",
            "PERSON"
          ],
          [
            "qualquer",
            "PERSON"
          ]
        ],
        "readability_score": 88.81455482495113,
        "semantic_density": 0,
        "word_count": 331,
        "unique_words": 215,
        "lexical_diversity": 0.649546827794562
      },
      "preservation_score": 1.695015154576586e-05
    },
    {
      "id": 1,
      "text": "— 129 —do a invasão da Polônia pela Alemanha Nazista em 1 de setem -\\nbro de 1939 e subsequentes declarações de guerra contra a Ale -\\nmanha pela França, nesse momento foi a evolução da ciência \\nem criar novas drogas sintéticas, foi criado a droga chamada \\nPervitin (metanfetamina). O efeito da metanfetamina no seu \\ncérebro é inibidor de cansaço e fome, transformando os sol -\\ndados alemães em super soldados, devido a essa situação em \\nque os soldados alemães ficavam, o planejamento da França foi \\nfeito um cálculo de tempo para as forças alemãs chegarem em \\nseu território, esse cálculo foi feito através de um padrão de se \\nmovimentar devido as condições normais humanas, fazendo a \\nFrança estar despreparada para o confronto, assim a Alemanha \\nconquistou o território pelo fator surpresa.\\nO Hitler é tão perspicaz com o conquistar a confiança do povo, \\nque logo após a conquista da França, ele fez questão de exaltar \\na dor do povo alemão em acabar com o Tratado de Versalhes \\nno mesmo vagão de trem que foi feito o mesmo. Muitos paí -\\nses que não se envolveram inicialmente, acabaram aderindo ao \\nconflito em resposta a eventos como a invasão da União Sovié -\\ntica pelos alemães, uma das piores coisas que poderia ter acon -\\ntecido para Alemanha, foi a derrota da guerra, os Russos eram \\nacostumados com o frio extremo, traçando uma estratégia de \\nrecuar e deixar os alemães morrerem pela própria dificulda -\\nde em se viver naquelas condições climáticas, mais os ataques \\njaponeses contra as forças dos Estados Unidos no Pacífico em \\nPearl Harbor, ocasionando o excesso de força “desnecessária” \\nde expressar o tamanho do seu poder de fogo.\\nApós a guerra se originou a Organização das Nações Unidas \\n(ONU) era estabelecida para estimular a cooperação global e \\nevitar futuros conflitos, a União Soviética e os Estados Unidos \\nemergiam como superpotências rivais, ocasionando interesses \\nmaiores dos mesmos, iniciando uma Guerra Fria. \\ncaos do passado sendo vivido no futuro editável.indd   129caos do passado sendo vivido no futuro editável.indd   129 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 212455,
      "chapter": 6,
      "page": 129,
      "segment_type": "page",
      "themes": {
        "filosofia": 69.76744186046511,
        "ciencia": 30.232558139534888
      },
      "difficulty": 36.50962099125364,
      "complexity_metrics": {
        "word_count": 343,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 42.875,
        "avg_word_length": 5.032069970845481,
        "unique_word_ratio": 0.6209912536443148,
        "avg_paragraph_length": 343.0,
        "punctuation_density": 0.09037900874635568,
        "line_break_count": 32,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "guerra",
          "frança",
          "alemães",
          "pela",
          "alemanha",
          "feito",
          "invasão",
          "contra",
          "metanfetamina",
          "soldados",
          "devido",
          "cálculo",
          "forças",
          "território",
          "condições",
          "povo",
          "após",
          "mesmo",
          "como",
          "união"
        ],
        "entities": [
          [
            "129",
            "CARDINAL"
          ],
          [
            "Alemanha Nazista",
            "PERSON"
          ],
          [
            "1",
            "CARDINAL"
          ],
          [
            "declarações de guerra contra",
            "ORG"
          ],
          [
            "França",
            "GPE"
          ],
          [
            "drogas sintéticas",
            "ORG"
          ],
          [
            "Pervitin",
            "PERSON"
          ],
          [
            "França",
            "GPE"
          ],
          [
            "alemãs chegarem",
            "PERSON"
          ],
          [
            "de se \\nmovimentar",
            "PERSON"
          ]
        ],
        "readability_score": 77.05287900874636,
        "semantic_density": 0,
        "word_count": 343,
        "unique_words": 213,
        "lexical_diversity": 0.6209912536443148
      },
      "preservation_score": 1.0731450785104233e-05
    },
    {
      "id": 1,
      "text": "— 130 —Durante a segunda guerra, tivemos liberação de massa escura... \\npropagação da massa escura, semelhante de uma bomba atô -\\nmica, com epicentro na Europa, jogando a massa escura para \\nfora da Europa, canalizando a energia envolto (vórtice) da mas -\\nsa escura e tendo concentração (quasar) de energia no epicen -\\ntro da massa escura, fazendo ter novos captores de energia pelo \\nmundo todo, inclusive no centro da massa escura, criando tec -\\nnologias revolucionárias perante a nossa própria necessidade. \\nDaí surgiu o computador, “bomba atômica” bem no epicentro \\ndo caos.\\ncaos do passado sendo vivido no futuro editável.indd   130caos do passado sendo vivido no futuro editável.indd   130 28/03/2022   14:53:3928/03/2022   14:53:39",
      "position": 214670,
      "chapter": 6,
      "page": 130,
      "segment_type": "page",
      "themes": {},
      "difficulty": 26.202802359882007,
      "complexity_metrics": {
        "word_count": 113,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 18.833333333333332,
        "avg_word_length": 5.398230088495575,
        "unique_word_ratio": 0.6814159292035398,
        "avg_paragraph_length": 113.0,
        "punctuation_density": 0.17699115044247787,
        "line_break_count": 10,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "escura",
          "massa",
          "energia",
          "bomba",
          "epicentro",
          "europa",
          "caos",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "durante",
          "segunda",
          "guerra",
          "tivemos",
          "liberação",
          "propagação",
          "semelhante"
        ],
        "entities": [
          [
            "130",
            "CARDINAL"
          ],
          [
            "tivemos liberação de massa escura",
            "ORG"
          ],
          [
            "semelhante de uma bomba atô -\\nmica",
            "ORG"
          ],
          [
            "Europa",
            "LOC"
          ],
          [
            "fora da Europa",
            "PERSON"
          ],
          [
            "tendo concentração",
            "ORG"
          ],
          [
            "fazendo",
            "ORG"
          ],
          [
            "pelo",
            "PERSON"
          ],
          [
            "editável.indd   130caos",
            "CARDINAL"
          ],
          [
            "editável.indd",
            "CARDINAL"
          ]
        ],
        "readability_score": 88.96386430678466,
        "semantic_density": 0,
        "word_count": 113,
        "unique_words": 77,
        "lexical_diversity": 0.6814159292035398
      },
      "preservation_score": 2.332924083718312e-06
    },
    {
      "id": 1,
      "text": "— 131 —Capítulo 13\\nEntendendo o meu caos, perante ao caos universal\\nEste capítulo, na verdade, é uma explicação analítica, sobre \\ncomo eu enxerguei todas essas análises, diante de como eu \\nvivo, como estudo, como eu enxerguei os padrões as quais eu \\ncoloquei aqui, pois depois da Segunda Guerra Mundial, teve \\nmuitas variações de energia pelo mundo todo, teve muito mais \\nconhecimento de um país para outro, teve tantas coisas em um \\ntotal mundial, que a propagação da energia ficou acessível para \\ntodo o entorno do mundo.\\nPartindo dessa visão de uma sequência de linha de tempo, irei \\nfalar daqui para frente sobre a energia que foi se propagando \\nno meu país e na minha vida. Talvez fique um pouco sem uma \\nlinha de tempo tão continua, os captadores de energia pelo \\nmundo aumentaram muito, o acesso de análise perante a ener -\\ngia captada, aumentou absurdamente, então tivemos pessoas \\nque evoluíram um estudo concreto, através de uma pequena \\ncaptação da energia, porém significativa para uma captação de \\nenergia já existente, nós transformando em matéria evolutiva \\natravés da captação da energia.\\nNão irei mais falar em forma de energia, massa escura, propa -\\ngação da energia, propagação da massa escura, vórtice, quasar. \\nIrei descrever uma forma de viver a vida no mundo real e não \\nno figurativo. Não irei fugir dos temas, não irei dar referências \\nquântica, física e matemática irei falar de dor física, dor senti -\\nmental, felicidade, amizade, amor, ódio, guerras, movimentos \\npolíticos, cultura, música, sentimento de sentir o sentimento e \\noutras coisas que se eu não escrevi aqui pode ser que eu escreva \\ncaos do passado sendo vivido no futuro editável.indd   131caos do passado sendo vivido no futuro editável.indd   131 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 215521,
      "chapter": 13,
      "page": 131,
      "segment_type": "page",
      "themes": {},
      "difficulty": 38.594904181184674,
      "complexity_metrics": {
        "word_count": 287,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 35.875,
        "avg_word_length": 5.10801393728223,
        "unique_word_ratio": 0.6202090592334495,
        "avg_paragraph_length": 287.0,
        "punctuation_density": 0.1672473867595819,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "irei",
          "como",
          "mundo",
          "caos",
          "teve",
          "falar",
          "captação",
          "capítulo",
          "perante",
          "enxerguei",
          "estudo",
          "aqui",
          "mundial",
          "pelo",
          "todo",
          "muito",
          "mais",
          "país",
          "coisas"
        ],
        "entities": [
          [
            "131",
            "CARDINAL"
          ],
          [
            "13",
            "CARDINAL"
          ],
          [
            "como eu enxerguei todas essas",
            "PERSON"
          ],
          [
            "diante de como eu \\nvivo",
            "PERSON"
          ],
          [
            "como eu enxerguei os",
            "PERSON"
          ],
          [
            "padrões",
            "GPE"
          ],
          [
            "eu \\ncoloquei aqui",
            "PERSON"
          ],
          [
            "Guerra Mundial",
            "PERSON"
          ],
          [
            "pelo",
            "PERSON"
          ],
          [
            "teve muito mais",
            "PERSON"
          ]
        ],
        "readability_score": 80.53009581881533,
        "semantic_density": 0,
        "word_count": 287,
        "unique_words": 178,
        "lexical_diversity": 0.6202090592334495
      },
      "preservation_score": 1.0818935438243673e-05
    },
    {
      "id": 1,
      "text": "— 132 —futuramente, por ter concordância com o assunto me levando \\na pensar na ocasião, que automaticamente me faz pensar em \\num contexto, devido ao meu subconsciente assimilar situações \\nsemelhantes ao que eu estou necessitando, precisando ou sen -\\ntindo...\\nParte 1 \\nBrasil Evolução sentimental e política\\nDécada de 50\\nDécada de 50 Brasil estava começando a ser visto pelo mundo, \\nestávamos em acessão musical e futebol, tínhamos a Carmem \\nMiranda que já vinha fazendo sucesso pelo mundo, levando \\no nome do Brasil aonde ia, por mas que ela tenha nascido em \\nPortugal, ela exaltou o nome do Brasil. O futebol na década de \\n50 disputou duas finais, uma foi vice e a outra campeão, levan -\\ndo pessoas negra das favelas a conhecer o mundo e ganhar seu \\nespaço perante a sociedade. Pelé disse: “Eu nunca tinha saído \\ndo Brasil. Eu nem sabia que existia outro país, quando cheguei \\nna Suécia, eram todos brancos e loiros, muito diferente das \\npessoas do meu país. Quando eu cheguei lá, as pessoas ficavam \\ncuriosas com a cor da minha pele, ficavam me tocando como \\nse fosse algo diferente. ” Nós não temos noção do nosso com -\\nportamento diante do “desconhecido” , levando-nos a criarmos \\numa imagem contextual, diante daquilo ou algo que eu estou \\n“acostumado a viver” , diante de cada “situação que eu vivo” .\\nNos transformando em pessoas com uma análise visual, às ve -\\nzes preconceituosa sobre aquilo que nos armazenamos, diante \\nda situação a qual nós já vivemos, olhamos ou ouvimos peran -\\nte ao estarmos vivendo de um julgamento de si próprio, de \\ncaos do passado sendo vivido no futuro editável.indd   132caos do passado sendo vivido no futuro editável.indd   132 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 217418,
      "chapter": 6,
      "page": 132,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 32.8602787456446,
      "complexity_metrics": {
        "word_count": 287,
        "sentence_count": 10,
        "paragraph_count": 1,
        "avg_sentence_length": 28.7,
        "avg_word_length": 4.867595818815331,
        "unique_word_ratio": 0.6655052264808362,
        "avg_paragraph_length": 287.0,
        "punctuation_density": 0.13588850174216027,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "brasil",
          "pessoas",
          "diante",
          "levando",
          "década",
          "mundo",
          "pensar",
          "estou",
          "pelo",
          "futebol",
          "nome",
          "país",
          "quando",
          "cheguei",
          "diferente",
          "ficavam",
          "algo",
          "situação",
          "passado",
          "sendo"
        ],
        "entities": [
          [
            "132",
            "CARDINAL"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "que eu",
            "PERSON"
          ],
          [
            "1",
            "CARDINAL"
          ],
          [
            "Brasil Evolução",
            "PERSON"
          ],
          [
            "Década",
            "GPE"
          ],
          [
            "Década",
            "GPE"
          ],
          [
            "pelo mundo",
            "PERSON"
          ],
          [
            "futebol",
            "GPE"
          ],
          [
            "sucesso pelo mundo",
            "PERSON"
          ]
        ],
        "readability_score": 84.1897212543554,
        "semantic_density": 0,
        "word_count": 287,
        "unique_words": 191,
        "lexical_diversity": 0.6655052264808362
      },
      "preservation_score": 1.1227197152894378e-05
    },
    {
      "id": 1,
      "text": "— 133 —acordo com o que nós analisamos perante o “melhor” para nós \\nmesmos.\\nNessa década veio a bossa nova (Vinícius de Moraes, Tom Jo -\\nbim, Erasmo Carlos, Roberto Carlos), poesia mais música jun -\\ntas, amor com sentimento em arte, música é arte da multidão. \\nNem sempre uma música vai ser boa ou ruim totalmente, ela \\nvai ser boa ou ruim proporcional ao seu sentimento diante \\ndaquela mesma música. Situações que você viveu com aquela \\nmúsica. Momentos que você só colocou aquela música para \\nficar te distraindo. Aquela música que fez você chorar. Aque -\\nla música que fez você odiar. Aquela música que você achou \\nruim, aquela música que você não entende nada, mas acha boa, \\naquela música que despertar um amor. Qualquer tipo de arte \\né a propagação do sentimento exercido na arte, perante a um \\nsentimento mútuo perante a mesma arte.\\nFutebol e música, duas artes adoradas pelo mundo todo, o Bra -\\nsil tinha tudo para ser foda!!! Todos nós sabemos que temos \\num padrão de felicidade e tristeza. O sentimento do brasileiro \\nna década de 50 era de amor, a arte no Brasil nessa década era \\nexaltando o amor diante de um viver feliz.\\nDécada de 60\\nComeçamos da mesma forma que a década de 50, ganhamos o \\ncampeonato mundial de futebol, o povo estava em êxtase com \\no futebol, com a arte gerando o caos dentro da sua própria \\nfelicidade.\\nA felicidade exaltada nos fizeram incomodar com quem não \\ngosta de ser feliz (regra, gera mais regra, que gera falta de liber -\\ndade). A liberdade de expressão, a liberdade em excesso traz \\n“benefícios maquiavélicos” , diante do incômodo ao outro que \\ncaos do passado sendo vivido no futuro editável.indd   133caos do passado sendo vivido no futuro editável.indd   133 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 219244,
      "chapter": 6,
      "page": 133,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 24.887686274509804,
      "complexity_metrics": {
        "word_count": 300,
        "sentence_count": 17,
        "paragraph_count": 1,
        "avg_sentence_length": 17.647058823529413,
        "avg_word_length": 4.74,
        "unique_word_ratio": 0.5833333333333334,
        "avg_paragraph_length": 300.0,
        "punctuation_density": 0.14333333333333334,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "música",
          "arte",
          "você",
          "aquela",
          "década",
          "sentimento",
          "amor",
          "perante",
          "ruim",
          "diante",
          "mesma",
          "futebol",
          "felicidade",
          "nessa",
          "carlos",
          "mais",
          "feliz",
          "caos",
          "regra",
          "gera"
        ],
        "entities": [
          [
            "133",
            "CARDINAL"
          ],
          [
            "nós analisamos perante o “melhor",
            "FAC"
          ],
          [
            "para nós \\nmesmos",
            "PERSON"
          ],
          [
            "Nessa",
            "ORG"
          ],
          [
            "Vinícius de Moraes",
            "ORG"
          ],
          [
            "Tom Jo -\\nbim",
            "PERSON"
          ],
          [
            "Erasmo Carlos",
            "PERSON"
          ],
          [
            "Roberto Carlos",
            "PERSON"
          ],
          [
            "poesia mais música jun -\\n",
            "PERSON"
          ],
          [
            "música é arte",
            "ORG"
          ]
        ],
        "readability_score": 89.75447058823529,
        "semantic_density": 0,
        "word_count": 300,
        "unique_words": 175,
        "lexical_diversity": 0.5833333333333334
      },
      "preservation_score": 1.2262432215044376e-05
    },
    {
      "id": 1,
      "text": "— 134 —não é feliz da mesma forma. Meu pensamento é correto diante \\nda sua forma de viver, controle da população perante a manter \\numa regra da minha certeza, de como é o certo de viver melhor \\ndo que você vive, perante a um contexto imposta por uma par -\\nte da sociedade.\\nVeio com força total o regime militar, gerando o caos no senti -\\nmento da arte aqui no Brasil, mudando a música em forma de \\npoesia romântica, para poesia protestante... Vieram os grandes \\nfestivais da música brasileira, nesse mesmo período o Brasil \\ndeixou de ganhar a Copa de 66, deixou de virar cartão pos -\\ntal perante ao mundo que tinha conquistado com as músicas \\ne o futebol, pois tinha virado uma vitrine mundial pela sua \\nprópria arte, regredindo na sua própria evolução, devido a sua \\nprópria “desvolução” . Criamos sentimentos de dor perante a \\narte, começamos a fazer músicas em forma de manifestação, \\nsurgindo grandes intérpretes da música (Elis Regina), pessoas \\nque cantavam com a alma, pessoas que cantavam como se “fos -\\nse para salvar vidas” . Nesse período, o Brasil passou o seu pior \\ncaos dos tempos modernos.\\nNo final da década, ganhamos um campeonato mundial na \\nbase da garra, um time que não tinha confiança do povo de ser \\ncapaz de ganhar aquele campeonato, jogando de uma forma \\ncomo nunca tinha sido vista antes, deixando o mundo em es -\\ntado de admiração perante aquela arte ali apresentada. Muita \\ngarra com muito amor.\\nDécada de 70\\nComeçamos o processo do movimento pela liberdade. E não \\níamos começar de forma diferente, pois o povo brasileiro têm \\numa energia de brigar com amor, não deixando os festivais aca -\\nbar e evoluindo o movimento pela liberdade de expressão e de \\ncaos do passado sendo vivido no futuro editável.indd   134caos do passado sendo vivido no futuro editável.indd   134 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 221108,
      "chapter": 6,
      "page": 134,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 31.31452380952381,
      "complexity_metrics": {
        "word_count": 315,
        "sentence_count": 12,
        "paragraph_count": 1,
        "avg_sentence_length": 26.25,
        "avg_word_length": 4.758730158730159,
        "unique_word_ratio": 0.5904761904761905,
        "avg_paragraph_length": 315.0,
        "punctuation_density": 0.12380952380952381,
        "line_break_count": 30,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "forma",
          "perante",
          "arte",
          "tinha",
          "como",
          "caos",
          "brasil",
          "música",
          "pela",
          "própria",
          "viver",
          "poesia",
          "grandes",
          "festivais",
          "nesse",
          "período",
          "deixou",
          "ganhar",
          "mundo",
          "músicas"
        ],
        "entities": [
          [
            "134",
            "CARDINAL"
          ],
          [
            "diante \\nda sua forma de viver",
            "PERSON"
          ],
          [
            "certo de viver melhor",
            "ORG"
          ],
          [
            "Veio",
            "PERSON"
          ],
          [
            "Brasil",
            "PERSON"
          ],
          [
            "forma de \\npoesia romântica",
            "PERSON"
          ],
          [
            "para poesia",
            "PERSON"
          ],
          [
            "Vieram",
            "PERSON"
          ],
          [
            "da música brasileira",
            "PERSON"
          ],
          [
            "deixou de virar",
            "ORG"
          ]
        ],
        "readability_score": 85.44738095238095,
        "semantic_density": 0,
        "word_count": 315,
        "unique_words": 186,
        "lexical_diversity": 0.5904761904761905
      },
      "preservation_score": 1.1591716540975364e-05
    },
    {
      "id": 1,
      "text": "— 135 —viver. Nessa década, o futebol era um futebol alegre, bonito de \\nse ver, as músicas começaram a ter palavras de amor, sofrimen -\\nto e liberdade (Tim Maia, Raul Seixas, Rita Lee), quase todos \\nos artistas que brigavam pela liberdade foram mortos, exilados \\nou presos. Na década de 70, esses mesmos artistas que foram \\npresos e exilados, voltaram para o Brasil, com o sentimento de \\nmuito amor, pois não deixaram de amar as pessoas próximas, \\njunto com a dor de ter vivido o que teve que ser vivido. Década \\nde 70, nós brasileiros estávamos em uma transição de regime, \\nentão a luta perante o regime militar e o regime militar pe -\\nrante a liberdade foram diminuindo os conflitos um para o \\noutro, não deixando de ter conflitos de ambas as partes, porém \\nao meu ver em fator histórico, menos agressivo que a década \\nde 60.\\nDécada de 80 \\nLiberdade\\nEssa década é a década que o brasileiro sente vontade de viver a \\nliberdade. Começamos a década com o movimento das diretas \\njá, com todos os artistas, todos os grandes líderes se juntaram, \\nfazendo o caos desistir de se manter no poder perante a liber -\\ndade. O futebol começou a aparecer para o mundo novamen -\\nte, inclusive foi através do meu time Flamengo, que ganhou \\no Campeonato Mundial de Clubes, voltando ao sentimento \\nde ganhar novamente um campeonato mundial com a seleção \\nbrasileira, transformando várias linhas de tempo em um sen -\\ntimento mútuo perante o querer viver a vida. Transformando \\ntodo esse sentimento de liberdade em música, vindo a década \\ndo Rock no Brasil como movimento de falar em liberdade, \\ncriando várias linhas de raciocínio, pensamentos diferentes, \\naceitação diferentes, movimentos ante preconceito aumentan -\\ncaos do passado sendo vivido no futuro editável.indd   135caos do passado sendo vivido no futuro editável.indd   135 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 223065,
      "chapter": 6,
      "page": 135,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 33.913430420711975,
      "complexity_metrics": {
        "word_count": 309,
        "sentence_count": 10,
        "paragraph_count": 1,
        "avg_sentence_length": 30.9,
        "avg_word_length": 4.922330097087379,
        "unique_word_ratio": 0.5954692556634305,
        "avg_paragraph_length": 309.0,
        "punctuation_density": 0.13915857605177995,
        "line_break_count": 30,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "década",
          "liberdade",
          "vivido",
          "viver",
          "futebol",
          "todos",
          "artistas",
          "sentimento",
          "regime",
          "perante",
          "amor",
          "exilados",
          "presos",
          "brasil",
          "militar",
          "conflitos",
          "movimento",
          "caos",
          "campeonato",
          "mundial"
        ],
        "entities": [
          [
            "135",
            "CARDINAL"
          ],
          [
            "Nessa",
            "PERSON"
          ],
          [
            "futebol",
            "GPE"
          ],
          [
            "bonito de \\nse ver",
            "PERSON"
          ],
          [
            "Tim Maia",
            "PERSON"
          ],
          [
            "Raul Seixas",
            "PERSON"
          ],
          [
            "Rita Lee",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "foram mortos",
            "PERSON"
          ],
          [
            "de 70",
            "PERSON"
          ]
        ],
        "readability_score": 83.07330097087379,
        "semantic_density": 0,
        "word_count": 309,
        "unique_words": 184,
        "lexical_diversity": 0.5954692556634305
      },
      "preservation_score": 1.1591716540975364e-05
    },
    {
      "id": 1,
      "text": "— 136 —do e ganhando espaço de igualdade perante a uma sociedade. \\nTodos sofriam preconceitos dentro daquilo que vivia, porém \\nalguns com mais facilidades por ter uma aceitação pela a sua \\naparência, diante de um “costume” de padrão comportamental \\nperante uma sociedade, sendo assim, tendo que lutar em me -\\nnos frentes perante o preconceito, ganhando espaço aos pou -\\ncos, proporcional ao tamanho do caos de tempo, proporcional \\nao tempo vivido por aquele caos (preconceitos em geral, pro -\\nporção de tempo que sofre, mais proporção da aceitação visual \\ne proporção com o maior poder monetário do meio em que se \\ntêm o próprio preconceito).\\nTivemos uma quebra muito grande, com o preconceito sexual \\nperante a homossexualidade, tivemos grandes artistas homos -\\nsexuais (Cazuza, Renato Russo), que conseguiram exaltar a sua \\ndor e ter uma proporção maior, devido a se ter mais pessoas \\nsemelhantes com poder na política, poder monetário, por ser \\nbranco (conforto visual criado, devido a se ter mais condições \\nfinanceiras, criando mais artes, criando uma linha de tempo \\nde história, tendo uma vida melhor, tendo mais conforto de \\nvida, dando condições de ter tempo para pensar no que você \\nestá precisando pensar, e não pensar por obrigação no caos que \\nvocê vive, fome). Nós somos frutos do meio em que vivemos, se \\nnão vivemos no meio que eu preciso viver, como eu chego até \\no meio social que eu quero ou preciso viver?\\nNa década de 80, também tivemos uma maior liberdade para \\nas mulheres, pois começamos a sair de um regime machista, \\nde “homem ser homem” e “mulher ser mulher” , aumentando a \\nliberdade da mulher de ter uma vida, diante do que eu quero \\nser perante minha própria vida. As mulheres começaram a ter \\npoder contra os homens, começamos a dar mais atenção, fazer \\nmais leis restritivas em o homem ter poder sobre a mulher. \\nNinguém tem que ter poder sobre ninguém, todos nós temos \\ncaos do passado sendo vivido no futuro editável.indd   136caos do passado sendo vivido no futuro editável.indd   136 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 225040,
      "chapter": 6,
      "page": 136,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 44.4702183121538,
      "complexity_metrics": {
        "word_count": 341,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 37.888888888888886,
        "avg_word_length": 4.9501466275659824,
        "unique_word_ratio": 0.5571847507331378,
        "avg_paragraph_length": 341.0,
        "punctuation_density": 0.1348973607038123,
        "line_break_count": 32,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "poder",
          "perante",
          "tempo",
          "caos",
          "meio",
          "vida",
          "mulher",
          "sendo",
          "tendo",
          "preconceito",
          "vivido",
          "proporção",
          "maior",
          "tivemos",
          "pensar",
          "homem",
          "ganhando",
          "espaço",
          "sociedade"
        ],
        "entities": [
          [
            "136",
            "CARDINAL"
          ],
          [
            "Todos",
            "GPE"
          ],
          [
            "monetário",
            "PERSON"
          ],
          [
            "preconceito",
            "PERSON"
          ],
          [
            "Tivemos",
            "PERSON"
          ],
          [
            "muito grande",
            "PERSON"
          ],
          [
            "tivemos",
            "PERSON"
          ],
          [
            "Cazuza",
            "PERSON"
          ],
          [
            "monetário",
            "PERSON"
          ],
          [
            "mais artes",
            "PERSON"
          ]
        ],
        "readability_score": 79.57051156728576,
        "semantic_density": 0,
        "word_count": 341,
        "unique_words": 190,
        "lexical_diversity": 0.5571847507331378
      },
      "preservation_score": 1.4930714135797195e-05
    },
    {
      "id": 1,
      "text": "— 137 —que fazer o melhor que pudermos em qualquer situação. A \\nmelhor forma de se viver a vida é se adaptar ao que têm que \\nse adaptar. Essa frase vêm de seus próprios questionamentos, \\ndiante do que você quer viver para o seu próprio futuro, se \\nvocê não tiver noção que você irá se adaptar, por que continuar \\nfazendo ou seguindo na mesma direção? Faça até o ponto, que \\nvocê consiga obter uma noção do futuro da adaptação do mes -\\nmo.\\nAeeee!!! Chegamos na década em que eu nasci, não que seja \\nimportante, porém necessária para compreender a forma como \\neu compreendi a minha vida, tornando a parte mais impor -\\ntante deste livro!!! Kkkkk Menos, menos... Nada é importante \\nperante a si próprio, pois, para você ser importante, outros fo -\\nram e são importantes para você. Eu, você, as pessoas de todo \\no mundo, não seriamos nada se não fossemos uma junção de \\nenergia, propagando em um tempo contínuo de si próprio, \\nem conjunto a energia onipresente do universo. Temos que \\nser um só, proporcional a um mundo material e ao mundo \\nsentimental (empatia, amor, caos, religião), mutuamente com \\no caos criado ao mundo.\\nDécada de 90\\nExtravagância da “liberdade”\\nEsse momento em que passamos por um período de caos, o \\npovo está exaltando os seus sentimentos, temos o sertanejo ro -\\nmântico do interior (Chitãozinho e Xororó, Leandro e Leonar -\\ndo, Zezé de Camargo e Luciano), temos o pagode romântico \\n(Raça Negra, Só pra Contrariar) temos as músicas animadas (É \\no Tchan, Molejo, axé), temos as músicas de “caos” (Racionais, \\nfunk). Estávamos cheios de opiniões, cheios de vida perante \\numa energia de local para local, aumentando a discrepância \\ncaos do passado sendo vivido no futuro editável.indd   137caos do passado sendo vivido no futuro editável.indd   137 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 227218,
      "chapter": 6,
      "page": 137,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 27.38515037593985,
      "complexity_metrics": {
        "word_count": 304,
        "sentence_count": 14,
        "paragraph_count": 1,
        "avg_sentence_length": 21.714285714285715,
        "avg_word_length": 4.855263157894737,
        "unique_word_ratio": 0.631578947368421,
        "avg_paragraph_length": 304.0,
        "punctuation_density": 0.18421052631578946,
        "line_break_count": 30,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "temos",
          "caos",
          "futuro",
          "mundo",
          "vida",
          "adaptar",
          "próprio",
          "importante",
          "energia",
          "melhor",
          "forma",
          "viver",
          "seus",
          "noção",
          "década",
          "menos",
          "nada",
          "perante",
          "músicas"
        ],
        "entities": [
          [
            "137",
            "CARDINAL"
          ],
          [
            "melhor que",
            "ORG"
          ],
          [
            "qualquer situação",
            "PERSON"
          ],
          [
            "melhor forma de se",
            "PERSON"
          ],
          [
            "viver para o",
            "PERSON"
          ],
          [
            "irá se adaptar",
            "PERSON"
          ],
          [
            "Faça",
            "PERSON"
          ],
          [
            "Aeeee",
            "PERSON"
          ],
          [
            "Chegamos",
            "PERSON"
          ],
          [
            "eu nasci",
            "PERSON"
          ]
        ],
        "readability_score": 87.68627819548873,
        "semantic_density": 0,
        "word_count": 304,
        "unique_words": 192,
        "lexical_diversity": 0.631578947368421
      },
      "preservation_score": 1.6840795729341564e-05
    },
    {
      "id": 1,
      "text": "— 138 —social, diferenciando ainda mais as classes sociais, devido à fal -\\nsa liberdade de nos dar um conforto perante a vida em que es -\\ntávamos vivendo. A balança de um viver feliz com simplicida -\\nde, aumentou a ganância de quem já tinha ganância, gerando \\no interesse pessoal de se ter muito perante a vida do outro. Eu \\npreciso “viver” melhor que você.\\nNessa década, tivemos mais uma vitória da seleção brasileira de \\nfutebol, ofuscando o caos em que a economia se encontrava, \\ncom um novo Plano Real (Fernando Henrique) para tentar \\nconter a inflação, devido aos nossos próprios excessos anterio -\\nres, ocasionando uma medida drástica que afetou muitas fa -\\nmílias. Antes da Copa, viemos de uma tentativa frustrada do \\nPlano Collor de conter a inflação, tirando todas as economias \\ndo próprio povo, pelo próprio erro de nós mesmos perante \\nnossa própria ganância, transformando a nossa luxúria no nos -\\nso próprio caos.\\nNo decorrer da década, nós viemos semelhante ao mundo, \\nporém menos desenvolvidos, com problemas diante do caos \\nda sociedade semelhante aos de outros países, expandindo a \\nganância pelo monetário, devido a enxergar uma melhor qua -\\nlidade de vida diante do outro que vive no “mesmo local” que \\nvocê.\\nComeçamos a viver a propagação da notícia simultaneamen -\\nte ao acontecimento, causa, efeito e percepção ao caos o qual \\n“não te prejudicava” .\\nGerando muito entendimento e a falta de entendimento por \\nnão saber interpretar os erros vistos e os seus próprios erros, \\ncom questionamentos e visões totalmente destoados, ao ver os \\nacontecimentos comparada com a sua interpretação, diante da \\nsua linha de tempo, ocasionando um boom de julgamentos, \\npreconceitos, ganância, certezas, extravagância, superego pe -\\ncaos do passado sendo vivido no futuro editável.indd   138caos do passado sendo vivido no futuro editável.indd   138 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 229142,
      "chapter": 6,
      "page": 138,
      "segment_type": "page",
      "themes": {},
      "difficulty": 33.79638157894737,
      "complexity_metrics": {
        "word_count": 304,
        "sentence_count": 10,
        "paragraph_count": 1,
        "avg_sentence_length": 30.4,
        "avg_word_length": 5.154605263157895,
        "unique_word_ratio": 0.6151315789473685,
        "avg_paragraph_length": 304.0,
        "punctuation_density": 0.13815789473684212,
        "line_break_count": 31,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "ganância",
          "caos",
          "devido",
          "perante",
          "vida",
          "viver",
          "próprio",
          "diante",
          "mais",
          "gerando",
          "muito",
          "outro",
          "melhor",
          "você",
          "década",
          "plano",
          "conter",
          "inflação",
          "próprios",
          "ocasionando"
        ],
        "entities": [
          [
            "138",
            "CARDINAL"
          ],
          [
            "ainda mais",
            "PERSON"
          ],
          [
            "de se",
            "PERSON"
          ],
          [
            "muito perante",
            "PERSON"
          ],
          [
            "Nessa",
            "PERSON"
          ],
          [
            "tivemos mais",
            "PERSON"
          ],
          [
            "vitória da seleção",
            "PERSON"
          ],
          [
            "brasileira de \\nfutebol",
            "PERSON"
          ],
          [
            "Plano Real",
            "ORG"
          ],
          [
            "Fernando Henrique",
            "PERSON"
          ]
        ],
        "readability_score": 83.25361842105264,
        "semantic_density": 0,
        "word_count": 304,
        "unique_words": 187,
        "lexical_diversity": 0.6151315789473685
      },
      "preservation_score": 1.3786123257222901e-05
    },
    {
      "id": 1,
      "text": "— 139 —rante sua própria “ liberdade” .\\nNovo milênio\\nAhhh, o início só teve merda!!! No início do novo milênio, \\ncomeçamos a ter muita música exaltando o sexo no mundo \\ntodo, o sexo era tudo que era necessário, voltando aos tempos \\ndos primórdios, sem controle do seu próprio desejo sexual... \\nAs músicas, as roupas, as danças, as propagandas quase tudo \\nnessa época exalava o apetite sexual... As músicas eram funks  \\ndo tipo: pau na buceta, buceta no pau. As danças junto com as \\nroupas eram uma maravilha para a minha idade. kkkkk\\nO hip-hop  americano aqui no Brasil ganhou uma proporção \\nabsurda, pois as músicas exalavam sexo.\\nEnquanto os Estados Unidos estavam sofrendo pelo próprio \\ncaos (Torres Gêmeas, por sempre estar dando a cara a tapa, \\numa hora o tapa volta para você. Infelizmente tivemos uma \\ngrande catástrofe, mostrando o pior da ganância, o “ganhar” \\nsempre, não quer dizer que você está no controle. A paciência, \\no caos, o amor pelo próximo dentro do meio em que eu vivo, \\ntransforma a sua dor semelhante à minha, ocasionando o caos \\ndentro caos que eu estou criando.\\nNo decorrer do novo milênio, tivemos uma nova vitória na \\nCopa do Mundo. Tínhamos um novo presidente, presidente \\nLula, do “povo” , entendia sobre a dor do pobre. Inicialmente, \\nessa junção deu muito certo. Mas, após o primeiro mandato, \\no fazer o bem se perdeu no que era necessário para conseguir \\nse fazer o bem. A jogada política feita para ter uma evolução \\nterritorial teve que ter subornos, roubos, eu só faço se você me \\nder dinheiro de volta. Mais uma vez a ganância de si próprio \\nvoltou para nós mesmos, em escala maior do que para só para \\ncaos do passado sendo vivido no futuro editável.indd   139caos do passado sendo vivido no futuro editável.indd   139 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 231154,
      "chapter": 6,
      "page": 139,
      "segment_type": "page",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 24.938032786885245,
      "complexity_metrics": {
        "word_count": 305,
        "sentence_count": 18,
        "paragraph_count": 1,
        "avg_sentence_length": 16.944444444444443,
        "avg_word_length": 4.79344262295082,
        "unique_word_ratio": 0.6655737704918033,
        "avg_paragraph_length": 305.0,
        "punctuation_density": 0.18688524590163935,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "caos",
          "novo",
          "milênio",
          "sexo",
          "próprio",
          "músicas",
          "você",
          "início",
          "teve",
          "mundo",
          "tudo",
          "necessário",
          "controle",
          "sexual",
          "roupas",
          "danças",
          "eram",
          "buceta",
          "minha",
          "pelo"
        ],
        "entities": [
          [
            "139",
            "CARDINAL"
          ],
          [
            "novo milênio",
            "PERSON"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "desejo",
            "PERSON"
          ],
          [
            "nessa",
            "PERSON"
          ],
          [
            "pau na buceta",
            "PERSON"
          ],
          [
            "Brasil",
            "PERSON"
          ],
          [
            "Enquanto os Estados Unidos",
            "ORG"
          ],
          [
            "pelo próprio \\ncaos",
            "PERSON"
          ]
        ],
        "readability_score": 90.08974499089253,
        "semantic_density": 0,
        "word_count": 305,
        "unique_words": 203,
        "lexical_diversity": 0.6655737704918033
      },
      "preservation_score": 1.4165223420827126e-05
    },
    {
      "id": 1,
      "text": "— 140 —si, com todos os brasileiros pagando pela própria ganância, do \\nseu próprio sistema político de querer “melhorar” , melhorando \\na quem têm muito mais pela sua ganância de ter mais, sendo \\nproporcional a quantidade de 1000 mil pessoas que poderiam \\nviver com aquela mesma quantidade de recursos monetário, \\nque apenas só uma família vive. A sua luxúria o faz gerar o caos \\nde quem não tem nada a ver com sua própria luxúria.\\nNo final dessa mesma década, tivemos outra queda da bolsa \\ndevido ao consumo excessivo de nós mesmos. Comprávamos \\nimóveis, carros, barcos tudo em forma de financiamento. As \\ntaxas de juros baixas, crédito ao cliente, liberação de emprés -\\ntimo, financiamentos sem comprovar renda, o sistema entrou \\nem colapso. A melhor analogia que se pode usar é Ouroboros, \\no símbolo da serpente comendo o seu próprio rabo.\\nPrimeira década do novo milênio\\nComeçamos muito bem... Começamos a década com um ca -\\ntaclismo que já se foi falado aqui mesmo neste livro, o terre -\\nmoto do Haiti. Como eu falei lá atrás, os grandes cataclismos \\nocorrem onde tem mais energia e caos, a oscilação da energia \\nterritorial nos faz aumentar a quantidade de massa próximo \\nao caos que nós mesmo criamos. Nos últimos 100 anos, o caos \\ntem se propagado de uma forma concentrada em lugares que \\nnão tinham tanto caos, a Europa e no Oriente Médio. Hoje em \\ndia, as maiores catástrofes do mundo são onde tem a maior \\nquantidade de caos (Ásia, região árabe e América do Norte). \\nTivemos um terremoto no Chile também em 2010. Todos os \\nsintomas de que estamos totalmente fora do eixo da Terra, oca -\\nsionando mais movimentação do magma, o deixando mais “es -\\ntressado” , com possibilidade de ocorrer novas erupções devido \\nao estresse de estar em atrito, gerando muita energia, entrando \\ncaos do passado sendo vivido no futuro editável.indd   140caos do passado sendo vivido no futuro editável.indd   140 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 233070,
      "chapter": 7,
      "page": 140,
      "segment_type": "page",
      "themes": {},
      "difficulty": 31.39560327198364,
      "complexity_metrics": {
        "word_count": 326,
        "sentence_count": 15,
        "paragraph_count": 1,
        "avg_sentence_length": 21.733333333333334,
        "avg_word_length": 4.874233128834356,
        "unique_word_ratio": 0.647239263803681,
        "avg_paragraph_length": 326.0,
        "punctuation_density": 0.13803680981595093,
        "line_break_count": 30,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "caos",
          "mais",
          "quantidade",
          "sendo",
          "década",
          "energia",
          "todos",
          "pela",
          "própria",
          "ganância",
          "próprio",
          "sistema",
          "quem",
          "muito",
          "mesma",
          "luxúria",
          "tivemos",
          "devido",
          "forma",
          "começamos"
        ],
        "entities": [
          [
            "140",
            "CARDINAL"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "própria ganância",
            "PERSON"
          ],
          [
            "político de querer “melhorar",
            "ORG"
          ],
          [
            "muito mais pela sua ganância de ter mais",
            "PERSON"
          ],
          [
            "aquela mesma quantidade de recursos monetário",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "tivemos outra",
            "ORG"
          ],
          [
            "de nós mesmos",
            "PERSON"
          ],
          [
            "taxas de juros baixas",
            "PERSON"
          ]
        ],
        "readability_score": 87.67106339468303,
        "semantic_density": 0,
        "word_count": 326,
        "unique_words": 211,
        "lexical_diversity": 0.647239263803681
      },
      "preservation_score": 1.268527470521832e-05
    },
    {
      "id": 1,
      "text": "— 141 —em colapso devido a não conseguir conter a energia, entrando \\nem erupção pela abertura que dá para desestressar.\\nA música e a tecnologia tiveram grandes avanços nessa última \\ndécada, tivemos aprimoramentos tecnológicos esperados para \\ndaqui a tantos anos, acontecendo em um ano. As músicas estão \\ncada vez mais variadas, criando variações de gosto musicais de \\ntodas as formas, criando sentimentos novos perante o querer \\nser ou ter, caos, depressão, ansiedade, cobrança diante de um \\nviver, egocentrismo, ganância. Estamos vivendo em um mun -\\ndo de ciclos viciosos, perante a nossa própria forma de que -\\nrer viver a vida, ao mesmo tempo sendo criado muitas regras \\npara conter quem eu não quero que melhore, transformando o \\nmeu querer acima de tudo e de todos, nos transformando em \\num sistema sem balanceamento, nós fazendo criar caos, mais \\ncatástrofes e cataclismo nós tornando reféns da sobrevivência \\nde um querer do universo.\\nNo decorrer dessa década, tivemos todos os tipos de disputas, \\ntivemos todos os tipos de ganância, tivemos todos os tipos de \\neu ser melhor que você, sou mais forte que você, gasto mais \\nque você.\\nE para nos “contemplar” com um pós-cataclismo, estamos no \\nmeio de uma pandemia a dois anos. O que isso te lembra?\\nEssa linha de tempo é relativa de uma energia de propagação, \\na nossa necessidade de nos mantermos em um ciclo perante a \\nenergia da Terra, sistema solar, galáxia e universo na proporção \\nda ação e reação de si próprio, perante uma ligação da energia \\nuniversal, com os fatos mais marcantes até o ano de 1950, se -\\nguindo uma linha de tempo religiosa, filosófica, matemática, \\nfísica, amor e caos.\\nIrei colocar um gráfico de absorção e necessidade básica de \\nviver de um ser humano, que acabou de nascer até aproxi -\\ncaos do passado sendo vivido no futuro editável.indd   141caos do passado sendo vivido no futuro editável.indd   141 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 235130,
      "chapter": 7,
      "page": 141,
      "segment_type": "page",
      "themes": {
        "ciencia": 56.52173913043479,
        "tecnologia": 43.47826086956522
      },
      "difficulty": 35.03885077186964,
      "complexity_metrics": {
        "word_count": 318,
        "sentence_count": 11,
        "paragraph_count": 1,
        "avg_sentence_length": 28.90909090909091,
        "avg_word_length": 4.977987421383648,
        "unique_word_ratio": 0.610062893081761,
        "avg_paragraph_length": 318.0,
        "punctuation_density": 0.1509433962264151,
        "line_break_count": 31,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "energia",
          "tivemos",
          "perante",
          "caos",
          "todos",
          "querer",
          "viver",
          "tempo",
          "sendo",
          "tipos",
          "você",
          "conter",
          "década",
          "anos",
          "criando",
          "ganância",
          "estamos",
          "nossa",
          "transformando"
        ],
        "entities": [
          [
            "141",
            "CARDINAL"
          ],
          [
            "abertura que dá para desestressar",
            "PERSON"
          ],
          [
            "última \\ndécada",
            "PERSON"
          ],
          [
            "tivemos aprimoramentos",
            "PERSON"
          ],
          [
            "tecnológicos esperados",
            "PERSON"
          ],
          [
            "cada vez mais",
            "ORG"
          ],
          [
            "depressão",
            "GPE"
          ],
          [
            "cobrança diante de um \\n",
            "PERSON"
          ],
          [
            "Estamos",
            "PERSON"
          ],
          [
            "de ciclos viciosos",
            "PERSON"
          ]
        ],
        "readability_score": 84.05205831903945,
        "semantic_density": 0,
        "word_count": 318,
        "unique_words": 194,
        "lexical_diversity": 0.610062893081761
      },
      "preservation_score": 1.2882115174782053e-05
    },
    {
      "id": 1,
      "text": "— 142 —madamente 3 anos de idade, em um gráfico de necessidade \\n“perfeita” para se viver dentro de uma necessidade de se ter o \\nnecessário proporcional a idade.\\nMemória afetiva\\nCriando lembranças boas e ruins (memórias afetivas) diante \\nda nossa vida no meio em que vivemos.\\nLembranças boas se criam com as limitações das pessoas que \\nestão mais próximos de nós. Aprendizado de fazer algo para \\nganhar algo, aprendizado do benefício e malefício.\\nLembranças ruins são a ausência do necessário!! Comida, bebi -\\nda, amor, carinho, conforto.\\nMemória construtiva \\nMemória construtiva se criam pela constância de se fazer algo \\nque é necessário!! Memória repetitiva, comer, beber água, usar \\nbanheiro, tomar banho, escovar os dentes...\\nMeio em que vivemos é necessário termos para criarmos boas \\nou má características diante das nossas pré-características que \\nvem no nosso DNA.\\nNós viemos com impulsos no nosso DNA, nascemos curiosos, \\nsorridentes, agressivos, cansados, preguiçosos. Essas caracterís -\\nticas têm benefícios e malefícios, de acordo com as pessoas que \\nvivem em nossa volta, pois mesmo sabendo lidar com a situa -\\nção das pré-características, podendo ser melhor direcionado \\ndiante de uma necessidade de uma sociedade.\\nProblemas se criam devido a não ter algo sem motivo.\\nProblemas são necessários para valores futuros, pois sem pro -\\ncaos do passado sendo vivido no futuro editável.indd   142caos do passado sendo vivido no futuro editável.indd   142 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 237176,
      "chapter": 7,
      "page": 142,
      "segment_type": "page",
      "themes": {},
      "difficulty": 24.34410480349345,
      "complexity_metrics": {
        "word_count": 229,
        "sentence_count": 15,
        "paragraph_count": 1,
        "avg_sentence_length": 15.266666666666667,
        "avg_word_length": 5.4803493449781655,
        "unique_word_ratio": 0.6419213973799127,
        "avg_paragraph_length": 229.0,
        "punctuation_density": 0.18340611353711792,
        "line_break_count": 26,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "necessário",
          "memória",
          "algo",
          "necessidade",
          "lembranças",
          "boas",
          "diante",
          "criam",
          "características",
          "idade",
          "ruins",
          "nossa",
          "meio",
          "vivemos",
          "pessoas",
          "aprendizado",
          "fazer",
          "construtiva",
          "nosso",
          "pois"
        ],
        "entities": [
          [
            "142",
            "CARDINAL"
          ],
          [
            "3",
            "CARDINAL"
          ],
          [
            "para se viver dentro de uma",
            "PERSON"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "Memória",
            "GPE"
          ],
          [
            "Criando",
            "PRODUCT"
          ],
          [
            "boas e ruins",
            "ORG"
          ],
          [
            "Lembranças",
            "PERSON"
          ],
          [
            "limitações das pessoas que \\nestão mais próximos de nós",
            "PERSON"
          ],
          [
            "Aprendizado de fazer",
            "ORG"
          ]
        ],
        "readability_score": 90.72256186317321,
        "semantic_density": 0,
        "word_count": 229,
        "unique_words": 147,
        "lexical_diversity": 0.6419213973799127
      },
      "preservation_score": 1.0235704417314092e-05
    },
    {
      "id": 1,
      "text": "— 143 —blemas não conseguiríamos evoluir, não iríamos ver benefí -\\ncios na vida diante de querer melhorar a própria vida, pois \\nos problemas são criados da seguinte forma: eu estar certo e \\nentender que é um erro ou acerto, de acordo com o meio em \\nque eu vivo.\\nImportância é a junção de todos os fatores que ocorrem em \\nsua volta.\\nImportância se cria com a sua ausência ou com os nossos ex -\\ncessos no meio em que nós vivemos, junto com o nosso DNA, \\ncriando uma importância diante da nossa necessidade, de acor -\\ndo com o meio em que vivemos nos transformando em pes -\\nsoas futuras com importância boas ou ruins.\\nOscilações de absorção\\nA.  Lembranças boas.\\nB.  Colo de quem vai te dar amor, criar, meio em que vivemos.\\nC.  Importância, família.\\nD.  Amamentação e uma linha de tempo contínua em \\n      evolução de adaptação.\\nE.  Nascimento e início da construção da memória construtiva.\\nF .  Sobrevivência e problema.\\nG.  Necessidade básica, lembrança de dor.\\nH.  Necessidade básica.\\ncaos do passado sendo vivido no futuro editável.indd   143caos do passado sendo vivido no futuro editável.indd   143 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 238796,
      "chapter": 7,
      "page": 143,
      "segment_type": "page",
      "themes": {},
      "difficulty": 20.845360339142722,
      "complexity_metrics": {
        "word_count": 193,
        "sentence_count": 22,
        "paragraph_count": 1,
        "avg_sentence_length": 8.772727272727273,
        "avg_word_length": 4.787564766839378,
        "unique_word_ratio": 0.6735751295336787,
        "avg_paragraph_length": 193.0,
        "punctuation_density": 0.18652849740932642,
        "line_break_count": 22,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "importância",
          "meio",
          "vivemos",
          "necessidade",
          "vida",
          "diante",
          "boas",
          "básica",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "blemas",
          "conseguiríamos",
          "evoluir",
          "iríamos",
          "benefí",
          "cios"
        ],
        "entities": [
          [
            "143",
            "CARDINAL"
          ],
          [
            "não conseguiríamos evoluir",
            "PERSON"
          ],
          [
            "não iríamos",
            "GPE"
          ],
          [
            "problemas são",
            "ORG"
          ],
          [
            "da seguinte forma",
            "PERSON"
          ],
          [
            "eu estar",
            "PERSON"
          ],
          [
            "eu",
            "PERSON"
          ],
          [
            "Importância se cria",
            "PERSON"
          ],
          [
            "de acor -\\n",
            "PERSON"
          ],
          [
            "Oscilações de absorção\\nA.  Lembranças",
            "ORG"
          ]
        ],
        "readability_score": 94.17736693358455,
        "semantic_density": 0,
        "word_count": 193,
        "unique_words": 130,
        "lexical_diversity": 0.6735751295336787
      },
      "preservation_score": 6.736318291736626e-06
    },
    {
      "id": 1,
      "text": "— 144 —Desenvolvimento de pensamentos\\nQuando eu comecei a escrever meus pensamentos, foi em uma \\nforma de fuga do meu próprio caos, me tornando refém do \\nsentimento que eu não conseguia interpretar, por não enten -\\nder o motivo da dor que eu sentia, perante não entender o \\nmotivo da minha própria dor, me levando a estudar o início \\ndo comportamento humano.\\nAo começar a estudar, eu percebia que muitos, muitos mesmos \\npassavam por situações piores que a minha, porém a minha era \\n“pior” diante de mim mesmo, me transformando em um ciclo \\nde viver em fuga.\\nNo início do meu caos (depressão), eu não percebi que esta -\\nva em depressão, pois eu vivia bebendo, fugindo da minha \\nprópria tristeza com pequenos momentos de felicidade, me \\ntransformando em um ciclo infinito de felicidade e caos. No \\ndecorrer da depressão e eu perceber que estava em depressão, \\nme levando a estudar a mente de pessoas semelhantes à mente \\nda minha ex. Como eu trabalho com público, foi mais fácil eu \\ndecifrar o comportamento humano devido a eu trabalhar com \\ncaos do passado sendo vivido no futuro editável.indd   144caos do passado sendo vivido no futuro editável.indd   144 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 240056,
      "chapter": 7,
      "page": 144,
      "segment_type": "page",
      "themes": {},
      "difficulty": 30.65714285714286,
      "complexity_metrics": {
        "word_count": 199,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 28.428571428571427,
        "avg_word_length": 4.919597989949748,
        "unique_word_ratio": 0.592964824120603,
        "avg_paragraph_length": 199.0,
        "punctuation_density": 0.12562814070351758,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "minha",
          "caos",
          "depressão",
          "estudar",
          "pensamentos",
          "fuga",
          "motivo",
          "própria",
          "levando",
          "início",
          "comportamento",
          "humano",
          "muitos",
          "transformando",
          "ciclo",
          "felicidade",
          "mente",
          "passado",
          "sendo",
          "vivido"
        ],
        "entities": [
          [
            "144",
            "CARDINAL"
          ],
          [
            "Quando eu",
            "PERSON"
          ],
          [
            "que eu não",
            "PERSON"
          ],
          [
            "eu sentia",
            "PERSON"
          ],
          [
            "eu percebia que",
            "PERSON"
          ],
          [
            "diante de mim mesmo",
            "PERSON"
          ],
          [
            "eu não percebi",
            "PERSON"
          ],
          [
            "eu vivia",
            "PERSON"
          ],
          [
            "fugindo da minha \\n",
            "PERSON"
          ],
          [
            "infinito de felicidade",
            "ORG"
          ]
        ],
        "readability_score": 84.30983488872937,
        "semantic_density": 0,
        "word_count": 199,
        "unique_words": 118,
        "lexical_diversity": 0.592964824120603
      },
      "preservation_score": 4.571073126535567e-06
    },
    {
      "id": 1,
      "text": "— 145 —muitas pessoas, isso me fez enxergar padrões comportamentais \\ndiante de mim mesmo.\\n Me levando a um poço, contendo água até o meu pescoço, \\nsem conseguir enxergar a saída, me fazendo me aprofundar \\nna minha própria vida e compreender o motivo da minha dor. \\nApós o nascimento do meu filho, a mãe dele levou ponto da \\nbuceta ao ânus, demorando a cicatrização, dificultando por \\nmuitas vezes ela ir ao banheiro, gritava de dor e, quando nós \\nfomos fazer sexo, ela pediu para parar, pois estava doendo mui -\\nto, parei. Na outra tentativa, ela pediu para continuar fazendo \\nela sentir dor ao ponto de criar uma repelência por mim, se \\nsentindo “estuprada” pelo seu marido, que ela amava e que ele \\ntambém a amava. Até então, nunca tínhamos brigado, começa -\\nmos a ter brigas toda hora pela ausência do sexo, me fazendo \\npor muitas vezes chorar por não entender o motivo. \\nSó vim descobrir o motivo após dez anos, ao me entender e \\nentender a dor do outro, através de amigas que me falavam \\nque a sensação de se sentir estuprada é horrível (um “amigo” \\ndo pai dessa minha amiga, colocou a mão na perna e ela se \\nsentiu impotente por não saber o que fazer). Redimensionei \\na sensação com mais a sensação da mulher perante o sexo, me \\nfez perceber esse caos criado pelo excesso de amor. Após tantas \\nbrigas, após não sabermos o motivo do início do caos, já era \\ntarde, pois tinha acabado o respeito, amor, confiança, compa -\\nnheirismo, vida social, meio em que vivemos, estilo de vida. \\nNo decorrer de querer descobrir a minha dor, eu fui me apro -\\nfundando cada vez mais e mais, perante o quanto eu “sofri” \\nsem perceber que era para eu ter sofrido, me fazendo pensar e \\nanalisar valores necessários para ser feliz.\\nNo planeta Terra, nós somos os únicos animais que conseguem \\nter o prazer quando querem ter prazer.\\ncaos do passado sendo vivido no futuro editável.indd   145caos do passado sendo vivido no futuro editável.indd   145 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 241371,
      "chapter": 7,
      "page": 145,
      "segment_type": "page",
      "themes": {},
      "difficulty": 29.669522314420274,
      "complexity_metrics": {
        "word_count": 343,
        "sentence_count": 13,
        "paragraph_count": 1,
        "avg_sentence_length": 26.384615384615383,
        "avg_word_length": 4.667638483965015,
        "unique_word_ratio": 0.6180758017492711,
        "avg_paragraph_length": 343.0,
        "punctuation_density": 0.14868804664723032,
        "line_break_count": 31,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "fazendo",
          "minha",
          "motivo",
          "após",
          "muitas",
          "vida",
          "sexo",
          "entender",
          "sensação",
          "mais",
          "caos",
          "enxergar",
          "ponto",
          "vezes",
          "quando",
          "fazer",
          "pediu",
          "pois",
          "sentir",
          "estuprada"
        ],
        "entities": [
          [
            "145",
            "CARDINAL"
          ],
          [
            "fez enxergar padrões comportamentais",
            "ORG"
          ],
          [
            "diante de mim mesmo",
            "PERSON"
          ],
          [
            "contendo água até",
            "ORG"
          ],
          [
            "Após",
            "PERSON"
          ],
          [
            "gritava de dor e",
            "PERSON"
          ],
          [
            "quando",
            "PERSON"
          ],
          [
            "ela pediu",
            "PERSON"
          ],
          [
            "para parar",
            "PERSON"
          ],
          [
            "ela pediu para continuar",
            "PERSON"
          ]
        ],
        "readability_score": 85.4074007625028,
        "semantic_density": 0,
        "word_count": 343,
        "unique_words": 212,
        "lexical_diversity": 0.6180758017492711
      },
      "preservation_score": 1.4690131339663746e-05
    },
    {
      "id": 1,
      "text": "— 146 —Na maioria das vezes, sendo refém do meu próprio instinto \\nprimário da necessidade sexual, me transformando em uma \\npessoa materialista perante a vontade de fazer sexo, pela fuga \\nde não ter aquilo que eu queria (família), por fugir dos meus \\npróprios problemas.\\nNessa caminhada de descobrimento pessoal, junto ao meu \\ntrabalho, no qual eu falo com 30 pessoas diferentes quase to -\\ndos os dias, me fizeram perceber um padrão comportamental \\ndiante do que acontece em nossa volta, me fazendo perceber \\ncomo falar, conversar perante minha própria necessidade.\\nNesse período, 24 anos até os 35 anos, eu fiz várias loucuras co -\\nmigo mesmo. Eu cheguei a 110 kg, eu fiquei sem beber duran -\\nte dois anos, fiquei sem fazer sexo mais de um ano, trabalhei 17 \\nhoras por dia durante 6 meses para construir uma casa, cuidei \\ndo meu filho de 1 ano até os 11 anos dele, tudo isso sempre \\nanalisando, interpretando e compreendendo um contexto de \\nretorno de caos e felicidades perante mim mesmo.\\nQuando cheguei ao auge da depressão, eu tive pessoas com \\nquem eu pudesse contar, me guiar, amar, cuidar, compreender, \\nadmirar, sustentar, valorizar, brigar, apoiar, todos os valores ne -\\ncessários que uma pessoa com família e amigos possa ter.\\nQuando fui a alguns psicólogos, eu começava a falar com eles, \\npercebia que ficavam perdidos diante dos meus pensamentos, \\ndiante de mim mesmo, pois eu me conhecia ao ponto de não \\nme preocupar com nada que tinha acontecido na minha vida, \\nsó com o fator da separação.\\nEu ia falando todos os meus “traumas” e nenhum desses mes -\\nmos “traumas” eram traumas, pois os meus “traumas” foram \\n“irrelevantes” perante o meu maior trauma. A minha primeira \\nvez em uma psicóloga, ela chorou comovida. A segunda, a mes -\\nma coisa. A terceira foi interessante, pois realmente eu tinha \\ncaos do passado sendo vivido no futuro editável.indd   146caos do passado sendo vivido no futuro editável.indd   146 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 243463,
      "chapter": 7,
      "page": 146,
      "segment_type": "page",
      "themes": {},
      "difficulty": 30.226219512195122,
      "complexity_metrics": {
        "word_count": 328,
        "sentence_count": 12,
        "paragraph_count": 1,
        "avg_sentence_length": 27.333333333333332,
        "avg_word_length": 4.920731707317073,
        "unique_word_ratio": 0.6554878048780488,
        "avg_paragraph_length": 328.0,
        "punctuation_density": 0.15853658536585366,
        "line_break_count": 31,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "perante",
          "meus",
          "anos",
          "traumas",
          "sendo",
          "diante",
          "minha",
          "mesmo",
          "pois",
          "necessidade",
          "pessoa",
          "fazer",
          "sexo",
          "família",
          "pessoas",
          "perceber",
          "falar",
          "cheguei",
          "fiquei",
          "caos"
        ],
        "entities": [
          [
            "146",
            "CARDINAL"
          ],
          [
            "que eu queria",
            "PERSON"
          ],
          [
            "família",
            "ORG"
          ],
          [
            "Nessa",
            "ORG"
          ],
          [
            "eu falo",
            "PERSON"
          ],
          [
            "30",
            "CARDINAL"
          ],
          [
            "fizeram",
            "ORG"
          ],
          [
            "perceber",
            "PERSON"
          ],
          [
            "Nesse",
            "ORG"
          ],
          [
            "24",
            "CARDINAL"
          ]
        ],
        "readability_score": 84.85711382113821,
        "semantic_density": 0,
        "word_count": 328,
        "unique_words": 215,
        "lexical_diversity": 0.6554878048780488
      },
      "preservation_score": 1.58201414427148e-05
    },
    {
      "id": 1,
      "text": "— 147 —uma lacuna em minha vida, me fazendo perceber que eu tinha \\ndefeitos devido àquela lacuna. Fiquei com essa quase 2 meses e \\npercebi que ela se perdeu.\\nFui em outra psicóloga, agora em terapia de casal com minha \\nex, na intenção de viver uma vida em “família” . Nessa vez em \\nque eu fui com ela na psicóloga, eu falei sobre como tudo \\naconteceu e minha ex concordava e só falava que não me ama -\\nva, e não sabia o motivo, só não me amava.\\nDesisti finalmente de ficar com a minha ex.\\nContinuei indo nessa psicóloga durante um mês. Mais uma \\nvez percebi que nós somos tratados igual a um cachorro ades -\\ntrado perante a necessidade do seu dono (sociedade), chegan -\\ndo ao ponto de o psicólogo querer me enviar para o psiquiatra, \\npor não conseguir acompanhar o meu raciocínio, por ele estar \\nmuito acelerado e não conseguia acompanhar o meu pensa -\\nmento. Eu sou contra remédio para a mente humana, remédio \\né necessário quando se está doente, a mente humana fica doen -\\nte devido a você não a usar corretamente. Assim como você faz \\nexercícios para o seu corpo, temos que fazer exercícios para a \\nnossa mente.\\nEntão, eu fui me aprofundando cada vez mais e mais na mi -\\nnha própria mente, percebendo ciclos infinitos de si próprio \\nperante a repetição dos acontecimentos, virando ciclos de si \\npróprio diante do seu ciclo proporcional ao ciclo que você está \\nvivendo, devido ao meio em que você vive e viveu a vida toda, \\nnos transformando receptores de energia, proporcional ao que \\nnós mesmos vivemos.\\nCriamos ciclos de memória construtiva (memória básica) e \\nmemória afetiva (lembranças de afeto, amor e caos), nesse mo -\\nmento, percebi que existem energias de captação perante a mi -\\nnha necessidade de acordo com o que eu vivi, com a absorção \\ncaos do passado sendo vivido no futuro editável.indd   147caos do passado sendo vivido no futuro editável.indd   147 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 245548,
      "chapter": 7,
      "page": 147,
      "segment_type": "page",
      "themes": {},
      "difficulty": 28.950184246890835,
      "complexity_metrics": {
        "word_count": 334,
        "sentence_count": 13,
        "paragraph_count": 1,
        "avg_sentence_length": 25.692307692307693,
        "avg_word_length": 4.649700598802395,
        "unique_word_ratio": 0.5868263473053892,
        "avg_paragraph_length": 334.0,
        "punctuation_density": 0.11377245508982035,
        "line_break_count": 31,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "minha",
          "mente",
          "você",
          "vida",
          "devido",
          "percebi",
          "psicóloga",
          "mais",
          "perante",
          "ciclos",
          "memória",
          "lacuna",
          "nessa",
          "como",
          "necessidade",
          "acompanhar",
          "mento",
          "remédio",
          "humana",
          "está"
        ],
        "entities": [
          [
            "147",
            "CARDINAL"
          ],
          [
            "fazendo",
            "ORG"
          ],
          [
            "perceber que eu",
            "PERSON"
          ],
          [
            "devido àquela lacuna",
            "PERSON"
          ],
          [
            "2",
            "CARDINAL"
          ],
          [
            "ela se perdeu.",
            "PERSON"
          ],
          [
            "Fui",
            "PERSON"
          ],
          [
            "Nessa vez",
            "PERSON"
          ],
          [
            "que eu fui",
            "ORG"
          ],
          [
            "eu falei sobre",
            "PERSON"
          ]
        ],
        "readability_score": 85.75893597420543,
        "semantic_density": 0,
        "word_count": 334,
        "unique_words": 196,
        "lexical_diversity": 0.5868263473053892
      },
      "preservation_score": 1.2656113154171841e-05
    },
    {
      "id": 1,
      "text": "— 148 —do meu subconsciente, de acordo com a minha absorção de \\nvida, em ciclos “involuntários” de acordo com a minha cap -\\ntação perante a minha própria linha de tempo, mandando a \\nminha necessidade momentânea de acordo com ciclo em que \\neu vivi, com a importância de cada momento de relevância \\npara mim mesmo. Meu pensamento é o certo, dentro daquilo \\nque eu vejo.\\nQuando me percebi, eu percebi todos em minha volta, me fa -\\nzendo reavaliar os meus ciclos de importância para mim mes -\\nmo, me fazendo enxergar a nossa própria prepotência diante \\nda nossa própria certeza.\\nTendo esse raciocínio, eu percebi como melhorar a minha \\nvida, comecei a realocar as minhas próprias memórias, dando \\nprioridade ao me lembrar de momentos felizes da minha vida, \\nevitando coisas que me fazem “mal” , e realocando as minhas \\nmemórias construtivas e afetivas, a importância dos momentos \\nfelizes diante do meu próprio ciclo (desfragmentar). \\nAo fazer isso, eu comecei a fazer isso com pessoas próximas de \\nmim, me fazendo enxergar como é a vida de cada pessoa, como \\ncada uma pensa e percebi que o que eu vivi, é o mesmo que \\ntodos viveram. \\nHoje, quando eu vejo um sorriso, eu penso: como essa pessoa \\nchegou a esse sorriso?\\nTodos os acontecimentos em minha volta, eu penso no trajeto \\ne não no acontecimento.\\nAssim, eu espero ter chegado a uma conclusão plausível, pe -\\nrante um viver melhor para nós mesmos.\\ncaos do passado sendo vivido no futuro editável.indd   148caos do passado sendo vivido no futuro editável.indd   148 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 247576,
      "chapter": 7,
      "page": 148,
      "segment_type": "page",
      "themes": {},
      "difficulty": 27.483206106870227,
      "complexity_metrics": {
        "word_count": 262,
        "sentence_count": 11,
        "paragraph_count": 1,
        "avg_sentence_length": 23.818181818181817,
        "avg_word_length": 4.854961832061068,
        "unique_word_ratio": 0.5610687022900763,
        "avg_paragraph_length": 262.0,
        "punctuation_density": 0.1450381679389313,
        "line_break_count": 27,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "minha",
          "vida",
          "percebi",
          "como",
          "acordo",
          "própria",
          "importância",
          "cada",
          "todos",
          "ciclos",
          "ciclo",
          "vivi",
          "mesmo",
          "vejo",
          "quando",
          "volta",
          "fazendo",
          "enxergar",
          "nossa",
          "diante"
        ],
        "entities": [
          [
            "148",
            "CARDINAL"
          ],
          [
            "para mim mesmo",
            "PERSON"
          ],
          [
            "Meu",
            "ORG"
          ],
          [
            "certo",
            "NORP"
          ],
          [
            "que eu vejo",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "eu percebi",
            "PERSON"
          ],
          [
            "meus ciclos de importância",
            "PERSON"
          ],
          [
            "mim",
            "PERSON"
          ],
          [
            "prepotência diante \\nda nossa",
            "PERSON"
          ]
        ],
        "readability_score": 86.63442054129077,
        "semantic_density": 0,
        "word_count": 262,
        "unique_words": 147,
        "lexical_diversity": 0.5610687022900763
      },
      "preservation_score": 9.842023478186629e-06
    },
    {
      "id": 1,
      "text": "— 149 —Minha vida\\nLinha de tempo\\nEu estudei um pouco de cabala judaica e esse estudo mexeu \\ncom a minha maneira de ver a propagação da energia, pois \\nesse estudo me mostrou que nascemos predeterminados a \\nalgo, e esse algo funciona da seguinte forma: meu aniversário \\né 30/08/1986, o Tesla tem estudo e muitas comprovações que \\nnós somos energia e toda energia tem um ciclo infinito, basta \\nconhecer o ciclo da energia para se ter a resposta do universo \\n(números infinitos).\\nE matemática do Tesla é semelhante à matemática da cabala, \\nesquema de redução a um número.\\n3+0+0+8+1+9+8+6 = 35 reduzir 3+5= 8\\nComo já falei, eu fiquei surpreso com o meu estudo sobre a \\ncabala judaica, pois ele me deu quase 100% de acerto, foi a \\nnumerologia mais próxima que eu já tinha visto, aquilo me \\nintrigou, eu sendo ateu, queria uma resposta física. Comecei a \\ncompreender melhor a energia, pois tudo é energia, nós somos \\nformandos de átomos, se somos formados de energia, propaga -\\nmos em uma energia.\\nQuando completei meu aniversário de 35 anos no dia \\n30/08/2021\\n3+5=8 grandes conquista e duplicidade de número, com eleva -\\nção espiritual\\n3+0+0+8+2+0+2+1=7 Espiritualidade muito elevada. Único nú -\\nmero que ocorre o ciclo de si, no próprio valor numérico ( \\nmais a frente terá a resposta).\\ncaos do passado sendo vivido no futuro editável.indd   149caos do passado sendo vivido no futuro editável.indd   149 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 249251,
      "chapter": 7,
      "page": 149,
      "segment_type": "page",
      "themes": {},
      "difficulty": 29.870060437006046,
      "complexity_metrics": {
        "word_count": 239,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 26.555555555555557,
        "avg_word_length": 4.937238493723849,
        "unique_word_ratio": 0.6359832635983264,
        "avg_paragraph_length": 239.0,
        "punctuation_density": 0.12552301255230125,
        "line_break_count": 27,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "estudo",
          "cabala",
          "esse",
          "pois",
          "somos",
          "ciclo",
          "resposta",
          "sendo",
          "minha",
          "judaica",
          "algo",
          "aniversário",
          "tesla",
          "matemática",
          "número",
          "mais",
          "passado",
          "vivido",
          "futuro"
        ],
        "entities": [
          [
            "149",
            "CARDINAL"
          ],
          [
            "Eu",
            "PERSON"
          ],
          [
            "pouco de cabala",
            "PERSON"
          ],
          [
            "que nascemos",
            "PERSON"
          ],
          [
            "30/08/1986",
            "DATE"
          ],
          [
            "basta",
            "NORP"
          ],
          [
            "para se",
            "PERSON"
          ],
          [
            "universo \\n",
            "PERSON"
          ],
          [
            "números",
            "PERSON"
          ],
          [
            "matemática da cabala",
            "PERSON"
          ]
        ],
        "readability_score": 85.24105067410507,
        "semantic_density": 0,
        "word_count": 239,
        "unique_words": 152,
        "lexical_diversity": 0.6359832635983264
      },
      "preservation_score": 7.676778312985571e-06
    },
    {
      "id": 1,
      "text": "— 150 —Início da minha vida\\nEu nasci em uma família rica, porém, meu pai me “abando -\\nnou” , ele sumiu quando eu tinha 4 anos de idade, deixando um \\nlegado de fome, falta de estrutura familiar, ausência de um pai, \\numa esposa que era dona de casa com quatro filhos negros, ela \\nsendo branca, em um local de muitos julgamentos perante sua \\naparência, sofrendo preconceitos ou pré-conceito em forma de \\ndiminuir uma pessoa perante a uma sociedade e outras coisas\\nNo decorrer da minha infância, eu não percebia o caos que eu \\nvivia, eu não era apegado a nada material, eu era uma criança \\nque achava normal passar fome e dificuldades, não vendo difi -\\nculdades no que eu vivi, pois eu chegava da escola já indo para \\na rua brincar, já que não adiantava eu ficar em casa sem comi -\\nda, preferia ir para a rua brincar com os meus amigos.\\nQuando tinha uns 7 anos, eu catava frutas nós pés e vendia em \\numa barraquinha que eu comprei no Mercadão de Madureira, \\ncom o dinheiro que meu pai me deu em uma das poucas vezes \\nque ele apareceu na minha infância. Vendia as frutas e elevei o \\nmeu negócio, comprei doces para vender em uma barraquinha \\nmaior, que eu comprei juntando o dinheiro das frutas. Não \\ndeu certo!!! kkkkk Meus irmãos eram os maiores consumido -\\nres da minha barraca e não me pagavam, quebrei!! \\nA situação financeira conseguiu ficar pior chegando ao caos \\npara mim quando eu não conseguia ir ao banheiro durante \\ntrês meses, devido a comer muita goiaba (aprendi que goiaba \\ntrava até a alma) por não ter outras coisas para comer.\\nFicamos sem luz, toda hora tínhamos que pedir dinheiro em -\\nprestado para comer, não tinha como sair com os meus amigos \\nda minha idade por não ter roupa ou dinheiro para fazer qual -\\nquer coisa e eu sempre improvisando em ser feliz com qual -\\nquer amigo.\\ncaos do passado sendo vivido no futuro editável.indd   150caos do passado sendo vivido no futuro editável.indd   150 28/03/2022   14:53:4028/03/2022   14:53:40\\n\\n6\\n, \\n9\\n, \\n3",
      "position": 250808,
      "chapter": 7,
      "page": 150,
      "segment_type": "page",
      "themes": {},
      "difficulty": 39.90310734463277,
      "complexity_metrics": {
        "word_count": 354,
        "sentence_count": 10,
        "paragraph_count": 2,
        "avg_sentence_length": 35.4,
        "avg_word_length": 4.477401129943503,
        "unique_word_ratio": 0.5903954802259888,
        "avg_paragraph_length": 177.0,
        "punctuation_density": 0.12146892655367232,
        "line_break_count": 37,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "minha",
          "dinheiro",
          "quando",
          "tinha",
          "sendo",
          "caos",
          "meus",
          "frutas",
          "comprei",
          "comer",
          "anos",
          "idade",
          "fome",
          "casa",
          "perante",
          "outras",
          "coisas",
          "infância",
          "brincar",
          "ficar"
        ],
        "entities": [
          [
            "150",
            "CARDINAL"
          ],
          [
            "Eu",
            "PERSON"
          ],
          [
            "uma família rica",
            "ORG"
          ],
          [
            "quando eu",
            "PERSON"
          ],
          [
            "4",
            "CARDINAL"
          ],
          [
            "legado de fome",
            "ORG"
          ],
          [
            "ausência de",
            "PERSON"
          ],
          [
            "dona de casa",
            "ORG"
          ],
          [
            "ela \\nsendo branca",
            "PERSON"
          ],
          [
            "forma de \\ndiminuir",
            "PERSON"
          ]
        ],
        "readability_score": 80.95677966101695,
        "semantic_density": 0,
        "word_count": 354,
        "unique_words": 209,
        "lexical_diversity": 0.5903954802259888
      },
      "preservation_score": 3.0750855578512005e-05
    },
    {
      "id": 1,
      "text": "— 151 —Na escola, eu era muito ruim. A única matéria que eu prestava \\nera a matemática, porém tinha um probleminha eu não conse -\\nguia desenvolver os cálculos, só sabia as respostas.\\nMeu pai reapareceu quando eu tinha por volta de 13, 14 anos. \\nMe aproximando do meu pai, começamos a viver uma vida de \\npai e filho, até o ponto que ele contratou uma puta para fazer \\nsexo comigo, pensando que eu seria gay por não me interessar \\nem sexo naquela idade (quase 17 anos).\\nApós eu fazer sexo... puta que pariu, que sensação de êxtase \\nviciante era aquela, como queria repetir, fazer mais e mais... \\nComecei a trabalhar como lavador de carro, em seguida apren -\\ndi a instalar Insulfilm e me dediquei a vida toda nessa profissão \\nde instalador.\\nApós alguns anos, meu trabalho ficou monótono, pois era \\nsempre a mesma coisa me transformando em um robô em \\nprodução, perante minha própria necessidade, ficando com \\nmuito tempo obsoleto para pensar em qualquer coisa, pois eu \\nestar ali, não estava com a mente ali de tão robotizado que \\nficou o meu trabalho, me fazendo abrir espaço para evoluir \\nminha mente.\\nMinhas epifanias\\nNo dia do meu aniversário, eu já estava com a ideia de termi -\\nnar esse projeto do meu livro, porém nunca tinha tempo para \\nterminar, não tinha as respostas que faltavam, não tinha muita \\ncoisa para terminar esse meu projeto do livro.\\nUm mês antes do meu aniversário, resolvi viajar sozinho para \\nver como funciona o estar sozinho em uma aventura minha \\nmesmo.\\ncaos do passado sendo vivido no futuro editável.indd   151caos do passado sendo vivido no futuro editável.indd   151 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 252920,
      "chapter": 7,
      "page": 151,
      "segment_type": "page",
      "themes": {},
      "difficulty": 27.242100909842847,
      "complexity_metrics": {
        "word_count": 279,
        "sentence_count": 13,
        "paragraph_count": 1,
        "avg_sentence_length": 21.46153846153846,
        "avg_word_length": 4.781362007168458,
        "unique_word_ratio": 0.6236559139784946,
        "avg_paragraph_length": 279.0,
        "punctuation_density": 0.15412186379928317,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "tinha",
          "anos",
          "fazer",
          "sexo",
          "como",
          "coisa",
          "minha",
          "muito",
          "porém",
          "respostas",
          "vida",
          "puta",
          "após",
          "mais",
          "trabalho",
          "ficou",
          "pois",
          "tempo",
          "estava",
          "mente"
        ],
        "entities": [
          [
            "151",
            "CARDINAL"
          ],
          [
            "eu era muito ruim",
            "PERSON"
          ],
          [
            "que eu prestava",
            "PERSON"
          ],
          [
            "probleminha eu",
            "PERSON"
          ],
          [
            "quando eu",
            "PERSON"
          ],
          [
            "volta de 13",
            "ORG"
          ],
          [
            "14",
            "CARDINAL"
          ],
          [
            "até o ponto",
            "ORG"
          ],
          [
            "pensando que eu seria",
            "ORG"
          ],
          [
            "17",
            "CARDINAL"
          ]
        ],
        "readability_score": 87.83482216708023,
        "semantic_density": 0,
        "word_count": 279,
        "unique_words": 174,
        "lexical_diversity": 0.6236559139784946
      },
      "preservation_score": 1.0206542866267617e-05
    },
    {
      "id": 1,
      "text": "— 152 —No dia do meu aniversário, eu acordei e tive a minha primei -\\nra epifania, eu consegui resolver uma lacuna na minha tese \\ne escrevi na parede da minha casa, em seguida meus amigos \\nchegaram para comemorar o meu aniversário junto comigo, \\nexpliquei a minha tese e de onde eu tirei a epifania que eu tive.\\nEu simplesmente acordei, fui na minha varanda, olhei para as \\nplantas, olhei para a minha casa e percebi que a minha casa \\nestava a minha cara, a minha energia.\\nNesse momento, eu percebi a ideia da propagação da energia \\nque nós mesmos emitimos, nesse mesmo dia mais tarde, apa -\\nreceram dois arco-íris na frente da minha casa (energia 9 vida), \\nchorei de emoção, fiquei emocionado, porém não vi como um \\nsinal do universo.\\nNo dia seguinte, eu peguei a estrada em direção à Rota do \\nCafé, eu estava indo em direção a Volta Redonda, porém estava \\ncansado de tanto pegar a estrada, entrei na primeira saída que \\neu vi, Japeri, fui seguindo a viagem cheio de fome, pois não \\ntinha comido nada, parei onde eu senti uma energia que eu \\nsenti e tive que parar.\\nParei e aconteceram milhões de coincidências entre mim e \\ntodos que ali estavam. Assim que eu cheguei, perguntei: — \\nIrmão, boa tarde!!! Tudo bem com você? Eu estava passando e \\ngostei da energia do seu estabelecimento, parei para comer um \\npão com linguiça, quanto custa?\\nEle: — Você veio do manicômio?\\nEu: — Não, por que a pergunta?\\nMe colocou para fala com o outro rapaz, pois não estava com \\na “cabeça” para me dar atenção (ele tinha acabado de passar \\npor um trauma). Assim que eu cheguei, parei e fiquei duran -\\nte oito horas conversando com aquelas pessoas, ali eu percebi \\ncaos do passado sendo vivido no futuro editável.indd   152caos do passado sendo vivido no futuro editável.indd   152 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 254674,
      "chapter": 7,
      "page": 152,
      "segment_type": "page",
      "themes": {},
      "difficulty": 28.524087426768816,
      "complexity_metrics": {
        "word_count": 317,
        "sentence_count": 14,
        "paragraph_count": 1,
        "avg_sentence_length": 22.642857142857142,
        "avg_word_length": 4.61198738170347,
        "unique_word_ratio": 0.5899053627760252,
        "avg_paragraph_length": 317.0,
        "punctuation_density": 0.1640378548895899,
        "line_break_count": 30,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "minha",
          "estava",
          "energia",
          "casa",
          "parei",
          "tive",
          "percebi",
          "aniversário",
          "acordei",
          "epifania",
          "tese",
          "onde",
          "olhei",
          "nesse",
          "tarde",
          "fiquei",
          "porém",
          "estrada",
          "direção",
          "pois"
        ],
        "entities": [
          [
            "152",
            "CARDINAL"
          ],
          [
            "eu acordei",
            "PERSON"
          ],
          [
            "eu consegui",
            "PERSON"
          ],
          [
            "da minha casa",
            "PERSON"
          ],
          [
            "meu aniversário junto comigo",
            "ORG"
          ],
          [
            "eu tive",
            "PERSON"
          ],
          [
            "Eu",
            "PERSON"
          ],
          [
            "varanda",
            "GPE"
          ],
          [
            "olhei para",
            "PERSON"
          ],
          [
            "olhei para",
            "PERSON"
          ]
        ],
        "readability_score": 87.29497521406039,
        "semantic_density": 0,
        "word_count": 317,
        "unique_words": 187,
        "lexical_diversity": 0.5899053627760252
      },
      "preservation_score": 1.4653679400855648e-05
    },
    {
      "id": 1,
      "text": "— 153 —o quanto nós queremos algo e as coisas acontecem, a energia \\nuniversal propaga diante de nós mesmos para um bem maior \\nem comum. Um dia depois do meu aniversário, eu encontrei \\num ciclo intenso de espiritualidade de receptor e emissor.\\nFui dormir no hotel, chegando ao hotel, eu tive um sonho se -\\nmelhante a um buraco negro, virei de bruços e continuei a \\nenxergar essa mesma imagem, não entendi nada. No dia se -\\nguinte, segui em direção a Paty do Alferes com intenção de me \\nhospedar em alguma chácara, alguma coisa dentro de alguma \\nenergia que eu me sentisse bem, continuei meu caminho sem \\nparar em Paty, pois não me senti à vontade com a energia, não \\nera a energia que eu precisava para eu sentir o conforto ne -\\ncessário para escrever o meu livro, passei direto pela cidade e \\ncontinuei sem rumo perante algo que não sabia. Ao olhar para \\no Waze para saber em qual cidade eu me localizava, levantei a \\ncabeça, em seguida, vi uma chácara, senti um ambiente fami -\\nliar e entrei sem saber nada. Voltei meus olhos para o telefo -\\nne, tinha uma mosca pousada nele, no primeiro momento eu \\nestava vendo como acontecimento, em seguida, eu pensei nos \\nsinais que vinham acontecendo. Assim que eu me liguei nos \\nsinais, eu entendi como terra (físico), pois eu tentei espantar a \\nmosca e ela só saiu devido a eu passar a mão próximo dela para \\nespantar. Cheguei na pousada e encontro um rapaz respon -\\nsável pela administração do local, perguntei para ele: Como \\nfunciona a hospedagem aqui?\\nEle: — Valor tal, os quartos disponíveis são esses.\\nEu: — Posso te fazer uma pergunta? Seu pai trabalhava muito \\ne você também?\\nEle: — Sim, aqui é um negócio de família. \\nEle me mostrou uma trilha para eu fazer. Odeio trilha, não \\nentendo por que fiz, porém fiz. No meio da trilha, eu passava \\ncaos do passado sendo vivido no futuro editável.indd   153caos do passado sendo vivido no futuro editável.indd   153 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 256596,
      "chapter": 7,
      "page": 153,
      "segment_type": "page",
      "themes": {},
      "difficulty": 27.55350547195622,
      "complexity_metrics": {
        "word_count": 344,
        "sentence_count": 17,
        "paragraph_count": 1,
        "avg_sentence_length": 20.235294117647058,
        "avg_word_length": 4.590116279069767,
        "unique_word_ratio": 0.625,
        "avg_paragraph_length": 344.0,
        "punctuation_density": 0.1511627906976744,
        "line_break_count": 31,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "continuei",
          "alguma",
          "como",
          "trilha",
          "algo",
          "hotel",
          "entendi",
          "nada",
          "paty",
          "chácara",
          "pois",
          "senti",
          "pela",
          "cidade",
          "saber",
          "seguida",
          "mosca",
          "pousada",
          "sinais"
        ],
        "entities": [
          [
            "153",
            "CARDINAL"
          ],
          [
            "quanto",
            "GPE"
          ],
          [
            "nós queremos",
            "GPE"
          ],
          [
            "coisas",
            "NORP"
          ],
          [
            "dia",
            "ORG"
          ],
          [
            "eu",
            "PERSON"
          ],
          [
            "Fui",
            "PERSON"
          ],
          [
            "eu",
            "PERSON"
          ],
          [
            "buraco",
            "NORP"
          ],
          [
            "virei de bruços e continuei",
            "ORG"
          ]
        ],
        "readability_score": 88.50531805745554,
        "semantic_density": 0,
        "word_count": 344,
        "unique_words": 215,
        "lexical_diversity": 0.625
      },
      "preservation_score": 1.4690131339663746e-05
    },
    {
      "id": 1,
      "text": "— 154 —pelas sombras e percebia que eu sentia a sombra, porém não \\nas tocava, foi quando eu tive uma ideia perante o meu sonho \\nde não ser matéria escura e sim massa escura, pois quando eu \\npassei pela estrada, eu estava com o som desligado e passou um \\ncaminhão muito rápido ao meu lado, eu senti o deslocamento \\ndo ar. Juntei as duas coisas e cheguei à forma de pensar sobre \\n“matéria escura” , em massa escura.\\nFui a um aviário, nesse aviário conversei com o dono e eu ex -\\npliquei todas as coisas que tinham ocorrido comigo, inclusive \\ndo arco-íris. Depois de cinco minutos, apareceu um novo arco -\\n-íris em um local que, de acordo com o próprio rapaz, ele nem \\nlembrava a última vez que tinha visto, pois ou chove muito ou \\nnão chove. Saiu um arco-íris sem ter caído nenhuma chuva.\\nO que falar sobre todos os acontecimentos? O que dizer sobre \\ntudo? Eu não sei o que pode ser, só sei que aconteceu.\\nParte científica do livro\\nTempo é relativo à energia material (existência, visual). Se não \\nexiste matéria, não existe tempo. Se nós somos formados de \\nátomos (menor particular da matéria) e os átomos se repelem \\ncausando energia entre eles é assim que funcionamos perante \\no mundo quântico, pois a energia é onipresente, em todos os \\nlugares temos energia, tudo que temos na vida é feito de ener -\\ngia.\\nAnalogia\\n“Algum tipo de droga e repara o seu corpo diante a um toque \\nde outra pessoa. ”\\n“Uma menina estava espirrando do meu lado ontem, vê se eu \\nnão estou com febre?”\\nTanto a droga, quanto a febre fazem um processo semelhan -\\ncaos do passado sendo vivido no futuro editável.indd   154caos do passado sendo vivido no futuro editável.indd   154 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 258663,
      "chapter": 7,
      "page": 154,
      "segment_type": "page",
      "themes": {
        "filosofia": 60.0,
        "arte": 40.0
      },
      "difficulty": 27.89217715231788,
      "complexity_metrics": {
        "word_count": 302,
        "sentence_count": 16,
        "paragraph_count": 1,
        "avg_sentence_length": 18.875,
        "avg_word_length": 4.5364238410596025,
        "unique_word_ratio": 0.6589403973509934,
        "avg_paragraph_length": 302.0,
        "punctuation_density": 0.1291390728476821,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "matéria",
          "escura",
          "energia",
          "pois",
          "arco",
          "íris",
          "quando",
          "perante",
          "massa",
          "estava",
          "muito",
          "lado",
          "coisas",
          "aviário",
          "chove",
          "todos",
          "tudo",
          "tempo",
          "existe",
          "átomos"
        ],
        "entities": [
          [
            "154",
            "CARDINAL"
          ],
          [
            "eu",
            "PERSON"
          ],
          [
            "foi quando eu",
            "PERSON"
          ],
          [
            "matéria",
            "GPE"
          ],
          [
            "massa escura",
            "PERSON"
          ],
          [
            "quando eu \\npassei pela",
            "PERSON"
          ],
          [
            "estrada",
            "ORG"
          ],
          [
            "eu estava",
            "PERSON"
          ],
          [
            "caminhão muito rápido",
            "PERSON"
          ],
          [
            "eu senti",
            "PERSON"
          ]
        ],
        "readability_score": 89.20157284768212,
        "semantic_density": 0,
        "word_count": 302,
        "unique_words": 199,
        "lexical_diversity": 0.6589403973509934
      },
      "preservation_score": 1.2262432215044376e-05
    },
    {
      "id": 1,
      "text": "— 155 —te em seu corpo. Nós somos feitos de átomos que formam as \\ncélulas, temos vários tipos de células diferentes, umas fazem \\nmeiose e outras fazem mitose. Quando o seu corpo têm algum \\ncolapso, seu corpo fica sobrecarregado de tanta energia, pois \\nas células fazem mitose, perante ao tamanho da sua doença, \\nsuperaquecendo o seu corpo. Têm o segundo fator na mesma \\nfrase, doenças psicossomáticas são doenças de estresse mental \\nque ocasionam uma doença física. Quais são as células nervo -\\nsas (energia) do nosso corpo? Neurônio. Quais são os lugares \\ncom maior concentração de neurônios? Cérebro na parte do \\nSUBCONSCIENTE e no intestino. E as células nervosas tam -\\nbém transportam doenças pelo nosso corpo, então, quanto \\nmais nervoso você viver, mais doenças você terá. Sabe aquele \\nincômodo na barriga? Esse incômodo, quer dizer que você está \\ncom algum caos dentro de você mesmo, pois a segunda maior \\nconcentração de células nervosas é no intestino.\\nA causa da febre já sabemos, mas não sabemos o motivo de \\nmedir a temperatura na virilha, sovaco e axilas. Por que isso \\nacontece nessas regiões?\\nMaior fluxo de sangue, sendo as maiores veias do corpo, com \\num maior fluxo de células nesses locais, gera mais energia ge -\\nrando mais energia (febre) nas regiões.\\nSe tempo “não existe” perante a energia do nosso próprio cor -\\npo (universo, galáxia, sistema solar, terra, nós), de concordância \\nentre os próprios ciclos de si próprio (universo, galáxia, sistema \\nsolar, terra, nós), uma oscilação, afetando a energia do outro, \\nsendo que o valor da sua energia é proporcional ao tamanho \\nda sua massa escura, pois quanto maior é a sua massa escura, \\nmais energia você consegue canalizar, concentrado mais ener -\\ngia, gerando um vórtice de energia maior, concentrado mais \\nenergia proporcional a quantidade de massa, que quando essa \\ncaos do passado sendo vivido no futuro editável.indd   155caos do passado sendo vivido no futuro editável.indd   155 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 260475,
      "chapter": 7,
      "page": 155,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 29.71795665634675,
      "complexity_metrics": {
        "word_count": 323,
        "sentence_count": 17,
        "paragraph_count": 1,
        "avg_sentence_length": 19.0,
        "avg_word_length": 5.102167182662539,
        "unique_word_ratio": 0.5851393188854489,
        "avg_paragraph_length": 323.0,
        "punctuation_density": 0.17027863777089783,
        "line_break_count": 31,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "corpo",
          "células",
          "mais",
          "maior",
          "você",
          "doenças",
          "sendo",
          "fazem",
          "pois",
          "nosso",
          "massa",
          "mitose",
          "quando",
          "algum",
          "perante",
          "tamanho",
          "doença",
          "quais",
          "concentração"
        ],
        "entities": [
          [
            "155",
            "CARDINAL"
          ],
          [
            "de células",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "têm algum",
            "PERSON"
          ],
          [
            "seu corpo",
            "ORG"
          ],
          [
            "fica sobrecarregado de tanta energia",
            "ORG"
          ],
          [
            "psicossomáticas",
            "CARDINAL"
          ],
          [
            "doenças de estresse",
            "PERSON"
          ],
          [
            "Neurônio",
            "PERSON"
          ],
          [
            "doenças pelo",
            "PERSON"
          ]
        ],
        "readability_score": 88.96934984520124,
        "semantic_density": 0,
        "word_count": 323,
        "unique_words": 189,
        "lexical_diversity": 0.5851393188854489
      },
      "preservation_score": 1.6272145483935225e-05
    },
    {
      "id": 1,
      "text": "— 156 —concentração de energia gera um valor de massa maior que a \\nmassa escura (entorno), expelindo um grande valor energético \\n(quasar) do seu próprio centro. \\nTemos buracos negros com menos massa que outros buracos \\nnegros. Esses buracos negros canalizam menos energia, entran -\\ndo em um ciclo menor de concentração de energia (vórtice), \\ntendo um ciclo menor de quantidade de energia canalizada, \\ngerando uma liberação de energia (quasar) menor que os bu -\\nracos negros com menos massa.\\nColoque isso em proporção de ciclo próprio, em combinação \\nde outros ciclos de si próprio, que todos os ciclos se mantém \\nno padrão do universo (maior quantidade de massa escura), \\nonde contendo mais massa escura se origina os buracos negros, \\npara manter um ciclo padronizado de energia do universo.\\nO que seria o tempo perante ao universo?\\nQuantos anos o universo vai viver?\\nQual é o tamanho do universo perante você?\\nQuem é mais importante, você ou o universo?\\nLogo pensamos que nós somos os “escravos” do universo, pois \\ntudo que façamos, logo iremos sofrer, pois o caos que criamos, \\nnão é mais forte que a energia do universo (Deus é bom o \\ntempo todo).\\nIsso me fez perceber o ciclo infinito dentro de outros ciclos \\ninfinitos, da propagação da energia (tempo) perante a sua exis -\\ntência física.\\nComo nos (buraco negro) absorvemos a energia em nossa vol -\\nta? Isso se chama memória.\\nTemos dois tipos de memória, memória afetiva e memória \\nconstrutiva.\\ncaos do passado sendo vivido no futuro editável.indd   156caos do passado sendo vivido no futuro editável.indd   156 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 262592,
      "chapter": 7,
      "page": 156,
      "segment_type": "page",
      "themes": {},
      "difficulty": 24.115151515151517,
      "complexity_metrics": {
        "word_count": 264,
        "sentence_count": 16,
        "paragraph_count": 1,
        "avg_sentence_length": 16.5,
        "avg_word_length": 5.011363636363637,
        "unique_word_ratio": 0.571969696969697,
        "avg_paragraph_length": 264.0,
        "punctuation_density": 0.12878787878787878,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "universo",
          "massa",
          "negros",
          "ciclo",
          "buracos",
          "memória",
          "escura",
          "próprio",
          "menos",
          "outros",
          "menor",
          "isso",
          "ciclos",
          "mais",
          "tempo",
          "perante",
          "concentração",
          "valor",
          "maior"
        ],
        "entities": [
          [
            "156",
            "CARDINAL"
          ],
          [
            "valor de massa",
            "ORG"
          ],
          [
            "massa escura",
            "PERSON"
          ],
          [
            "Temos",
            "PERSON"
          ],
          [
            "buracos",
            "NORP"
          ],
          [
            "buracos",
            "NORP"
          ],
          [
            "negros canalizam menos",
            "PRODUCT"
          ],
          [
            "canalizada",
            "GPE"
          ],
          [
            "ciclos se mantém",
            "PERSON"
          ],
          [
            "universo (maior quantidade de massa escura",
            "ORG"
          ]
        ],
        "readability_score": 90.24659090909091,
        "semantic_density": 0,
        "word_count": 264,
        "unique_words": 151,
        "lexical_diversity": 0.571969696969697
      },
      "preservation_score": 1.2262432215044376e-05
    },
    {
      "id": 1,
      "text": "— 157 —Memória afetiva é separado em duas nomenclaturas, lembran -\\nças boas e lembranças ruins. E a absorção dessas memórias, \\ncomo funciona? Nós somos captadores de energia, no decor -\\nrer da nossa evolução, nós captamos a energia do universo \\nperante a “necessidade” do próprio universo, pois os seres vi -\\nvos que habitam a Terra começaram a desestabilizar a energia \\ndela perante o universo, assim, a Terra junto com os seres vivos \\ncriaram uma conexão entre si perante a energia do universo, \\nobrigando as espécies a evoluírem de acordo com a sua pró -\\npria necessidade, para manter um ciclo de energia universal. \\nNós seres humanos somos a espécie evoluída da Terra, devido \\na conseguirmos captar a energia do nosso próprio planeta em \\num ciclo de energia entre universo, galáxia, sistema solar, Ter -\\nra, nós, porém nós mesmos tiramos o eixo da Terra, perante a \\nnossa consequência física ao físico do planeta Terra, nos mos -\\ntrando que tudo que há no universo e um único universo, nos \\ntransformando em um mundo quântico de propagação única \\ncontinua de nós mesmos.\\nVamos voltar ao assunto sobre como absorvemos as nossas me -\\nmórias. Memória construtiva é aquela memória que você usa \\nno seu dia a dia, aquela memória que o seu subconsciente tra -\\nbalha involuntariamente, em ciclos constante e contínuo. Me -\\nmória afetiva é aquela que você tem uma lembrança marcante \\nde si próprio, com características evolutivas carma, DNA, com \\numa pré-propagação de como a sua energia será direcionada \\nao meio em que vivemos.\\nComo nós nascemos sem manual de instrução, como sabería -\\nmos o acerto sem o erro? Nós temos ciclos de nós mesmos, \\naprendizados de nós mesmos, evolução de acordo com a cana -\\nlização proporcional à massa escura (universo, galáxia, sistema \\nsolar, Terra, nós). É errando que se aprende, porém concertan -\\ndo o erro do ciclo dos nossos próprios erros.\\ncaos do passado sendo vivido no futuro editável.indd   157caos do passado sendo vivido no futuro editável.indd   157 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 264317,
      "chapter": 7,
      "page": 157,
      "segment_type": "page",
      "themes": {},
      "difficulty": 32.82895393691854,
      "complexity_metrics": {
        "word_count": 339,
        "sentence_count": 13,
        "paragraph_count": 1,
        "avg_sentence_length": 26.076923076923077,
        "avg_word_length": 4.935103244837758,
        "unique_word_ratio": 0.5693215339233039,
        "avg_paragraph_length": 339.0,
        "punctuation_density": 0.13864306784660768,
        "line_break_count": 32,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "universo",
          "terra",
          "como",
          "memória",
          "perante",
          "mesmos",
          "próprio",
          "seres",
          "ciclo",
          "aquela",
          "afetiva",
          "somos",
          "nossa",
          "evolução",
          "necessidade",
          "entre",
          "acordo",
          "planeta",
          "galáxia"
        ],
        "entities": [
          [
            "157",
            "CARDINAL"
          ],
          [
            "Memória",
            "GPE"
          ],
          [
            "nós captamos",
            "ORG"
          ],
          [
            "universo \\nperante",
            "ORG"
          ],
          [
            "próprio universo",
            "PERSON"
          ],
          [
            "Terra",
            "ORG"
          ],
          [
            "dela perante",
            "PERSON"
          ],
          [
            "universo",
            "ORG"
          ],
          [
            "Terra",
            "ORG"
          ],
          [
            "evoluírem de acordo",
            "PERSON"
          ]
        ],
        "readability_score": 85.48100748808713,
        "semantic_density": 0,
        "word_count": 339,
        "unique_words": 193,
        "lexical_diversity": 0.5693215339233039
      },
      "preservation_score": 1.539729895254086e-05
    },
    {
      "id": 1,
      "text": "— 158 —Lembranças são os momentos marcantes em sua vida, por isso, \\nocorrendo a divisão da memória afetiva, nos gerando persona -\\nlidade de acordo com a minha própria energia (carma, DNA), \\nde acordo com o meio em que eu vivo, captando a frequência \\nsemelhante à minha, gerando histórias em ciclos em comum, \\ncriando as lembranças boas (energia) e ruins (buraco negro). \\nAs lembranças são os nossos sentimentos, quando acessamos \\nnossas lembranças, nós ficamos tristes ou felizes, nos transfor -\\nmando em ciclos proporcionais à minha captação de energia \\n(subconsciente). Aí vêm a quantidade de memórias absorvidas \\ndiante de nós mesmos. \\nAnalogia\\nGráfico de acesso à informação (cérebro) do momento em que \\nse precisa ser acessado de acordo com o que se está vivendo.\\nPense você sendo um computador com o processador Pen -\\ncaos do passado sendo vivido no futuro editável.indd   158caos do passado sendo vivido no futuro editável.indd   158 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 266469,
      "chapter": 7,
      "page": 158,
      "segment_type": "page",
      "themes": {},
      "difficulty": 27.724675324675324,
      "complexity_metrics": {
        "word_count": 154,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 22.0,
        "avg_word_length": 5.2727272727272725,
        "unique_word_ratio": 0.6948051948051948,
        "avg_paragraph_length": 154.0,
        "punctuation_density": 0.13636363636363635,
        "line_break_count": 15,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "lembranças",
          "acordo",
          "minha",
          "energia",
          "sendo",
          "gerando",
          "ciclos",
          "passado",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "momentos",
          "marcantes",
          "vida",
          "isso",
          "ocorrendo",
          "divisão",
          "memória",
          "afetiva"
        ],
        "entities": [
          [
            "158",
            "CARDINAL"
          ],
          [
            "eu",
            "PERSON"
          ],
          [
            "lembranças boas",
            "PERSON"
          ],
          [
            "buraco negro",
            "ORG"
          ],
          [
            "quando acessamos",
            "PERSON"
          ],
          [
            "nossas lembranças",
            "PERSON"
          ],
          [
            "nós ficamos",
            "GPE"
          ],
          [
            "diante de nós mesmos",
            "PERSON"
          ],
          [
            "Analogia\\nGráfico de",
            "ORG"
          ],
          [
            "precisa ser acessado de acordo",
            "ORG"
          ]
        ],
        "readability_score": 87.41818181818182,
        "semantic_density": 0,
        "word_count": 154,
        "unique_words": 107,
        "lexical_diversity": 0.6948051948051948
      },
      "preservation_score": 3.936809391274651e-06
    },
    {
      "id": 1,
      "text": "— 159 —tium 200, esse computador tem um HD de 100 gigas, quanto \\ntempo esse computador irá demorar para atingir o acesso às \\ninformações contidas no HD?\\nPensa em um computador octacore 3.8 GHz com um HD de \\n100 gigas, quanto tempo ele leva para acessar as informações?\\nIsso é uma análise de quantidade de inteligência proporcional \\nao seu acesso às informações de si próprio (captação energia, \\nmeio em que vive).\\nPorém, temos mais uma forma de acessar essas informações \\nsão as lembranças contextuais, o que seriam lembranças con -\\ntextuais? Lembranças contextuais são aquelas que você sente a \\nenergia do ambiente, captando de uma forma de lembranças \\nrelativas para si próprio (artistas, religiosos, filósofos, profetas, \\nmessias) criando soluções, matemática, filosófica, emoções, \\nmúsica, arte, uma expressão de propagar a energia captada, \\nexaltando esse sentimento em ciclos diante da sua própria cap -\\ntação de energia, interpretativa para si próprio.\\nComo você pensa diante de...\\nComo você pensa ao olhar algo?\\nComo você pensa ao ouvir algo?\\nComo você pensa ao sentir algo?\\nComo você pensa ao comer algo?\\nComo você pensa ao sentir um cheiro?\\nQual é o “sentido” mais importante, são os cinco sentidos ou é \\no sentido da sua própria captação diante do seu entendimento \\ndo que é viver?\\nA melhor forma de se enxergar toda essa teoria é simples. Nós \\ntemos cinco sentidos: tato, paladar, olfato, audição e visão, to -\\ncaos do passado sendo vivido no futuro editável.indd   159caos do passado sendo vivido no futuro editável.indd   159 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 267568,
      "chapter": 7,
      "page": 159,
      "segment_type": "page",
      "themes": {
        "ciencia": 56.52173913043479,
        "arte": 43.47826086956522
      },
      "difficulty": 28.669453450671604,
      "complexity_metrics": {
        "word_count": 254,
        "sentence_count": 17,
        "paragraph_count": 1,
        "avg_sentence_length": 14.941176470588236,
        "avg_word_length": 5.145669291338582,
        "unique_word_ratio": 0.5826771653543307,
        "avg_paragraph_length": 254.0,
        "punctuation_density": 0.18503937007874016,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "pensa",
          "você",
          "como",
          "informações",
          "energia",
          "lembranças",
          "algo",
          "esse",
          "computador",
          "próprio",
          "forma",
          "diante",
          "gigas",
          "quanto",
          "tempo",
          "acesso",
          "acessar",
          "captação",
          "temos",
          "mais"
        ],
        "entities": [
          [
            "159",
            "CARDINAL"
          ],
          [
            "200",
            "CARDINAL"
          ],
          [
            "100",
            "CARDINAL"
          ],
          [
            "irá demorar",
            "PERSON"
          ],
          [
            "3.8",
            "CARDINAL"
          ],
          [
            "Porém",
            "PERSON"
          ],
          [
            "lembranças contextuais",
            "PERSON"
          ],
          [
            "seriam",
            "NORP"
          ],
          [
            "Lembranças",
            "PERSON"
          ],
          [
            "matemática",
            "GPE"
          ]
        ],
        "readability_score": 90.98571097730431,
        "semantic_density": 0,
        "word_count": 254,
        "unique_words": 148,
        "lexical_diversity": 0.5826771653543307
      },
      "preservation_score": 1.1839589724870433e-05
    },
    {
      "id": 1,
      "text": "— 160 —dos com os seus valores a serem usados em um ciclo, somos \\ncinco elementos de energia de nós mesmos: universo, galáxia, \\nsistema, planeta, eu, criando um grande ciclo de vida univer -\\nsal!!!\\nExcesso de regras está destruindo o viver melhor.\\nEstamos cada vez mais exigentes em ser algo que não temos \\nque ser, se fazemos alguma coisa “fora da regra” que nos faz \\nfelizes, afeta o ser correto diante de uma vida que todos imagi -\\nnam ser correta.\\nSe somos uma imagem pública, não podemos fazer isso ou \\naquilo, se somos um esportista, não podemos fazer isso ou \\naquilo, se vivemos em algumas classes sociais, não podemos \\nfazer isso ou aquilo.\\nSe somos seres humanos querendo viver, não podemos viver \\nisso ou aquilo.\\nHoje, a exigência de “ser exemplo” para outros não é exemplo, \\né a destruição de um viver feliz, sua felicidade não pode ser \\nrealizada pela discriminação diante do que a sociedade impôs \\no que você têm que ser, diante daquilo que você propôs a ser \\npara ter uma vida melhor.\\nEstamos com tantas regras, que temos uma sociedade que só vê \\ncomo necessário para vida, ser o melhor. Tenista Naomi Osaka \\nem depressão. Ser a melhor ginástica, Simone Biles em depres -\\nsão. Ser o melhor comediante, Whindersson Nunes em depres -\\nsão. Será mesmo que estamos à procura de viver melhor ou \\nestamos à procura de sermos doutrinados para fazer um “mun -\\ndo melhor”? Vemos um UFC com vários atletas em depressão, \\nvemos um UFC que antes eram vários atletas de artes marciais \\ndiferentes, hoje quem têm só uma especialidade de lutar?\\nO que é ser humano?\\ncaos do passado sendo vivido no futuro editável.indd   160caos do passado sendo vivido no futuro editável.indd   160 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 269266,
      "chapter": 8,
      "page": 160,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 26.922635135135135,
      "complexity_metrics": {
        "word_count": 296,
        "sentence_count": 16,
        "paragraph_count": 1,
        "avg_sentence_length": 18.5,
        "avg_word_length": 4.736486486486487,
        "unique_word_ratio": 0.5675675675675675,
        "avg_paragraph_length": 296.0,
        "punctuation_density": 0.1554054054054054,
        "line_break_count": 30,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "melhor",
          "viver",
          "somos",
          "vida",
          "estamos",
          "podemos",
          "fazer",
          "isso",
          "aquilo",
          "diante",
          "ciclo",
          "regras",
          "temos",
          "hoje",
          "exemplo",
          "sociedade",
          "você",
          "depressão",
          "depres",
          "procura"
        ],
        "entities": [
          [
            "160",
            "CARDINAL"
          ],
          [
            "de energia de nós mesmos",
            "ORG"
          ],
          [
            "universo",
            "PERSON"
          ],
          [
            "galáxia",
            "PERSON"
          ],
          [
            "eu",
            "PERSON"
          ],
          [
            "Excesso de regras",
            "ORG"
          ],
          [
            "Estamos",
            "PERSON"
          ],
          [
            "vez mais",
            "PERSON"
          ],
          [
            "fazemos alguma",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ]
        ],
        "readability_score": 89.32905405405405,
        "semantic_density": 0,
        "word_count": 296,
        "unique_words": 168,
        "lexical_diversity": 0.5675675675675675
      },
      "preservation_score": 1.2903986338066913e-05
    },
    {
      "id": 1,
      "text": "— 161 —O que temos que ser como humano?\\nSomos feitos só de regras feitas pelo humano e o Universo?\\nResumo\\nLinha de tempo contínua perante a massa escura, pois eu falo \\nem massa escura por ser semelhante a sentir uma sombra de \\numa árvore, sentir a massa do caminhão ao passar. Fiz uma \\nlinha de raciocínio de ciclo de si próprio, modificando o ciclo \\nde si próprio de outro, virando um ciclo de ciclo de si próprio \\nde concordância de ciclos de sempre estarem na mesma pro -\\npagação da energia, criando o caos e se organizando diante do \\npróprio caos, expansão do universo pelo próprio caos gerado \\nde si próprio. Matéria, planeta, sistema, galáxia e universo, tudo \\nem um único ciclo de caos e adaptação diante do seu próprio \\ncaos, de um caos com a maior massa, obrigando a quem tem a \\nmenor massa a se adaptar a quem têm a maior massa.\\nTeoria quântica de ação e reação da energia, em uma concor -\\ndância do movimento da própria energia.\\ncaos do passado sendo vivido no futuro editável.indd   161caos do passado sendo vivido no futuro editável.indd   161 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 271104,
      "chapter": 8,
      "page": 161,
      "segment_type": "page",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 30.722970639032813,
      "complexity_metrics": {
        "word_count": 193,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 21.444444444444443,
        "avg_word_length": 4.606217616580311,
        "unique_word_ratio": 0.5803108808290155,
        "avg_paragraph_length": 193.0,
        "punctuation_density": 0.12953367875647667,
        "line_break_count": 17,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "próprio",
          "caos",
          "massa",
          "ciclo",
          "universo",
          "energia",
          "humano",
          "pelo",
          "linha",
          "escura",
          "sentir",
          "diante",
          "maior",
          "quem",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd"
        ],
        "entities": [
          [
            "161",
            "CARDINAL"
          ],
          [
            "Somos",
            "PERSON"
          ],
          [
            "pelo humano e",
            "PERSON"
          ],
          [
            "Universo",
            "GPE"
          ],
          [
            "pois eu falo \\n",
            "PERSON"
          ],
          [
            "modificando o ciclo \\nde si próprio de outro",
            "ORG"
          ],
          [
            "universo pelo",
            "PERSON"
          ],
          [
            "Matéria",
            "GPE"
          ],
          [
            "galáxia e universo",
            "PERSON"
          ],
          [
            "único ciclo de caos",
            "ORG"
          ]
        ],
        "readability_score": 87.89591249280369,
        "semantic_density": 0,
        "word_count": 193,
        "unique_words": 112,
        "lexical_diversity": 0.5803108808290155
      },
      "preservation_score": 3.594161166478524e-06
    },
    {
      "id": 1,
      "text": "— 162 —Círculo 360° dividido por 9 (40° do centro para o meio), sen -\\ndo que a divisão têm que ser feita de 90 ou 270° , dividindo na \\nmesma proporção do meio para ponta, traçar uma linha hori -\\nzontal 0° a 180° (linha de tempo) no meio do círculo, marcar \\n90° número 9 reduzido na soma até a redução a chegar um \\núnico número 130° reduzido dá 4, sendo o número 1 como se \\nfosse sentido horário (relógio), número 2 170° dando 8, 3 190° \\ngraus dando 1, 4 230° dando 5, 9 270° novamente pois temos \\ndois triângulos em um único círculo, material e energia, 5 310° \\ndando 4, 6 350° dando 8, 7 10° dando 1, 8 50° dando 5.\\nAnálise de número perante o comportamento humano, em \\ncontexto e proporção universal.\\n1 calcula – análise de benefícios ou malefícios para cada um \\n– pessoas com muito sentimento ou pouco sentimento – mun -\\ndo material\\n2 executa – pulso da minha certeza diante do meu próprio caos \\n– pessoas explosivas ou sentimentais – mundo material\\n3 físico – matéria – tempo – consciência – meio em que se \\nencontra – mundo material\\n4 reação – sentimento da energia emitida. De acordo com a sua \\nnecessidade (pode ser mutável). Ambos os lados estão envian -\\ndo energia, ocasionando a reação de ambos os lados seja ela \\nagradável, boa, suportável ou ruim.\\n5 envia – momento que a consciência recebe os valores da sua \\nvida diante da sua importância, muita ou pouca importância, \\nrelativo de acordo como se foi criado no meio em que viveu \\n“mundo energia’\\n6 energia – subconsciente – sentimento – alma – empatia – \\nmundo espiritual – captação de energia relativo para cada um \\n– quântico “ mundo energia “ , \\ncaos do passado sendo vivido no futuro editável.indd   162caos do passado sendo vivido no futuro editável.indd   162 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 272319,
      "chapter": 8,
      "page": 162,
      "segment_type": "page",
      "themes": {
        "filosofia": 53.57142857142857,
        "ciencia": 46.42857142857144
      },
      "difficulty": 39.369278996865205,
      "complexity_metrics": {
        "word_count": 319,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 39.875,
        "avg_word_length": 4.470219435736677,
        "unique_word_ratio": 0.5611285266457681,
        "avg_paragraph_length": 319.0,
        "punctuation_density": 0.10031347962382445,
        "line_break_count": 30,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "dando",
          "energia",
          "meio",
          "número",
          "mundo",
          "material",
          "sentimento",
          "círculo",
          "sendo",
          "proporção",
          "linha",
          "tempo",
          "reduzido",
          "único",
          "como",
          "análise",
          "cada",
          "pessoas",
          "diante",
          "caos"
        ],
        "entities": [
          [
            "9",
            "CARDINAL"
          ],
          [
            "40",
            "CARDINAL"
          ],
          [
            "para o meio",
            "PERSON"
          ],
          [
            "que",
            "CARDINAL"
          ],
          [
            "ser feita de 90",
            "ORG"
          ],
          [
            "270",
            "CARDINAL"
          ],
          [
            "meio para ponta",
            "PERSON"
          ],
          [
            "180",
            "CARDINAL"
          ],
          [
            "90° número",
            "QUANTITY"
          ],
          [
            "130",
            "CARDINAL"
          ]
        ],
        "readability_score": 78.721434169279,
        "semantic_density": 0,
        "word_count": 319,
        "unique_words": 179,
        "lexical_diversity": 0.5611285266457681
      },
      "preservation_score": 1.0935581642429588e-05
    },
    {
      "id": 1,
      "text": "— 163 —7 absorção – sentimento – entendimento sobre o que é bom \\nou ruim perante a um viver a minha necessidade – mundo \\nespiritual – captação de energia perante ao meio em que eu \\nvivo – quântico “mundo energia”\\n8 percepção – fruto do meio – de acordo com a sua forma de \\nviver a vida – importância, valores – DNA junto ao meio em \\nque nós vivemos – “mundo energia”\\n9 movimento - vida – equilíbrio \\nCálculo em ciclo infinito\\n1+1 = 2\\n2+2 = 4\\n4+4 = 8\\n8+8 =1 6 reduzir 1+6 = 7\\n7+7 =14 = 5\\n5+5 =10 =1 \\nCiclo infinito cortando o triângulo da vida\\n3+3 =6\\n6+6 =12\\n12+3 =15 = 6\\n12+6 =18 = 9\\n12+12 = 24 = 6\\n24+3 = 27 = 9\\n24+6 =3 \\n24+24 = 48 = 12 = 3\\n48+3 = 51 = 6\\ncaos do passado sendo vivido no futuro editável.indd   163caos do passado sendo vivido no futuro editável.indd   163 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 274206,
      "chapter": 8,
      "page": 163,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.12857142857143,
      "complexity_metrics": {
        "word_count": 168,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 56.0,
        "avg_word_length": 3.761904761904762,
        "unique_word_ratio": 0.6369047619047619,
        "avg_paragraph_length": 168.0,
        "punctuation_density": 0.041666666666666664,
        "line_break_count": 25,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mundo",
          "energia",
          "meio",
          "vida",
          "perante",
          "viver",
          "ciclo",
          "infinito",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "absorção",
          "sentimento",
          "entendimento",
          "ruim",
          "minha",
          "necessidade"
        ],
        "entities": [
          [
            "163",
            "CARDINAL"
          ],
          [
            "que eu",
            "PERSON"
          ],
          [
            "8",
            "CARDINAL"
          ],
          [
            "9",
            "CARDINAL"
          ],
          [
            "2",
            "CARDINAL"
          ],
          [
            "4",
            "CARDINAL"
          ],
          [
            "1 6",
            "CARDINAL"
          ],
          [
            "1+6",
            "CARDINAL"
          ],
          [
            "7",
            "CARDINAL"
          ],
          [
            "7+7",
            "DATE"
          ]
        ],
        "readability_score": 70.87142857142857,
        "semantic_density": 0,
        "word_count": 168,
        "unique_words": 107,
        "lexical_diversity": 0.6369047619047619
      },
      "preservation_score": 2.5516357165669033e-06
    },
    {
      "id": 1,
      "text": "— 164 —48+6 = 54 = 9\\nQuando vemos uma repetição do número na alternância, ve -\\nmos que ele obriga a dar o número oposto, abrigando a manter \\num padrão entre o físico e a energia.\\n9+9 = 18 = 9\\n18+9 = 27 = 9\\n18+18 = 36 = 9\\n36+9 = 45 = 9\\n1+2+4+8+7+5 = 27 = 9\\n9 é o número da vida, é a junção de tudo que existe.\\n9 é o número que segue seu próprio ciclo, pois 9 é o número de \\ntodas as médias da exatidão 45° , 90° , 180° , 270° , 360° .\\nTodos os números somado a si próprio dá o ciclo de si próprio, \\nterminando em 9. Porém têm um número que segue uma re -\\ngra diferente.\\nApenas um número de si próprio dá uma volta em si próprio \\nno seu próprio número, esse é o número 7, é o número que in -\\nterpreta a energia, é o número que dá o entendimento da vida, \\nesse número temos muitas referências de vida para esse núme -\\nro: 7 dias da semana, 7 selos do Apocalipse, 7 Maravilhas do \\nMundo, 7 pecados capitais, é o único número que dá volta no \\nseu próprio número entre o ciclo 1,2,4,8,7,5,1. Reduzir o nú -\\nmero somado dá uma sequência infinita de redução infinita.\\n7+7=14+7=21+7=28+7=35+7=42+7=49\\n7  5   3   1  8   6  4*\\n49+ 7=56+7=63+7=70+7=77+7=84...\\n4* 2  9  7  5  3\\ncaos do passado sendo vivido no futuro editável.indd   164caos do passado sendo vivido no futuro editável.indd   164 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 275137,
      "chapter": 8,
      "page": 164,
      "segment_type": "page",
      "themes": {},
      "difficulty": 26.021339347675227,
      "complexity_metrics": {
        "word_count": 262,
        "sentence_count": 11,
        "paragraph_count": 1,
        "avg_sentence_length": 23.818181818181817,
        "avg_word_length": 3.950381679389313,
        "unique_word_ratio": 0.5152671755725191,
        "avg_paragraph_length": 262.0,
        "punctuation_density": 0.15267175572519084,
        "line_break_count": 27,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "número",
          "próprio",
          "vida",
          "ciclo",
          "esse",
          "entre",
          "energia",
          "segue",
          "somado",
          "volta",
          "infinita",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "quando",
          "vemos",
          "repetição"
        ],
        "entities": [
          [
            "164",
            "CARDINAL"
          ],
          [
            "48+6",
            "CARDINAL"
          ],
          [
            "54",
            "CARDINAL"
          ],
          [
            "9",
            "CARDINAL"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "9+9",
            "TIME"
          ],
          [
            "18",
            "CARDINAL"
          ],
          [
            "9",
            "CARDINAL"
          ],
          [
            "18+9",
            "DATE"
          ],
          [
            "27",
            "CARDINAL"
          ]
        ],
        "readability_score": 86.9057945870923,
        "semantic_density": 0,
        "word_count": 262,
        "unique_words": 135,
        "lexical_diversity": 0.5152671755725191
      },
      "preservation_score": 9.251502069495433e-06
    },
    {
      "id": 1,
      "text": "— 165 —Todos os demais números do ciclo infinito 1,2,4,8,7,5 dão ci -\\nclo de si próprios em 9 números reduzidos e todos os núme -\\nros têm um ciclo dentro de si próprio de sequência dos nove \\nnúmeros.\\n1+1=2+1=3+1=4+1=5+1=6+1=7+1=8+1=9+1\\n1  2  3   4  5  6  7 8 9\\n10+1=11+1=12+1=13+1=14...   \\n1  2  3  4  5\\n2+2=4+2=6+2=8+2=10+2=12+2=14+2=16+2\\n2 4 6  8  1  3  5 7\\n18+2=20+2=22+2=24+2=26+2=28+2=30...\\n9  2   4  6  8   1  3...\\n3 é o número da matéria, é o impulso, é o físico da energia, é a \\nbase do triângulo do número 9 esse número segue o ciclo de \\n3,6, 9...\\n3+3=6+3=9+3=12+3=15+3=18+3=21+3=24...\\n3  6  9  3   6   9  3   6\\n4+4=8+4=12+4=16+4=20+4=24+4=28+4=32\\n4  8  3   7   2   6   1  5\\n36+4=40+4=44+4=48+4=52...\\n9   4  8   3  7...\\n5+5=10+5=15+5=20+5=25+5=30+5=35+5\\n5  1   6  2   7   3   8\\n40+5=45+5=50+5=55+5=60...\\n4   9   5  1  6\\ncaos do passado sendo vivido no futuro editável.indd   165caos do passado sendo vivido no futuro editável.indd   165 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 276577,
      "chapter": 8,
      "page": 165,
      "segment_type": "page",
      "themes": {},
      "difficulty": 20.185625,
      "complexity_metrics": {
        "word_count": 160,
        "sentence_count": 12,
        "paragraph_count": 1,
        "avg_sentence_length": 13.333333333333334,
        "avg_word_length": 4.68125,
        "unique_word_ratio": 0.48125,
        "avg_paragraph_length": 160.0,
        "punctuation_density": 0.25625,
        "line_break_count": 25,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "números",
          "ciclo",
          "número",
          "todos",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "demais",
          "infinito",
          "próprios",
          "reduzidos",
          "núme",
          "dentro",
          "próprio",
          "sequência",
          "nove",
          "matéria"
        ],
        "entities": [
          [
            "165",
            "CARDINAL"
          ],
          [
            "1,2,4,8,7,5",
            "CARDINAL"
          ],
          [
            "9",
            "CARDINAL"
          ],
          [
            "1+1=2+1=3+1=4+1=5+1=6+1=7+1=8+1=9+1",
            "DATE"
          ],
          [
            "1",
            "CARDINAL"
          ],
          [
            "1",
            "CARDINAL"
          ],
          [
            "6  8  1  3",
            "QUANTITY"
          ],
          [
            "18+2=20+2=22+2=24+2=26+2=28+2=30",
            "DATE"
          ],
          [
            "9  2",
            "CARDINAL"
          ],
          [
            "1",
            "CARDINAL"
          ]
        ],
        "readability_score": 91.92895833333333,
        "semantic_density": 0,
        "word_count": 160,
        "unique_words": 77,
        "lexical_diversity": 0.48125
      },
      "preservation_score": 8.20168623182219e-06
    },
    {
      "id": 1,
      "text": "— 166 —6 é o número da energia da base do triângulo, esse número \\njuntamente ao número 7, mostra o quanto esse lado do triân -\\ngulo é mais importante que o lado físico do triângulo. São dois \\nciclos de importância da vida em um mesmo lado, pois o saber \\ndrenar a energia do universo para si próprio é mais importante \\nque viver o lado físico da energia. \\n6+6=12+6=18+6=24+6=30+6=36+6=42...\\n6  3  9   6   3   9   6\\nO lado da energia é tão importante para o mundo, que a maio -\\nria das numerologias e quase todos os estudos de importância \\nde padrão perante aos números, dão ênfase ao lado dos núme -\\nros 5,6,7,8. \\nNa cabala judaica, o número 8 é o número de nascença de \\npessoas importantes. É a maior quantidade de pessoas que nas -\\nceram nessa data que modificaram o mundo. \\n8 na minha teoria da energia em ciclo de propagação é o nú -\\nmero da captação da energia, o 7 é a interpretação da energia, \\ne o 5 é a execução da energia para o físico, sendo o número 1 \\n(Divino, início do movimento) é o que transforma a energia \\npara o mundo físico, o 2 é execução no mundo físico e o 4 \\ntransforma o físico, para energia.\\nCortando o 3 mundo físico, material, palpável, 6 o número da \\nenergia, alma, subconsciente, empatia, 9 é o número da vida, é \\no número de quem faz ligação com todos, é o centro de tudo.\\n8+8=16+8=24+8=32+8=40+8=48+8=56+8 \\n8  7  6   5   4   3  2\\n64+8=72+8=80+8=88+8=96+8=104... \\n6   9  8   7   6   5\\ncaos do passado sendo vivido no futuro editável.indd   166caos do passado sendo vivido no futuro editável.indd   166 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 277681,
      "chapter": 8,
      "page": 166,
      "segment_type": "page",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 27.285328638497653,
      "complexity_metrics": {
        "word_count": 284,
        "sentence_count": 12,
        "paragraph_count": 1,
        "avg_sentence_length": 23.666666666666668,
        "avg_word_length": 4.362676056338028,
        "unique_word_ratio": 0.4823943661971831,
        "avg_paragraph_length": 284.0,
        "punctuation_density": 0.15140845070422534,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "número",
          "físico",
          "lado",
          "mundo",
          "importante",
          "sendo",
          "triângulo",
          "esse",
          "mais",
          "importância",
          "vida",
          "todos",
          "pessoas",
          "execução",
          "transforma",
          "passado",
          "vivido",
          "futuro",
          "editável"
        ],
        "entities": [
          [
            "166",
            "CARDINAL"
          ],
          [
            "6",
            "CARDINAL"
          ],
          [
            "juntamente ao número",
            "PERSON"
          ],
          [
            "mostra",
            "LOC"
          ],
          [
            "lado físico",
            "PERSON"
          ],
          [
            "universo para",
            "PERSON"
          ],
          [
            "mais importante \\n",
            "PERSON"
          ],
          [
            "lado físico da energia",
            "PERSON"
          ],
          [
            "6+6=12+6=18+6=24+6=30+6=36",
            "DATE"
          ],
          [
            "6  3",
            "CARDINAL"
          ]
        ],
        "readability_score": 86.85786384976525,
        "semantic_density": 0,
        "word_count": 284,
        "unique_words": 137,
        "lexical_diversity": 0.4823943661971831
      },
      "preservation_score": 1.061480458091832e-05
    },
    {
      "id": 1,
      "text": "— 167 —Gráfico de conexão entre círculo e triângulo\\nGráfico de várias linhas de tempo em propagação do movi -\\nmento em propagação da energia em movimento de concor -\\ndância.\\nCada triângulo cria um movimento proporcional.\\ncaos do passado sendo vivido no futuro editável.indd   167caos do passado sendo vivido no futuro editável.indd   167 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 279372,
      "chapter": 8,
      "page": 167,
      "segment_type": "page",
      "themes": {},
      "difficulty": 22.563157894736843,
      "complexity_metrics": {
        "word_count": 57,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 11.4,
        "avg_word_length": 5.543859649122807,
        "unique_word_ratio": 0.6842105263157895,
        "avg_paragraph_length": 57.0,
        "punctuation_density": 0.14035087719298245,
        "line_break_count": 5,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "gráfico",
          "triângulo",
          "propagação",
          "movimento",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "conexão",
          "entre",
          "círculo",
          "várias",
          "linhas",
          "tempo",
          "movi",
          "mento",
          "energia",
          "concor"
        ],
        "entities": [
          [
            "167",
            "CARDINAL"
          ],
          [
            "Gráfico de várias linhas de tempo",
            "ORG"
          ],
          [
            "movimento de concor -\\ndância",
            "ORG"
          ],
          [
            "Cada",
            "PERSON"
          ],
          [
            "editável.indd",
            "CARDINAL"
          ],
          [
            "167caos",
            "CARDINAL"
          ],
          [
            "editável.indd",
            "CARDINAL"
          ],
          [
            "167",
            "CARDINAL"
          ]
        ],
        "readability_score": 92.63684210526316,
        "semantic_density": 0,
        "word_count": 57,
        "unique_words": 39,
        "lexical_diversity": 0.6842105263157895
      },
      "preservation_score": 4.374232656971835e-07
    },
    {
      "id": 1,
      "text": "— 168 —Gráfico demonstrativo de união de energia\\nGráfico demonstrativo de propagação de ciclo dentro de outro \\nciclo.\\ncaos do passado sendo vivido no futuro editável.indd   168caos do passado sendo vivido no futuro editável.indd   168 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 279868,
      "chapter": 8,
      "page": 168,
      "segment_type": "page",
      "themes": {},
      "difficulty": 21.823684210526316,
      "complexity_metrics": {
        "word_count": 38,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 9.5,
        "avg_word_length": 6.078947368421052,
        "unique_word_ratio": 0.6578947368421053,
        "avg_paragraph_length": 38.0,
        "punctuation_density": 0.18421052631578946,
        "line_break_count": 3,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "gráfico",
          "demonstrativo",
          "ciclo",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "união",
          "energia",
          "propagação",
          "dentro",
          "outro",
          "caos"
        ],
        "entities": [
          [
            "168",
            "CARDINAL"
          ],
          [
            "Gráfico",
            "ORG"
          ],
          [
            "Gráfico",
            "ORG"
          ],
          [
            "de propagação de ciclo dentro de outro",
            "ORG"
          ],
          [
            "editável.indd   168caos",
            "CARDINAL"
          ],
          [
            "editável.indd",
            "CARDINAL"
          ],
          [
            "168",
            "CARDINAL"
          ]
        ],
        "readability_score": 93.42631578947369,
        "semantic_density": 0,
        "word_count": 38,
        "unique_words": 25,
        "lexical_diversity": 0.6578947368421053
      },
      "preservation_score": 1.9684046956373255e-07
    },
    {
      "id": 1,
      "text": "— 169 —Teoria do movimento da energia em propagação perfeita.\\n“Se descobrirmos a magnificência dos números 3,6 e 9 desco -\\nbrimos a magnitude da existência em um viver a vida. ” Nikola \\nTesla\\nDeus fez o mundo distante dele, para enxergar como melhor \\nfazê-lo!\\nNossos movimentos gera uma ação e um reação, nesse mesmo \\nmovimento temos uma ação e uma reação proporcional ao \\nmovimento inicial. \\nQuando estamos com uma vida muito turbulenta, com mui -\\ntos problemas para se pensar, conseguimos controlar os nossos \\nimpulsos?\\nQuando estamos correndo, competindo, jogando a ambição \\nde executar o movimento nos faz sentir câimbras, dores mus -\\nculares, exaustão...\\nEm uma partida de futebol, futebol americano, basquete, vôlei \\nquem interpreta melhor a organização de se jogar, o jogador \\nque está dentro do jogo ou o técnico que está fora do jogo?\\nTudo em nossas vidas têm uma necessidade de se movimentar \\ncorretamente, de acordo com a reação que irá ter diante da \\nnossa própria ação, seja ela física (corpo) ou Quântica (nossa \\nmente não têm gravidade e nem tempo, tudo dentro dela é \\numa energia onipresente). Essa mesma ação cria uma reação, \\nessa reação qual é o tamanho do movimento e o gasto de ener -\\ngia para conter a ele?\\nAo descobrirmos a magnificência do número 9 (vida), desco -\\nbrimos o sentido da vida, mas para se chegarmos ao número \\n9 Temos um trajeto de concordância de valores entre o 3 e o \\n6, para chegarmos a concordância dos números 3 e 6, temos \\ncaos do passado sendo vivido no futuro editável.indd   169caos do passado sendo vivido no futuro editável.indd   169 28/03/2022   14:53:4028/03/2022   14:53:40",
      "position": 280261,
      "chapter": 8,
      "page": 169,
      "segment_type": "page",
      "themes": {
        "filosofia": 53.57142857142857,
        "ciencia": 46.42857142857144
      },
      "difficulty": 29.919871794871796,
      "complexity_metrics": {
        "word_count": 273,
        "sentence_count": 12,
        "paragraph_count": 1,
        "avg_sentence_length": 22.75,
        "avg_word_length": 4.871794871794871,
        "unique_word_ratio": 0.6190476190476191,
        "avg_paragraph_length": 273.0,
        "punctuation_density": 0.1391941391941392,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "movimento",
          "reação",
          "vida",
          "ação",
          "temos",
          "energia",
          "descobrirmos",
          "magnificência",
          "números",
          "desco",
          "brimos",
          "melhor",
          "nossos",
          "quando",
          "estamos",
          "futebol",
          "está",
          "dentro",
          "jogo",
          "tudo"
        ],
        "entities": [
          [
            "169",
            "CARDINAL"
          ],
          [
            "magnificência dos",
            "ORG"
          ],
          [
            "números",
            "ORG"
          ],
          [
            "3,6",
            "CARDINAL"
          ],
          [
            "9 desco -\\nbrimos",
            "QUANTITY"
          ],
          [
            "para enxergar como melhor",
            "PERSON"
          ],
          [
            "ação e uma reação",
            "ORG"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "muito turbulenta",
            "PERSON"
          ],
          [
            "para se pensar",
            "PERSON"
          ]
        ],
        "readability_score": 87.16346153846153,
        "semantic_density": 0,
        "word_count": 273,
        "unique_words": 169,
        "lexical_diversity": 0.6190476190476191
      },
      "preservation_score": 1.141674723469649e-05
    },
    {
      "id": 1,
      "text": "— 170 —que ter uma concordância de movimento entre o 1,2,4,8,7 e \\n5 nos mostrando a necessidade de se viver em um equilíbrio \\nemocional e corpóreo.\\nTudo em nossa vida é um ciclo de aprendizado sem preceden -\\ntes de quando será usado, temos marcações de energia atem -\\nporal, 12 horas do relógio, 12 signos do zodíacos, estrela de \\nDavi (melhor captação de movimentar-se)tudo nos mostrando \\no nosso próprio ciclo universal!\\n9\\n9 - 360° - 06\\n8 - 330°\\n3\\n7 - 300°\\n9\\n9 - 270°3\\n1 - 30°\\n6\\n2 - 60°\\n99 - 90°\\n33 - 120°\\n64 - 150°\\n99 - 180°\\n35 - 210°66 - 240°\\ncaos do passado sendo vivido no futuro editável.indd   170caos do passado sendo vivido no futuro editável.indd   170 28/03/2022   14:53:4128/03/2022   14:53:41",
      "position": 282004,
      "chapter": 8,
      "page": 170,
      "segment_type": "page",
      "themes": {},
      "difficulty": 29.76766917293233,
      "complexity_metrics": {
        "word_count": 133,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 26.6,
        "avg_word_length": 4.225563909774436,
        "unique_word_ratio": 0.6842105263157895,
        "avg_paragraph_length": 133.0,
        "punctuation_density": 0.12030075187969924,
        "line_break_count": 23,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mostrando",
          "tudo",
          "ciclo",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "concordância",
          "movimento",
          "entre",
          "necessidade",
          "viver",
          "equilíbrio",
          "emocional",
          "corpóreo",
          "nossa",
          "vida",
          "aprendizado"
        ],
        "entities": [
          [
            "170",
            "CARDINAL"
          ],
          [
            "1,2,4,8,7 e \\n",
            "PERCENT"
          ],
          [
            "5",
            "CARDINAL"
          ],
          [
            "Tudo",
            "PERSON"
          ],
          [
            "tes de quando",
            "PERSON"
          ],
          [
            "12",
            "CARDINAL"
          ],
          [
            "relógio",
            "GPE"
          ],
          [
            "12",
            "CARDINAL"
          ],
          [
            "zodíacos",
            "ORG"
          ],
          [
            "estrela de \\nDavi",
            "ORG"
          ]
        ],
        "readability_score": 85.43233082706767,
        "semantic_density": 0,
        "word_count": 133,
        "unique_words": 91,
        "lexical_diversity": 0.6842105263157895
      },
      "preservation_score": 6.036441066621133e-06
    },
    {
      "id": 1,
      "text": "— 171 —Os números multiplicados entre eles terminam em 9 (vida) a \\nsequência entre 3,6 e 9 e qualquer número multiplicados por \\nesses mesmos números, terminam o ciclo em 9.\\nE a sequência entre 1,2,4,8,7 e 5 terminam a sequência em 1 \\n(início do movimento).\\nMúltiplos de término 9\\n3x1 = 3x3 =9\\n3x2 = 6x3 =18 – 9\\n3x4 = 12 – 3x3 = 9\\n3x8 = 24 – 6x3 = 18 – 9\\n3x7 = 21 – 3x3 = 9 \\n3x5 = 15 – 6x3 = 18 – 9\\nMúltiplos de término 1\\n1x1 = 1\\n2x2 = 4x2 = 8x2 = 16 – 7x2 = 14 – 5x2 = 10 – 1\\n4x4 = 16 – 7x4 = 28 – 10 – 1\\n8x8 = 64 – 10 – 1\\n7x7 = 49 – 13 – 4x7 = 28 – 10 – 1\\n5x5 = 25 – 7x5 = 35 – 8x5 = 40 – 4x5 = 20 – 2x5 = 10 – 1\\nNúmero 1 é o início de tudo. \\nNúmero 2 é o trajeto da física.\\ncaos do passado sendo vivido no futuro editável.indd   171caos do passado sendo vivido no futuro editável.indd   171 28/03/2022   14:53:4128/03/2022   14:53:41",
      "position": 282826,
      "chapter": 8,
      "page": 171,
      "segment_type": "page",
      "themes": {},
      "difficulty": 27.493034825870648,
      "complexity_metrics": {
        "word_count": 201,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 28.714285714285715,
        "avg_word_length": 3.0945273631840795,
        "unique_word_ratio": 0.48258706467661694,
        "avg_paragraph_length": 201.0,
        "punctuation_density": 0.07960199004975124,
        "line_break_count": 21,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "entre",
          "terminam",
          "sequência",
          "número",
          "números",
          "multiplicados",
          "início",
          "múltiplos",
          "término",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "eles",
          "vida",
          "qualquer",
          "esses",
          "mesmos"
        ],
        "entities": [
          [
            "171",
            "CARDINAL"
          ],
          [
            "9",
            "CARDINAL"
          ],
          [
            "3,6",
            "CARDINAL"
          ],
          [
            "9 e qualquer número",
            "QUANTITY"
          ],
          [
            "mesmos números",
            "PERSON"
          ],
          [
            "terminam o ciclo em",
            "ORG"
          ],
          [
            "9",
            "CARDINAL"
          ],
          [
            "1,2,4,8,7",
            "CARDINAL"
          ],
          [
            "1",
            "CARDINAL"
          ],
          [
            "Múltiplos de",
            "PERSON"
          ]
        ],
        "readability_score": 84.71449893390192,
        "semantic_density": 0,
        "word_count": 201,
        "unique_words": 97,
        "lexical_diversity": 0.48258706467661694
      },
      "preservation_score": 3.3681591458683127e-06
    },
    {
      "id": 1,
      "text": "— 172 —Número 4 é a transformação da física para energia quântica.\\nNúmero 8 é o início da energia quântica.\\nNúmero 7 é o trajeto da energia quântica.\\nNúmero 5 é a transformação da energia quântica para física.\\nTudo em nosso universo se resume em somar, multiplicar e \\nreduzir até se adaptar a própria energia.\\n“Nós somos um eterno movimento físico e quântico de gerar \\ncaos e se adaptar ao próprio caos... ”\\nTodos os gráficos são cálculos de ciclos de si próprios, afetan -\\ndo o outro ciclo de si próprio em constante caos, gerado pela \\nprópria evolução em querer se adaptar, gerando mais caos se \\nexpandindo e adaptando, gerando mais caos e se adaptando. \\nEm um ciclo infinito de caos afunilando a energia, criando \\ncaminhos de energia perante o caos, tendo uma maior mas -\\nsa perante a energia, criando “caminhos” de energia, fazendo \\na absorção da energia ser melhor interpretada por ter menos \\nenergia no nosso próprio entorno. Gerando grandes captado -\\nres diante de uma necessidade de se manter em um ciclo de \\nsobrevivência de cada um, sendo que o maior caos sempre irá \\nmanter uma canalização de energia maior, do que a o caos que \\nnos mesmos criamos diante do nosso próprio planeta. Univer -\\nso controla as galáxias, que cada galáxia têm um buraco negro \\ncom uma maior massa, gerando um epicentro e formando um \\n“furacão de areia” de sistemas, criando caos em seu entorno, \\nfazendo não conseguirmos acessar e enxergar planetas “próxi -\\nmos” de nós, por não termos ângulo ou uma grande quanti -\\ndade de astros em nossa frente, fazendo calcularmos a energia \\ncaos do passado sendo vivido no futuro editável.indd   172caos do passado sendo vivido no futuro editável.indd   172 28/03/2022   14:53:4128/03/2022   14:53:41",
      "position": 283777,
      "chapter": 8,
      "page": 172,
      "segment_type": "page",
      "themes": {},
      "difficulty": 29.48390410958904,
      "complexity_metrics": {
        "word_count": 292,
        "sentence_count": 12,
        "paragraph_count": 1,
        "avg_sentence_length": 24.333333333333332,
        "avg_word_length": 4.832191780821918,
        "unique_word_ratio": 0.5513698630136986,
        "avg_paragraph_length": 292.0,
        "punctuation_density": 0.11643835616438356,
        "line_break_count": 27,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "caos",
          "número",
          "quântica",
          "próprio",
          "gerando",
          "maior",
          "nosso",
          "adaptar",
          "ciclo",
          "criando",
          "fazendo",
          "sendo",
          "transformação",
          "física",
          "própria",
          "mais",
          "adaptando",
          "caminhos",
          "perante"
        ],
        "entities": [
          [
            "172",
            "CARDINAL"
          ],
          [
            "4",
            "CARDINAL"
          ],
          [
            "para",
            "GPE"
          ],
          [
            "Número 8",
            "PERSON"
          ],
          [
            "Número 7",
            "PERSON"
          ],
          [
            "Número 5",
            "PERSON"
          ],
          [
            "quântica",
            "NORP"
          ],
          [
            "para física",
            "PERSON"
          ],
          [
            "Tudo",
            "PERSON"
          ],
          [
            "universo se resume",
            "PERSON"
          ]
        ],
        "readability_score": 86.38367579908676,
        "semantic_density": 0,
        "word_count": 292,
        "unique_words": 161,
        "lexical_diversity": 0.5513698630136986
      },
      "preservation_score": 9.842023478186629e-06
    },
    {
      "id": 1,
      "text": "— 173 —universal em estudarmos astrologia, cabala, religião tudo aqui -\\nlo que estuda o universo. Diante de um padrão cíclico de caos \\ngerado pela maior massa gravitacional de cada galáxia, nos \\ntransformando em um ser que briga consigo em se adaptar ao \\ncaos do universo!!!\\nEu dou sentindo a ter existido Deus, Big Bang , Moisés, Pitágo -\\nras, Jesus, Issac Newton, Darwin, Tesla, Einstein.\\nNão sei se isso pode ser uma coisa boa ou ruim.\\nVejo alguns seres humanos capazes de entender e outros não.\\nVejo o mundo no caos e, a qualquer momento, pode vir piorar \\no caos, pois, no meu próprio cálculo, mostra que estamos pró -\\nximos de ter um novo cataclismo (apocalipse). \\nEu falei para um amigo que estou torcendo para eu estar erra -\\ndo, o perder o meu viver é perder as minhas maiores conquis -\\ntas (minha família, meus amigos, meu estilo de vida).\\nNós nascemos sem saber nada, sem manual de instrução de \\ncomo viver (universo em expansão aprendendo com o seu \\ncaos), vivendo em um caos em adaptação ao caos do próprio \\nuniverso.\\nO que têm a ver energia, religião, filosofia, matemática, geopo -\\nlítica, física, ciências e física quântica?\\nQuando nós começamos a viver no mundo, nós vivíamos co -\\nnectados com o mundo iguais animais irracionais (pássaros \\nvoando para longe de catástrofes), a partir dessa forma de cap -\\ntar a energia necessária para sobreviver, começamos a retirar \\nmais do que o necessário para nossa sobrevivência (próximo a \\nlinha do Equador temos uma maior produção de alimentos), \\nassim começamos a retirar muito mais do que o necessário do \\nEgito (grande quantidade de mão escrava), Palestina (religião, \\ncaos do passado sendo vivido no futuro editável.indd   173caos do passado sendo vivido no futuro editável.indd   173 28/03/2022   14:53:4128/03/2022   14:53:41",
      "position": 285618,
      "chapter": 8,
      "page": 173,
      "segment_type": "page",
      "themes": {
        "filosofia": 53.57142857142857,
        "ciencia": 46.42857142857144
      },
      "difficulty": 29.014576365663324,
      "complexity_metrics": {
        "word_count": 299,
        "sentence_count": 12,
        "paragraph_count": 1,
        "avg_sentence_length": 24.916666666666668,
        "avg_word_length": 4.909698996655519,
        "unique_word_ratio": 0.6622073578595318,
        "avg_paragraph_length": 299.0,
        "punctuation_density": 0.16722408026755853,
        "line_break_count": 29,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "caos",
          "universo",
          "religião",
          "mundo",
          "viver",
          "começamos",
          "maior",
          "pode",
          "vejo",
          "próprio",
          "perder",
          "energia",
          "física",
          "retirar",
          "mais",
          "necessário",
          "passado",
          "sendo",
          "vivido",
          "futuro"
        ],
        "entities": [
          [
            "173",
            "CARDINAL"
          ],
          [
            "astrologia",
            "GPE"
          ],
          [
            "cabala",
            "GPE"
          ],
          [
            "Diante de um padrão",
            "PERSON"
          ],
          [
            "gerado pela",
            "PERSON"
          ],
          [
            "massa gravitacional de cada galáxia",
            "PERSON"
          ],
          [
            "Eu dou sentindo",
            "PERSON"
          ],
          [
            "Deus",
            "PERSON"
          ],
          [
            "Big Bang",
            "GPE"
          ],
          [
            "Jesus",
            "PERSON"
          ]
        ],
        "readability_score": 86.06875696767001,
        "semantic_density": 0,
        "word_count": 299,
        "unique_words": 198,
        "lexical_diversity": 0.6622073578595318
      },
      "preservation_score": 1.5433750891348957e-05
    },
    {
      "id": 1,
      "text": "— 174 —grande quantidade de mão de obra escrava), Grécia (filosofia, \\ngrande quantidade de mão de obra escrava), Roma (filosofia, \\nreligião e mão de obra escrava), cataclismo (explosão vulcâni -\\nca, devido á Terra perder o eixo e rotacionar entre as engrena -\\ngens com uma maior intensidade, devido a nós tirarmos mais \\nde um lado da terra e menos de outro lado, perdendo o equi -\\nlíbrio do eixo da terra), expansão da Europa (países litorâneos, \\nmaior facilidade em fazer comércio, maior quantidade de mão \\nescrava) devido a ter menos recursos para retirar das suas terras \\n(quantidade de terra para plantio e crescimento desordenado), \\ncrescimento de países fora do eixo Eurásia (países próximos \\nà linha do Equador, melhor plantio devido à temperatura), \\ncrescimento dos EUA, primeiro país a “dominar” a tecnologia \\nfora da Eurásia (menos pessoas urbanas e mais agrícola, mão \\nde obra escrava), Alemanha período das guerras (mão de obra \\nescrava), atualmente, a China teve um crescimento em trinta \\nanos nunca visto no mundo (China tinha 80% da população \\nagrícola, hoje a China têm 50% agrícola e urbano), nos fazen -\\ndo compreender um outro padrão.\\nO aumento da classe média faz o dinheiro girar no país todo \\nem todas as classes, assim fazendo a economia subir e melho -\\nrar o país. Porém, têm um problema, a quantidade de pessoas \\nna classe média consumindo mais do que o necessário para \\na sua sobrevivência, retirando mais recursos do planeta Terra, \\nfazendo os próprios seres humanos viverem regionalmente de -\\nvido a não terem recursos para todos!!!\\nQual é o próximo país em ascensão?\\nÍndia, pois, no momento, é o país com a maior quantidade \\nde mão de obra escrava, espaço físico para plantio grande, tec -\\nnologias avançadas e grande população (mão de obra escrava) \\npara ter uma produção de recursos para o mundo todo.\\ncaos do passado sendo vivido no futuro editável.indd   174caos do passado sendo vivido no futuro editável.indd   174 28/03/2022   14:53:4128/03/2022   14:53:41",
      "position": 287522,
      "chapter": 8,
      "page": 174,
      "segment_type": "page",
      "themes": {
        "filosofia": 56.60377358490566,
        "ciencia": 24.528301886792455,
        "tecnologia": 18.867924528301888
      },
      "difficulty": 35.187767584097855,
      "complexity_metrics": {
        "word_count": 327,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 40.875,
        "avg_word_length": 5.009174311926605,
        "unique_word_ratio": 0.5474006116207951,
        "avg_paragraph_length": 327.0,
        "punctuation_density": 0.1345565749235474,
        "line_break_count": 31,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "escrava",
          "obra",
          "quantidade",
          "terra",
          "país",
          "grande",
          "devido",
          "maior",
          "mais",
          "recursos",
          "crescimento",
          "eixo",
          "menos",
          "países",
          "plantio",
          "agrícola",
          "china",
          "filosofia",
          "lado",
          "outro"
        ],
        "entities": [
          [
            "174",
            "CARDINAL"
          ],
          [
            "Grécia",
            "PERSON"
          ],
          [
            "Roma",
            "PERSON"
          ],
          [
            "de outro lado",
            "PERSON"
          ],
          [
            "Europa",
            "LOC"
          ],
          [
            "das suas",
            "PERSON"
          ],
          [
            "Eurásia",
            "PERSON"
          ],
          [
            "Equador",
            "GPE"
          ],
          [
            "EUA",
            "ORG"
          ],
          [
            "primeiro",
            "ORG"
          ]
        ],
        "readability_score": 78.05974770642202,
        "semantic_density": 0,
        "word_count": 327,
        "unique_words": 179,
        "lexical_diversity": 0.5474006116207951
      },
      "preservation_score": 1.7176153566376073e-05
    },
    {
      "id": 1,
      "text": "— 175 —Além disso tudo que nós fazemos para a nossa própria sobre -\\nvivência, como iremos fazer isso tudo para a sobrevivência do \\nnosso próprio planeta?\\nTemos que ensinar um ao outro, pois o nosso caos do passado \\nestá sendo vivido no nosso futuro!!!\\ncaos do passado sendo vivido no futuro editável.indd   175caos do passado sendo vivido no futuro editável.indd   175 28/03/2022   14:53:4128/03/2022   14:53:41",
      "position": 289630,
      "chapter": 8,
      "page": 175,
      "segment_type": "page",
      "themes": {},
      "difficulty": 23.255384615384614,
      "complexity_metrics": {
        "word_count": 65,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 13.0,
        "avg_word_length": 5.184615384615385,
        "unique_word_ratio": 0.676923076923077,
        "avg_paragraph_length": 65.0,
        "punctuation_density": 0.18461538461538463,
        "line_break_count": 5,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "nosso",
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "tudo",
          "caos",
          "editável",
          "indd",
          "além",
          "disso",
          "fazemos",
          "nossa",
          "própria",
          "vivência",
          "como",
          "iremos",
          "fazer",
          "isso",
          "sobrevivência"
        ],
        "entities": [
          [
            "175",
            "CARDINAL"
          ],
          [
            "fazemos para",
            "PERSON"
          ],
          [
            "Temos",
            "PERSON"
          ],
          [
            "editável.indd",
            "CARDINAL"
          ],
          [
            "175caos",
            "CARDINAL"
          ],
          [
            "editável.indd",
            "CARDINAL"
          ],
          [
            "175",
            "CARDINAL"
          ],
          [
            "14:53:4128/03/2022",
            "CARDINAL"
          ]
        ],
        "readability_score": 91.94461538461539,
        "semantic_density": 0,
        "word_count": 65,
        "unique_words": 44,
        "lexical_diversity": 0.676923076923077
      },
      "preservation_score": 5.467790821214793e-07
    },
    {
      "id": 1,
      "text": "— 176 —\\ncaos do passado sendo vivido no futuro editável.indd   176caos do passado sendo vivido no futuro editável.indd   176 28/03/2022   14:53:4128/03/2022   14:53:41",
      "position": 290157,
      "chapter": 8,
      "page": 176,
      "segment_type": "page",
      "themes": {},
      "difficulty": 20.953623188405796,
      "complexity_metrics": {
        "word_count": 23,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 7.666666666666667,
        "avg_word_length": 5.956521739130435,
        "unique_word_ratio": 0.6086956521739131,
        "avg_paragraph_length": 23.0,
        "punctuation_density": 0.2608695652173913,
        "line_break_count": 1,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "caos"
        ],
        "entities": [
          [
            "176",
            "CARDINAL"
          ],
          [
            "editável.indd",
            "CARDINAL"
          ],
          [
            "176caos",
            "CARDINAL"
          ],
          [
            "editável.indd",
            "CARDINAL"
          ],
          [
            "176",
            "CARDINAL"
          ],
          [
            "14:53:4128/03/2022",
            "CARDINAL"
          ]
        ],
        "readability_score": 94.37971014492754,
        "semantic_density": 0,
        "word_count": 23,
        "unique_words": 14,
        "lexical_diversity": 0.6086956521739131
      },
      "preservation_score": 5.8323102092957795e-08
    },
    {
      "id": 1,
      "text": "— 177 —POSFÁCIO\\nTeoria sobre massa gravitacional de um buraco negro!!!\\nAssisti a um filme e, ao dormir, eu sonhei com o filme, geral -\\nmente quando eu sonho com algo, eu penso que esse mesmo \\nalgo é algum pensamento ou alguma coisa que seja da minha \\nvida, sentimento, problemas, amor, sexo, felicidade, ódio. Só \\nalguma referência. Nesse mesmo sentindo, eu me senti em \\nneurose. Não uma neurose de maluco, sim uma neurose de \\nnão compreender. Ficou um vazio, um vago. Simplesmente \\nnão tinha uma resposta, era uma ausência não sendo ausência \\ne sim só veio um sonho avulso, estranho, porém vai ter enten -\\ndimento. Percebi que essa ausência não era ausência, pois eu \\nnão sentia aflição, medo, felicidade, dor eu não sentia nada, \\nsimplesmente vivenciei. Nessa vivência, veio um vazio. Com \\nesse vazio, eu comecei a pensar: o que está acontecendo? Nova -\\nmente comecei a pensar no que estava se passando, qual moti -\\nvo dessa ausência. Fiquei interpretando semelhanças de acon -\\ntecimentos perante minha vida de semelhança, para entender \\no processo evolutivo de ter acontecido essa ausência, como foi \\no processo até aqui? Como foi a origem dessa ausência? Perce -\\nbi que não era ausência e sim excesso de energia em pensar o \\nmelhor, em ter feito o melhor para mim, percebi que eu não \\ntenho como viver melhor e sim viver, pois estou vivendo tan -\\ntos momentos bons que não me sinto merecedor. Por eu ser \\num pouco desapegado com bens materiais, e viver muito com \\nbons momentos sentimentais, eu estou tendo excesso de ener -\\ngia, me criando ausência (como se fosse um apagão). Nesse \\nmomento, eu percebi que o excesso de energia não é escassez e \\nsim ausência de energia. E, nessa ausência de energia, se cria o \\nvácuo. Nesse vácuo, se têm energia, porém a massa desse vácuo \\ncaos do passado sendo vivido no futuro editável.indd   177caos do passado sendo vivido no futuro editável.indd   177 28/03/2022   14:53:4128/03/2022   14:53:41",
      "position": 290440,
      "chapter": 8,
      "page": 177,
      "segment_type": "page",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 32.15615501519757,
      "complexity_metrics": {
        "word_count": 329,
        "sentence_count": 20,
        "paragraph_count": 1,
        "avg_sentence_length": 16.45,
        "avg_word_length": 4.811550151975684,
        "unique_word_ratio": 0.5775075987841946,
        "avg_paragraph_length": 329.0,
        "punctuation_density": 0.19148936170212766,
        "line_break_count": 30,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "ausência",
          "energia",
          "como",
          "nesse",
          "neurose",
          "vazio",
          "sendo",
          "percebi",
          "pensar",
          "excesso",
          "melhor",
          "viver",
          "vácuo",
          "massa",
          "filme",
          "mente",
          "sonho",
          "algo",
          "esse",
          "mesmo"
        ],
        "entities": [
          [
            "177",
            "CARDINAL"
          ],
          [
            "Teoria",
            "GPE"
          ],
          [
            "buraco",
            "NORP"
          ],
          [
            "Assisti",
            "PERSON"
          ],
          [
            "eu sonhei",
            "PERSON"
          ],
          [
            "mente quando eu",
            "PERSON"
          ],
          [
            "eu penso que",
            "PERSON"
          ],
          [
            "eu",
            "PERSON"
          ],
          [
            "ausência não",
            "PERSON"
          ],
          [
            "ausência \\n",
            "PERSON"
          ]
        ],
        "readability_score": 90.33153495440729,
        "semantic_density": 0,
        "word_count": 329,
        "unique_words": 190,
        "lexical_diversity": 0.5775075987841946
      },
      "preservation_score": 1.640337246364438e-05
    },
    {
      "id": 1,
      "text": "— 178 —é maior, mais intensa. Comecei a pensar que a energia é ve -\\nlocidade. Se energia é velocidade e velocidade têm gravidade, \\num buraco negro é mais rápido que a velocidade da luz. Logo, \\neu comecei a pensar em nos redemoinhos das galáxias, na ve -\\nlocidade em que giramos no entorno de cada buraco negro, \\ntudo sendo engolido para o seu centro, criando um círculo de \\nfótons no seu entorno, fazendo conseguir realizar um cálculo \\nmatemático através da, massa da velocidade da luz vezes a força \\ncentrípeta proporcional ao tamanho do buraco negro.\\nMarcelo Jubilado Catharino\\ncaos do passado sendo vivido no futuro editável.indd   178caos do passado sendo vivido no futuro editável.indd   178 28/03/2022   14:53:4128/03/2022   14:53:41",
      "position": 292495,
      "chapter": 8,
      "page": 178,
      "segment_type": "page",
      "themes": {},
      "difficulty": 25.17310924369748,
      "complexity_metrics": {
        "word_count": 119,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 17.0,
        "avg_word_length": 5.100840336134453,
        "unique_word_ratio": 0.6890756302521008,
        "avg_paragraph_length": 119.0,
        "punctuation_density": 0.15126050420168066,
        "line_break_count": 10,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "velocidade",
          "buraco",
          "negro",
          "sendo",
          "mais",
          "comecei",
          "pensar",
          "energia",
          "locidade",
          "entorno",
          "passado",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "maior",
          "intensa",
          "gravidade",
          "rápido",
          "logo"
        ],
        "entities": [
          [
            "178",
            "CARDINAL"
          ],
          [
            "mais intensa",
            "PERSON"
          ],
          [
            "buraco",
            "NORP"
          ],
          [
            "Logo",
            "PERSON"
          ],
          [
            "eu",
            "PERSON"
          ],
          [
            "buraco",
            "NORP"
          ],
          [
            "fazendo conseguir",
            "ORG"
          ],
          [
            "buraco negro",
            "ORG"
          ],
          [
            "Marcelo Jubilado Catharino",
            "PERSON"
          ],
          [
            "editável.indd",
            "CARDINAL"
          ]
        ],
        "readability_score": 89.96974789915967,
        "semantic_density": 0,
        "word_count": 119,
        "unique_words": 82,
        "lexical_diversity": 0.6890756302521008
      },
      "preservation_score": 1.6038853075563393e-06
    },
    {
      "id": 1,
      "text": "caos do passado sendo vivido no futuro editável.indd   179caos do passado sendo vivido no futuro editável.indd   179 28/03/2022   14:53:4128/03/2022   14:53:41",
      "position": 293350,
      "chapter": 8,
      "page": 179,
      "segment_type": "page",
      "themes": {},
      "difficulty": 20.64666666666667,
      "complexity_metrics": {
        "word_count": 20,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 6.666666666666667,
        "avg_word_length": 6.6,
        "unique_word_ratio": 0.65,
        "avg_paragraph_length": 20.0,
        "punctuation_density": 0.3,
        "line_break_count": 0,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "caos"
        ],
        "entities": [
          [
            "editável.indd",
            "CARDINAL"
          ],
          [
            "179caos",
            "CARDINAL"
          ],
          [
            "editável.indd",
            "CARDINAL"
          ],
          [
            "179",
            "CARDINAL"
          ],
          [
            "14:53:4128/03/2022",
            "CARDINAL"
          ]
        ],
        "readability_score": 94.68666666666667,
        "semantic_density": 0,
        "word_count": 20,
        "unique_words": 13,
        "lexical_diversity": 0.65
      },
      "preservation_score": 0.0
    },
    {
      "id": 1,
      "text": "Este livro foi composto em \\nSabon Next LT Pro\\npela Editora Autografia\\ne impresso em pólen 80.\\ncaos do passado sendo vivido no futuro editável.indd   180caos do passado sendo vivido no futuro editável.indd   180 28/03/2022   14:53:4128/03/2022   14:53:41",
      "position": 293625,
      "chapter": 9,
      "page": 180,
      "segment_type": "page",
      "themes": {},
      "difficulty": 21.561486486486487,
      "complexity_metrics": {
        "word_count": 37,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 9.25,
        "avg_word_length": 5.621621621621622,
        "unique_word_ratio": 0.7837837837837838,
        "avg_paragraph_length": 37.0,
        "punctuation_density": 0.1891891891891892,
        "line_break_count": 4,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "passado",
          "sendo",
          "vivido",
          "futuro",
          "editável",
          "indd",
          "este",
          "livro",
          "composto",
          "sabon",
          "next",
          "pela",
          "editora",
          "autografia",
          "impresso",
          "pólen",
          "caos"
        ],
        "entities": [
          [
            "Editora Autografia",
            "PERSON"
          ],
          [
            "80",
            "DATE"
          ],
          [
            "editável.indd",
            "CARDINAL"
          ],
          [
            "180caos",
            "CARDINAL"
          ],
          [
            "editável.indd",
            "CARDINAL"
          ],
          [
            "180",
            "CARDINAL"
          ],
          [
            "14:53:4128/03/2022",
            "CARDINAL"
          ]
        ],
        "readability_score": 93.68851351351351,
        "semantic_density": 0,
        "word_count": 37,
        "unique_words": 29,
        "lexical_diversity": 0.7837837837837838
      },
      "preservation_score": 2.0413085732535226e-07
    }
  ],
  "book_name": "miolo_caos do passado sendo vivido no futuro_28032022.pdf",
  "book_cover": "book_cover.png"
}"""
        
        if not analysis_data_str or analysis_data_str == "##BOOK_ANALYSIS_DATA##":
            st.error("🚨 Dados de análise não encontrados")
            st.info("""
            📋 **Solução de problemas:**
            1. Execute primeiro a análise do livro no módulo principal
            2. Aguarde o processamento completo dos dados
            3. Recarregue a página após a análise ser concluída
            """)
            
            if st.button("📊 Executar Análise do Livro", type="primary"):
                st.switch_page("main_analysis.py")
            return
        
        analysis_data_str = analysis_data_str.strip()
        
        if analysis_data_str.startswith('"""') and analysis_data_str.endswith('"""'):
            analysis_data_str = analysis_data_str[3:-3].strip()
        
        try:
            analysis_data = json.loads(analysis_data_str)
            st.success("✅ JSON carregado com sucesso!")
        except json.JSONDecodeError as e:
            st.error(f"🚨 Erro ao decodificar JSON: {str(e)}")
            
            st.text(f"Linha: {e.lineno}, Coluna: {e.colno}, Char: {e.pos}")
            
            start = max(0, e.pos - 100)
            end = min(len(analysis_data_str), e.pos + 100)
            error_context = analysis_data_str[start:end]
            st.code(f"...{error_context}...", language="json")
            
            try:
                cleaned_json = analysis_data_str
                cleaned_json = re.sub(r'(?<!\\)"', '\\"', cleaned_json)
                cleaned_json = cleaned_json.replace('\n', '\\n').replace('\r', '\\r')
                
                analysis_data = json.loads(f'"{cleaned_json}"')
                st.success("✅ JSON reparado manualmente!")
            except Exception as e2:
                st.error(f"❌ Não foi possível reparar o JSON: {str(e2)}")
                st.info("""
                📋 **Solução de problemas:**
                1. Verifique se os dados de análise estão no formato JSON válido
                2. Execute novamente a análise do livro
                3. Se o problema persistir, verifique o arquivo de origem
                """)
                return
        
        if not analysis_data or 'segments' not in analysis_data:
            st.error("🚨 Estrutura de dados inválida: campo 'segments' não encontrado")
            st.info("""
            📋 **Solução de problemas:**
            1. Verifique se o arquivo de análise foi gerado corretamente
            2. Certifique-se de que o processo de análise foi concluído com sucesso
            3. Execute novamente a análise do livro
            """)
            return
        
        reader = QuantumBookReader(analysis_data)
        reader.render()
        
    except Exception as e:
        st.error(f"🚨 Erro inesperado: {str(e)}")
        st.info("""
        📋 **Solução de problemas:**
        1. Recarregue a página e tente novamente
        2. Verifique se há problemas com seus dados de entrada
        3. Consulte o suporte técnico se o problema persistir
        """)

if __name__ == "__main__":
    main()