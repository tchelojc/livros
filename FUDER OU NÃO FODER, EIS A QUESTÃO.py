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
    "total_segments": 151,
    "total_chapters": 5,
    "total_pages": 93,
    "avg_difficulty": 26.76858885610817,
    "max_difficulty": 40.31739130434782,
    "min_difficulty": 16.7,
    "theme_distribution": {
      "arte": 100.0
    },
    "total_words": 6971,
    "avg_words_per_segment": 46.16556291390729,
    "formatting_preservation": 74.17218543046357,
    "preservation_score": 0.00011098320072444544,
    "book_name": "fuder ou nao fuder eis a questão.docx",
    "analysis_timestamp": "2025-09-15T19:49:36",
    "structure_preserved": false
  },
  "theme_analysis": {
    "arte": [
      {
        "segment": 5,
        "score": 100.0,
        "position": 1232,
        "chapter": 1
      },
      {
        "segment": 62,
        "score": 100.0,
        "position": 15496,
        "chapter": 4
      },
      {
        "segment": 73,
        "score": 100.0,
        "position": 17904,
        "chapter": 4
      },
      {
        "segment": 83,
        "score": 100.0,
        "position": 18979,
        "chapter": 4
      },
      {
        "segment": 107,
        "score": 100.0,
        "position": 23398,
        "chapter": 4
      },
      {
        "segment": 120,
        "score": 100.0,
        "position": 28170,
        "chapter": 4
      },
      {
        "segment": 124,
        "score": 100.0,
        "position": 29572,
        "chapter": 4
      }
    ]
  },
  "difficulty_map": [
    {
      "segment": 1,
      "difficulty": 19.65714285714286,
      "position": 0,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 7,
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "segment": 2,
      "difficulty": 19.1,
      "position": 35,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 1,
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "segment": 3,
      "difficulty": 36.49281437125748,
      "position": 49,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 167,
      "preservation_score": 0.0
    },
    {
      "segment": 4,
      "difficulty": 32.40625,
      "position": 1049,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 32,
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "segment": 5,
      "difficulty": 36.37288135593221,
      "position": 1232,
      "chapter": 1,
      "main_theme": "arte",
      "word_count": 59,
      "preservation_score": 2.7249533836408556e-05
    },
    {
      "segment": 6,
      "difficulty": 36.8,
      "position": 1563,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 48,
      "preservation_score": 4.087430075461283e-05
    },
    {
      "segment": 7,
      "difficulty": 18.6,
      "position": 1901,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 3,
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "segment": 8,
      "difficulty": 23.5,
      "position": 1926,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 14,
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "segment": 9,
      "difficulty": 37.29041095890411,
      "position": 2011,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 73,
      "preservation_score": 4.087430075461283e-05
    },
    {
      "segment": 10,
      "difficulty": 25.24142857142857,
      "position": 2400,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 35,
      "preservation_score": 4.768668421371498e-05
    },
    {
      "segment": 11,
      "difficulty": 30.751724137931035,
      "position": 2610,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 29,
      "preservation_score": 2.0437150377306416e-05
    },
    {
      "segment": 12,
      "difficulty": 36.343859649122805,
      "position": 2762,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 171,
      "preservation_score": 0.0001226229022638385
    },
    {
      "segment": 13,
      "difficulty": 17.65,
      "position": 3700,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 2,
      "preservation_score": 6.812383459102139e-06
    },
    {
      "segment": 14,
      "difficulty": 22.225,
      "position": 3714,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 12,
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "segment": 15,
      "difficulty": 21.29,
      "position": 3776,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 10,
      "preservation_score": 6.812383459102139e-06
    },
    {
      "segment": 16,
      "difficulty": 23.7,
      "position": 3830,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 15,
      "preservation_score": 6.812383459102139e-06
    },
    {
      "segment": 17,
      "difficulty": 22.838461538461537,
      "position": 3907,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 13,
      "preservation_score": 6.812383459102139e-06
    },
    {
      "segment": 18,
      "difficulty": 23.392857142857142,
      "position": 3979,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 14,
      "preservation_score": 6.812383459102139e-06
    },
    {
      "segment": 19,
      "difficulty": 36.480327868852456,
      "position": 4060,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 61,
      "preservation_score": 3.406191729551069e-05
    },
    {
      "segment": 20,
      "difficulty": 31.4,
      "position": 4424,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 30,
      "preservation_score": 2.0437150377306416e-05
    },
    {
      "segment": 21,
      "difficulty": 38.308571428571426,
      "position": 4595,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 35,
      "preservation_score": 5.449906767281711e-05
    },
    {
      "segment": 22,
      "difficulty": 19.7,
      "position": 4842,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 6,
      "preservation_score": 6.812383459102139e-06
    },
    {
      "segment": 23,
      "difficulty": 19.6,
      "position": 4883,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 6,
      "preservation_score": 6.812383459102139e-06
    },
    {
      "segment": 24,
      "difficulty": 20.725,
      "position": 4922,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 4,
      "preservation_score": 6.812383459102139e-06
    },
    {
      "segment": 25,
      "difficulty": 18.5,
      "position": 4950,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 4,
      "preservation_score": 6.812383459102139e-06
    },
    {
      "segment": 26,
      "difficulty": 19.87142857142857,
      "position": 4975,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 7,
      "preservation_score": 6.812383459102139e-06
    },
    {
      "segment": 27,
      "difficulty": 19.3,
      "position": 5015,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 5,
      "preservation_score": 6.812383459102139e-06
    },
    {
      "segment": 28,
      "difficulty": 18.94,
      "position": 5051,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 5,
      "preservation_score": 6.812383459102139e-06
    },
    {
      "segment": 29,
      "difficulty": 19.36,
      "position": 5081,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 5,
      "preservation_score": 6.812383459102139e-06
    },
    {
      "segment": 30,
      "difficulty": 19.52857142857143,
      "position": 5118,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 7,
      "preservation_score": 6.812383459102139e-06
    },
    {
      "segment": 31,
      "difficulty": 24.7,
      "position": 5150,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 17,
      "preservation_score": 6.812383459102139e-06
    },
    {
      "segment": 32,
      "difficulty": 20.0,
      "position": 5237,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 7,
      "preservation_score": 6.812383459102139e-06
    },
    {
      "segment": 33,
      "difficulty": 19.785714285714285,
      "position": 5280,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 7,
      "preservation_score": 6.812383459102139e-06
    },
    {
      "segment": 34,
      "difficulty": 17.8,
      "position": 5318,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 2,
      "preservation_score": 6.812383459102139e-06
    },
    {
      "segment": 35,
      "difficulty": 30.99590476190476,
      "position": 5333,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 175,
      "preservation_score": 0.0
    },
    {
      "segment": 36,
      "difficulty": 38.529411764705884,
      "position": 6333,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 51,
      "preservation_score": 8.174860150922567e-05
    },
    {
      "segment": 37,
      "difficulty": 18.8,
      "position": 6645,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 3,
      "preservation_score": 2.0437150377306416e-05
    },
    {
      "segment": 38,
      "difficulty": 36.379464285714285,
      "position": 6672,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 112,
      "preservation_score": 6.131145113191925e-05
    },
    {
      "segment": 39,
      "difficulty": 36.46115107913669,
      "position": 7300,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 139,
      "preservation_score": 0.00010899813534563423
    },
    {
      "segment": 40,
      "difficulty": 36.43467741935484,
      "position": 8119,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 124,
      "preservation_score": 9.537336842742996e-05
    },
    {
      "segment": 41,
      "difficulty": 36.56923076923077,
      "position": 8837,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 65,
      "preservation_score": 5.449906767281711e-05
    },
    {
      "segment": 42,
      "difficulty": 19.45,
      "position": 9243,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 6,
      "preservation_score": 6.812383459102139e-06
    },
    {
      "segment": 43,
      "difficulty": 23.82,
      "position": 9279,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 15,
      "preservation_score": 2.7249533836408556e-05
    },
    {
      "segment": 44,
      "difficulty": 25.3,
      "position": 9363,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 18,
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "segment": 45,
      "difficulty": 19.9,
      "position": 9461,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 6,
      "preservation_score": 3.406191729551069e-05
    },
    {
      "segment": 46,
      "difficulty": 18.35,
      "position": 9507,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 4,
      "preservation_score": 2.0437150377306416e-05
    },
    {
      "segment": 47,
      "difficulty": 18.175,
      "position": 9530,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 8,
      "preservation_score": 6.812383459102139e-06
    },
    {
      "segment": 48,
      "difficulty": 31.671311475409837,
      "position": 9577,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 61,
      "preservation_score": 5.449906767281711e-05
    },
    {
      "segment": 49,
      "difficulty": 32.58779069767442,
      "position": 9929,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 129,
      "preservation_score": 0.00014987243610024706
    },
    {
      "segment": 50,
      "difficulty": 28.2875,
      "position": 10688,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 24,
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "segment": 51,
      "difficulty": 40.31739130434782,
      "position": 10817,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 184,
      "preservation_score": 0.00014306005264114492
    },
    {
      "segment": 52,
      "difficulty": 36.46280991735537,
      "position": 11810,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 121,
      "preservation_score": 0.00011581051880473634
    },
    {
      "segment": 53,
      "difficulty": 36.54,
      "position": 12523,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 165,
      "preservation_score": 0.00013624766918204277
    },
    {
      "segment": 54,
      "difficulty": 36.435838150289015,
      "position": 13536,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 173,
      "preservation_score": 0.0
    },
    {
      "segment": 55,
      "difficulty": 29.34285714285714,
      "position": 14536,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 21,
      "preservation_score": 4.768668421371498e-05
    },
    {
      "segment": 56,
      "difficulty": 18.95,
      "position": 14688,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 4,
      "preservation_score": 0.0
    },
    {
      "segment": 57,
      "difficulty": 30.454901960784312,
      "position": 14719,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 85,
      "preservation_score": 0.00010899813534563423
    },
    {
      "segment": 58,
      "difficulty": 19.85,
      "position": 15171,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 6,
      "preservation_score": 6.812383459102139e-06
    },
    {
      "segment": 59,
      "difficulty": 20.5,
      "position": 15216,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 18,
      "preservation_score": 3.406191729551069e-05
    },
    {
      "segment": 60,
      "difficulty": 19.168181818181818,
      "position": 15295,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 11,
      "preservation_score": 4.087430075461283e-05
    },
    {
      "segment": 61,
      "difficulty": 22.4,
      "position": 15359,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 24,
      "preservation_score": 3.406191729551069e-05
    },
    {
      "segment": 62,
      "difficulty": 29.87777777777778,
      "position": 15496,
      "chapter": 4,
      "main_theme": "arte",
      "word_count": 27,
      "preservation_score": 7.493621805012353e-05
    },
    {
      "segment": 63,
      "difficulty": 36.391999999999996,
      "position": 15648,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 125,
      "preservation_score": 6.812383459102139e-05
    },
    {
      "segment": 64,
      "difficulty": 36.36808510638298,
      "position": 16354,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 141,
      "preservation_score": 8.856098496832781e-05
    },
    {
      "segment": 65,
      "difficulty": 20.7625,
      "position": 17140,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 8,
      "preservation_score": 6.812383459102139e-06
    },
    {
      "segment": 66,
      "difficulty": 18.52,
      "position": 17196,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 5,
      "preservation_score": 6.812383459102139e-06
    },
    {
      "segment": 67,
      "difficulty": 22.575,
      "position": 17219,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 12,
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "segment": 68,
      "difficulty": 26.275,
      "position": 17295,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 20,
      "preservation_score": 6.812383459102139e-06
    },
    {
      "segment": 69,
      "difficulty": 19.485714285714288,
      "position": 17401,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 7,
      "preservation_score": 6.812383459102139e-06
    },
    {
      "segment": 70,
      "difficulty": 19.87142857142857,
      "position": 17432,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 7,
      "preservation_score": 6.812383459102139e-06
    },
    {
      "segment": 71,
      "difficulty": 36.29692307692308,
      "position": 17472,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 65,
      "preservation_score": 7.493621805012353e-05
    },
    {
      "segment": 72,
      "difficulty": 19.978571428571428,
      "position": 17820,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 14,
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "segment": 73,
      "difficulty": 36.434782608695656,
      "position": 17904,
      "chapter": 4,
      "main_theme": "arte",
      "word_count": 46,
      "preservation_score": 4.768668421371498e-05
    },
    {
      "segment": 74,
      "difficulty": 18.2,
      "position": 18171,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 1,
      "preservation_score": 6.812383459102139e-06
    },
    {
      "segment": 75,
      "difficulty": 22.35,
      "position": 18183,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 12,
      "preservation_score": 2.0437150377306416e-05
    },
    {
      "segment": 76,
      "difficulty": 20.4625,
      "position": 18250,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 8,
      "preservation_score": 3.406191729551069e-05
    },
    {
      "segment": 77,
      "difficulty": 20.4625,
      "position": 18298,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 16,
      "preservation_score": 4.768668421371498e-05
    },
    {
      "segment": 78,
      "difficulty": 27.869565217391305,
      "position": 18393,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 46,
      "preservation_score": 3.406191729551069e-05
    },
    {
      "segment": 79,
      "difficulty": 36.17169811320755,
      "position": 18651,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 53,
      "preservation_score": 6.812383459102139e-05
    },
    {
      "segment": 80,
      "difficulty": 18.0,
      "position": 18912,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 3,
      "preservation_score": 6.812383459102139e-06
    },
    {
      "segment": 81,
      "difficulty": 18.275,
      "position": 18931,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 4,
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "segment": 82,
      "difficulty": 18.575,
      "position": 18953,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 4,
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "segment": 83,
      "difficulty": 36.35911602209944,
      "position": 18979,
      "chapter": 4,
      "main_theme": "arte",
      "word_count": 181,
      "preservation_score": 0.0
    },
    {
      "segment": 84,
      "difficulty": 36.468032786885246,
      "position": 19979,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 122,
      "preservation_score": 0.00011581051880473634
    },
    {
      "segment": 85,
      "difficulty": 22.961111111111112,
      "position": 20699,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 27,
      "preservation_score": 2.7249533836408556e-05
    },
    {
      "segment": 86,
      "difficulty": 24.060000000000002,
      "position": 20836,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 15,
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "segment": 87,
      "difficulty": 22.081818181818182,
      "position": 20930,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 11,
      "preservation_score": 4.768668421371498e-05
    },
    {
      "segment": 88,
      "difficulty": 21.23,
      "position": 21000,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 10,
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "segment": 89,
      "difficulty": 19.52857142857143,
      "position": 21052,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 7,
      "preservation_score": 6.812383459102139e-06
    },
    {
      "segment": 90,
      "difficulty": 23.564285714285717,
      "position": 21084,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 14,
      "preservation_score": 2.7249533836408556e-05
    },
    {
      "segment": 91,
      "difficulty": 17.8,
      "position": 21173,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 3,
      "preservation_score": 6.812383459102139e-06
    },
    {
      "segment": 92,
      "difficulty": 17.6,
      "position": 21190,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 3,
      "preservation_score": 2.0437150377306416e-05
    },
    {
      "segment": 93,
      "difficulty": 22.075,
      "position": 21205,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 12,
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "segment": 94,
      "difficulty": 24.911764705882355,
      "position": 21261,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 17,
      "preservation_score": 2.0437150377306416e-05
    },
    {
      "segment": 95,
      "difficulty": 28.759999999999998,
      "position": 21359,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 50,
      "preservation_score": 4.768668421371498e-05
    },
    {
      "segment": 96,
      "difficulty": 22.55,
      "position": 21620,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 12,
      "preservation_score": 3.406191729551069e-05
    },
    {
      "segment": 97,
      "difficulty": 19.614285714285714,
      "position": 21695,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 7,
      "preservation_score": 2.0437150377306416e-05
    },
    {
      "segment": 98,
      "difficulty": 29.855555555555554,
      "position": 21729,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 27,
      "preservation_score": 2.0437150377306416e-05
    },
    {
      "segment": 99,
      "difficulty": 21.563636363636363,
      "position": 21880,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 11,
      "preservation_score": 2.0437150377306416e-05
    },
    {
      "segment": 100,
      "difficulty": 17.9,
      "position": 21931,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 6,
      "preservation_score": 2.0437150377306416e-05
    },
    {
      "segment": 101,
      "difficulty": 20.866666666666667,
      "position": 21966,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 9,
      "preservation_score": 3.406191729551069e-05
    },
    {
      "segment": 102,
      "difficulty": 27.90869565217391,
      "position": 22017,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 23,
      "preservation_score": 2.0437150377306416e-05
    },
    {
      "segment": 103,
      "difficulty": 23.261320754716984,
      "position": 22149,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 53,
      "preservation_score": 9.537336842742996e-05
    },
    {
      "segment": 104,
      "difficulty": 19.18,
      "position": 22471,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 5,
      "preservation_score": 2.0437150377306416e-05
    },
    {
      "segment": 105,
      "difficulty": 19.785714285714285,
      "position": 22505,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 7,
      "preservation_score": 6.812383459102139e-06
    },
    {
      "segment": 106,
      "difficulty": 36.475,
      "position": 22543,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 144,
      "preservation_score": 0.00010218575188653208
    },
    {
      "segment": 107,
      "difficulty": 36.40898876404495,
      "position": 23398,
      "chapter": 4,
      "main_theme": "arte",
      "word_count": 89,
      "preservation_score": 0.00010218575188653208
    },
    {
      "segment": 108,
      "difficulty": 19.025,
      "position": 23906,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 4,
      "preservation_score": 6.812383459102139e-06
    },
    {
      "segment": 109,
      "difficulty": 18.2,
      "position": 23939,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 4,
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "segment": 110,
      "difficulty": 18.6,
      "position": 23961,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 3,
      "preservation_score": 6.812383459102139e-06
    },
    {
      "segment": 111,
      "difficulty": 18.759999999999998,
      "position": 23986,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 5,
      "preservation_score": 2.0437150377306416e-05
    },
    {
      "segment": 112,
      "difficulty": 36.412727272727274,
      "position": 24013,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 55,
      "preservation_score": 2.7249533836408556e-05
    },
    {
      "segment": 113,
      "difficulty": 36.48612716763006,
      "position": 24328,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 173,
      "preservation_score": 0.00014306005264114492
    },
    {
      "segment": 114,
      "difficulty": 19.403846153846153,
      "position": 25359,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 13,
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "segment": 115,
      "difficulty": 36.413333333333334,
      "position": 25423,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 135,
      "preservation_score": 0.000197559120313962
    },
    {
      "segment": 116,
      "difficulty": 18.94,
      "position": 26197,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 5,
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "segment": 117,
      "difficulty": 19.21,
      "position": 26227,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 10,
      "preservation_score": 3.406191729551069e-05
    },
    {
      "segment": 118,
      "difficulty": 36.416,
      "position": 26295,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 175,
      "preservation_score": 0.0
    },
    {
      "segment": 119,
      "difficulty": 38.27951807228916,
      "position": 27295,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 166,
      "preservation_score": 7.493621805012353e-05
    },
    {
      "segment": 120,
      "difficulty": 36.357458563535914,
      "position": 28170,
      "chapter": 4,
      "main_theme": "arte",
      "word_count": 181,
      "preservation_score": 0.0
    },
    {
      "segment": 121,
      "difficulty": 28.40625,
      "position": 29170,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 48,
      "preservation_score": 5.449906767281711e-05
    },
    {
      "segment": 122,
      "difficulty": 27.35,
      "position": 29444,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 22,
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "segment": 123,
      "difficulty": 16.7,
      "position": 29566,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 1,
      "preservation_score": 6.812383459102139e-06
    },
    {
      "segment": 124,
      "difficulty": 36.34257425742574,
      "position": 29572,
      "chapter": 4,
      "main_theme": "arte",
      "word_count": 101,
      "preservation_score": 0.00010218575188653208
    },
    {
      "segment": 125,
      "difficulty": 31.35,
      "position": 30127,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 30,
      "preservation_score": 2.7249533836408556e-05
    },
    {
      "segment": 126,
      "difficulty": 21.29,
      "position": 30293,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 10,
      "preservation_score": 3.406191729551069e-05
    },
    {
      "segment": 127,
      "difficulty": 28.82,
      "position": 30347,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 25,
      "preservation_score": 2.7249533836408556e-05
    },
    {
      "segment": 128,
      "difficulty": 19.0,
      "position": 30483,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 6,
      "preservation_score": 2.0437150377306416e-05
    },
    {
      "segment": 129,
      "difficulty": 19.240000000000002,
      "position": 30510,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 5,
      "preservation_score": 3.406191729551069e-05
    },
    {
      "segment": 130,
      "difficulty": 22.407692307692308,
      "position": 30545,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 13,
      "preservation_score": 2.7249533836408556e-05
    },
    {
      "segment": 131,
      "difficulty": 36.41730769230769,
      "position": 30621,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 156,
      "preservation_score": 0.00014306005264114492
    },
    {
      "segment": 132,
      "difficulty": 29.6,
      "position": 31515,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 27,
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "segment": 133,
      "difficulty": 36.34814814814815,
      "position": 31644,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 81,
      "preservation_score": 5.449906767281711e-05
    },
    {
      "segment": 134,
      "difficulty": 36.38837209302326,
      "position": 32090,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 43,
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "segment": 135,
      "difficulty": 33.70857142857143,
      "position": 32333,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 35,
      "preservation_score": 5.449906767281711e-05
    },
    {
      "segment": 136,
      "difficulty": 28.2375,
      "position": 32510,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 24,
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "segment": 137,
      "difficulty": 36.34098360655737,
      "position": 32635,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 183,
      "preservation_score": 0.0
    },
    {
      "segment": 138,
      "difficulty": 30.307142857142857,
      "position": 33635,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 28,
      "preservation_score": 4.087430075461283e-05
    },
    {
      "segment": 139,
      "difficulty": 20.1625,
      "position": 33786,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 8,
      "preservation_score": 6.812383459102139e-06
    },
    {
      "segment": 140,
      "difficulty": 21.439999999999998,
      "position": 33830,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 10,
      "preservation_score": 6.812383459102139e-06
    },
    {
      "segment": 141,
      "difficulty": 35.80769230769231,
      "position": 33889,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 39,
      "preservation_score": 2.7249533836408556e-05
    },
    {
      "segment": 142,
      "difficulty": 36.369325153374234,
      "position": 34099,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 163,
      "preservation_score": 8.174860150922567e-05
    },
    {
      "segment": 143,
      "difficulty": 36.4,
      "position": 35007,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 63,
      "preservation_score": 4.087430075461283e-05
    },
    {
      "segment": 144,
      "difficulty": 36.38367346938776,
      "position": 35365,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 49,
      "preservation_score": 4.087430075461283e-05
    },
    {
      "segment": 145,
      "difficulty": 31.970967741935485,
      "position": 35641,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 31,
      "preservation_score": 4.768668421371498e-05
    },
    {
      "segment": 146,
      "difficulty": 36.48478260869565,
      "position": 35827,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 138,
      "preservation_score": 0.00014987243610024706
    },
    {
      "segment": 147,
      "difficulty": 36.4027027027027,
      "position": 36649,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 111,
      "preservation_score": 5.449906767281711e-05
    },
    {
      "segment": 148,
      "difficulty": 36.27951807228916,
      "position": 37281,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 83,
      "preservation_score": 2.7249533836408556e-05
    },
    {
      "segment": 149,
      "difficulty": 24.02,
      "position": 37719,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 15,
      "preservation_score": 3.406191729551069e-05
    },
    {
      "segment": 150,
      "difficulty": 36.308510638297875,
      "position": 37812,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 47,
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "segment": 151,
      "difficulty": 37.50921501706485,
      "position": 38066,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 293,
      "preservation_score": 0.011444804211291593
    }
  ],
  "segments": [
    {
      "id": 1,
      "text": "Fuder ou não fuder, és a questão?\\n\\n",
      "position": 0,
      "chapter": 1,
      "page": 1,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 19.65714285714286,
      "complexity_metrics": {
        "word_count": 7,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 7.0,
        "avg_word_length": 3.857142857142857,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 7.0,
        "punctuation_density": 0.2857142857142857,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "fuder",
          "questão"
        ],
        "entities": [],
        "readability_score": 95.34285714285714,
        "semantic_density": 0,
        "word_count": 7,
        "unique_words": 7,
        "lexical_diversity": 1.0
      },
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "id": 2,
      "text": "“Penetração”\\n\\n",
      "position": 35,
      "chapter": 1,
      "page": 2,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 19.1,
      "complexity_metrics": {
        "word_count": 1,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 1.0,
        "avg_word_length": 12.0,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 1.0,
        "punctuation_density": 0.0,
        "line_break_count": 2,
        "formatting_preservation_score": 50.0
      },
      "analysis": {
        "keywords": [
          "penetração"
        ],
        "entities": [
          [
            "Penetração",
            "ORG"
          ]
        ],
        "readability_score": 95.9,
        "semantic_density": 0,
        "word_count": 1,
        "unique_words": 1,
        "lexical_diversity": 1.0
      },
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "id": 3,
      "text": "   Todos nós nascemos através de um amor, sexo, fuder, transar e todas as formas de pensar em colocar o coelho na toca, da ré no kibe, colar velcro e gozar, gozar sem precedentes, gozar e ter prazer de morder, socar, xingar, amar, acariciar, beijar, chupar até ficar igual a uma vaca que o chupa cabra chupou, chupar tanto de ficar com a língua dormente durante uma semana sem conseguir falar o quanto foi gostosa aquela buceta, vulva, flor de lótus, “grelhuda”, olho que nada ver, o terceiro olho, aquela rola veiúda, santo Graal, ciclope, fimose e como quisermos imaginar o que ninguém nos ensina, pois somos criados com tantas restrições quando o assunto é sexo, não podendo falar a própria palavra na frente das mulheres, pois é desrespeito... mulheres longe dos homens falam abertamente sobre sexo... homossexuais se beijando é estranho... são tantos julgamentos que os próprios julgamentos são motivacionais para aqueles que gostam de se mostrar, não estando errado em fazer e sim como fazer, p",
      "position": 49,
      "chapter": 1,
      "page": 3,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.49281437125748,
      "complexity_metrics": {
        "word_count": 167,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 41.75,
        "avg_word_length": 4.976047904191617,
        "unique_word_ratio": 0.7664670658682635,
        "avg_paragraph_length": 167.0,
        "punctuation_density": 0.2215568862275449,
        "line_break_count": 0,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "sexo",
          "gozar",
          "chupar",
          "ficar",
          "falar",
          "aquela",
          "olho",
          "como",
          "pois",
          "mulheres",
          "julgamentos",
          "fazer",
          "todos",
          "nascemos",
          "através",
          "amor",
          "fuder",
          "transar",
          "todas",
          "formas"
        ],
        "entities": [
          [
            "nascemos através de um amor",
            "PERSON"
          ],
          [
            "formas de pensar",
            "PERSON"
          ],
          [
            "amar",
            "PERSON"
          ],
          [
            "beijar",
            "ORG"
          ],
          [
            "chupar até ficar",
            "ORG"
          ],
          [
            "chupar tanto de ficar",
            "ORG"
          ],
          [
            "semana sem",
            "PERSON"
          ],
          [
            "gostosa aquela buceta",
            "PERSON"
          ],
          [
            "vulva",
            "GPE"
          ],
          [
            "olho",
            "GPE"
          ]
        ],
        "readability_score": 77.63218562874252,
        "semantic_density": 0,
        "word_count": 167,
        "unique_words": 128,
        "lexical_diversity": 0.7664670658682635
      },
      "preservation_score": 0.0
    },
    {
      "id": 4,
      "text": "ois não são todos que sabem e vão entender o manifesto desnecessário diante de uma necessidade de sermos democrático, não adianta o exagero pela causa e sim mostrar o amor da causa.\\n\\n",
      "position": 1049,
      "chapter": 1,
      "page": 4,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 32.40625,
      "complexity_metrics": {
        "word_count": 32,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 32.0,
        "avg_word_length": 4.6875,
        "unique_word_ratio": 0.84375,
        "avg_paragraph_length": 32.0,
        "punctuation_density": 0.0625,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "causa",
          "todos",
          "sabem",
          "entender",
          "manifesto",
          "desnecessário",
          "diante",
          "necessidade",
          "sermos",
          "democrático",
          "adianta",
          "exagero",
          "pela",
          "mostrar",
          "amor"
        ],
        "entities": [
          [
            "todos",
            "NORP"
          ],
          [
            "exagero pela",
            "PERSON"
          ],
          [
            "amor da causa",
            "PERSON"
          ]
        ],
        "readability_score": 82.59375,
        "semantic_density": 0,
        "word_count": 32,
        "unique_words": 27,
        "lexical_diversity": 0.84375
      },
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "id": 5,
      "text": "A ideia de escrever esse livro sobre sexo sem ter estudado e estudado muito na prática e em debates agressivos com puxões de cabelo, xingando de puta e como resposta minha mãe era xingada do nada, e do nada vem uma mão mais agressiva nas partes mais sensíveis, por muitas vezes nos deixando pensativos sobre onde isso vai parar? \\n\\n",
      "position": 1232,
      "chapter": 1,
      "page": 5,
      "segment_type": "preserved_segment",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 36.37288135593221,
      "complexity_metrics": {
        "word_count": 59,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 59.0,
        "avg_word_length": 4.576271186440678,
        "unique_word_ratio": 0.847457627118644,
        "avg_paragraph_length": 59.0,
        "punctuation_density": 0.06779661016949153,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "estudado",
          "nada",
          "mais",
          "ideia",
          "escrever",
          "esse",
          "livro",
          "sexo",
          "muito",
          "prática",
          "debates",
          "agressivos",
          "puxões",
          "cabelo",
          "xingando",
          "puta",
          "como",
          "resposta",
          "minha",
          "xingada"
        ],
        "entities": [
          [
            "estudado",
            "GPE"
          ],
          [
            "muito na",
            "PERSON"
          ],
          [
            "puxões de cabelo",
            "ORG"
          ],
          [
            "xingando de puta",
            "ORG"
          ],
          [
            "xingada",
            "GPE"
          ],
          [
            "nada",
            "GPE"
          ],
          [
            "nada vem",
            "ORG"
          ],
          [
            "mais sensíveis",
            "PERSON"
          ]
        ],
        "readability_score": 69.12711864406779,
        "semantic_density": 0,
        "word_count": 59,
        "unique_words": 50,
        "lexical_diversity": 0.847457627118644
      },
      "preservation_score": 2.7249533836408556e-05
    },
    {
      "id": 6,
      "text": "Através dessa reflexão sexual e com muitos amigos me apoiando e contando histórias para apimentar, esquentar, aquecer, abraçar, namorar e proteger àqueles que são os nossos momentos inesquecíveis e por muitas vezes acaba em uma punheta, siririca ou curirica por serem pessoas inesquecíveis pelos prazeres inesquecíveis e inimagináveis. \\n\\n",
      "position": 1563,
      "chapter": 1,
      "page": 6,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.8,
      "complexity_metrics": {
        "word_count": 48,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 48.0,
        "avg_word_length": 6.0,
        "unique_word_ratio": 0.8541666666666666,
        "avg_paragraph_length": 48.0,
        "punctuation_density": 0.125,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "inesquecíveis",
          "através",
          "dessa",
          "reflexão",
          "sexual",
          "muitos",
          "amigos",
          "apoiando",
          "contando",
          "histórias",
          "apimentar",
          "esquentar",
          "aquecer",
          "abraçar",
          "namorar",
          "proteger",
          "àqueles",
          "nossos",
          "momentos",
          "muitas"
        ],
        "entities": [
          [
            "para apimentar",
            "PERSON"
          ],
          [
            "abraçar",
            "ORG"
          ],
          [
            "curirica",
            "GPE"
          ],
          [
            "serem pessoas",
            "GPE"
          ]
        ],
        "readability_score": 74.2,
        "semantic_density": 0,
        "word_count": 48,
        "unique_words": 41,
        "lexical_diversity": 0.8541666666666666
      },
      "preservation_score": 4.087430075461283e-05
    },
    {
      "id": 7,
      "text": "Capítulo 1 “introdução”\\n\\n",
      "position": 1901,
      "chapter": 2,
      "page": 1,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 18.6,
      "complexity_metrics": {
        "word_count": 3,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 3.0,
        "avg_word_length": 7.0,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 3.0,
        "punctuation_density": 0.0,
        "line_break_count": 2,
        "formatting_preservation_score": 50.0
      },
      "analysis": {
        "keywords": [
          "capítulo",
          "introdução"
        ],
        "entities": [],
        "readability_score": 96.4,
        "semantic_density": 0,
        "word_count": 3,
        "unique_words": 3,
        "lexical_diversity": 1.0
      },
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "id": 8,
      "text": "Quantos desejos sexuais deixamos de fazer, por imaginar que é errado fazer no sexo?\\n\\n",
      "position": 1926,
      "chapter": 2,
      "page": 2,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 23.5,
      "complexity_metrics": {
        "word_count": 14,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 14.0,
        "avg_word_length": 5.0,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 14.0,
        "punctuation_density": 0.14285714285714285,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "fazer",
          "quantos",
          "desejos",
          "sexuais",
          "deixamos",
          "imaginar",
          "errado",
          "sexo"
        ],
        "entities": [
          [
            "desejos",
            "PERSON"
          ],
          [
            "deixamos de fazer",
            "ORG"
          ]
        ],
        "readability_score": 91.5,
        "semantic_density": 0,
        "word_count": 14,
        "unique_words": 14,
        "lexical_diversity": 1.0
      },
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "id": 9,
      "text": "Como a ideia desse livro é ser sério, cômico e penetrante irei ser bem sincero com as minhas opiniões e a minha visão, sempre deixando bem claro que os meus sentimentos sobre a minha forma de ver e sentir é relativo ao meu gosto, as minhas experiências, as minhas expectativas, o ser hétero é o fator determinante para eu ter um valor pelo meu cu de ser o local mais intocável do mundo. \\n\\n",
      "position": 2011,
      "chapter": 2,
      "page": 3,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 37.29041095890411,
      "complexity_metrics": {
        "word_count": 73,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 73.0,
        "avg_word_length": 4.301369863013699,
        "unique_word_ratio": 0.7397260273972602,
        "avg_paragraph_length": 73.0,
        "punctuation_density": 0.0821917808219178,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "minhas",
          "minha",
          "como",
          "ideia",
          "desse",
          "livro",
          "sério",
          "cômico",
          "penetrante",
          "irei",
          "sincero",
          "opiniões",
          "visão",
          "sempre",
          "deixando",
          "claro",
          "meus",
          "sentimentos",
          "forma",
          "sentir"
        ],
        "entities": [
          [
            "para eu",
            "PERSON"
          ],
          [
            "pelo meu cu de ser",
            "PERSON"
          ]
        ],
        "readability_score": 62.20958904109589,
        "semantic_density": 0,
        "word_count": 73,
        "unique_words": 54,
        "lexical_diversity": 0.7397260273972602
      },
      "preservation_score": 4.087430075461283e-05
    },
    {
      "id": 10,
      "text": "Meu ânus é tão é tão intocável, que uma mulher, com suas peculiaridades sexuais, vamos dizer que tinha um certo talento em proporcionar uma boa foda... sabe aqueles boquetes que desce molhando e sobe secando?\\n\\n",
      "position": 2400,
      "chapter": 2,
      "page": 4,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 25.24142857142857,
      "complexity_metrics": {
        "word_count": 35,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 17.5,
        "avg_word_length": 4.9714285714285715,
        "unique_word_ratio": 0.8571428571428571,
        "avg_paragraph_length": 35.0,
        "punctuation_density": 0.2,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "ânus",
          "intocável",
          "mulher",
          "suas",
          "peculiaridades",
          "sexuais",
          "vamos",
          "dizer",
          "tinha",
          "certo",
          "talento",
          "proporcionar",
          "foda",
          "sabe",
          "aqueles",
          "boquetes",
          "desce",
          "molhando",
          "sobe",
          "secando"
        ],
        "entities": [
          [
            "tão",
            "PRODUCT"
          ],
          [
            "vamos dizer",
            "PERSON"
          ]
        ],
        "readability_score": 89.75857142857143,
        "semantic_density": 0,
        "word_count": 35,
        "unique_words": 30,
        "lexical_diversity": 0.8571428571428571
      },
      "preservation_score": 4.768668421371498e-05
    },
    {
      "id": 11,
      "text": "Era tão bom, tão bom, que a minha barriga era sugada junta quando ela subia e quando ela descia eu quase não aguentava de tanto cala frio na barriga. \\n\\n",
      "position": 2610,
      "chapter": 2,
      "page": 5,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 30.751724137931035,
      "complexity_metrics": {
        "word_count": 29,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 29.0,
        "avg_word_length": 4.172413793103448,
        "unique_word_ratio": 0.8620689655172413,
        "avg_paragraph_length": 29.0,
        "punctuation_density": 0.10344827586206896,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "barriga",
          "quando",
          "minha",
          "sugada",
          "junta",
          "subia",
          "descia",
          "quase",
          "aguentava",
          "tanto",
          "cala",
          "frio"
        ],
        "entities": [
          [
            "quando ela",
            "PERSON"
          ],
          [
            "subia",
            "GPE"
          ],
          [
            "quando ela",
            "PERSON"
          ],
          [
            "descia eu",
            "PERSON"
          ],
          [
            "aguentava de tanto",
            "ORG"
          ]
        ],
        "readability_score": 84.24827586206897,
        "semantic_density": 0,
        "word_count": 29,
        "unique_words": 25,
        "lexical_diversity": 0.8620689655172413
      },
      "preservation_score": 2.0437150377306416e-05
    },
    {
      "id": 12,
      "text": "Ela estava ali fazendo esse trabalho maravilhoso e eu na minha curtindo esse momento mental de sequelado, imaginando algo com nada e quando me dei conta, ela estava no curioso caso de Benjamin Button chupando tanto que a bochecha ficava uma bola em cada lado da boca, fiquei surpreso ao ver o talento e fraco, tão fraco que amoleceu o corpo... a pessoa com toda a sua experiência de vida pois era mais velha e já tinha vivido mais tipos de situações, percebeu o meu momento de fragilidade se sentiu confortável, resolveu avançar para a linha do desconforto para aqueles que são héteros, a linha que “divide os homens dos meninos “, onde o cu se contraí involuntariamente, onde percebemos o quanto o cu é o centro de tudo e do nada o centro virou o centro de atenção para ela também... não gostaria de falar sobre isso porém preciso falar para todos entenderem que é um livro sobre sexo e o meu ver essa situação a qual eu me encontrava.\\n\\n",
      "position": 2762,
      "chapter": 2,
      "page": 6,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.343859649122805,
      "complexity_metrics": {
        "word_count": 171,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 57.0,
        "avg_word_length": 4.47953216374269,
        "unique_word_ratio": 0.6842105263157895,
        "avg_paragraph_length": 171.0,
        "punctuation_density": 0.0935672514619883,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "centro",
          "estava",
          "esse",
          "momento",
          "nada",
          "fraco",
          "mais",
          "linha",
          "onde",
          "falar",
          "fazendo",
          "trabalho",
          "maravilhoso",
          "minha",
          "curtindo",
          "mental",
          "sequelado",
          "imaginando",
          "algo",
          "quando"
        ],
        "entities": [
          [
            "Ela estava",
            "PERSON"
          ],
          [
            "nada e quando",
            "ORG"
          ],
          [
            "dei conta",
            "PERSON"
          ],
          [
            "ela estava",
            "PERSON"
          ],
          [
            "de Benjamin Button",
            "PERSON"
          ],
          [
            "tanto",
            "GPE"
          ],
          [
            "lado da boca",
            "PERSON"
          ],
          [
            "fraco",
            "ORG"
          ],
          [
            "tão fraco que amoleceu",
            "ORG"
          ],
          [
            "resolveu avançar",
            "PERSON"
          ]
        ],
        "readability_score": 70.1561403508772,
        "semantic_density": 0,
        "word_count": 171,
        "unique_words": 117,
        "lexical_diversity": 0.6842105263157895
      },
      "preservation_score": 0.0001226229022638385
    },
    {
      "id": 13,
      "text": "sabendo que:\\n\\n",
      "position": 3700,
      "chapter": 2,
      "page": 7,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 17.65,
      "complexity_metrics": {
        "word_count": 2,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 2.0,
        "avg_word_length": 5.5,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 2.0,
        "punctuation_density": 0.5,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "sabendo"
        ],
        "entities": [],
        "readability_score": 97.35,
        "semantic_density": 0,
        "word_count": 2,
        "unique_words": 2,
        "lexical_diversity": 1.0
      },
      "preservation_score": 6.812383459102139e-06
    },
    {
      "id": 14,
      "text": "Minha mãe já tinha 3 filhos e queria uma menina, estou aqui.\\n\\n",
      "position": 3714,
      "chapter": 2,
      "page": 8,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 22.225,
      "complexity_metrics": {
        "word_count": 12,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 12.0,
        "avg_word_length": 4.083333333333333,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 12.0,
        "punctuation_density": 0.16666666666666666,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "minha",
          "tinha",
          "filhos",
          "queria",
          "menina",
          "estou",
          "aqui"
        ],
        "entities": [
          [
            "3",
            "CARDINAL"
          ]
        ],
        "readability_score": 92.775,
        "semantic_density": 0,
        "word_count": 12,
        "unique_words": 12,
        "lexical_diversity": 1.0
      },
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "id": 15,
      "text": "Fui criado por uma mãe solteira com 4 filhos homens.\\n\\n",
      "position": 3776,
      "chapter": 2,
      "page": 9,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 21.29,
      "complexity_metrics": {
        "word_count": 10,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 10.0,
        "avg_word_length": 4.3,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 10.0,
        "punctuation_density": 0.1,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "criado",
          "solteira",
          "filhos",
          "homens"
        ],
        "entities": [
          [
            "4",
            "CARDINAL"
          ]
        ],
        "readability_score": 93.71,
        "semantic_density": 0,
        "word_count": 10,
        "unique_words": 10,
        "lexical_diversity": 1.0
      },
      "preservation_score": 6.812383459102139e-06
    },
    {
      "id": 16,
      "text": " Perdi a virgindade com uma puta que o meu pai contratou com quase 17 anos.\\n\\n",
      "position": 3830,
      "chapter": 2,
      "page": 10,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 23.7,
      "complexity_metrics": {
        "word_count": 15,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 15.0,
        "avg_word_length": 4.0,
        "unique_word_ratio": 0.9333333333333333,
        "avg_paragraph_length": 15.0,
        "punctuation_density": 0.06666666666666667,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "perdi",
          "virgindade",
          "puta",
          "contratou",
          "quase",
          "anos"
        ],
        "entities": [
          [
            "Perdi",
            "ORG"
          ],
          [
            "17",
            "CARDINAL"
          ]
        ],
        "readability_score": 91.3,
        "semantic_density": 0,
        "word_count": 15,
        "unique_words": 14,
        "lexical_diversity": 0.9333333333333333
      },
      "preservation_score": 6.812383459102139e-06
    },
    {
      "id": 17,
      "text": "Esse mesmo pai contratou uma puta pois pensava que eu poderia ser gay.\\n\\n",
      "position": 3907,
      "chapter": 2,
      "page": 11,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 22.838461538461537,
      "complexity_metrics": {
        "word_count": 13,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 13.0,
        "avg_word_length": 4.461538461538462,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 13.0,
        "punctuation_density": 0.07692307692307693,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "esse",
          "mesmo",
          "contratou",
          "puta",
          "pois",
          "pensava",
          "poderia"
        ],
        "entities": [],
        "readability_score": 92.16153846153846,
        "semantic_density": 0,
        "word_count": 13,
        "unique_words": 13,
        "lexical_diversity": 1.0
      },
      "preservation_score": 6.812383459102139e-06
    },
    {
      "id": 18,
      "text": "Após perder a virgindade fui a procura por sexo de uma forma muito gananciosa. \\n\\n",
      "position": 3979,
      "chapter": 2,
      "page": 12,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 23.392857142857142,
      "complexity_metrics": {
        "word_count": 14,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 14.0,
        "avg_word_length": 4.642857142857143,
        "unique_word_ratio": 0.9285714285714286,
        "avg_paragraph_length": 14.0,
        "punctuation_density": 0.07142857142857142,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "após",
          "perder",
          "virgindade",
          "procura",
          "sexo",
          "forma",
          "muito",
          "gananciosa"
        ],
        "entities": [
          [
            "Após",
            "ORG"
          ],
          [
            "de uma forma muito gananciosa",
            "PERSON"
          ]
        ],
        "readability_score": 91.60714285714286,
        "semantic_density": 0,
        "word_count": 14,
        "unique_words": 13,
        "lexical_diversity": 0.9285714285714286
      },
      "preservation_score": 6.812383459102139e-06
    },
    {
      "id": 19,
      "text": "Quando ela deu uma linguada bem no meio do olho, onde a imagem de centro lembra um vulcão entrando em erupção, minha mão direita involuntariamente deu um tapa na moça e ela deu duas roladas laterais, levantando toda descabelada e desorientada perguntando o que foi isso e eu pedindo desculpas, falando para ela não fazer isso pois eu fiz isso involuntariamente. \\n\\n",
      "position": 4060,
      "chapter": 2,
      "page": 13,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.480327868852456,
      "complexity_metrics": {
        "word_count": 61,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 61.0,
        "avg_word_length": 4.934426229508197,
        "unique_word_ratio": 0.8360655737704918,
        "avg_paragraph_length": 61.0,
        "punctuation_density": 0.08196721311475409,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "isso",
          "involuntariamente",
          "quando",
          "linguada",
          "meio",
          "olho",
          "onde",
          "imagem",
          "centro",
          "lembra",
          "vulcão",
          "entrando",
          "erupção",
          "minha",
          "direita",
          "tapa",
          "moça",
          "duas",
          "roladas",
          "laterais"
        ],
        "entities": [
          [
            "Quando ela",
            "PERSON"
          ],
          [
            "laterais",
            "GPE"
          ],
          [
            "levantando",
            "GPE"
          ],
          [
            "toda descabelada e desorientada perguntando",
            "ORG"
          ],
          [
            "eu pedindo desculpas",
            "PERSON"
          ],
          [
            "falando",
            "NORP"
          ],
          [
            "para ela não fazer",
            "PERSON"
          ],
          [
            "eu",
            "PERSON"
          ]
        ],
        "readability_score": 68.01967213114754,
        "semantic_density": 0,
        "word_count": 61,
        "unique_words": 51,
        "lexical_diversity": 0.8360655737704918
      },
      "preservation_score": 3.406191729551069e-05
    },
    {
      "id": 20,
      "text": "Ela por me conhecer e saber como sou, não afetou o momento assim continuamos fudendo, trepando e transando até o garçom bater na porta do motel nos expulsando do quarto.\\n\\n",
      "position": 4424,
      "chapter": 2,
      "page": 14,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 31.4,
      "complexity_metrics": {
        "word_count": 30,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 30.0,
        "avg_word_length": 4.666666666666667,
        "unique_word_ratio": 0.9,
        "avg_paragraph_length": 30.0,
        "punctuation_density": 0.1,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "conhecer",
          "saber",
          "como",
          "afetou",
          "momento",
          "assim",
          "continuamos",
          "fudendo",
          "trepando",
          "transando",
          "garçom",
          "bater",
          "porta",
          "motel",
          "expulsando",
          "quarto"
        ],
        "entities": [
          [
            "transando até",
            "ORG"
          ]
        ],
        "readability_score": 83.6,
        "semantic_density": 0,
        "word_count": 30,
        "unique_words": 27,
        "lexical_diversity": 0.9
      },
      "preservation_score": 2.0437150377306416e-05
    },
    {
      "id": 21,
      "text": "Como esse capítulo é para penetrar os leitores na ideia do livro, irei colocar uns questionamentos que mais escuto como rótulos, preconceitos, medo, meio social, estrutura familiar e outras questões limitadoras, conservadoras, imaginárias e etc.\\n\\n",
      "position": 4595,
      "chapter": 2,
      "page": 15,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 38.308571428571426,
      "complexity_metrics": {
        "word_count": 35,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 35.0,
        "avg_word_length": 6.0285714285714285,
        "unique_word_ratio": 0.9714285714285714,
        "avg_paragraph_length": 35.0,
        "punctuation_density": 0.22857142857142856,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "como",
          "esse",
          "capítulo",
          "penetrar",
          "leitores",
          "ideia",
          "livro",
          "irei",
          "colocar",
          "questionamentos",
          "mais",
          "escuto",
          "rótulos",
          "preconceitos",
          "medo",
          "meio",
          "social",
          "estrutura",
          "familiar",
          "outras"
        ],
        "entities": [
          [
            "medo",
            "GPE"
          ]
        ],
        "readability_score": 80.69142857142857,
        "semantic_density": 0,
        "word_count": 35,
        "unique_words": 34,
        "lexical_diversity": 0.9714285714285714
      },
      "preservation_score": 5.449906767281711e-05
    },
    {
      "id": 22,
      "text": "Por quais motivos necessitamos de sexo?\\n\\n",
      "position": 4842,
      "chapter": 2,
      "page": 16,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 19.7,
      "complexity_metrics": {
        "word_count": 6,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 6.0,
        "avg_word_length": 5.666666666666667,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 6.0,
        "punctuation_density": 0.16666666666666666,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quais",
          "motivos",
          "necessitamos",
          "sexo"
        ],
        "entities": [
          [
            "motivos necessitamos de sexo",
            "PERSON"
          ]
        ],
        "readability_score": 95.3,
        "semantic_density": 0,
        "word_count": 6,
        "unique_words": 6,
        "lexical_diversity": 1.0
      },
      "preservation_score": 6.812383459102139e-06
    },
    {
      "id": 23,
      "text": "Quais são os nossos gatilhos sexuais?\\n\\n",
      "position": 4883,
      "chapter": 2,
      "page": 17,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 19.6,
      "complexity_metrics": {
        "word_count": 6,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 6.0,
        "avg_word_length": 5.333333333333333,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 6.0,
        "punctuation_density": 0.16666666666666666,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quais",
          "nossos",
          "gatilhos",
          "sexuais"
        ],
        "entities": [],
        "readability_score": 95.4,
        "semantic_density": 0,
        "word_count": 6,
        "unique_words": 6,
        "lexical_diversity": 1.0
      },
      "preservation_score": 6.812383459102139e-06
    },
    {
      "id": 24,
      "text": "Quais são os preconceitos?\\n\\n",
      "position": 4922,
      "chapter": 2,
      "page": 18,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 20.725,
      "complexity_metrics": {
        "word_count": 4,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 4.0,
        "avg_word_length": 5.75,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 4.0,
        "punctuation_density": 0.25,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quais",
          "preconceitos"
        ],
        "entities": [],
        "readability_score": 96.275,
        "semantic_density": 0,
        "word_count": 4,
        "unique_words": 4,
        "lexical_diversity": 1.0
      },
      "preservation_score": 6.812383459102139e-06
    },
    {
      "id": 25,
      "text": "Como a religião limita?\\n\\n",
      "position": 4950,
      "chapter": 2,
      "page": 19,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 18.5,
      "complexity_metrics": {
        "word_count": 4,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 4.0,
        "avg_word_length": 5.0,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 4.0,
        "punctuation_density": 0.25,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "como",
          "religião",
          "limita"
        ],
        "entities": [],
        "readability_score": 96.5,
        "semantic_density": 0,
        "word_count": 4,
        "unique_words": 4,
        "lexical_diversity": 1.0
      },
      "preservation_score": 6.812383459102139e-06
    },
    {
      "id": 26,
      "text": "Quais são os limites ou temos limites?\\n\\n",
      "position": 4975,
      "chapter": 2,
      "page": 20,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 19.87142857142857,
      "complexity_metrics": {
        "word_count": 7,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 7.0,
        "avg_word_length": 4.571428571428571,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 7.0,
        "punctuation_density": 0.14285714285714285,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "limites",
          "quais",
          "temos"
        ],
        "entities": [],
        "readability_score": 95.12857142857143,
        "semantic_density": 0,
        "word_count": 7,
        "unique_words": 7,
        "lexical_diversity": 1.0
      },
      "preservation_score": 6.812383459102139e-06
    },
    {
      "id": 27,
      "text": "Como enxergamos e como imaginamos?\\n\\n",
      "position": 5015,
      "chapter": 2,
      "page": 21,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 19.3,
      "complexity_metrics": {
        "word_count": 5,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 5.0,
        "avg_word_length": 6.0,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 5.0,
        "punctuation_density": 0.2,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "como",
          "enxergamos",
          "imaginamos"
        ],
        "entities": [
          [
            "Como",
            "ORG"
          ]
        ],
        "readability_score": 95.7,
        "semantic_density": 0,
        "word_count": 5,
        "unique_words": 5,
        "lexical_diversity": 1.0
      },
      "preservation_score": 6.812383459102139e-06
    },
    {
      "id": 28,
      "text": "Qual é a necessidade visual?\\n\\n",
      "position": 5051,
      "chapter": 2,
      "page": 22,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 18.94,
      "complexity_metrics": {
        "word_count": 5,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 5.0,
        "avg_word_length": 4.8,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 5.0,
        "punctuation_density": 0.2,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "qual",
          "necessidade",
          "visual"
        ],
        "entities": [],
        "readability_score": 96.06,
        "semantic_density": 0,
        "word_count": 5,
        "unique_words": 5,
        "lexical_diversity": 1.0
      },
      "preservation_score": 6.812383459102139e-06
    },
    {
      "id": 29,
      "text": "Por quais motivos criamos fetiches?\\n\\n",
      "position": 5081,
      "chapter": 2,
      "page": 23,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 19.36,
      "complexity_metrics": {
        "word_count": 5,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 5.0,
        "avg_word_length": 6.2,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 5.0,
        "punctuation_density": 0.2,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quais",
          "motivos",
          "criamos",
          "fetiches"
        ],
        "entities": [],
        "readability_score": 95.64,
        "semantic_density": 0,
        "word_count": 5,
        "unique_words": 5,
        "lexical_diversity": 1.0
      },
      "preservation_score": 6.812383459102139e-06
    },
    {
      "id": 30,
      "text": "Como é para se chegar ao amor?\\n\\n",
      "position": 5118,
      "chapter": 2,
      "page": 24,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 19.52857142857143,
      "complexity_metrics": {
        "word_count": 7,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 7.0,
        "avg_word_length": 3.4285714285714284,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 7.0,
        "punctuation_density": 0.14285714285714285,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "como",
          "chegar",
          "amor"
        ],
        "entities": [],
        "readability_score": 95.47142857142858,
        "semantic_density": 0,
        "word_count": 7,
        "unique_words": 7,
        "lexical_diversity": 1.0
      },
      "preservation_score": 6.812383459102139e-06
    },
    {
      "id": 31,
      "text": "Quantas diferentes forma existe de enxergar o amor e como foi a forma de ver o sexo? \\n\\n",
      "position": 5150,
      "chapter": 2,
      "page": 25,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 24.7,
      "complexity_metrics": {
        "word_count": 17,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 17.0,
        "avg_word_length": 4.0,
        "unique_word_ratio": 0.8235294117647058,
        "avg_paragraph_length": 17.0,
        "punctuation_density": 0.058823529411764705,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "forma",
          "quantas",
          "diferentes",
          "existe",
          "enxergar",
          "amor",
          "como",
          "sexo"
        ],
        "entities": [
          [
            "Quantas",
            "GPE"
          ]
        ],
        "readability_score": 90.3,
        "semantic_density": 0,
        "word_count": 17,
        "unique_words": 14,
        "lexical_diversity": 0.8235294117647058
      },
      "preservation_score": 6.812383459102139e-06
    },
    {
      "id": 32,
      "text": "Quantas formas têm de interpretar o sexo?\\n\\n",
      "position": 5237,
      "chapter": 2,
      "page": 26,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 20.0,
      "complexity_metrics": {
        "word_count": 7,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 7.0,
        "avg_word_length": 5.0,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 7.0,
        "punctuation_density": 0.14285714285714285,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quantas",
          "formas",
          "interpretar",
          "sexo"
        ],
        "entities": [
          [
            "Quantas",
            "GPE"
          ],
          [
            "formas têm de interpretar",
            "ORG"
          ]
        ],
        "readability_score": 95.0,
        "semantic_density": 0,
        "word_count": 7,
        "unique_words": 7,
        "lexical_diversity": 1.0
      },
      "preservation_score": 6.812383459102139e-06
    },
    {
      "id": 33,
      "text": "Porque o sexo anal é tão importante?\\n\\n",
      "position": 5280,
      "chapter": 2,
      "page": 27,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 19.785714285714285,
      "complexity_metrics": {
        "word_count": 7,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 7.0,
        "avg_word_length": 4.285714285714286,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 7.0,
        "punctuation_density": 0.14285714285714285,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "porque",
          "sexo",
          "anal",
          "importante"
        ],
        "entities": [],
        "readability_score": 95.21428571428571,
        "semantic_density": 0,
        "word_count": 7,
        "unique_words": 7,
        "lexical_diversity": 1.0
      },
      "preservation_score": 6.812383459102139e-06
    },
    {
      "id": 34,
      "text": "Pensa comigo:\\n\\n",
      "position": 5318,
      "chapter": 2,
      "page": 28,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 17.8,
      "complexity_metrics": {
        "word_count": 2,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 2.0,
        "avg_word_length": 6.0,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 2.0,
        "punctuation_density": 0.5,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "pensa",
          "comigo"
        ],
        "entities": [],
        "readability_score": 97.2,
        "semantic_density": 0,
        "word_count": 2,
        "unique_words": 2,
        "lexical_diversity": 1.0
      },
      "preservation_score": 6.812383459102139e-06
    },
    {
      "id": 35,
      "text": " Nós éramos animais cheio de fome e cheio de tesão, nossos instintos primitivos são tão dominantes perante aos nosso desejos, que nunca deixamos de esquecer o único momento de prazer  ao lado de uma fogueira quentinha e confortável após aquele dia tenso de se caçar... eu fico me imaginando no lugar dos humanos das cavernas caçando, cheio de medo de ser comido ao invés de comer, essa parada era tão sinistra, que a cada 8 segundos no máximo nós precisamos tirar a nossa atenção da presa para não se fuder, até porque, quem se concentra demais acaba levando uma linguada no rabo... nada para fazer... nada para pensar... quase nenhum momento de felicidade... provavelmente muitos momentos de alegria e a felicidade era no papai e mamãe, conchinha penetrante cheia de areia, ouriço, espanador de aço, kibe na farinha de rosca, churros com açúcar de cristal e para se ter tudo isso é necessário ter o que comer para sentir a energia do amor e essa que faz a gente ficar no escuro nos ocasionando vária",
      "position": 5333,
      "chapter": 2,
      "page": 29,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 30.99590476190476,
      "complexity_metrics": {
        "word_count": 175,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 29.166666666666668,
        "avg_word_length": 4.708571428571428,
        "unique_word_ratio": 0.7257142857142858,
        "avg_paragraph_length": 175.0,
        "punctuation_density": 0.15428571428571428,
        "line_break_count": 0,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "cheio",
          "momento",
          "comer",
          "essa",
          "nada",
          "felicidade",
          "éramos",
          "animais",
          "fome",
          "tesão",
          "nossos",
          "instintos",
          "primitivos",
          "dominantes",
          "perante",
          "nosso",
          "desejos",
          "nunca",
          "deixamos",
          "esquecer"
        ],
        "entities": [
          [
            "animais cheio de fome e cheio de tesão",
            "ORG"
          ],
          [
            "tão",
            "ORG"
          ],
          [
            "aos nosso desejos",
            "PERSON"
          ],
          [
            "deixamos de esquecer",
            "ORG"
          ],
          [
            "único momento de",
            "ORG"
          ],
          [
            "lado de uma fogueira",
            "PERSON"
          ],
          [
            "dia",
            "ORG"
          ],
          [
            "de se caçar...",
            "PERSON"
          ],
          [
            "eu fico",
            "PERSON"
          ],
          [
            "das cavernas",
            "PRODUCT"
          ]
        ],
        "readability_score": 84.00409523809523,
        "semantic_density": 0,
        "word_count": 175,
        "unique_words": 127,
        "lexical_diversity": 0.7257142857142858
      },
      "preservation_score": 0.0
    },
    {
      "id": 36,
      "text": "s alegrias, merdas, tombos, pimenta no cu dos outros é refresco, alguém têm que se fuder para outros se darem bem, guerras, preconceitos, evolução, adaptação, necessidades, brigas, conflitos e tudo aquilo que nós vivemos hoje em dia de uma forma preguiçosa e confortável pensando o dia todo em como fazer sexo.\\n\\n",
      "position": 6333,
      "chapter": 2,
      "page": 30,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 38.529411764705884,
      "complexity_metrics": {
        "word_count": 51,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 51.0,
        "avg_word_length": 5.098039215686274,
        "unique_word_ratio": 0.8823529411764706,
        "avg_paragraph_length": 51.0,
        "punctuation_density": 0.23529411764705882,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "outros",
          "alegrias",
          "merdas",
          "tombos",
          "pimenta",
          "refresco",
          "alguém",
          "fuder",
          "darem",
          "guerras",
          "preconceitos",
          "evolução",
          "adaptação",
          "necessidades",
          "brigas",
          "conflitos",
          "tudo",
          "aquilo",
          "vivemos",
          "hoje"
        ],
        "entities": [
          [
            "merdas",
            "PERSON"
          ],
          [
            "para outros se darem",
            "PERSON"
          ],
          [
            "que",
            "CARDINAL"
          ],
          [
            "dia de uma forma",
            "ORG"
          ],
          [
            "dia",
            "ORG"
          ]
        ],
        "readability_score": 72.97058823529412,
        "semantic_density": 0,
        "word_count": 51,
        "unique_words": 45,
        "lexical_diversity": 0.8823529411764706
      },
      "preservation_score": 8.174860150922567e-05
    },
    {
      "id": 37,
      "text": "Todos somos entediados!!!\\n\\n",
      "position": 6645,
      "chapter": 2,
      "page": 31,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 18.8,
      "complexity_metrics": {
        "word_count": 3,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 3.0,
        "avg_word_length": 7.666666666666667,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 3.0,
        "punctuation_density": 1.0,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "todos",
          "somos",
          "entediados"
        ],
        "entities": [],
        "readability_score": 96.2,
        "semantic_density": 0,
        "word_count": 3,
        "unique_words": 3,
        "lexical_diversity": 1.0
      },
      "preservation_score": 2.0437150377306416e-05
    },
    {
      "id": 38,
      "text": "Vivemos em um tédio sem fim de obrigações e problemas que imaginamos, não por termos muita imaginação e sim por não saber viver, pensando que o fator de estar vivo é pior que ter nascido, não sendo grato em perder o tédio em transar até parar de pensar no próprio tédio. Nós somos tão entediados que após nove meses vemos o resultado de uma noite, manhã, tarde entre vindas e idas entre paredes gosmentas e pegajosas de um corpo com profundidade relativa ao espaço tempo de um outro corpo, esse outro corpo de um formato peculiar e intrigante, por muitas vezes apelidado pelo próprio corpo que habita em uma forma de grandeza.\\n\\n",
      "position": 6672,
      "chapter": 2,
      "page": 32,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.379464285714285,
      "complexity_metrics": {
        "word_count": 112,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 56.0,
        "avg_word_length": 4.598214285714286,
        "unique_word_ratio": 0.6964285714285714,
        "avg_paragraph_length": 112.0,
        "punctuation_density": 0.08035714285714286,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "corpo",
          "tédio",
          "próprio",
          "entre",
          "outro",
          "vivemos",
          "obrigações",
          "problemas",
          "imaginamos",
          "termos",
          "muita",
          "imaginação",
          "saber",
          "viver",
          "pensando",
          "fator",
          "vivo",
          "pior",
          "nascido",
          "sendo"
        ],
        "entities": [
          [
            "Vivemos",
            "PERSON"
          ],
          [
            "que imaginamos",
            "PERSON"
          ],
          [
            "pensando que",
            "ORG"
          ],
          [
            "fator de estar",
            "ORG"
          ],
          [
            "vemos",
            "PERSON"
          ],
          [
            "tarde entre",
            "PERSON"
          ],
          [
            "vindas e idas",
            "PERSON"
          ],
          [
            "outro corpo",
            "PERSON"
          ],
          [
            "pelo próprio corpo",
            "PERSON"
          ],
          [
            "uma forma de grandeza",
            "PERSON"
          ]
        ],
        "readability_score": 70.62053571428572,
        "semantic_density": 0,
        "word_count": 112,
        "unique_words": 78,
        "lexical_diversity": 0.6964285714285714
      },
      "preservation_score": 6.131145113191925e-05
    },
    {
      "id": 39,
      "text": " Essa grandeza é tão grande que muitos lutam espada “cúm” escudo, por muitas vezes esses duelos se transformam em uma batalha e as vezes nessas batalhas, dependendo de como é o terreno onde ocorre, necessita chamar as guerreiras da idade média, também conhecidas como abertura do mar vermelho, não atoa, até porque, bem próximo do mar vermelho têm um caminho estreito, com ondulações e com um terreno cheio de barro pelo caminho, esse caminho é muito perigoso pois onde se encontra tem muitos desafios mentais, insistência, clemência e qualquer coisa que motiva o outro a enfrentar os sacrifícios e as dificuldades do acesso, não só por ter muito barro no trajeto e sim pela dificuldade em chegar ao ponto de começar a batalha e por muitas vezes a batalha se perde antes mesmo de começar, pela dificuldade de chegar. \\n\\n",
      "position": 7300,
      "chapter": 2,
      "page": 33,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.46115107913669,
      "complexity_metrics": {
        "word_count": 139,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 139.0,
        "avg_word_length": 4.870503597122302,
        "unique_word_ratio": 0.697841726618705,
        "avg_paragraph_length": 139.0,
        "punctuation_density": 0.10071942446043165,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "vezes",
          "batalha",
          "caminho",
          "muitos",
          "muitas",
          "como",
          "terreno",
          "onde",
          "vermelho",
          "barro",
          "muito",
          "pela",
          "dificuldade",
          "chegar",
          "começar",
          "essa",
          "grandeza",
          "grande",
          "lutam",
          "espada"
        ],
        "entities": [
          [
            "Essa",
            "PERSON"
          ],
          [
            "dependendo de como",
            "ORG"
          ],
          [
            "necessita chamar",
            "PERSON"
          ],
          [
            "também",
            "ORG"
          ],
          [
            "como abertura",
            "PERSON"
          ],
          [
            "mar vermelho",
            "PERSON"
          ],
          [
            "não atoa",
            "ORG"
          ],
          [
            "mar vermelho têm",
            "PERSON"
          ],
          [
            "pelo",
            "PERSON"
          ],
          [
            "insistência",
            "GPE"
          ]
        ],
        "readability_score": 29.038848920863316,
        "semantic_density": 0,
        "word_count": 139,
        "unique_words": 97,
        "lexical_diversity": 0.697841726618705
      },
      "preservation_score": 0.00010899813534563423
    },
    {
      "id": 40,
      "text": "Temos também uma questão a mais nesse trajeto, temos muitas ofertas e demandas, pois todos aqueles que ousam enfrentar esse caminho, encaram com a concorrência daqueles que lutam com espada e daquelas que vem com o visual do Hitler, outros preferem as skinhead, essas são mais fanáticas em bater bola, até porque, têm outras que preferem lutar em igualdade pois o lado que contém espada é muito arcaico, pois pensam muito com a cabeça de baixo, assim tornando uma guerra mais fácil de se ter um estratégia, e isso, não veio pela a sagacidade das guerreiras e sim pela cabeça dominante ser aquela que não pensa, só agindo por impulso e quando agimos por impulsão, merdas acontecem e merdas cagadas não voltam ao rabo.\\n\\n",
      "position": 8119,
      "chapter": 2,
      "page": 34,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.43467741935484,
      "complexity_metrics": {
        "word_count": 124,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 124.0,
        "avg_word_length": 4.782258064516129,
        "unique_word_ratio": 0.7338709677419355,
        "avg_paragraph_length": 124.0,
        "punctuation_density": 0.11290322580645161,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "pois",
          "temos",
          "espada",
          "preferem",
          "muito",
          "cabeça",
          "pela",
          "merdas",
          "também",
          "questão",
          "nesse",
          "trajeto",
          "muitas",
          "ofertas",
          "demandas",
          "todos",
          "aqueles",
          "ousam",
          "enfrentar"
        ],
        "entities": [
          [
            "todos",
            "CARDINAL"
          ],
          [
            "ousam enfrentar",
            "PERSON"
          ],
          [
            "Hitler",
            "PERSON"
          ],
          [
            "outros preferem",
            "PERSON"
          ],
          [
            "mais fanáticas",
            "PERSON"
          ],
          [
            "que preferem lutar",
            "PERSON"
          ],
          [
            "muito arcaico",
            "PERSON"
          ],
          [
            "pensam muito",
            "PERSON"
          ],
          [
            "não veio pela",
            "PERSON"
          ],
          [
            "ser aquela que",
            "ORG"
          ]
        ],
        "readability_score": 36.56532258064516,
        "semantic_density": 0,
        "word_count": 124,
        "unique_words": 91,
        "lexical_diversity": 0.7338709677419355
      },
      "preservation_score": 9.537336842742996e-05
    },
    {
      "id": 41,
      "text": "Assim percebemos que o trajeto por muitas vezes é complicado, outras vezes se tornam mais fáceis, tudo depende do espaço, tempo e circunstâncias dos duelos e das batalhas enfrentadas, tendo compaixão, consentimento e as regras combinadas necessárias de nada irá nos afetar e sim engrandecer, até porque, grandes guerreiros e guerreiras só se tornam grandes pelo amor em conjunto e não só para si próprio.\\n\\n",
      "position": 8837,
      "chapter": 2,
      "page": 35,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.56923076923077,
      "complexity_metrics": {
        "word_count": 65,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 65.0,
        "avg_word_length": 5.230769230769231,
        "unique_word_ratio": 0.8461538461538461,
        "avg_paragraph_length": 65.0,
        "punctuation_density": 0.12307692307692308,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "vezes",
          "tornam",
          "grandes",
          "assim",
          "percebemos",
          "trajeto",
          "muitas",
          "complicado",
          "outras",
          "mais",
          "fáceis",
          "tudo",
          "depende",
          "espaço",
          "tempo",
          "circunstâncias",
          "duelos",
          "batalhas",
          "enfrentadas",
          "tendo"
        ],
        "entities": [
          [
            "batalhas enfrentadas",
            "PERSON"
          ],
          [
            "necessárias de nada",
            "PERSON"
          ],
          [
            "pelo amor",
            "PERSON"
          ]
        ],
        "readability_score": 65.93076923076923,
        "semantic_density": 0,
        "word_count": 65,
        "unique_words": 55,
        "lexical_diversity": 0.8461538461538461
      },
      "preservation_score": 5.449906767281711e-05
    },
    {
      "id": 42,
      "text": "Capítulo 2 o que está acontecendo?\\n\\n",
      "position": 9243,
      "chapter": 3,
      "page": 1,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 19.45,
      "complexity_metrics": {
        "word_count": 6,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 6.0,
        "avg_word_length": 4.833333333333333,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 6.0,
        "punctuation_density": 0.16666666666666666,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "capítulo",
          "está",
          "acontecendo"
        ],
        "entities": [],
        "readability_score": 95.55,
        "semantic_density": 0,
        "word_count": 6,
        "unique_words": 6,
        "lexical_diversity": 1.0
      },
      "preservation_score": 6.812383459102139e-06
    },
    {
      "id": 43,
      "text": "  Não sei vocês, mas quando eu perdi a virgindade eu queria fuder todos os dias!!!\\n\\n",
      "position": 9279,
      "chapter": 3,
      "page": 2,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 23.82,
      "complexity_metrics": {
        "word_count": 15,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 15.0,
        "avg_word_length": 4.4,
        "unique_word_ratio": 0.9333333333333333,
        "avg_paragraph_length": 15.0,
        "punctuation_density": 0.26666666666666666,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "vocês",
          "quando",
          "perdi",
          "virgindade",
          "queria",
          "fuder",
          "todos",
          "dias"
        ],
        "entities": [
          [
            "mas quando eu perdi",
            "PERSON"
          ],
          [
            "eu queria",
            "PERSON"
          ]
        ],
        "readability_score": 91.18,
        "semantic_density": 0,
        "word_count": 15,
        "unique_words": 14,
        "lexical_diversity": 0.9333333333333333
      },
      "preservation_score": 2.7249533836408556e-05
    },
    {
      "id": 44,
      "text": "Queria tanto fuder, que eu fudi o meu pau em uma madeira pensando que estava metendo na buceta. \\n\\n",
      "position": 9363,
      "chapter": 3,
      "page": 3,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 25.3,
      "complexity_metrics": {
        "word_count": 18,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 18.0,
        "avg_word_length": 4.333333333333333,
        "unique_word_ratio": 0.9444444444444444,
        "avg_paragraph_length": 18.0,
        "punctuation_density": 0.1111111111111111,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "queria",
          "tanto",
          "fuder",
          "fudi",
          "madeira",
          "pensando",
          "estava",
          "metendo",
          "buceta"
        ],
        "entities": [
          [
            "Queria",
            "PERSON"
          ],
          [
            "que eu",
            "PERSON"
          ],
          [
            "uma madeira pensando que estava",
            "ORG"
          ],
          [
            "na buceta",
            "PERSON"
          ]
        ],
        "readability_score": 89.7,
        "semantic_density": 0,
        "word_count": 18,
        "unique_words": 17,
        "lexical_diversity": 0.9444444444444444
      },
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "id": 45,
      "text": " pular uma página para deixar “assustado”...\\n\\n",
      "position": 9461,
      "chapter": 3,
      "page": 4,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 19.9,
      "complexity_metrics": {
        "word_count": 6,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 6.0,
        "avg_word_length": 6.333333333333333,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 6.0,
        "punctuation_density": 0.5,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "pular",
          "página",
          "deixar",
          "assustado"
        ],
        "entities": [
          [
            "pular",
            "ORG"
          ],
          [
            "página",
            "GPE"
          ],
          [
            "para deixar",
            "PERSON"
          ]
        ],
        "readability_score": 95.1,
        "semantic_density": 0,
        "word_count": 6,
        "unique_words": 6,
        "lexical_diversity": 1.0
      },
      "preservation_score": 3.406191729551069e-05
    },
    {
      "id": 46,
      "text": "Come cu de curioso...\\n\\n",
      "position": 9507,
      "chapter": 3,
      "page": 5,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 18.35,
      "complexity_metrics": {
        "word_count": 4,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 4.0,
        "avg_word_length": 4.5,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 4.0,
        "punctuation_density": 0.75,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "come",
          "curioso"
        ],
        "entities": [
          [
            "Come cu de curioso",
            "PERSON"
          ]
        ],
        "readability_score": 96.65,
        "semantic_density": 0,
        "word_count": 4,
        "unique_words": 4,
        "lexical_diversity": 1.0
      },
      "preservation_score": 2.0437150377306416e-05
    },
    {
      "id": 47,
      "text": "Está sentindo alguma coisa aí atrás ? Kkkkkkk\\n\\n",
      "position": 9530,
      "chapter": 3,
      "page": 6,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 18.175,
      "complexity_metrics": {
        "word_count": 8,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 4.0,
        "avg_word_length": 4.75,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 8.0,
        "punctuation_density": 0.125,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "está",
          "sentindo",
          "alguma",
          "coisa",
          "atrás",
          "kkkkkkk"
        ],
        "entities": [],
        "readability_score": 96.575,
        "semantic_density": 0,
        "word_count": 8,
        "unique_words": 8,
        "lexical_diversity": 1.0
      },
      "preservation_score": 6.812383459102139e-06
    },
    {
      "id": 48,
      "text": "Onde meu pai morava era um prédio com uma marcenaria na garagem e lá continham algumas bancadas de madeira, me parecia o local perfeito... Só que a inexperiência por ter sido comido por uma única mulher de utilidade pública para homens ou mulheres, sei lá, qualquer humano que sinta prazer sem prejudicar a ninguém e o fazendo ficar em êxtase, faça. \\n\\n",
      "position": 9577,
      "chapter": 3,
      "page": 7,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 31.671311475409837,
      "complexity_metrics": {
        "word_count": 61,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 30.5,
        "avg_word_length": 4.737704918032787,
        "unique_word_ratio": 0.8852459016393442,
        "avg_paragraph_length": 61.0,
        "punctuation_density": 0.13114754098360656,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "onde",
          "morava",
          "prédio",
          "marcenaria",
          "garagem",
          "continham",
          "algumas",
          "bancadas",
          "madeira",
          "parecia",
          "local",
          "perfeito",
          "inexperiência",
          "sido",
          "comido",
          "única",
          "mulher",
          "utilidade",
          "pública",
          "homens"
        ],
        "entities": [
          [
            "bancadas de madeira",
            "ORG"
          ],
          [
            "qualquer humano",
            "PERSON"
          ]
        ],
        "readability_score": 83.32868852459016,
        "semantic_density": 0,
        "word_count": 61,
        "unique_words": 54,
        "lexical_diversity": 0.8852459016393442
      },
      "preservation_score": 5.449906767281711e-05
    },
    {
      "id": 49,
      "text": "Coloquei a menina ali sentada na bancada e comecei a beijar, parecíamos um polvo de tanta mão que continha... o Goro (Mortal Kombat) ficaria perdido e não conseguiria acompanhar os movimentos de tão iniciantes que eram... se estivéssemos jogando bola íamos parecer que estávamos no jardim de infância com todos correndo para a bola ao mesmo tempo... nessa minha infantilidade coloquei o menor para fora e recebi a punheta mais torta que recebi em minha vida, porém, nesse momento, me senti no Céu glorificado pelo toque divino e novamente o instinto primitivo falou mais alto, tirei a roupa da coitada, coloquei como se fosse o homem alfa em cima da bancada e sem perceber, fui empurrar e empurrei na bancada, não tinha percebido que o cume era mais alto!!!\\n\\n",
      "position": 9929,
      "chapter": 3,
      "page": 8,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 32.58779069767442,
      "complexity_metrics": {
        "word_count": 129,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 32.25,
        "avg_word_length": 4.875968992248062,
        "unique_word_ratio": 0.7441860465116279,
        "avg_paragraph_length": 129.0,
        "punctuation_density": 0.15503875968992248,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "coloquei",
          "bancada",
          "mais",
          "bola",
          "minha",
          "recebi",
          "alto",
          "menina",
          "sentada",
          "comecei",
          "beijar",
          "parecíamos",
          "polvo",
          "tanta",
          "continha",
          "goro",
          "mortal",
          "kombat",
          "ficaria",
          "perdido"
        ],
        "entities": [
          [
            "Coloquei",
            "PERSON"
          ],
          [
            "ali",
            "NORP"
          ],
          [
            "Goro",
            "PERSON"
          ],
          [
            "Mortal Kombat",
            "PERSON"
          ],
          [
            "ficaria perdido e",
            "PERSON"
          ],
          [
            "movimentos de tão",
            "ORG"
          ],
          [
            "jogando bola",
            "PERSON"
          ],
          [
            "íamos",
            "ORG"
          ],
          [
            "que estávamos",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ]
        ],
        "readability_score": 82.41220930232558,
        "semantic_density": 0,
        "word_count": 129,
        "unique_words": 96,
        "lexical_diversity": 0.7441860465116279
      },
      "preservation_score": 0.00014987243610024706
    },
    {
      "id": 50,
      "text": "Nós vivemos tantas loucuras e devido a esses momentos serem tão inesquecíveis eu me pergunto: o que é loucura e o que é viver? \\n\\n",
      "position": 10688,
      "chapter": 3,
      "page": 9,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 28.2875,
      "complexity_metrics": {
        "word_count": 24,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 24.0,
        "avg_word_length": 4.291666666666667,
        "unique_word_ratio": 0.8333333333333334,
        "avg_paragraph_length": 24.0,
        "punctuation_density": 0.08333333333333333,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "vivemos",
          "tantas",
          "loucuras",
          "devido",
          "esses",
          "momentos",
          "serem",
          "inesquecíveis",
          "pergunto",
          "loucura",
          "viver"
        ],
        "entities": [],
        "readability_score": 86.7125,
        "semantic_density": 0,
        "word_count": 24,
        "unique_words": 20,
        "lexical_diversity": 0.8333333333333334
      },
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "id": 51,
      "text": "Temos tantos preconceitos estruturais que quem tem cu, tem medo de viver aqueles momentos que nunca mais vão se repetir, até porque, todo tempo que vivemos e passamos é relativo para mim e para você, pois eu não sei a forma que você pensa, eu não sei a sua linha raciocínio, eu não sei a sua forma de interpretar, eu não sei como é a sua mente criativa, eu só sei que nada sei e irei saber quando estiver no espaço tempo em que estiver acontecendo, pois o mar vermelho só corre para baixo, semelhante a brocha, borracha fraca, nunca aconteceu isso comigo, chupa aí para vê se sobe porque o tempo já passou e nós não vimos, pois estávamos ocupados pensando em como fazer sexo a cada 28 minutos que perdemos a concentração em nossos trabalhos, família, amigos e tudo aquilo que era para ser mais importante que uma foda, uma trepada que nos faz gastar além de tempo, muito dinheiro que por muitas vezes, aquela foda, fudeu com a vida de muitos que eram para ser mais amados e não mais fudidos.\\n\\n",
      "position": 10817,
      "chapter": 3,
      "page": 10,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 40.31739130434782,
      "complexity_metrics": {
        "word_count": 184,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 184.0,
        "avg_word_length": 4.391304347826087,
        "unique_word_ratio": 0.6304347826086957,
        "avg_paragraph_length": 184.0,
        "punctuation_density": 0.11413043478260869,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "tempo",
          "pois",
          "nunca",
          "porque",
          "você",
          "forma",
          "como",
          "estiver",
          "foda",
          "temos",
          "tantos",
          "preconceitos",
          "estruturais",
          "quem",
          "medo",
          "viver",
          "aqueles",
          "momentos",
          "repetir"
        ],
        "entities": [
          [
            "medo de viver",
            "PERSON"
          ],
          [
            "repetir",
            "CARDINAL"
          ],
          [
            "para mim",
            "PERSON"
          ],
          [
            "para você",
            "PERSON"
          ],
          [
            "eu não",
            "PERSON"
          ],
          [
            "eu não",
            "PERSON"
          ],
          [
            "eu não",
            "PERSON"
          ],
          [
            "eu não",
            "PERSON"
          ],
          [
            "eu só sei",
            "PERSON"
          ],
          [
            "nada sei",
            "ORG"
          ]
        ],
        "readability_score": 6.682608695652178,
        "semantic_density": 0,
        "word_count": 184,
        "unique_words": 116,
        "lexical_diversity": 0.6304347826086957
      },
      "preservation_score": 0.00014306005264114492
    },
    {
      "id": 52,
      "text": "Primeira namorada a gente nunca esquece, até porque, rola amor, sexo, fuder, transar, trepar, fetiches e tudo aquilo que libera toda a energia que está entre os dois corpos cheios de tesão e essa energia tem que ser gasta de alguma forma, como todos nós sabemos a melhor forma de gastar energia é fazendo exercícios e com uma boa parceira a motivação vai lá para cima, por muitas vezes temos que diminuir o ritmo para não dar fadiga, surpresas desagradáveis, teto preto, mordidas de mosquito, lugar para se esconder, um apoiar no outro e muitas outras formas, basta termos imaginações para saber quais tipos de exercícios servem para os nossos corpos e o que pretendemos obter, hipertrofia ou perca de gordura? \\n\\n",
      "position": 11810,
      "chapter": 3,
      "page": 11,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.46280991735537,
      "complexity_metrics": {
        "word_count": 121,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 121.0,
        "avg_word_length": 4.87603305785124,
        "unique_word_ratio": 0.7768595041322314,
        "avg_paragraph_length": 121.0,
        "punctuation_density": 0.14049586776859505,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "corpos",
          "forma",
          "exercícios",
          "muitas",
          "primeira",
          "namorada",
          "gente",
          "nunca",
          "esquece",
          "porque",
          "rola",
          "amor",
          "sexo",
          "fuder",
          "transar",
          "trepar",
          "fetiches",
          "tudo",
          "aquilo"
        ],
        "entities": [
          [
            "namorada",
            "ORG"
          ],
          [
            "gasta de alguma forma",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "nós sabemos",
            "ORG"
          ],
          [
            "para cima",
            "PERSON"
          ],
          [
            "mordidas de mosquito",
            "PERSON"
          ],
          [
            "para se esconder",
            "PERSON"
          ],
          [
            "outras formas",
            "PERSON"
          ],
          [
            "basta",
            "NORP"
          ]
        ],
        "readability_score": 38.03719008264463,
        "semantic_density": 0,
        "word_count": 121,
        "unique_words": 94,
        "lexical_diversity": 0.7768595041322314
      },
      "preservation_score": 0.00011581051880473634
    },
    {
      "id": 53,
      "text": "Hipertrofia – temos momentos que imaginamos ser mais fortes do que realmente somos, esses momentos temos que aproveitar e estarmos muitos dispostos a chegar ao limite dos nossos corpos. Começamos com pequenos movimentos acompanhados de sussurros, respiração forte, ofegante e involuntariamente os nossos corpos vão se adaptando ao movimento, não fique assustado com a intensidade dos movimentos é necessário ser intenso para o corpo se acostumar com a carga dos exercícios, pois a próxima etapa nos deixa com o abdômen e pernas exausta só dependendo de quanto tempo e a intensidade está sendo executado, nunca se afobe demais e nunca seja frio demais, seja aquilo que tem que ser no momento que precisa ser, se for para pegar pesado, pegue, se for para pegar leve, pegue e independente de como for, precisa ser intenso e dedicado, pois sem dedicação e dor, não tem ganho. Se fizermos todo exercício de uma forma prazerosa e com amor, acabaremos o exercício com muita endorfina, dopamina, serotonina e ocitocina.\\n\\n",
      "position": 12523,
      "chapter": 3,
      "page": 12,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.54,
      "complexity_metrics": {
        "word_count": 165,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 55.0,
        "avg_word_length": 5.133333333333334,
        "unique_word_ratio": 0.6666666666666666,
        "avg_paragraph_length": 165.0,
        "punctuation_density": 0.12121212121212122,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "temos",
          "momentos",
          "nossos",
          "corpos",
          "movimentos",
          "intensidade",
          "intenso",
          "pois",
          "nunca",
          "demais",
          "seja",
          "precisa",
          "pegar",
          "pegue",
          "exercício",
          "hipertrofia",
          "imaginamos",
          "mais",
          "fortes",
          "realmente"
        ],
        "entities": [
          [
            "Começamos",
            "PERSON"
          ],
          [
            "de sussurros",
            "GPE"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "pernas exausta",
            "ORG"
          ],
          [
            "dependendo de quanto",
            "ORG"
          ],
          [
            "pesado",
            "GPE"
          ],
          [
            "acabaremos",
            "PERSON"
          ],
          [
            "muita endorfina",
            "PERSON"
          ],
          [
            "ocitocina",
            "GPE"
          ]
        ],
        "readability_score": 70.96000000000001,
        "semantic_density": 0,
        "word_count": 165,
        "unique_words": 110,
        "lexical_diversity": 0.6666666666666666
      },
      "preservation_score": 0.00013624766918204277
    },
    {
      "id": 54,
      "text": "Perda de gordura – até começar a queimar, temos que nos fuder muito para atingirmos aquela conquista que tanto sonhamos e almejamos, nada vem do céu, muito menos uma boa rola ou uma boa buceta e se por acaso em meio a tempestade um raio nos atingir, temos que ser gratos, até porque, raramente um raio cai no mesmo lugar e quando cai, as cicatrizes são diferentes, as dores e a energia que passa pelos nossos corpos não são tão intensas de uma experiência para outra, e isso, por mais que essa situação seja um caso do acaso é prejudicial e pode ocasionar mortes não sabendo tratar a lesão, logo os nossos esforços, são em vão, até porque, para perdermos gorduras temos que ser mais dedicados que aqueles que vão a procura de hipertrofia, pois para se perder temos que ser repetitivos e adaptáveis com situações rotineiras, enjoativas, preguiçosas mas quando atingimos os nossos objetivos, metas, corpo, peitos, bunda, pernas e tudo aquilo que almejamos como estímulo e amor próprio, nós não ganhamos",
      "position": 13536,
      "chapter": 3,
      "page": 13,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.435838150289015,
      "complexity_metrics": {
        "word_count": 173,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 173.0,
        "avg_word_length": 4.786127167630058,
        "unique_word_ratio": 0.6705202312138728,
        "avg_paragraph_length": 173.0,
        "punctuation_density": 0.1329479768786127,
        "line_break_count": 0,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "temos",
          "nossos",
          "muito",
          "almejamos",
          "acaso",
          "raio",
          "porque",
          "quando",
          "mais",
          "perda",
          "gordura",
          "começar",
          "queimar",
          "fuder",
          "atingirmos",
          "aquela",
          "conquista",
          "tanto",
          "sonhamos",
          "nada"
        ],
        "entities": [
          [
            "Perda de gordura – até começar",
            "ORG"
          ],
          [
            "muito para atingirmos aquela",
            "PERSON"
          ],
          [
            "sonhamos",
            "PERSON"
          ],
          [
            "nada vem",
            "ORG"
          ],
          [
            "muito menos",
            "PERSON"
          ],
          [
            "quando cai",
            "PERSON"
          ],
          [
            "passa pelos",
            "PERSON"
          ],
          [
            "intensas de uma",
            "ORG"
          ],
          [
            "para outra",
            "PERSON"
          ],
          [
            "não sabendo",
            "FAC"
          ]
        ],
        "readability_score": 12.064161849710985,
        "semantic_density": 0,
        "word_count": 173,
        "unique_words": 116,
        "lexical_diversity": 0.6705202312138728
      },
      "preservation_score": 0.0
    },
    {
      "id": 55,
      "text": " só endorfina, dopamina, serotonina e ocitocina, também ganhamos muita autoestima, motivação de vida, estrutura familiar e muito, muito sexo com amor.\\n\\n",
      "position": 14536,
      "chapter": 3,
      "page": 14,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 29.34285714285714,
      "complexity_metrics": {
        "word_count": 21,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 21.0,
        "avg_word_length": 6.142857142857143,
        "unique_word_ratio": 0.9523809523809523,
        "avg_paragraph_length": 21.0,
        "punctuation_density": 0.3333333333333333,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "muito",
          "endorfina",
          "dopamina",
          "serotonina",
          "ocitocina",
          "também",
          "ganhamos",
          "muita",
          "autoestima",
          "motivação",
          "vida",
          "estrutura",
          "familiar",
          "sexo",
          "amor"
        ],
        "entities": [
          [
            "ocitocina",
            "GPE"
          ],
          [
            "também ganhamos muita autoestima",
            "PERSON"
          ],
          [
            "motivação de vida",
            "ORG"
          ],
          [
            "muito sexo",
            "PERSON"
          ]
        ],
        "readability_score": 87.65714285714286,
        "semantic_density": 0,
        "word_count": 21,
        "unique_words": 20,
        "lexical_diversity": 0.9523809523809523
      },
      "preservation_score": 4.768668421371498e-05
    },
    {
      "id": 56,
      "text": "Capítulo 3 suruba sentimental\\n\\n",
      "position": 14688,
      "chapter": 4,
      "page": 1,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 18.95,
      "complexity_metrics": {
        "word_count": 4,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 4.0,
        "avg_word_length": 6.5,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 4.0,
        "punctuation_density": 0.0,
        "line_break_count": 2,
        "formatting_preservation_score": 50.0
      },
      "analysis": {
        "keywords": [
          "capítulo",
          "suruba",
          "sentimental"
        ],
        "entities": [
          [
            "3",
            "CARDINAL"
          ],
          [
            "suruba",
            "GPE"
          ]
        ],
        "readability_score": 96.05,
        "semantic_density": 0,
        "word_count": 4,
        "unique_words": 4,
        "lexical_diversity": 1.0
      },
      "preservation_score": 0.0
    },
    {
      "id": 57,
      "text": "Quando comecei a fazer sexo com frequência, era tanta vagina, cu e boquete que quando eu ia tocar uma punheta eu me perdia entre sexo, fuder, transar, trepar, meter e amor. Assim logo o meu sentir o sentimento, era quando o meu pau ficava duro e naquela época eu era puro suco, meu pênis ficava ereto por andar de ônibus e aquela trepidação no saco me fazia ter muitos insights de cu... eu nem gosto muito de comer o cu, gosto mesmo é da gritaria!!! \\n\\n",
      "position": 14719,
      "chapter": 4,
      "page": 2,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 30.454901960784312,
      "complexity_metrics": {
        "word_count": 85,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 28.333333333333332,
        "avg_word_length": 4.294117647058823,
        "unique_word_ratio": 0.7764705882352941,
        "avg_paragraph_length": 85.0,
        "punctuation_density": 0.18823529411764706,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "quando",
          "sexo",
          "ficava",
          "gosto",
          "comecei",
          "fazer",
          "frequência",
          "tanta",
          "vagina",
          "boquete",
          "tocar",
          "punheta",
          "perdia",
          "entre",
          "fuder",
          "transar",
          "trepar",
          "meter",
          "amor",
          "assim"
        ],
        "entities": [
          [
            "Quando",
            "PERSON"
          ],
          [
            "quando eu ia",
            "PERSON"
          ],
          [
            "meter e amor",
            "PERSON"
          ],
          [
            "meu pau ficava duro e",
            "ORG"
          ],
          [
            "naquela época eu era puro suco",
            "ORG"
          ],
          [
            "de ônibus e",
            "PERSON"
          ],
          [
            "aquela trepidação",
            "PERSON"
          ],
          [
            "eu nem",
            "PERSON"
          ],
          [
            "muito de comer o cu",
            "ORG"
          ],
          [
            "gosto mesmo",
            "PERSON"
          ]
        ],
        "readability_score": 84.54509803921569,
        "semantic_density": 0,
        "word_count": 85,
        "unique_words": 66,
        "lexical_diversity": 0.7764705882352941
      },
      "preservation_score": 0.00010899813534563423
    },
    {
      "id": 58,
      "text": "Quando eu lembro dessas gritarias falando: \\n\\n",
      "position": 15171,
      "chapter": 4,
      "page": 3,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 19.85,
      "complexity_metrics": {
        "word_count": 6,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 6.0,
        "avg_word_length": 6.166666666666667,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 6.0,
        "punctuation_density": 0.16666666666666666,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quando",
          "lembro",
          "dessas",
          "gritarias",
          "falando"
        ],
        "entities": [
          [
            "Quando eu",
            "PERSON"
          ]
        ],
        "readability_score": 95.15,
        "semantic_density": 0,
        "word_count": 6,
        "unique_words": 6,
        "lexical_diversity": 1.0
      },
      "preservation_score": 6.812383459102139e-06
    },
    {
      "id": 59,
      "text": "Seu safado!!! você só gosta de comer o meu cu, só por que eu não gosto de dá.\\n\\n",
      "position": 15216,
      "chapter": 4,
      "page": 4,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 20.5,
      "complexity_metrics": {
        "word_count": 18,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 9.0,
        "avg_word_length": 3.3333333333333335,
        "unique_word_ratio": 0.8888888888888888,
        "avg_paragraph_length": 18.0,
        "punctuation_density": 0.2777777777777778,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "safado",
          "você",
          "gosta",
          "comer",
          "gosto"
        ],
        "entities": [
          [
            "você só gosta de comer",
            "PERSON"
          ],
          [
            "que eu não gosto de dá.",
            "PERSON"
          ]
        ],
        "readability_score": 94.5,
        "semantic_density": 0,
        "word_count": 18,
        "unique_words": 16,
        "lexical_diversity": 0.8888888888888888
      },
      "preservation_score": 3.406191729551069e-05
    },
    {
      "id": 60,
      "text": "Gosta desse cuzinho? come ele gostosinho que ele é “só seu”...\\n\\n",
      "position": 15295,
      "chapter": 4,
      "page": 5,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 19.168181818181818,
      "complexity_metrics": {
        "word_count": 11,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 5.5,
        "avg_word_length": 4.7272727272727275,
        "unique_word_ratio": 0.9090909090909091,
        "avg_paragraph_length": 11.0,
        "punctuation_density": 0.36363636363636365,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "gosta",
          "desse",
          "cuzinho",
          "come",
          "gostosinho"
        ],
        "entities": [
          [
            "Gosta",
            "PERSON"
          ]
        ],
        "readability_score": 95.83181818181818,
        "semantic_density": 0,
        "word_count": 11,
        "unique_words": 10,
        "lexical_diversity": 0.9090909090909091
      },
      "preservation_score": 4.087430075461283e-05
    },
    {
      "id": 61,
      "text": "Desculpa, nunca tinha acontecido isso antes. Relaxa, só não suja o meu edredom e vamos para o chuveiro, lá você se limpa e continuamos.\\n\\n",
      "position": 15359,
      "chapter": 4,
      "page": 6,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 22.4,
      "complexity_metrics": {
        "word_count": 24,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 12.0,
        "avg_word_length": 4.666666666666667,
        "unique_word_ratio": 0.9166666666666666,
        "avg_paragraph_length": 24.0,
        "punctuation_density": 0.20833333333333334,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "desculpa",
          "nunca",
          "tinha",
          "acontecido",
          "isso",
          "antes",
          "relaxa",
          "suja",
          "edredom",
          "vamos",
          "chuveiro",
          "você",
          "limpa",
          "continuamos"
        ],
        "entities": [
          [
            "Desculpa",
            "PERSON"
          ],
          [
            "Relaxa",
            "PERSON"
          ],
          [
            "você se limpa e continuamos",
            "PERSON"
          ]
        ],
        "readability_score": 92.6,
        "semantic_density": 0,
        "word_count": 24,
        "unique_words": 22,
        "lexical_diversity": 0.9166666666666666
      },
      "preservation_score": 3.406191729551069e-05
    },
    {
      "id": 62,
      "text": "Temos pênis, vagina, ânus, boca, braços, pé e qualquer parte do corpo que imaginamos usar no sexo, ou fuder, ou transar, ou trepar, ou meter, ou amar.\\n\\n",
      "position": 15496,
      "chapter": 4,
      "page": 7,
      "segment_type": "preserved_segment",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 29.87777777777778,
      "complexity_metrics": {
        "word_count": 27,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 27.0,
        "avg_word_length": 4.592592592592593,
        "unique_word_ratio": 0.8518518518518519,
        "avg_paragraph_length": 27.0,
        "punctuation_density": 0.4074074074074074,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "temos",
          "pênis",
          "vagina",
          "ânus",
          "boca",
          "braços",
          "qualquer",
          "parte",
          "corpo",
          "imaginamos",
          "usar",
          "sexo",
          "fuder",
          "transar",
          "trepar",
          "meter",
          "amar"
        ],
        "entities": [
          [
            "Temos",
            "PERSON"
          ],
          [
            "braços",
            "GPE"
          ],
          [
            "qualquer parte",
            "PERSON"
          ]
        ],
        "readability_score": 85.12222222222222,
        "semantic_density": 0,
        "word_count": 27,
        "unique_words": 23,
        "lexical_diversity": 0.8518518518518519
      },
      "preservation_score": 7.493621805012353e-05
    },
    {
      "id": 63,
      "text": "Temos tantas combinações diferentes de ter prazer que a nossa imaginação nós limita em pensar que isso possa certo, até porque, nem todas as religiões nos permite fuder assim como em alguns lares familiares não se pode ter sexo, também temos lugares antagônicos que só podem ter sexo e isso é um problema para aqueles que são sentimentais ou feios, pois nem sempre têm facilidades em ter um momento de fazer o guerreiro chorar, a menina do olho esticado salivar, o pisca pisca iluminar o caminho para aqueles que só tem momentos difíceis na vida, não por escolha e sim por nascer como tinha que nascer, e isso, nos faz nós menosprezar diante de uma sociedade em que uma imagem vale mais que mil palavras.\\n\\n",
      "position": 15648,
      "chapter": 4,
      "page": 8,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.391999999999996,
      "complexity_metrics": {
        "word_count": 125,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 125.0,
        "avg_word_length": 4.64,
        "unique_word_ratio": 0.736,
        "avg_paragraph_length": 125.0,
        "punctuation_density": 0.08,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "isso",
          "temos",
          "como",
          "sexo",
          "aqueles",
          "pisca",
          "nascer",
          "tantas",
          "combinações",
          "diferentes",
          "prazer",
          "nossa",
          "imaginação",
          "limita",
          "pensar",
          "possa",
          "certo",
          "porque",
          "todas",
          "religiões"
        ],
        "entities": [
          [
            "Temos",
            "PERSON"
          ],
          [
            "nem todas",
            "PERSON"
          ],
          [
            "também temos lugares",
            "PERSON"
          ],
          [
            "antagônicos",
            "PERSON"
          ],
          [
            "nem sempre",
            "PERSON"
          ],
          [
            "momento de fazer",
            "ORG"
          ],
          [
            "olho esticado salivar",
            "ORG"
          ],
          [
            "faz",
            "ORG"
          ]
        ],
        "readability_score": 36.108,
        "semantic_density": 0,
        "word_count": 125,
        "unique_words": 92,
        "lexical_diversity": 0.736
      },
      "preservation_score": 6.812383459102139e-05
    },
    {
      "id": 64,
      "text": "Temos opções visuais de todos os tipos e gostos, e isso, para aqueles que levam os fetiches acima da imaginação é um prato cheio de momentos inimagináveis que podem se transformar em imagináveis. Temos momentos que pegamos gatos e quando acordamos pela manhã é uma lebre, outras vezes imaginamos que uma silhueta é um violão e quando tiramos a roupa, percebemos que o m3, era maior que o espaço onde estava armazenado, semelhante a um botijão de gás que cabe 16m3 e na hora de abastecer entraram 20m3, não fique triste com o caso do acaso e sim sermos gratos e, se isso acontecer, não temos que ser rude com a situação e sim nos adaptarmos com aqueles momentos únicos e inesquecíveis em sermos fortes e amado, até porque, uma grande guerreira não é feita na felicidade e sim no caos. \\n\\n",
      "position": 16354,
      "chapter": 4,
      "page": 9,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.36808510638298,
      "complexity_metrics": {
        "word_count": 141,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 70.5,
        "avg_word_length": 4.560283687943262,
        "unique_word_ratio": 0.6737588652482269,
        "avg_paragraph_length": 141.0,
        "punctuation_density": 0.09219858156028368,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "temos",
          "momentos",
          "isso",
          "aqueles",
          "quando",
          "sermos",
          "opções",
          "visuais",
          "todos",
          "tipos",
          "gostos",
          "levam",
          "fetiches",
          "acima",
          "imaginação",
          "prato",
          "cheio",
          "inimagináveis",
          "podem",
          "transformar"
        ],
        "entities": [
          [
            "para aqueles",
            "PERSON"
          ],
          [
            "acima da imaginação",
            "PERSON"
          ],
          [
            "cheio de momentos inimagináveis",
            "FAC"
          ],
          [
            "Temos",
            "PERSON"
          ],
          [
            "vezes imaginamos",
            "PERSON"
          ],
          [
            "m3",
            "GPE"
          ],
          [
            "botijão de gás que",
            "ORG"
          ],
          [
            "16m3",
            "CARDINAL"
          ],
          [
            "hora de abastecer",
            "PERSON"
          ],
          [
            "20m3",
            "DATE"
          ]
        ],
        "readability_score": 63.38191489361702,
        "semantic_density": 0,
        "word_count": 141,
        "unique_words": 95,
        "lexical_diversity": 0.6737588652482269
      },
      "preservation_score": 8.856098496832781e-05
    },
    {
      "id": 65,
      "text": "Quantas formas diferentes temos em ter afetos sexuais?\\n\\n",
      "position": 17140,
      "chapter": 4,
      "page": 10,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 20.7625,
      "complexity_metrics": {
        "word_count": 8,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 8.0,
        "avg_word_length": 5.875,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 8.0,
        "punctuation_density": 0.125,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quantas",
          "formas",
          "diferentes",
          "temos",
          "afetos",
          "sexuais"
        ],
        "entities": [
          [
            "Quantas",
            "GPE"
          ]
        ],
        "readability_score": 94.2375,
        "semantic_density": 0,
        "word_count": 8,
        "unique_words": 8,
        "lexical_diversity": 1.0
      },
      "preservation_score": 6.812383459102139e-06
    },
    {
      "id": 66,
      "text": "O que é afeto sexual?\\n\\n",
      "position": 17196,
      "chapter": 4,
      "page": 11,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 18.52,
      "complexity_metrics": {
        "word_count": 5,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 5.0,
        "avg_word_length": 3.4,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 5.0,
        "punctuation_density": 0.2,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "afeto",
          "sexual"
        ],
        "entities": [],
        "readability_score": 96.48,
        "semantic_density": 0,
        "word_count": 5,
        "unique_words": 5,
        "lexical_diversity": 1.0
      },
      "preservation_score": 6.812383459102139e-06
    },
    {
      "id": 67,
      "text": "Quantas formas de afetos sexuais precisamos ter, para chegar a ter prazer?\\n\\n",
      "position": 17219,
      "chapter": 4,
      "page": 12,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 22.575,
      "complexity_metrics": {
        "word_count": 12,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 12.0,
        "avg_word_length": 5.25,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 12.0,
        "punctuation_density": 0.16666666666666666,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quantas",
          "formas",
          "afetos",
          "sexuais",
          "precisamos",
          "chegar",
          "prazer"
        ],
        "entities": [
          [
            "Quantas",
            "GPE"
          ],
          [
            "precisamos ter",
            "PERSON"
          ]
        ],
        "readability_score": 92.425,
        "semantic_density": 0,
        "word_count": 12,
        "unique_words": 12,
        "lexical_diversity": 1.0
      },
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "id": 68,
      "text": "Quantas formas de ter prazer temos e qual é o prazer que precisamos viver para entendermos o que é amar?\\n\\n",
      "position": 17295,
      "chapter": 4,
      "page": 13,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 26.275,
      "complexity_metrics": {
        "word_count": 20,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 20.0,
        "avg_word_length": 4.25,
        "unique_word_ratio": 0.8,
        "avg_paragraph_length": 20.0,
        "punctuation_density": 0.05,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "prazer",
          "quantas",
          "formas",
          "temos",
          "qual",
          "precisamos",
          "viver",
          "entendermos",
          "amar"
        ],
        "entities": [
          [
            "Quantas",
            "GPE"
          ]
        ],
        "readability_score": 88.725,
        "semantic_density": 0,
        "word_count": 20,
        "unique_words": 16,
        "lexical_diversity": 0.8
      },
      "preservation_score": 6.812383459102139e-06
    },
    {
      "id": 69,
      "text": "Qual é a forma certa de amar?\\n\\n",
      "position": 17401,
      "chapter": 4,
      "page": 14,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 19.485714285714288,
      "complexity_metrics": {
        "word_count": 7,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 7.0,
        "avg_word_length": 3.2857142857142856,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 7.0,
        "punctuation_density": 0.14285714285714285,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "qual",
          "forma",
          "certa",
          "amar"
        ],
        "entities": [],
        "readability_score": 95.51428571428572,
        "semantic_density": 0,
        "word_count": 7,
        "unique_words": 7,
        "lexical_diversity": 1.0
      },
      "preservation_score": 6.812383459102139e-06
    },
    {
      "id": 70,
      "text": "Esse capítulo é uma saga sexual sobre:\\n\\n",
      "position": 17432,
      "chapter": 4,
      "page": 15,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 19.87142857142857,
      "complexity_metrics": {
        "word_count": 7,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 7.0,
        "avg_word_length": 4.571428571428571,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 7.0,
        "punctuation_density": 0.14285714285714285,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "esse",
          "capítulo",
          "saga",
          "sexual"
        ],
        "entities": [],
        "readability_score": 95.12857142857143,
        "semantic_density": 0,
        "word_count": 7,
        "unique_words": 7,
        "lexical_diversity": 1.0
      },
      "preservation_score": 6.812383459102139e-06
    },
    {
      "id": 71,
      "text": "Sexo – Fui a um puteiro em Madureira, lá é o local onde Deus não duvida que possa acontecer, como dizia Arlindo Cruz, lá é um doce lugar, que é eterno no meu coração, que aos poetas traz inspiração, pra cantar, escrever e fazer uma suruba sentimental para compor, cantar, pintar, dançar e tudo aquilo que só é vivido com muito amor entre o caos. \\n\\n",
      "position": 17472,
      "chapter": 4,
      "page": 16,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.29692307692308,
      "complexity_metrics": {
        "word_count": 65,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 65.0,
        "avg_word_length": 4.323076923076923,
        "unique_word_ratio": 0.8307692307692308,
        "avg_paragraph_length": 65.0,
        "punctuation_density": 0.16923076923076924,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "cantar",
          "sexo",
          "puteiro",
          "madureira",
          "local",
          "onde",
          "deus",
          "duvida",
          "possa",
          "acontecer",
          "como",
          "dizia",
          "arlindo",
          "cruz",
          "doce",
          "lugar",
          "eterno",
          "coração",
          "poetas",
          "traz"
        ],
        "entities": [
          [
            "Madureira",
            "ORG"
          ],
          [
            "Deus",
            "LOC"
          ],
          [
            "Arlindo Cruz",
            "PERSON"
          ],
          [
            "uma suruba",
            "ORG"
          ],
          [
            "muito amor",
            "PERSON"
          ]
        ],
        "readability_score": 66.20307692307692,
        "semantic_density": 0,
        "word_count": 65,
        "unique_words": 54,
        "lexical_diversity": 0.8307692307692308
      },
      "preservation_score": 7.493621805012353e-05
    },
    {
      "id": 72,
      "text": "Sabe quando estamos sem dinheiro e queremos ser enganados? Esse foi um dia desses!\\n\\n",
      "position": 17820,
      "chapter": 4,
      "page": 17,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 19.978571428571428,
      "complexity_metrics": {
        "word_count": 14,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 7.0,
        "avg_word_length": 4.928571428571429,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 14.0,
        "punctuation_density": 0.14285714285714285,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "sabe",
          "quando",
          "estamos",
          "dinheiro",
          "queremos",
          "enganados",
          "esse",
          "desses"
        ],
        "entities": [
          [
            "quando estamos",
            "PERSON"
          ],
          [
            "sem dinheiro e queremos ser enganados",
            "ORG"
          ],
          [
            "dia",
            "ORG"
          ]
        ],
        "readability_score": 95.02142857142857,
        "semantic_density": 0,
        "word_count": 14,
        "unique_words": 14,
        "lexical_diversity": 1.0
      },
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "id": 73,
      "text": "Nós héteros somos alfa e queremos nos sentir fortes, então, aquele que quer dar prazer para ganhar dinheiro, aprenda a elogiar a parte do corpo que deixa a outra pessoa pensar que é grande, assim aqueles momentos sem prazer para um, torna-se prazeroso para o outro.\\n\\n",
      "position": 17904,
      "chapter": 4,
      "page": 18,
      "segment_type": "preserved_segment",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 36.434782608695656,
      "complexity_metrics": {
        "word_count": 46,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 46.0,
        "avg_word_length": 4.782608695652174,
        "unique_word_ratio": 0.8478260869565217,
        "avg_paragraph_length": 46.0,
        "punctuation_density": 0.13043478260869565,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "prazer",
          "héteros",
          "somos",
          "alfa",
          "queremos",
          "sentir",
          "fortes",
          "então",
          "aquele",
          "quer",
          "ganhar",
          "dinheiro",
          "aprenda",
          "elogiar",
          "parte",
          "corpo",
          "deixa",
          "outra",
          "pessoa",
          "pensar"
        ],
        "entities": [
          [
            "prazer",
            "PERSON"
          ],
          [
            "para ganhar dinheiro",
            "PERSON"
          ],
          [
            "aprenda",
            "ORG"
          ]
        ],
        "readability_score": 75.56521739130434,
        "semantic_density": 0,
        "word_count": 46,
        "unique_words": 39,
        "lexical_diversity": 0.8478260869565217
      },
      "preservation_score": 4.768668421371498e-05
    },
    {
      "id": 74,
      "text": "Exemplos: \\n\\n",
      "position": 18171,
      "chapter": 4,
      "page": 19,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 18.2,
      "complexity_metrics": {
        "word_count": 1,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 1.0,
        "avg_word_length": 9.0,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 1.0,
        "punctuation_density": 1.0,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "exemplos"
        ],
        "entities": [],
        "readability_score": 96.8,
        "semantic_density": 0,
        "word_count": 1,
        "unique_words": 1,
        "lexical_diversity": 1.0
      },
      "preservation_score": 6.812383459102139e-06
    },
    {
      "id": 75,
      "text": "Coloca devagar pois sua rola é muito grande e pode me machucar...\\n\\n",
      "position": 18183,
      "chapter": 4,
      "page": 20,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 22.35,
      "complexity_metrics": {
        "word_count": 12,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 12.0,
        "avg_word_length": 4.5,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 12.0,
        "punctuation_density": 0.25,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "coloca",
          "devagar",
          "pois",
          "rola",
          "muito",
          "grande",
          "pode",
          "machucar"
        ],
        "entities": [
          [
            "Coloca",
            "GPE"
          ]
        ],
        "readability_score": 92.65,
        "semantic_density": 0,
        "word_count": 12,
        "unique_words": 12,
        "lexical_diversity": 1.0
      },
      "preservation_score": 2.0437150377306416e-05
    },
    {
      "id": 76,
      "text": "Aí, soca devagar, está batendo no meu útero...\\n\\n",
      "position": 18250,
      "chapter": 4,
      "page": 21,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 20.4625,
      "complexity_metrics": {
        "word_count": 8,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 8.0,
        "avg_word_length": 4.875,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 8.0,
        "punctuation_density": 0.625,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "soca",
          "devagar",
          "está",
          "batendo",
          "útero"
        ],
        "entities": [],
        "readability_score": 94.5375,
        "semantic_density": 0,
        "word_count": 8,
        "unique_words": 8,
        "lexical_diversity": 1.0
      },
      "preservation_score": 3.406191729551069e-05
    },
    {
      "id": 77,
      "text": "Coloca esse pau todo em sua boca... Assim que essa frase acontecer, nunca deixe de indagar...\\n\\n",
      "position": 18298,
      "chapter": 4,
      "page": 22,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 20.4625,
      "complexity_metrics": {
        "word_count": 16,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 8.0,
        "avg_word_length": 4.875,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 16.0,
        "punctuation_density": 0.4375,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "coloca",
          "esse",
          "todo",
          "boca",
          "assim",
          "essa",
          "frase",
          "acontecer",
          "nunca",
          "deixe",
          "indagar"
        ],
        "entities": [
          [
            "Coloca",
            "GPE"
          ]
        ],
        "readability_score": 94.5375,
        "semantic_density": 0,
        "word_count": 16,
        "unique_words": 16,
        "lexical_diversity": 1.0
      },
      "preservation_score": 4.768668421371498e-05
    },
    {
      "id": 78,
      "text": "Cheguei ao puteiro onde um dos maiores sexo que eu já tive aconteceu, não por ser prazeroso e sim pela intensidade e é essa intensidade que nos move em fazer sexo, sexo e mais sexo. Como teríamos imaginação para fazer sexo, sem estímulo para ter insights? \\n\\n",
      "position": 18393,
      "chapter": 4,
      "page": 23,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 27.869565217391305,
      "complexity_metrics": {
        "word_count": 46,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 23.0,
        "avg_word_length": 4.565217391304348,
        "unique_word_ratio": 0.8260869565217391,
        "avg_paragraph_length": 46.0,
        "punctuation_density": 0.10869565217391304,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "sexo",
          "intensidade",
          "fazer",
          "cheguei",
          "puteiro",
          "onde",
          "maiores",
          "tive",
          "aconteceu",
          "prazeroso",
          "pela",
          "essa",
          "move",
          "mais",
          "como",
          "teríamos",
          "imaginação",
          "estímulo",
          "insights"
        ],
        "entities": [
          [
            "Cheguei",
            "PERSON"
          ],
          [
            "que eu já tive",
            "PERSON"
          ],
          [
            "para fazer",
            "PERSON"
          ]
        ],
        "readability_score": 87.13043478260869,
        "semantic_density": 0,
        "word_count": 46,
        "unique_words": 38,
        "lexical_diversity": 0.8260869565217391
      },
      "preservation_score": 3.406191729551069e-05
    },
    {
      "id": 79,
      "text": "O fazer chega a ser viciante de tão bom que é o momento, não toda hora e para a vida toda, e sim de acordo com o nosso poder fazer, respeitando o combinado faça, assim, eu só tinha R$ 30,00 no bolso em moedas, às coloquei acima do balcão e comecei a contar...\\n\\n",
      "position": 18651,
      "chapter": 4,
      "page": 24,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.17169811320755,
      "complexity_metrics": {
        "word_count": 53,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 53.0,
        "avg_word_length": 3.9056603773584904,
        "unique_word_ratio": 0.8679245283018868,
        "avg_paragraph_length": 53.0,
        "punctuation_density": 0.18867924528301888,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "fazer",
          "toda",
          "chega",
          "viciante",
          "momento",
          "hora",
          "vida",
          "acordo",
          "nosso",
          "poder",
          "respeitando",
          "combinado",
          "faça",
          "assim",
          "tinha",
          "bolso",
          "moedas",
          "coloquei",
          "acima",
          "balcão"
        ],
        "entities": [
          [
            "respeitando o combinado faça",
            "ORG"
          ],
          [
            "eu só",
            "PERSON"
          ],
          [
            "coloquei acima",
            "PERSON"
          ]
        ],
        "readability_score": 72.32830188679245,
        "semantic_density": 0,
        "word_count": 53,
        "unique_words": 46,
        "lexical_diversity": 0.8679245283018868
      },
      "preservation_score": 6.812383459102139e-05
    },
    {
      "id": 80,
      "text": "Tabela de preços:\\n\\n",
      "position": 18912,
      "chapter": 4,
      "page": 25,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 18.0,
      "complexity_metrics": {
        "word_count": 3,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 3.0,
        "avg_word_length": 5.0,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 3.0,
        "punctuation_density": 0.3333333333333333,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "tabela",
          "preços"
        ],
        "entities": [],
        "readability_score": 97.0,
        "semantic_density": 0,
        "word_count": 3,
        "unique_words": 3,
        "lexical_diversity": 1.0
      },
      "preservation_score": 6.812383459102139e-06
    },
    {
      "id": 81,
      "text": "Cada minuto R$ 1,00.\\n\\n",
      "position": 18931,
      "chapter": 4,
      "page": 26,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 18.275,
      "complexity_metrics": {
        "word_count": 4,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 4.0,
        "avg_word_length": 4.25,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 4.0,
        "punctuation_density": 0.5,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "cada",
          "minuto"
        ],
        "entities": [],
        "readability_score": 96.725,
        "semantic_density": 0,
        "word_count": 4,
        "unique_words": 4,
        "lexical_diversity": 1.0
      },
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "id": 82,
      "text": "Consumo mínimo R$ 20,00.\\n\\n",
      "position": 18953,
      "chapter": 4,
      "page": 27,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 18.575,
      "complexity_metrics": {
        "word_count": 4,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 4.0,
        "avg_word_length": 5.25,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 4.0,
        "punctuation_density": 0.5,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "consumo",
          "mínimo"
        ],
        "entities": [
          [
            "20,00",
            "DATE"
          ]
        ],
        "readability_score": 96.425,
        "semantic_density": 0,
        "word_count": 4,
        "unique_words": 4,
        "lexical_diversity": 1.0
      },
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "id": 83,
      "text": "Paguei e o caminho para o quarto era uma escada atrás do balcão bem estreita e torta cheias de degraus incoerentes e difíceis de achar um padrão, e eu bêbado tornou o acesso mais difícil ainda, até porque, antes disso eu e a galera que não tinha muita diversão não por falta de imaginação e sim por falta de dinheiro, nos restava aquilo que dava para fazer dentro das nossas condições e estilo de vida que éramos felizes. Cheguei ao quarto e fiquei deslumbrado com aquele quarto, pois antes de subir, um amigo me indicou a pegar o melhor quarto e eu esperei durante meia hora para subir, pois aquele quarto era muito cobiçado por ter ventilador e chuveiro, isso me deixou mais curioso ainda do local onde estava. Olhei para o meu entorno e as medidas eram bem extravagantes para um quarto de puteiro, 4 x 4 aproximadamente com uma cama de casal, um biombo com chuveiro, as paredes feitas com tapumes de madeira e o teto também, aí que veio a primeira parte interessante ao extremo... tinha um ventila",
      "position": 18979,
      "chapter": 4,
      "page": 28,
      "segment_type": "preserved_segment",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 36.35911602209944,
      "complexity_metrics": {
        "word_count": 181,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 45.25,
        "avg_word_length": 4.530386740331492,
        "unique_word_ratio": 0.6408839779005525,
        "avg_paragraph_length": 181.0,
        "punctuation_density": 0.09392265193370165,
        "line_break_count": 0,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "quarto",
          "mais",
          "ainda",
          "antes",
          "tinha",
          "falta",
          "aquele",
          "pois",
          "subir",
          "chuveiro",
          "paguei",
          "caminho",
          "escada",
          "atrás",
          "balcão",
          "estreita",
          "torta",
          "cheias",
          "degraus",
          "incoerentes"
        ],
        "entities": [
          [
            "Paguei",
            "PERSON"
          ],
          [
            "eu",
            "PERSON"
          ],
          [
            "acesso mais difícil ainda",
            "PERSON"
          ],
          [
            "disso eu",
            "PERSON"
          ],
          [
            "diversão",
            "ORG"
          ],
          [
            "que dava para",
            "PERSON"
          ],
          [
            "das nossas condições",
            "PRODUCT"
          ],
          [
            "Cheguei ao",
            "PERSON"
          ],
          [
            "eu esperei",
            "ORG"
          ],
          [
            "hora",
            "NORP"
          ]
        ],
        "readability_score": 76.01588397790056,
        "semantic_density": 0,
        "word_count": 181,
        "unique_words": 116,
        "lexical_diversity": 0.6408839779005525
      },
      "preservation_score": 0.0
    },
    {
      "id": 84,
      "text": "dor tufão (ventilador de ferro, ventilador de parede, ventilador de escola) com a grade apoiada em um círculo feito por alguma tico-tico (máquina de cortar madeira), eu olhei para aquilo e me assustei pelo vento que vinha nas minhas nádegas em algumas posições e em outras passava pelo saco e chegava até a olhota, porém feliz por estar em uma temperatura ambiente de aproximadamente 40 graus célsius me dedicando ao limite do corpo (30 minutos) essa foi uma das poucas vezes que não tive ejaculação precoce (mentira com um pouco de verdade, não posso ser tão hétero ao ponto de omitir o que todos deveriam falar com naturalidade, e isso, serve para conseguirmos fazer com aqueles que amamos felizes iguais nós somos).\\n\\n",
      "position": 19979,
      "chapter": 4,
      "page": 29,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.468032786885246,
      "complexity_metrics": {
        "word_count": 122,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 122.0,
        "avg_word_length": 4.89344262295082,
        "unique_word_ratio": 0.7704918032786885,
        "avg_paragraph_length": 122.0,
        "punctuation_density": 0.06557377049180328,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "ventilador",
          "tico",
          "pelo",
          "tufão",
          "ferro",
          "parede",
          "escola",
          "grade",
          "apoiada",
          "círculo",
          "feito",
          "alguma",
          "máquina",
          "cortar",
          "madeira",
          "olhei",
          "aquilo",
          "assustei",
          "vento",
          "vinha"
        ],
        "entities": [
          [
            "de parede",
            "PERSON"
          ],
          [
            "ventilador de escola",
            "PERSON"
          ],
          [
            "alguma tico-tico",
            "PERSON"
          ],
          [
            "máquina de cortar madeira",
            "ORG"
          ],
          [
            "eu olhei",
            "PERSON"
          ],
          [
            "pelo",
            "PERSON"
          ],
          [
            "outras passava pelo",
            "PERSON"
          ],
          [
            "chegava até",
            "ORG"
          ],
          [
            "temperatura ambiente de aproximadamente",
            "ORG"
          ],
          [
            "40",
            "CARDINAL"
          ]
        ],
        "readability_score": 37.531967213114754,
        "semantic_density": 0,
        "word_count": 122,
        "unique_words": 94,
        "lexical_diversity": 0.7704918032786885
      },
      "preservation_score": 0.00011581051880473634
    },
    {
      "id": 85,
      "text": "“Eu só tenho esse distúrbio devido a minha mãe me tirar do banheiro em 3 min de banho, logo tive que me adaptar ao pouco tempo. Kkkkkk”\\n\\n",
      "position": 20699,
      "chapter": 4,
      "page": 30,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 22.961111111111112,
      "complexity_metrics": {
        "word_count": 27,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 13.5,
        "avg_word_length": 4.037037037037037,
        "unique_word_ratio": 0.9629629629629629,
        "avg_paragraph_length": 27.0,
        "punctuation_density": 0.07407407407407407,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "tenho",
          "esse",
          "distúrbio",
          "devido",
          "minha",
          "tirar",
          "banheiro",
          "banho",
          "logo",
          "tive",
          "adaptar",
          "pouco",
          "tempo",
          "kkkkkk"
        ],
        "entities": [
          [
            "3",
            "CARDINAL"
          ]
        ],
        "readability_score": 92.03888888888889,
        "semantic_density": 0,
        "word_count": 27,
        "unique_words": 26,
        "lexical_diversity": 0.9629629629629629
      },
      "preservation_score": 2.7249533836408556e-05
    },
    {
      "id": 86,
      "text": "Eu fazendo aquele sexo selvagem felizão, bateram na porta falando que Tinha acabado o tempo.\\n\\n",
      "position": 20836,
      "chapter": 4,
      "page": 31,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 24.060000000000002,
      "complexity_metrics": {
        "word_count": 15,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 15.0,
        "avg_word_length": 5.2,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 15.0,
        "punctuation_density": 0.13333333333333333,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "fazendo",
          "aquele",
          "sexo",
          "selvagem",
          "felizão",
          "bateram",
          "porta",
          "falando",
          "tinha",
          "acabado",
          "tempo"
        ],
        "entities": [
          [
            "Eu",
            "ORG"
          ],
          [
            "selvagem felizão",
            "PERSON"
          ],
          [
            "bateram na porta falando",
            "PERSON"
          ],
          [
            "Tinha",
            "PRODUCT"
          ]
        ],
        "readability_score": 90.94,
        "semantic_density": 0,
        "word_count": 15,
        "unique_words": 15,
        "lexical_diversity": 1.0
      },
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "id": 87,
      "text": "Menina – continua, continua, mete essa rola, não para, tá gostoso!!!\\n\\n",
      "position": 20930,
      "chapter": 4,
      "page": 32,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 22.081818181818182,
      "complexity_metrics": {
        "word_count": 11,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 11.0,
        "avg_word_length": 5.2727272727272725,
        "unique_word_ratio": 0.9090909090909091,
        "avg_paragraph_length": 11.0,
        "punctuation_density": 0.6363636363636364,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "continua",
          "menina",
          "mete",
          "essa",
          "rola",
          "gostoso"
        ],
        "entities": [
          [
            "Menina",
            "LOC"
          ],
          [
            "essa rola",
            "PERSON"
          ]
        ],
        "readability_score": 92.91818181818182,
        "semantic_density": 0,
        "word_count": 11,
        "unique_words": 10,
        "lexical_diversity": 0.9090909090909091
      },
      "preservation_score": 4.768668421371498e-05
    },
    {
      "id": 88,
      "text": "Eu – estão batendo na porta, vão ficar bolado não?\\n\\n",
      "position": 21000,
      "chapter": 4,
      "page": 33,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 21.23,
      "complexity_metrics": {
        "word_count": 10,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 10.0,
        "avg_word_length": 4.1,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 10.0,
        "punctuation_density": 0.2,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "estão",
          "batendo",
          "porta",
          "ficar",
          "bolado"
        ],
        "entities": [
          [
            "bolado",
            "ORG"
          ]
        ],
        "readability_score": 93.77,
        "semantic_density": 0,
        "word_count": 10,
        "unique_words": 10,
        "lexical_diversity": 1.0
      },
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "id": 89,
      "text": "Menina – para de falar e mete.\\n\\n",
      "position": 21052,
      "chapter": 4,
      "page": 34,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 19.52857142857143,
      "complexity_metrics": {
        "word_count": 7,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 7.0,
        "avg_word_length": 3.4285714285714284,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 7.0,
        "punctuation_density": 0.14285714285714285,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "menina",
          "falar",
          "mete"
        ],
        "entities": [
          [
            "Menina",
            "LOC"
          ]
        ],
        "readability_score": 95.47142857142858,
        "semantic_density": 0,
        "word_count": 7,
        "unique_words": 7,
        "lexical_diversity": 1.0
      },
      "preservation_score": 6.812383459102139e-06
    },
    {
      "id": 90,
      "text": "Aumentei a intensidade dos exercícios para aumentar o calor e ferver o leite, gozei!!! \\n\\n",
      "position": 21084,
      "chapter": 4,
      "page": 35,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 23.564285714285717,
      "complexity_metrics": {
        "word_count": 14,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 14.0,
        "avg_word_length": 5.214285714285714,
        "unique_word_ratio": 0.9285714285714286,
        "avg_paragraph_length": 14.0,
        "punctuation_density": 0.2857142857142857,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "aumentei",
          "intensidade",
          "exercícios",
          "aumentar",
          "calor",
          "ferver",
          "leite",
          "gozei"
        ],
        "entities": [
          [
            "para aumentar",
            "PERSON"
          ],
          [
            "calor",
            "ORG"
          ]
        ],
        "readability_score": 91.43571428571428,
        "semantic_density": 0,
        "word_count": 14,
        "unique_words": 13,
        "lexical_diversity": 0.9285714285714286
      },
      "preservation_score": 2.7249533836408556e-05
    },
    {
      "id": 91,
      "text": "Menina – gozou?\\n\\n",
      "position": 21173,
      "chapter": 4,
      "page": 36,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 17.8,
      "complexity_metrics": {
        "word_count": 3,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 3.0,
        "avg_word_length": 4.333333333333333,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 3.0,
        "punctuation_density": 0.3333333333333333,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "menina",
          "gozou"
        ],
        "entities": [
          [
            "Menina",
            "LOC"
          ]
        ],
        "readability_score": 97.2,
        "semantic_density": 0,
        "word_count": 3,
        "unique_words": 3,
        "lexical_diversity": 1.0
      },
      "preservation_score": 6.812383459102139e-06
    },
    {
      "id": 92,
      "text": "Eu – gozei!!!\\n\\n",
      "position": 21190,
      "chapter": 4,
      "page": 37,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 17.6,
      "complexity_metrics": {
        "word_count": 3,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 3.0,
        "avg_word_length": 3.6666666666666665,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 3.0,
        "punctuation_density": 1.0,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "gozei"
        ],
        "entities": [],
        "readability_score": 97.4,
        "semantic_density": 0,
        "word_count": 3,
        "unique_words": 3,
        "lexical_diversity": 1.0
      },
      "preservation_score": 2.0437150377306416e-05
    },
    {
      "id": 93,
      "text": "Menina – agora que você gozou é a minha vez de gozar!!\\n\\n",
      "position": 21205,
      "chapter": 4,
      "page": 38,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 22.075,
      "complexity_metrics": {
        "word_count": 12,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 12.0,
        "avg_word_length": 3.5833333333333335,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 12.0,
        "punctuation_density": 0.16666666666666666,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "menina",
          "agora",
          "você",
          "gozou",
          "minha",
          "gozar"
        ],
        "entities": [
          [
            "Menina",
            "LOC"
          ]
        ],
        "readability_score": 92.925,
        "semantic_density": 0,
        "word_count": 12,
        "unique_words": 12,
        "lexical_diversity": 1.0
      },
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "id": 94,
      "text": "Nesse momento bateram na porta com mais intensidade e a menina não teve escolha, abriu a porta!!\\n\\n",
      "position": 21261,
      "chapter": 4,
      "page": 39,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 24.911764705882355,
      "complexity_metrics": {
        "word_count": 17,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 17.0,
        "avg_word_length": 4.705882352941177,
        "unique_word_ratio": 0.9411764705882353,
        "avg_paragraph_length": 17.0,
        "punctuation_density": 0.17647058823529413,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "porta",
          "nesse",
          "momento",
          "bateram",
          "mais",
          "intensidade",
          "menina",
          "teve",
          "escolha",
          "abriu"
        ],
        "entities": [
          [
            "Nesse",
            "ORG"
          ]
        ],
        "readability_score": 90.08823529411765,
        "semantic_density": 0,
        "word_count": 17,
        "unique_words": 16,
        "lexical_diversity": 0.9411764705882353
      },
      "preservation_score": 2.0437150377306416e-05
    },
    {
      "id": 95,
      "text": "Eu estava atrás da porta pelado e na época eu era bonito e forte, entraram 3 mulheres no quarto pois só tinha aquele banheiro para tomar banho. Quando vi aquela situação eu me senti em um harém, foi tanto que saí de trás da porta falando: estou em um harém!!!\\n\\n",
      "position": 21359,
      "chapter": 4,
      "page": 40,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 28.759999999999998,
      "complexity_metrics": {
        "word_count": 50,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 25.0,
        "avg_word_length": 4.2,
        "unique_word_ratio": 0.88,
        "avg_paragraph_length": 50.0,
        "punctuation_density": 0.14,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "porta",
          "harém",
          "estava",
          "atrás",
          "pelado",
          "época",
          "bonito",
          "forte",
          "entraram",
          "mulheres",
          "quarto",
          "pois",
          "tinha",
          "aquele",
          "banheiro",
          "tomar",
          "banho",
          "quando",
          "aquela",
          "situação"
        ],
        "entities": [
          [
            "Eu estava",
            "PERSON"
          ],
          [
            "3",
            "CARDINAL"
          ],
          [
            "para tomar",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "aquela situação eu",
            "PERSON"
          ]
        ],
        "readability_score": 86.24,
        "semantic_density": 0,
        "word_count": 50,
        "unique_words": 44,
        "lexical_diversity": 0.88
      },
      "preservation_score": 4.768668421371498e-05
    },
    {
      "id": 96,
      "text": "As meninas – humm que indiozinho bonito, olha que bunda, quero apertar!!!\\n\\n",
      "position": 21620,
      "chapter": 4,
      "page": 41,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 22.55,
      "complexity_metrics": {
        "word_count": 12,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 12.0,
        "avg_word_length": 5.166666666666667,
        "unique_word_ratio": 0.9166666666666666,
        "avg_paragraph_length": 12.0,
        "punctuation_density": 0.4166666666666667,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "meninas",
          "humm",
          "indiozinho",
          "bonito",
          "olha",
          "bunda",
          "quero",
          "apertar"
        ],
        "entities": [],
        "readability_score": 92.45,
        "semantic_density": 0,
        "word_count": 12,
        "unique_words": 11,
        "lexical_diversity": 0.9166666666666666
      },
      "preservation_score": 3.406191729551069e-05
    },
    {
      "id": 97,
      "text": "Eu – olha e aprecie sem tocar!!!\\n\\n",
      "position": 21695,
      "chapter": 4,
      "page": 42,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 19.614285714285714,
      "complexity_metrics": {
        "word_count": 7,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 7.0,
        "avg_word_length": 3.7142857142857144,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 7.0,
        "punctuation_density": 0.42857142857142855,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "olha",
          "aprecie",
          "tocar"
        ],
        "entities": [
          [
            "Eu",
            "PERSON"
          ]
        ],
        "readability_score": 95.38571428571429,
        "semantic_density": 0,
        "word_count": 7,
        "unique_words": 7,
        "lexical_diversity": 1.0
      },
      "preservation_score": 2.0437150377306416e-05
    },
    {
      "id": 98,
      "text": "Todas as meninas tomaram banho e eu deitado com a menina esperando (nessa hora não tinha regra de não beijar e muito menos tinha tempo) elas saírem. \\n\\n",
      "position": 21729,
      "chapter": 4,
      "page": 43,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 29.855555555555554,
      "complexity_metrics": {
        "word_count": 27,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 27.0,
        "avg_word_length": 4.518518518518518,
        "unique_word_ratio": 0.8888888888888888,
        "avg_paragraph_length": 27.0,
        "punctuation_density": 0.037037037037037035,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "tinha",
          "todas",
          "meninas",
          "tomaram",
          "banho",
          "deitado",
          "menina",
          "esperando",
          "nessa",
          "hora",
          "regra",
          "beijar",
          "muito",
          "menos",
          "tempo",
          "elas",
          "saírem"
        ],
        "entities": [
          [
            "eu deitado",
            "PERSON"
          ],
          [
            "nessa hora",
            "PERSON"
          ],
          [
            "não tinha",
            "ORG"
          ],
          [
            "regra de não beijar e muito",
            "ORG"
          ],
          [
            "elas saírem",
            "PERSON"
          ]
        ],
        "readability_score": 85.14444444444445,
        "semantic_density": 0,
        "word_count": 27,
        "unique_words": 24,
        "lexical_diversity": 0.8888888888888888
      },
      "preservation_score": 2.0437150377306416e-05
    },
    {
      "id": 99,
      "text": "Eu – vou tomar um banho (o chuveiro era um cano).\\n\\n",
      "position": 21880,
      "chapter": 4,
      "page": 44,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 21.563636363636363,
      "complexity_metrics": {
        "word_count": 11,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 11.0,
        "avg_word_length": 3.5454545454545454,
        "unique_word_ratio": 0.9090909090909091,
        "avg_paragraph_length": 11.0,
        "punctuation_density": 0.09090909090909091,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "tomar",
          "banho",
          "chuveiro",
          "cano"
        ],
        "entities": [
          [
            "Eu",
            "ORG"
          ]
        ],
        "readability_score": 93.43636363636364,
        "semantic_density": 0,
        "word_count": 11,
        "unique_words": 10,
        "lexical_diversity": 0.9090909090909091
      },
      "preservation_score": 2.0437150377306416e-05
    },
    {
      "id": 100,
      "text": "Menina – acabou? venha me comer!!\\n\\n",
      "position": 21931,
      "chapter": 4,
      "page": 45,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 17.9,
      "complexity_metrics": {
        "word_count": 6,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 3.0,
        "avg_word_length": 4.666666666666667,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 6.0,
        "punctuation_density": 0.5,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "menina",
          "acabou",
          "venha",
          "comer"
        ],
        "entities": [
          [
            "Menina",
            "LOC"
          ]
        ],
        "readability_score": 97.1,
        "semantic_density": 0,
        "word_count": 6,
        "unique_words": 6,
        "lexical_diversity": 1.0
      },
      "preservation_score": 2.0437150377306416e-05
    },
    {
      "id": 101,
      "text": "Eu – filha, começa os trabalhos de novo, chupa!!!\\n\\n",
      "position": 21966,
      "chapter": 4,
      "page": 46,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 20.866666666666667,
      "complexity_metrics": {
        "word_count": 9,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 9.0,
        "avg_word_length": 4.555555555555555,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 9.0,
        "punctuation_density": 0.5555555555555556,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "filha",
          "começa",
          "trabalhos",
          "novo",
          "chupa"
        ],
        "entities": [
          [
            "começa os trabalhos de novo",
            "ORG"
          ]
        ],
        "readability_score": 94.13333333333334,
        "semantic_density": 0,
        "word_count": 9,
        "unique_words": 9,
        "lexical_diversity": 1.0
      },
      "preservation_score": 3.406191729551069e-05
    },
    {
      "id": 102,
      "text": "Deu àquela mamada estilo Lázaro, assim o meu escudeiro não muito fiel e às vezes morto, ressuscitou após a respiração boca a boca.\\n\\n",
      "position": 22017,
      "chapter": 4,
      "page": 47,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 27.90869565217391,
      "complexity_metrics": {
        "word_count": 23,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 23.0,
        "avg_word_length": 4.695652173913044,
        "unique_word_ratio": 0.9565217391304348,
        "avg_paragraph_length": 23.0,
        "punctuation_density": 0.13043478260869565,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "boca",
          "àquela",
          "mamada",
          "estilo",
          "lázaro",
          "assim",
          "escudeiro",
          "muito",
          "fiel",
          "vezes",
          "morto",
          "ressuscitou",
          "após",
          "respiração"
        ],
        "entities": [
          [
            "mamada",
            "NORP"
          ],
          [
            "Lázaro",
            "PERSON"
          ],
          [
            "meu",
            "ORG"
          ],
          [
            "não muito fiel",
            "PERSON"
          ]
        ],
        "readability_score": 87.09130434782608,
        "semantic_density": 0,
        "word_count": 23,
        "unique_words": 22,
        "lexical_diversity": 0.9565217391304348
      },
      "preservation_score": 2.0437150377306416e-05
    },
    {
      "id": 103,
      "text": "Depois de 2 horas dentro daquele quarto eu não lembrava da escada (quando desci me senti semelhante a um galo gigante... se eu tomasse um susto minha perna quebrava), não lembrava dos meus amigos (cabeça de cima raramente funciona, imagina nessas horas?)... eu só estava preocupado que eu não tinha dinheiro para pagar. \\n\\n",
      "position": 22149,
      "chapter": 4,
      "page": 48,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 23.261320754716984,
      "complexity_metrics": {
        "word_count": 53,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 13.25,
        "avg_word_length": 5.037735849056604,
        "unique_word_ratio": 0.8490566037735849,
        "avg_paragraph_length": 53.0,
        "punctuation_density": 0.18867924528301888,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "horas",
          "lembrava",
          "depois",
          "dentro",
          "daquele",
          "quarto",
          "escada",
          "quando",
          "desci",
          "senti",
          "semelhante",
          "galo",
          "gigante",
          "tomasse",
          "susto",
          "minha",
          "perna",
          "quebrava",
          "meus",
          "amigos"
        ],
        "entities": [
          [
            "Depois de 2",
            "ORG"
          ],
          [
            "quarto eu não lembrava da escada",
            "PERSON"
          ],
          [
            "quando desci",
            "PERSON"
          ],
          [
            "se eu",
            "PERSON"
          ],
          [
            "não lembrava",
            "PERSON"
          ],
          [
            "funciona",
            "GPE"
          ],
          [
            "imagina nessas",
            "PERSON"
          ],
          [
            "eu só estava",
            "PERSON"
          ],
          [
            "preocupado",
            "GPE"
          ],
          [
            "eu não",
            "PERSON"
          ]
        ],
        "readability_score": 91.86367924528302,
        "semantic_density": 0,
        "word_count": 53,
        "unique_words": 45,
        "lexical_diversity": 0.8490566037735849
      },
      "preservation_score": 9.537336842742996e-05
    },
    {
      "id": 104,
      "text": "Quase apanhei dos meus amigos!!!\\n\\n",
      "position": 22471,
      "chapter": 4,
      "page": 49,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 19.18,
      "complexity_metrics": {
        "word_count": 5,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 5.0,
        "avg_word_length": 5.6,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 5.0,
        "punctuation_density": 0.6,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quase",
          "apanhei",
          "meus",
          "amigos"
        ],
        "entities": [],
        "readability_score": 95.82,
        "semantic_density": 0,
        "word_count": 5,
        "unique_words": 5,
        "lexical_diversity": 1.0
      },
      "preservation_score": 2.0437150377306416e-05
    },
    {
      "id": 105,
      "text": "Sexo não precisa pensar e sim fazer.\\n\\n",
      "position": 22505,
      "chapter": 4,
      "page": 50,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 19.785714285714285,
      "complexity_metrics": {
        "word_count": 7,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 7.0,
        "avg_word_length": 4.285714285714286,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 7.0,
        "punctuation_density": 0.14285714285714285,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "sexo",
          "precisa",
          "pensar",
          "fazer"
        ],
        "entities": [],
        "readability_score": 95.21428571428571,
        "semantic_density": 0,
        "word_count": 7,
        "unique_words": 7,
        "lexical_diversity": 1.0
      },
      "preservation_score": 6.812383459102139e-06
    },
    {
      "id": 106,
      "text": "Fuder –  temos momentos que necessitamos que a preciosa necessita ser valorizada ou aqueles momentos em que necessitamos fazer o menor chorar, além dessas duas opções, temos aquela que todos tem e não têm coragem de usar, e quando usam, nunca deixam de usar, não sei porque isso acontece como foi dito antes sou “cufobia” e onde a família do Tarzan é feliz é necessário ter segurança com o cipó, até porque, o cipó não estando seguro pode ocorrer a queda ao se balançar e nessas quedas o prejudicado é o próximo a se balançar... Nossas vidas, são corpos físicos cheios de instintos impulsivos pela própria necessidade gananciosa de ter aquilo que sentimos e imaginamos como necessário, até vermos que as nossas importâncias são relativas e instintivas de acordo com as nossas formas de vermos e sentirmos os nossos próprios traumas corpóreas e mentais. \\n\\n",
      "position": 22543,
      "chapter": 4,
      "page": 51,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.475,
      "complexity_metrics": {
        "word_count": 144,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 72.0,
        "avg_word_length": 4.916666666666667,
        "unique_word_ratio": 0.7152777777777778,
        "avg_paragraph_length": 144.0,
        "punctuation_density": 0.09027777777777778,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "nossas",
          "temos",
          "momentos",
          "necessitamos",
          "usar",
          "porque",
          "como",
          "necessário",
          "cipó",
          "balançar",
          "vermos",
          "fuder",
          "preciosa",
          "necessita",
          "valorizada",
          "aqueles",
          "fazer",
          "menor",
          "chorar",
          "além"
        ],
        "entities": [
          [
            "valorizada",
            "GPE"
          ],
          [
            "dessas duas",
            "GPE"
          ],
          [
            "temos aquela",
            "PERSON"
          ],
          [
            "quando usam",
            "PERSON"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "próximo",
            "PERSON"
          ],
          [
            "Nossas",
            "PERSON"
          ],
          [
            "de instintos",
            "PERSON"
          ],
          [
            "impulsivos pela",
            "PERSON"
          ],
          [
            "própria necessidade",
            "ORG"
          ]
        ],
        "readability_score": 62.525,
        "semantic_density": 0,
        "word_count": 144,
        "unique_words": 103,
        "lexical_diversity": 0.7152777777777778
      },
      "preservation_score": 0.00010218575188653208
    },
    {
      "id": 107,
      "text": "Fuder não é apenas enfiar, comer, chupar e tocar, e sim, FUDER, puxar cabelo, ficar tenso, agressivo, muito vezes barulhento e semelhante a torcida do Flamengo cantando o hino e na parte de sermos consagrados no gramado, sempre amado, mais cotado é o ponto pico de uma boa foda e essas pessoas que tem esse dom é semelhante ao dom de ter nascido para jogar bola, advogado, pedreiro, aplicador de película protetora ao ponto de passarmos na rua por uma pessoa e aquela nos fazer ter imaginações, tipo assim:\\n\\n",
      "position": 23398,
      "chapter": 4,
      "page": 52,
      "segment_type": "preserved_segment",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 36.40898876404495,
      "complexity_metrics": {
        "word_count": 89,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 89.0,
        "avg_word_length": 4.696629213483146,
        "unique_word_ratio": 0.7865168539325843,
        "avg_paragraph_length": 89.0,
        "punctuation_density": 0.16853932584269662,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "fuder",
          "semelhante",
          "ponto",
          "apenas",
          "enfiar",
          "comer",
          "chupar",
          "tocar",
          "puxar",
          "cabelo",
          "ficar",
          "tenso",
          "agressivo",
          "muito",
          "vezes",
          "barulhento",
          "torcida",
          "flamengo",
          "cantando",
          "hino"
        ],
        "entities": [
          [
            "puxar cabelo",
            "PERSON"
          ],
          [
            "ficar tenso",
            "PERSON"
          ],
          [
            "muito vezes",
            "PERSON"
          ],
          [
            "Flamengo",
            "PERSON"
          ],
          [
            "sempre amado",
            "ORG"
          ],
          [
            "mais cotado",
            "ORG"
          ],
          [
            "ponto pico de uma boa foda",
            "ORG"
          ],
          [
            "para jogar bola",
            "PERSON"
          ],
          [
            "advogado",
            "GPE"
          ],
          [
            "pedreiro",
            "GPE"
          ]
        ],
        "readability_score": 54.09101123595506,
        "semantic_density": 0,
        "word_count": 89,
        "unique_words": 70,
        "lexical_diversity": 0.7865168539325843
      },
      "preservation_score": 0.00010218575188653208
    },
    {
      "id": 108,
      "text": "Imagina aquela pessoa fudendo? \\n\\n",
      "position": 23906,
      "chapter": 4,
      "page": 53,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 19.025,
      "complexity_metrics": {
        "word_count": 4,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 4.0,
        "avg_word_length": 6.75,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 4.0,
        "punctuation_density": 0.25,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "imagina",
          "aquela",
          "pessoa",
          "fudendo"
        ],
        "entities": [
          [
            "Imagina aquela pessoa fudendo",
            "PERSON"
          ]
        ],
        "readability_score": 95.975,
        "semantic_density": 0,
        "word_count": 4,
        "unique_words": 4,
        "lexical_diversity": 1.0
      },
      "preservation_score": 6.812383459102139e-06
    },
    {
      "id": 109,
      "text": "Deve ser mó fodão!! \\n\\n",
      "position": 23939,
      "chapter": 4,
      "page": 54,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 18.2,
      "complexity_metrics": {
        "word_count": 4,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 4.0,
        "avg_word_length": 4.0,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 4.0,
        "punctuation_density": 0.5,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "deve",
          "fodão"
        ],
        "entities": [],
        "readability_score": 96.8,
        "semantic_density": 0,
        "word_count": 4,
        "unique_words": 4,
        "lexical_diversity": 1.0
      },
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "id": 110,
      "text": "Imagina aquela posição?\\n\\n",
      "position": 23961,
      "chapter": 4,
      "page": 55,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 18.6,
      "complexity_metrics": {
        "word_count": 3,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 3.0,
        "avg_word_length": 7.0,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 3.0,
        "punctuation_density": 0.3333333333333333,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "imagina",
          "aquela",
          "posição"
        ],
        "entities": [
          [
            "Imagina aquela",
            "PERSON"
          ]
        ],
        "readability_score": 96.4,
        "semantic_density": 0,
        "word_count": 3,
        "unique_words": 3,
        "lexical_diversity": 1.0
      },
      "preservation_score": 6.812383459102139e-06
    },
    {
      "id": 111,
      "text": "O seu cheiro é Gostoso!!!\\n\\n",
      "position": 23986,
      "chapter": 4,
      "page": 56,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 18.759999999999998,
      "complexity_metrics": {
        "word_count": 5,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 5.0,
        "avg_word_length": 4.2,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 5.0,
        "punctuation_density": 0.6,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "cheiro",
          "gostoso"
        ],
        "entities": [],
        "readability_score": 96.24,
        "semantic_density": 0,
        "word_count": 5,
        "unique_words": 5,
        "lexical_diversity": 1.0
      },
      "preservation_score": 2.0437150377306416e-05
    },
    {
      "id": 112,
      "text": "E muitos também têm o dom de controlar o sentimento para manter o pau levantado, algumas vezes esse dom veio através de um bloqueio mental pelo medo de amar e não ser retribuído, fazendo a cabeça de baixo ter uma carreira de microempreendedor individual, com a cabeça de cima servindo só para arrumar os serviços.\\n\\n",
      "position": 24013,
      "chapter": 4,
      "page": 57,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.412727272727274,
      "complexity_metrics": {
        "word_count": 55,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 55.0,
        "avg_word_length": 4.709090909090909,
        "unique_word_ratio": 0.8,
        "avg_paragraph_length": 55.0,
        "punctuation_density": 0.07272727272727272,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "cabeça",
          "muitos",
          "também",
          "controlar",
          "sentimento",
          "manter",
          "levantado",
          "algumas",
          "vezes",
          "esse",
          "veio",
          "através",
          "bloqueio",
          "mental",
          "pelo",
          "medo",
          "amar",
          "retribuído",
          "fazendo",
          "baixo"
        ],
        "entities": [
          [
            "dom de controlar",
            "ORG"
          ],
          [
            "para manter",
            "PERSON"
          ],
          [
            "pau levantado",
            "PERSON"
          ],
          [
            "pelo medo de amar",
            "PERSON"
          ],
          [
            "carreira de microempreendedor",
            "ORG"
          ],
          [
            "servindo só para arrumar os",
            "PERSON"
          ]
        ],
        "readability_score": 71.08727272727273,
        "semantic_density": 0,
        "word_count": 55,
        "unique_words": 44,
        "lexical_diversity": 0.8
      },
      "preservation_score": 2.7249533836408556e-05
    },
    {
      "id": 113,
      "text": "Nem sempre essas pessoas que vivem para fuder, foram sempre assim, muitos sentiram tanto amor em uma foda, que fudeu com a beleza de interpretar o amar, não por escolha e sim por proteção de querer fuder pelas necessidades corpóreas e como fugas mentais de si próprio, não estando errado, porém se errar, acatar com as próprias consequências. Muitas mulheres morrem sem nunca sentirem prazer, outras morrem de tanto prazer... Àquelas que morrem sem sentir prazer, acontece por muitas vezes a devido ninguém nunca ter ensinado o sentir, outras por falta de atenção no sentir e outras por se enganar em fuder com a própria necessidade de viver democraticamente onde não se têm democracia, até porque, entender sobre termos direitos iguais em confiarmos um para com o outro diante do nosso próprio sentir uma rola veiúda entrando na nossa buceta e por muitas vezes quando se erra o buraco de cima ou de baixo, depende do ângulo que estejamos vendo, o acidente pode ser dolorido e engraçado, fácil e questionável, penetrado e fudido.\\n\\n",
      "position": 24328,
      "chapter": 4,
      "page": 58,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.48612716763006,
      "complexity_metrics": {
        "word_count": 173,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 57.666666666666664,
        "avg_word_length": 4.953757225433526,
        "unique_word_ratio": 0.6878612716763006,
        "avg_paragraph_length": 173.0,
        "punctuation_density": 0.12138728323699421,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "sentir",
          "fuder",
          "muitas",
          "morrem",
          "prazer",
          "outras",
          "sempre",
          "tanto",
          "próprio",
          "nunca",
          "vezes",
          "essas",
          "pessoas",
          "vivem",
          "assim",
          "muitos",
          "sentiram",
          "amor",
          "foda",
          "fudeu"
        ],
        "entities": [
          [
            "foram sempre assim",
            "ORG"
          ],
          [
            "mentais de si próprio",
            "ORG"
          ],
          [
            "morrem sem",
            "PERSON"
          ],
          [
            "outras morrem de tanto",
            "PERSON"
          ],
          [
            "Àquelas",
            "GPE"
          ],
          [
            "morrem sem",
            "PERSON"
          ],
          [
            "têm democracia",
            "ORG"
          ],
          [
            "vezes quando",
            "PERSON"
          ],
          [
            "buraco de cima",
            "ORG"
          ]
        ],
        "readability_score": 69.68053949903661,
        "semantic_density": 0,
        "word_count": 173,
        "unique_words": 119,
        "lexical_diversity": 0.6878612716763006
      },
      "preservation_score": 0.00014306005264114492
    },
    {
      "id": 114,
      "text": "Uma boa foda é uma boa foda. Quantos tipos de fuder nós temos?\\n\\n",
      "position": 25359,
      "chapter": 4,
      "page": 59,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 19.403846153846153,
      "complexity_metrics": {
        "word_count": 13,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 6.5,
        "avg_word_length": 3.8461538461538463,
        "unique_word_ratio": 0.9230769230769231,
        "avg_paragraph_length": 13.0,
        "punctuation_density": 0.15384615384615385,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "foda",
          "quantos",
          "tipos",
          "fuder",
          "temos"
        ],
        "entities": [],
        "readability_score": 95.59615384615384,
        "semantic_density": 0,
        "word_count": 13,
        "unique_words": 12,
        "lexical_diversity": 0.9230769230769231
      },
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "id": 115,
      "text": "Temos aquela que é na hora do almoço, temos aquela que é só para esvaziar o saco, temos àquela para relaxar, temos aquela que saímos suados, temos àquela que é só umazinha, temos aquelas que é uma chupada de Oiapoque a Chuí porém todos as fodas lembradas, só são lembradas por ter sido feito com algum sentimento marcante, seja uma boca, peito, cabelo, bunda, cu, pênis, piroca, tamanho, cor, formato, forma de fazer o boquete, forma que geme, forma que fala, forma de fuder é única para cada um, não temos culpa de sermos criados em uma sociedade que sempre impôs como importância uma “perfeição” em ter a melhor casa, melhor carro, as pessoas mais bonitas, mais gostosas, famosas e qualquer humano que possa vir ser um fetiche em ser lembrado como uma foda memorável!!  \\n\\n",
      "position": 25423,
      "chapter": 4,
      "page": 60,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.413333333333334,
      "complexity_metrics": {
        "word_count": 135,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 135.0,
        "avg_word_length": 4.711111111111111,
        "unique_word_ratio": 0.674074074074074,
        "avg_paragraph_length": 135.0,
        "punctuation_density": 0.2,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "temos",
          "forma",
          "aquela",
          "àquela",
          "lembradas",
          "como",
          "melhor",
          "mais",
          "hora",
          "almoço",
          "esvaziar",
          "saco",
          "relaxar",
          "saímos",
          "suados",
          "umazinha",
          "aquelas",
          "chupada",
          "oiapoque",
          "chuí"
        ],
        "entities": [
          [
            "Temos",
            "PERSON"
          ],
          [
            "hora",
            "NORP"
          ],
          [
            "temos aquela",
            "PERSON"
          ],
          [
            "saco",
            "ORG"
          ],
          [
            "àquela",
            "GPE"
          ],
          [
            "para relaxar",
            "PERSON"
          ],
          [
            "temos aquela",
            "PERSON"
          ],
          [
            "que saímos",
            "PERSON"
          ],
          [
            "Chuí",
            "ORG"
          ],
          [
            "fodas",
            "NORP"
          ]
        ],
        "readability_score": 31.086666666666673,
        "semantic_density": 0,
        "word_count": 135,
        "unique_words": 91,
        "lexical_diversity": 0.674074074074074
      },
      "preservation_score": 0.000197559120313962
    },
    {
      "id": 116,
      "text": "Lembranças dê uma boa foda!!\\n\\n",
      "position": 26197,
      "chapter": 4,
      "page": 61,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 18.94,
      "complexity_metrics": {
        "word_count": 5,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 5.0,
        "avg_word_length": 4.8,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 5.0,
        "punctuation_density": 0.4,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "lembranças",
          "foda"
        ],
        "entities": [
          [
            "Lembranças",
            "ORG"
          ]
        ],
        "readability_score": 96.06,
        "semantic_density": 0,
        "word_count": 5,
        "unique_words": 5,
        "lexical_diversity": 1.0
      },
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "id": 117,
      "text": "Sabe aquele “proibido” com muito sentimento? Essa foda foi assim!!\\n\\n",
      "position": 26227,
      "chapter": 4,
      "page": 62,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 19.21,
      "complexity_metrics": {
        "word_count": 10,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 5.0,
        "avg_word_length": 5.7,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 10.0,
        "punctuation_density": 0.3,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "sabe",
          "aquele",
          "proibido",
          "muito",
          "sentimento",
          "essa",
          "foda",
          "assim"
        ],
        "entities": [
          [
            "muito sentimento",
            "PERSON"
          ],
          [
            "Essa",
            "PERSON"
          ]
        ],
        "readability_score": 95.79,
        "semantic_density": 0,
        "word_count": 10,
        "unique_words": 10,
        "lexical_diversity": 1.0
      },
      "preservation_score": 3.406191729551069e-05
    },
    {
      "id": 118,
      "text": "Após fuder muito por uma fuga interminável por alguém semelhante ao amor vivido, eu não sentia tanta necessidade de fuder sem ter sentimento, eu não sei explicar, eu sei que é necessário sentir e ter para eu ter relação sexual com uma mulher, logo, eu sempre coloco dificuldades em ter relacionamento com alguém, não fazia isso sabendo, e sim, por ter sentimentos incubados sem querer enfrentar e encarar os fatos. Com esse pensamento de posse extremista de um sonho vivido e “perdido”, era difícil eu perceber o quão mal eu fiz para outras mulheres, não conseguindo ver o valor do amor real que outras estavam me proporcionando e não estavam sendo retribuídas, peço desculpas pelos meus atos e espero que todas estejam felizes e amadas consigo mesmo. Por um caso do acaso do destino, eu não lembrava a última vez que eu tinha feito sexo, fui tirar umas férias após 18 anos sem férias só trabalhando, bebendo e fudendo, as vezes era acordado por um irmão me olhando de cima para baixo... Dei carona d",
      "position": 26295,
      "chapter": 4,
      "page": 63,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.416,
      "complexity_metrics": {
        "word_count": 175,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 43.75,
        "avg_word_length": 4.72,
        "unique_word_ratio": 0.7028571428571428,
        "avg_paragraph_length": 175.0,
        "punctuation_density": 0.11428571428571428,
        "line_break_count": 0,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "após",
          "fuder",
          "alguém",
          "amor",
          "vivido",
          "outras",
          "estavam",
          "férias",
          "muito",
          "fuga",
          "interminável",
          "semelhante",
          "sentia",
          "tanta",
          "necessidade",
          "sentimento",
          "explicar",
          "necessário",
          "sentir",
          "relação"
        ],
        "entities": [
          [
            "Após",
            "PERSON"
          ],
          [
            "muito",
            "PERSON"
          ],
          [
            "eu não sentia",
            "PERSON"
          ],
          [
            "eu não",
            "PERSON"
          ],
          [
            "eu",
            "PERSON"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "para eu",
            "PERSON"
          ],
          [
            "eu sempre",
            "PERSON"
          ],
          [
            "querer enfrentar",
            "PERSON"
          ],
          [
            "era difícil eu perceber o quão",
            "ORG"
          ]
        ],
        "readability_score": 76.709,
        "semantic_density": 0,
        "word_count": 175,
        "unique_words": 123,
        "lexical_diversity": 0.7028571428571428
      },
      "preservation_score": 0.0
    },
    {
      "id": 119,
      "text": "e minas para o Rio a uma menina linda e simpática de um sorriso cativante e impossível de ser esquecido, essa mesma menina veio ser minha namorada e não sei dizer o quanto ela foi importante para a minha vida, sei dizer que tivemos momentos com lembranças impagáveis e uma dessas foi em um banheiro de motel, nós dois estávamos em processo de fusão e a água que tocava evaporava de tão quente que estava o atrito, nesse atrito não sei de onde me surgiu uma força para fuder que me senti o Goku elevando o QI, levantei ela com meus dois braços e a colei na parede do banheiro, e a fudi com a minha rola batendo meio dia em ponto e ela vindo de cima para baixo, por incrível que isso pareça, nesse momento percebi a importância da academia, foi a melhor forma que usei meus 15 anos de academia, nada poderia superar a mistura carnal e a selvageria de uma foda com sentimento.\\n\\n",
      "position": 27295,
      "chapter": 4,
      "page": 64,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 38.27951807228916,
      "complexity_metrics": {
        "word_count": 166,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 166.0,
        "avg_word_length": 4.265060240963855,
        "unique_word_ratio": 0.6144578313253012,
        "avg_paragraph_length": 166.0,
        "punctuation_density": 0.06626506024096386,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "minha",
          "menina",
          "dizer",
          "banheiro",
          "dois",
          "atrito",
          "nesse",
          "meus",
          "academia",
          "minas",
          "linda",
          "simpática",
          "sorriso",
          "cativante",
          "impossível",
          "esquecido",
          "essa",
          "mesma",
          "veio",
          "namorada"
        ],
        "entities": [
          [
            "linda e simpática de",
            "PERSON"
          ],
          [
            "essa mesma",
            "ORG"
          ],
          [
            "menina veio ser minha namorada",
            "PERSON"
          ],
          [
            "não sei dizer o",
            "ORG"
          ],
          [
            "quanto ela",
            "PERSON"
          ],
          [
            "importante para",
            "PERSON"
          ],
          [
            "sei dizer",
            "ORG"
          ],
          [
            "tivemos momentos",
            "ORG"
          ],
          [
            "processo de fusão",
            "ORG"
          ],
          [
            "evaporava de tão",
            "ORG"
          ]
        ],
        "readability_score": 15.72048192771085,
        "semantic_density": 0,
        "word_count": 166,
        "unique_words": 102,
        "lexical_diversity": 0.6144578313253012
      },
      "preservation_score": 7.493621805012353e-05
    },
    {
      "id": 120,
      "text": "Transar –  Muitas vezes o transar é uma fuga da falta de fuder... transar não tem amor, transar é só para passar o tempo é gostoso fazer e é de graça, desde uma rapidinha ou aquela devagarinho sem muita emoção, com emoção suficiente para gozar e ser feliz, muitas vezes procuramos uma transa e nós enrolamos e é esse tipo de história que todos querem ler. Bêbado, cheio de tesão, com dinheiro na carteira e sem ninguém para transar fui a procura onde o cheiro lembra um caminhão de sexo que deixou um rastro de chorume, fui parar onde as escadas são becos intermináveis e muito fáceis de se perder, lembrando as escadas da cena de Harry Potter no castelo de Hogwarts, aqueles que são héteros e moram no Rio de Janeiro, qualquer dia estamos aí na vila mimosa, se não for, têm curiosidade em conhecer. Subi para um quarto com uma cama de solteiro feita de pedra com um colchão que pela espessura, deveria ter sido feito pelo mesmo material que estava sobre, assim coloquei aquela bunda (não encontrei n",
      "position": 28170,
      "chapter": 4,
      "page": 65,
      "segment_type": "preserved_segment",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 36.357458563535914,
      "complexity_metrics": {
        "word_count": 181,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 45.25,
        "avg_word_length": 4.524861878453039,
        "unique_word_ratio": 0.6961325966850829,
        "avg_paragraph_length": 181.0,
        "punctuation_density": 0.10497237569060773,
        "line_break_count": 0,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "transar",
          "muitas",
          "vezes",
          "aquela",
          "emoção",
          "onde",
          "escadas",
          "fuga",
          "falta",
          "fuder",
          "amor",
          "passar",
          "tempo",
          "gostoso",
          "fazer",
          "graça",
          "desde",
          "rapidinha",
          "devagarinho",
          "muita"
        ],
        "entities": [
          [
            "Muitas",
            "PERSON"
          ],
          [
            "sem muita",
            "PERSON"
          ],
          [
            "de história",
            "ORG"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "querem",
            "PERSON"
          ],
          [
            "Bêbado",
            "ORG"
          ],
          [
            "caminhão de sexo que",
            "PERSON"
          ],
          [
            "de se perder",
            "PERSON"
          ],
          [
            "Harry Potter",
            "PERSON"
          ],
          [
            "castelo de Hogwarts",
            "PERSON"
          ]
        ],
        "readability_score": 76.01754143646409,
        "semantic_density": 0,
        "word_count": 181,
        "unique_words": 126,
        "lexical_diversity": 0.6961325966850829
      },
      "preservation_score": 0.0
    },
    {
      "id": 121,
      "text": "enhuma mulher que tivesse algum encanto melhor que esse) para o alto e comecei a transar em movimentos repetitivos sem muita empolgação, só fazendo o meu trabalho e ela o dela, após meia hora gozei!!! Estou percebendo que o meu padrão de primeira foda boa, dura meia hora.\\n\\n",
      "position": 29170,
      "chapter": 4,
      "page": 66,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 28.40625,
      "complexity_metrics": {
        "word_count": 48,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 24.0,
        "avg_word_length": 4.6875,
        "unique_word_ratio": 0.8333333333333334,
        "avg_paragraph_length": 48.0,
        "punctuation_density": 0.14583333333333334,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "meia",
          "hora",
          "enhuma",
          "mulher",
          "tivesse",
          "algum",
          "encanto",
          "melhor",
          "esse",
          "alto",
          "comecei",
          "transar",
          "movimentos",
          "repetitivos",
          "muita",
          "empolgação",
          "fazendo",
          "trabalho",
          "dela",
          "após"
        ],
        "entities": [
          [
            "para o alto e comecei",
            "PERSON"
          ],
          [
            "dela",
            "GPE"
          ],
          [
            "após meia",
            "PERSON"
          ],
          [
            "hora",
            "NORP"
          ],
          [
            "meia hora",
            "PERSON"
          ]
        ],
        "readability_score": 86.59375,
        "semantic_density": 0,
        "word_count": 48,
        "unique_words": 40,
        "lexical_diversity": 0.8333333333333334
      },
      "preservation_score": 5.449906767281711e-05
    },
    {
      "id": 122,
      "text": "Após eu gozar, ela perguntou se eu queria continuar pois paguei para transar com ela durante 1 hora e nos restava tempo.\\n\\n",
      "position": 29444,
      "chapter": 4,
      "page": 67,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 27.35,
      "complexity_metrics": {
        "word_count": 22,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 22.0,
        "avg_word_length": 4.5,
        "unique_word_ratio": 0.9090909090909091,
        "avg_paragraph_length": 22.0,
        "punctuation_density": 0.09090909090909091,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "após",
          "gozar",
          "perguntou",
          "queria",
          "continuar",
          "pois",
          "paguei",
          "transar",
          "durante",
          "hora",
          "restava",
          "tempo"
        ],
        "entities": [
          [
            "Após eu",
            "PERSON"
          ],
          [
            "ela perguntou se eu queria",
            "PERSON"
          ],
          [
            "paguei para",
            "PERSON"
          ],
          [
            "ela durante",
            "PERSON"
          ],
          [
            "1",
            "CARDINAL"
          ]
        ],
        "readability_score": 87.65,
        "semantic_density": 0,
        "word_count": 22,
        "unique_words": 20,
        "lexical_diversity": 0.9090909090909091
      },
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "id": 123,
      "text": "Sim!\\n\\n",
      "position": 29566,
      "chapter": 4,
      "page": 68,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 16.7,
      "complexity_metrics": {
        "word_count": 1,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 1.0,
        "avg_word_length": 4.0,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 1.0,
        "punctuation_density": 1.0,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [],
        "entities": [
          [
            "Sim",
            "PERSON"
          ]
        ],
        "readability_score": 98.3,
        "semantic_density": 0,
        "word_count": 1,
        "unique_words": 1,
        "lexical_diversity": 1.0
      },
      "preservation_score": 6.812383459102139e-06
    },
    {
      "id": 124,
      "text": "Após esse momento, as lembranças foram pausadas por um sono profundo, acordei com um rapaz que arruma os quartos da vila mimosa, enquanto ele estava arrumando os quartos, ele me acordou me confundindo com um mendigo, pois no quarto ao lado dormindo, ele tinha acabado de acordar um. O melhor de tudo foi eu dormir com a carteira ao lado da cama, junto ao meu telefone e lá se permaneceu até eu acordar com o rapaz falando: viu, se fosse em outro lugar você teria sido roubado, depois vão falar que aqui só têm ladrão, tá vendo como as pessoas mentem!!! \\n\\n",
      "position": 29572,
      "chapter": 4,
      "page": 69,
      "segment_type": "preserved_segment",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 36.34257425742574,
      "complexity_metrics": {
        "word_count": 101,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 50.5,
        "avg_word_length": 4.475247524752476,
        "unique_word_ratio": 0.801980198019802,
        "avg_paragraph_length": 101.0,
        "punctuation_density": 0.1485148514851485,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "rapaz",
          "quartos",
          "lado",
          "acordar",
          "após",
          "esse",
          "momento",
          "lembranças",
          "pausadas",
          "sono",
          "profundo",
          "acordei",
          "arruma",
          "vila",
          "mimosa",
          "enquanto",
          "estava",
          "arrumando",
          "acordou",
          "confundindo"
        ],
        "entities": [
          [
            "Após",
            "PERSON"
          ],
          [
            "foram pausadas",
            "PERSON"
          ],
          [
            "enquanto ele estava arrumando",
            "PERSON"
          ],
          [
            "eu",
            "PERSON"
          ],
          [
            "lado da cama",
            "PERSON"
          ],
          [
            "até eu",
            "PERSON"
          ],
          [
            "outro lugar",
            "PERSON"
          ],
          [
            "teria",
            "GPE"
          ]
        ],
        "readability_score": 73.40742574257426,
        "semantic_density": 0,
        "word_count": 101,
        "unique_words": 81,
        "lexical_diversity": 0.801980198019802
      },
      "preservation_score": 0.00010218575188653208
    },
    {
      "id": 125,
      "text": "Saí dê lá emocionado, em êxtase por uma noite louca vivida sem fazer mal a ninguém e lendária pela história, doido para contar para alguém, liguei para o meu irmão.\\n\\n",
      "position": 30127,
      "chapter": 4,
      "page": 70,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 31.35,
      "complexity_metrics": {
        "word_count": 30,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 30.0,
        "avg_word_length": 4.5,
        "unique_word_ratio": 0.9333333333333333,
        "avg_paragraph_length": 30.0,
        "punctuation_density": 0.13333333333333333,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "emocionado",
          "êxtase",
          "noite",
          "louca",
          "vivida",
          "fazer",
          "ninguém",
          "lendária",
          "pela",
          "história",
          "doido",
          "contar",
          "alguém",
          "liguei",
          "irmão"
        ],
        "entities": [
          [
            "fazer",
            "ORG"
          ],
          [
            "pela história",
            "PERSON"
          ],
          [
            "doido",
            "ORG"
          ],
          [
            "para contar",
            "PERSON"
          ],
          [
            "liguei",
            "NORP"
          ]
        ],
        "readability_score": 83.65,
        "semantic_density": 0,
        "word_count": 30,
        "unique_words": 28,
        "lexical_diversity": 0.9333333333333333
      },
      "preservation_score": 2.7249533836408556e-05
    },
    {
      "id": 126,
      "text": "Eu- irmão, você não têm noção onde eu dormir hoje!!!\\n\\n",
      "position": 30293,
      "chapter": 4,
      "page": 71,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 21.29,
      "complexity_metrics": {
        "word_count": 10,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 10.0,
        "avg_word_length": 4.3,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 10.0,
        "punctuation_density": 0.4,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "irmão",
          "você",
          "noção",
          "onde",
          "dormir",
          "hoje"
        ],
        "entities": [
          [
            "eu",
            "PERSON"
          ]
        ],
        "readability_score": 93.71,
        "semantic_density": 0,
        "word_count": 10,
        "unique_words": 10,
        "lexical_diversity": 1.0
      },
      "preservation_score": 3.406191729551069e-05
    },
    {
      "id": 127,
      "text": "Irmão- viado, minha mãe vai te matar estão todos preocupados com você, minha mãe está enchendo o saco de todo mundo por causa de você.\\n\\n",
      "position": 30347,
      "chapter": 4,
      "page": 72,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 28.82,
      "complexity_metrics": {
        "word_count": 25,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 25.0,
        "avg_word_length": 4.4,
        "unique_word_ratio": 0.88,
        "avg_paragraph_length": 25.0,
        "punctuation_density": 0.12,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "minha",
          "você",
          "irmão",
          "viado",
          "matar",
          "estão",
          "todos",
          "preocupados",
          "está",
          "enchendo",
          "saco",
          "todo",
          "mundo",
          "causa"
        ],
        "entities": [
          [
            "saco de",
            "ORG"
          ]
        ],
        "readability_score": 86.18,
        "semantic_density": 0,
        "word_count": 25,
        "unique_words": 22,
        "lexical_diversity": 0.88
      },
      "preservation_score": 2.7249533836408556e-05
    },
    {
      "id": 128,
      "text": "Eu – dormi na VM viado!!!\\n\\n",
      "position": 30483,
      "chapter": 4,
      "page": 73,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 19.0,
      "complexity_metrics": {
        "word_count": 6,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 6.0,
        "avg_word_length": 3.3333333333333335,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 6.0,
        "punctuation_density": 0.5,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "dormi",
          "viado"
        ],
        "entities": [],
        "readability_score": 96.0,
        "semantic_density": 0,
        "word_count": 6,
        "unique_words": 6,
        "lexical_diversity": 1.0
      },
      "preservation_score": 2.0437150377306416e-05
    },
    {
      "id": 129,
      "text": "Irmão- caralhooooo, sou teu fã!!!\\n\\n",
      "position": 30510,
      "chapter": 4,
      "page": 74,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 19.240000000000002,
      "complexity_metrics": {
        "word_count": 5,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 5.0,
        "avg_word_length": 5.8,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 5.0,
        "punctuation_density": 0.8,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "irmão",
          "caralhooooo"
        ],
        "entities": [],
        "readability_score": 95.76,
        "semantic_density": 0,
        "word_count": 5,
        "unique_words": 5,
        "lexical_diversity": 1.0
      },
      "preservation_score": 3.406191729551069e-05
    },
    {
      "id": 130,
      "text": "Quem é hetero raiz, sabe a importância de viver uma experiência dessa !!! \\n\\n",
      "position": 30545,
      "chapter": 4,
      "page": 75,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 22.407692307692308,
      "complexity_metrics": {
        "word_count": 13,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 13.0,
        "avg_word_length": 4.6923076923076925,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 13.0,
        "punctuation_density": 0.3076923076923077,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quem",
          "hetero",
          "raiz",
          "sabe",
          "importância",
          "viver",
          "experiência",
          "dessa"
        ],
        "entities": [
          [
            "Quem",
            "GPE"
          ],
          [
            "raiz",
            "GPE"
          ]
        ],
        "readability_score": 92.09230769230768,
        "semantic_density": 0,
        "word_count": 13,
        "unique_words": 13,
        "lexical_diversity": 1.0
      },
      "preservation_score": 2.7249533836408556e-05
    },
    {
      "id": 131,
      "text": "Trepar – aqui é quando nós colocamos em uma imaginação de sermos animais não muito selvagem, tipo assim: quando o pau está ficando mole após gozar e a mulher quase gozando e desesperada para gozar, quando esse desespero bate trepamos iguais a um coelho, cachorro, dois patinhos na lagoa, fingir que não está fazendo nada... Assim podemos ter aquela trepada boa e podemos ter aquela trepada satisfatória, nunca é ruim trepar, até porque, não faz mal, emagrece, melhora a pele, autoestima, amor próprio, autoestima e tudo aquilo que pode se atingir em ter uma boa trepada. Nem sempre precisando gozar para ser bom e sim por muitas vezes ser divertido e engraçado, pois a confiança em ter uma boa trepada é o momento íntimo do trajeto de se tornar uma boa foda, as vezes uma boa trepada é só para instigar ou apimentar aquele momento onde a imaginação precisa ser exaltada para ter uma boa foda!\\n\\n",
      "position": 30621,
      "chapter": 4,
      "page": 76,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.41730769230769,
      "complexity_metrics": {
        "word_count": 156,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 52.0,
        "avg_word_length": 4.7243589743589745,
        "unique_word_ratio": 0.6730769230769231,
        "avg_paragraph_length": 156.0,
        "punctuation_density": 0.1346153846153846,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "trepada",
          "quando",
          "gozar",
          "trepar",
          "imaginação",
          "assim",
          "está",
          "podemos",
          "aquela",
          "autoestima",
          "vezes",
          "momento",
          "foda",
          "aqui",
          "colocamos",
          "sermos",
          "animais",
          "muito",
          "selvagem",
          "tipo"
        ],
        "entities": [
          [
            "quando nós colocamos",
            "ORG"
          ],
          [
            "de sermos",
            "ORG"
          ],
          [
            "muito selvagem",
            "PERSON"
          ],
          [
            "quando",
            "PERSON"
          ],
          [
            "pau está ficando mole após",
            "ORG"
          ],
          [
            "para gozar",
            "PERSON"
          ],
          [
            "quando",
            "PERSON"
          ],
          [
            "aquela trepada boa",
            "PERSON"
          ],
          [
            "aquela trepada satisfatória",
            "ORG"
          ],
          [
            "faz",
            "ORG"
          ]
        ],
        "readability_score": 72.58269230769231,
        "semantic_density": 0,
        "word_count": 156,
        "unique_words": 105,
        "lexical_diversity": 0.6730769230769231
      },
      "preservation_score": 0.00014306005264114492
    },
    {
      "id": 132,
      "text": "Meter –  Se meter fosse só enfiar o pau e esfregar os grandes lábios na buceta ou no ânus, qual é a graça em ter outra pessoa? \\n\\n",
      "position": 31515,
      "chapter": 4,
      "page": 77,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 29.6,
      "complexity_metrics": {
        "word_count": 27,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 27.0,
        "avg_word_length": 3.6666666666666665,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 27.0,
        "punctuation_density": 0.07407407407407407,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "meter",
          "fosse",
          "enfiar",
          "esfregar",
          "grandes",
          "lábios",
          "buceta",
          "ânus",
          "qual",
          "graça",
          "outra",
          "pessoa"
        ],
        "entities": [
          [
            "Meter",
            "PERSON"
          ],
          [
            "Se meter",
            "PERSON"
          ],
          [
            "pau e esfregar",
            "ORG"
          ],
          [
            "outra",
            "NORP"
          ]
        ],
        "readability_score": 85.4,
        "semantic_density": 0,
        "word_count": 27,
        "unique_words": 27,
        "lexical_diversity": 1.0
      },
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "id": 133,
      "text": "Enfia o pênis em uma torta de maçã, deve ser muito bom, fez muito sucesso na década de 90 e para época foi um baita conselho para aqueles que enxergam e respeitam o estilo sexual que cada um possa ter como direcionamento, felicidade, alegria, dor, prazer e qualquer momento que podemos ser e ter um meter lendário, épico e emblemático chegando a nós deixar marcados por uma noite de causar inveja no tesão de urso que metemos igual a um coelho.\\n\\n",
      "position": 31644,
      "chapter": 4,
      "page": 78,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.34814814814815,
      "complexity_metrics": {
        "word_count": 81,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 81.0,
        "avg_word_length": 4.493827160493828,
        "unique_word_ratio": 0.7530864197530864,
        "avg_paragraph_length": 81.0,
        "punctuation_density": 0.09876543209876543,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "muito",
          "enfia",
          "pênis",
          "torta",
          "maçã",
          "deve",
          "sucesso",
          "década",
          "época",
          "baita",
          "conselho",
          "aqueles",
          "enxergam",
          "respeitam",
          "estilo",
          "sexual",
          "cada",
          "possa",
          "como",
          "direcionamento"
        ],
        "entities": [
          [
            "Enfia",
            "PRODUCT"
          ],
          [
            "muito bom",
            "PERSON"
          ],
          [
            "fez muito sucesso",
            "PERSON"
          ],
          [
            "década de 90",
            "ORG"
          ],
          [
            "conselho",
            "NORP"
          ],
          [
            "meter lendário",
            "PERSON"
          ],
          [
            "épico e emblemático chegando",
            "ORG"
          ],
          [
            "uma noite de causar inveja no",
            "ORG"
          ]
        ],
        "readability_score": 58.15185185185185,
        "semantic_density": 0,
        "word_count": 81,
        "unique_words": 61,
        "lexical_diversity": 0.7530864197530864
      },
      "preservation_score": 5.449906767281711e-05
    },
    {
      "id": 134,
      "text": "Meter é calmante de tanto atrito feito em busca da hipertrofia junto a necessidade de se perder gordura, os esforços feitos são intensos para o corpo e a mente que ambos ficam esgotados e saturados de tanta paixão provinda dê uma boa metida.\\n\\n",
      "position": 32090,
      "chapter": 4,
      "page": 79,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.38837209302326,
      "complexity_metrics": {
        "word_count": 43,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 43.0,
        "avg_word_length": 4.627906976744186,
        "unique_word_ratio": 0.9069767441860465,
        "avg_paragraph_length": 43.0,
        "punctuation_density": 0.046511627906976744,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "meter",
          "calmante",
          "tanto",
          "atrito",
          "feito",
          "busca",
          "hipertrofia",
          "junto",
          "necessidade",
          "perder",
          "gordura",
          "esforços",
          "feitos",
          "intensos",
          "corpo",
          "mente",
          "ambos",
          "ficam",
          "esgotados",
          "saturados"
        ],
        "entities": [
          [
            "Meter",
            "PERSON"
          ],
          [
            "de tanto",
            "ORG"
          ],
          [
            "atrito feito",
            "PERSON"
          ],
          [
            "são intensos para",
            "ORG"
          ],
          [
            "provinda",
            "PERSON"
          ]
        ],
        "readability_score": 77.11162790697674,
        "semantic_density": 0,
        "word_count": 43,
        "unique_words": 39,
        "lexical_diversity": 0.9069767441860465
      },
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "id": 135,
      "text": "Brincadeira de fazer criança, como é bom, como é bom, pode ser na cama, no mato, no carro, nas alturas e onde for meter sendo bem gostoso e prazeroso, vá com força e com amor.\\n\\n",
      "position": 32333,
      "chapter": 4,
      "page": 80,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 33.70857142857143,
      "complexity_metrics": {
        "word_count": 35,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 35.0,
        "avg_word_length": 4.0285714285714285,
        "unique_word_ratio": 0.8,
        "avg_paragraph_length": 35.0,
        "punctuation_density": 0.22857142857142856,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "como",
          "brincadeira",
          "fazer",
          "criança",
          "pode",
          "cama",
          "mato",
          "carro",
          "alturas",
          "onde",
          "meter",
          "sendo",
          "gostoso",
          "prazeroso",
          "força",
          "amor"
        ],
        "entities": [
          [
            "Brincadeira de fazer",
            "PERSON"
          ]
        ],
        "readability_score": 81.29142857142857,
        "semantic_density": 0,
        "word_count": 35,
        "unique_words": 28,
        "lexical_diversity": 0.8
      },
      "preservation_score": 5.449906767281711e-05
    },
    {
      "id": 136,
      "text": "Isso me faz lembrar da primeira e única vez em que eu fui em motel com piscina aquecida e teto elétrico, me senti playboy! \\n\\n",
      "position": 32510,
      "chapter": 4,
      "page": 81,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 28.2375,
      "complexity_metrics": {
        "word_count": 24,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 24.0,
        "avg_word_length": 4.125,
        "unique_word_ratio": 0.875,
        "avg_paragraph_length": 24.0,
        "punctuation_density": 0.08333333333333333,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "isso",
          "lembrar",
          "primeira",
          "única",
          "motel",
          "piscina",
          "aquecida",
          "teto",
          "elétrico",
          "senti",
          "playboy"
        ],
        "entities": [
          [
            "faz",
            "ORG"
          ],
          [
            "lembrar da primeira",
            "PERSON"
          ],
          [
            "eu fui",
            "PERSON"
          ],
          [
            "piscina aquecida",
            "ORG"
          ],
          [
            "elétrico",
            "ORG"
          ]
        ],
        "readability_score": 86.7625,
        "semantic_density": 0,
        "word_count": 24,
        "unique_words": 21,
        "lexical_diversity": 0.875
      },
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "id": 137,
      "text": "Os homens provém de serem Homem, Alfa, Líder, Macho, Leão quê come todas as leoas e é o fodão, pica da galáxia, sinistro, o cara, até porque, esse sentimento machista e arcaico proveio de ser o Homem da casa, obrigação de sustentar a família, família acima de tudo, minha mulher é minha vida, logo, não podemos generalizar o sentimento machista como sendo totalmente ruim, pois vejo que muitos homens que souberam herdar esse sentir e adaptar para o viver nos dias atuais, esses são os melhores filhos, melhores maridos e melhores pais. Voltemos ao meter no motel com piscina aquecida e teto elétrico com a mulher que me fez pensar em desistir de tudo... estávamos nesse paraíso sexual com muita vontade de meter por não meter a muito tempo, não por falta de vontade e amor, e sim, por não entender e compreender as dores, traumas, excesso de amor, fome, família e tudo que provém da vida quando se ama e quer o melhor sem saber o que é melhor para o outro, porém o tesão estava tão grande e o amor f",
      "position": 32635,
      "chapter": 4,
      "page": 82,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.34098360655737,
      "complexity_metrics": {
        "word_count": 183,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 61.0,
        "avg_word_length": 4.469945355191257,
        "unique_word_ratio": 0.6721311475409836,
        "avg_paragraph_length": 183.0,
        "punctuation_density": 0.15846994535519127,
        "line_break_count": 0,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "família",
          "tudo",
          "melhores",
          "meter",
          "amor",
          "homens",
          "provém",
          "homem",
          "esse",
          "sentimento",
          "machista",
          "minha",
          "mulher",
          "vida",
          "vontade",
          "melhor",
          "serem",
          "alfa",
          "líder",
          "macho"
        ],
        "entities": [
          [
            "Alfa",
            "PERSON"
          ],
          [
            "pica da galáxia",
            "PERSON"
          ],
          [
            "arcaico proveio de ser",
            "ORG"
          ],
          [
            "obrigação de sustentar",
            "ORG"
          ],
          [
            "família acima de tudo",
            "ORG"
          ],
          [
            "não podemos generalizar o",
            "ORG"
          ],
          [
            "vejo",
            "GPE"
          ],
          [
            "souberam herdar",
            "PERSON"
          ],
          [
            "Voltemos",
            "ORG"
          ],
          [
            "piscina aquecida",
            "ORG"
          ]
        ],
        "readability_score": 68.15901639344263,
        "semantic_density": 0,
        "word_count": 183,
        "unique_words": 123,
        "lexical_diversity": 0.6721311475409836
      },
      "preservation_score": 0.0
    },
    {
      "id": 138,
      "text": "oi tão exaltado, que a cada gemida, sentada, socada, toque, puxão de cabelo e tudo que possa vir ser em meter gostoso e ser lembrado como obra prima.\\n\\n",
      "position": 33635,
      "chapter": 4,
      "page": 83,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 30.307142857142857,
      "complexity_metrics": {
        "word_count": 28,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 28.0,
        "avg_word_length": 4.357142857142857,
        "unique_word_ratio": 0.8928571428571429,
        "avg_paragraph_length": 28.0,
        "punctuation_density": 0.21428571428571427,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "exaltado",
          "cada",
          "gemida",
          "sentada",
          "socada",
          "toque",
          "puxão",
          "cabelo",
          "tudo",
          "possa",
          "meter",
          "gostoso",
          "lembrado",
          "como",
          "obra",
          "prima"
        ],
        "entities": [
          [
            "sentada",
            "GPE"
          ]
        ],
        "readability_score": 84.69285714285715,
        "semantic_density": 0,
        "word_count": 28,
        "unique_words": 25,
        "lexical_diversity": 0.8928571428571429
      },
      "preservation_score": 4.087430075461283e-05
    },
    {
      "id": 139,
      "text": "    Amar – Como explicar o que é relativo?\\n\\n",
      "position": 33786,
      "chapter": 4,
      "page": 84,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 20.1625,
      "complexity_metrics": {
        "word_count": 8,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 8.0,
        "avg_word_length": 3.875,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 8.0,
        "punctuation_density": 0.125,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "amar",
          "como",
          "explicar",
          "relativo"
        ],
        "entities": [],
        "readability_score": 94.8375,
        "semantic_density": 0,
        "word_count": 8,
        "unique_words": 8,
        "lexical_diversity": 1.0
      },
      "preservation_score": 6.812383459102139e-06
    },
    {
      "id": 140,
      "text": "Por quais motivos precisamos ler e aprender sobre o amor?\\n\\n",
      "position": 33830,
      "chapter": 4,
      "page": 85,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 21.439999999999998,
      "complexity_metrics": {
        "word_count": 10,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 10.0,
        "avg_word_length": 4.8,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 10.0,
        "punctuation_density": 0.1,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quais",
          "motivos",
          "precisamos",
          "aprender",
          "amor"
        ],
        "entities": [
          [
            "motivos precisamos",
            "PERSON"
          ]
        ],
        "readability_score": 93.56,
        "semantic_density": 0,
        "word_count": 10,
        "unique_words": 10,
        "lexical_diversity": 1.0
      },
      "preservation_score": 6.812383459102139e-06
    },
    {
      "id": 141,
      "text": "Não posso dizer o que eu não sei, porém posso dizer o que eu passei, assim irei tentar me expressar de uma forma que não seja agressiva quando o cutucar quem estiver lendo devagar, prazeroso e com muito amor.\\n\\n",
      "position": 33889,
      "chapter": 4,
      "page": 86,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 35.80769230769231,
      "complexity_metrics": {
        "word_count": 39,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 39.0,
        "avg_word_length": 4.358974358974359,
        "unique_word_ratio": 0.7948717948717948,
        "avg_paragraph_length": 39.0,
        "punctuation_density": 0.10256410256410256,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "posso",
          "dizer",
          "porém",
          "passei",
          "assim",
          "irei",
          "tentar",
          "expressar",
          "forma",
          "seja",
          "agressiva",
          "quando",
          "cutucar",
          "quem",
          "estiver",
          "lendo",
          "devagar",
          "prazeroso",
          "muito",
          "amor"
        ],
        "entities": [
          [
            "posso dizer",
            "ORG"
          ],
          [
            "eu não",
            "PERSON"
          ],
          [
            "porém posso dizer",
            "ORG"
          ],
          [
            "que eu passei",
            "FAC"
          ],
          [
            "agressiva quando",
            "PERSON"
          ],
          [
            "cutucar quem",
            "FAC"
          ],
          [
            "muito amor",
            "PERSON"
          ]
        ],
        "readability_score": 79.1923076923077,
        "semantic_density": 0,
        "word_count": 39,
        "unique_words": 31,
        "lexical_diversity": 0.7948717948717948
      },
      "preservation_score": 2.7249533836408556e-05
    },
    {
      "id": 142,
      "text": "Através dessa entrada amorosa e simpática irei descrever o meu amor no amorzinho gostoso e aconchegante de arrepiar até os cabelos do cu de tanta satisfação que é ter esse momento, sendo lendário pela beleza dê um olhar, tocar, sentir, conectar, confiar e tudo que provém do sentir a empatia no ato de fazer um papai e mamãe, virar de ladinho e só ficar conectado semelhante ao filme Avatar na cena de quando os nativos conecta-se a árvore e fica marolando, divagando e em êxtase por estar conectado igual a um cachorro preso pela vagina e o pênis, assim percebemos que o amor é estar conectado e não afastado daqueles momentos que nós motiva a trabalhar igual a um louco e chegar correndo em casa para ficar mais tempo com aqueles que são os nossos motivos de não gemer e sim sussurrar, não gritar e sim ficar ofegante para não incomodar aqueles que vieram de uma manhã, tarde ou noite de muito amorzinho.\\n\\n",
      "position": 34099,
      "chapter": 4,
      "page": 87,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.369325153374234,
      "complexity_metrics": {
        "word_count": 163,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 163.0,
        "avg_word_length": 4.564417177914111,
        "unique_word_ratio": 0.6809815950920245,
        "avg_paragraph_length": 163.0,
        "punctuation_density": 0.06748466257668712,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "ficar",
          "conectado",
          "amor",
          "amorzinho",
          "pela",
          "sentir",
          "igual",
          "aqueles",
          "através",
          "dessa",
          "entrada",
          "amorosa",
          "simpática",
          "irei",
          "descrever",
          "gostoso",
          "aconchegante",
          "arrepiar",
          "cabelos",
          "tanta"
        ],
        "entities": [
          [
            "entrada amorosa",
            "PERSON"
          ],
          [
            "cu de tanta satisfação que",
            "PERSON"
          ],
          [
            "virar de",
            "ORG"
          ],
          [
            "Avatar",
            "PERSON"
          ],
          [
            "cena de quando",
            "ORG"
          ],
          [
            "nativos conecta-se",
            "PERSON"
          ],
          [
            "fica",
            "GPE"
          ],
          [
            "estar",
            "PRODUCT"
          ],
          [
            "vagina e o pênis",
            "ORG"
          ],
          [
            "assim percebemos",
            "PERSON"
          ]
        ],
        "readability_score": 17.130674846625766,
        "semantic_density": 0,
        "word_count": 163,
        "unique_words": 111,
        "lexical_diversity": 0.6809815950920245
      },
      "preservation_score": 8.174860150922567e-05
    },
    {
      "id": 143,
      "text": "O amor nem sempre precisa ter o ato sexual, as vezes só precisamos de uma companhia para dormir de conchinha e abraçados, semelhantes a estarmos no ventre de nossa mãe ou encostado só para ter certeza que tem alguém ali e se sentir seguro por sentir a confiança no tocar, acariciar, beijar, chupar até amolecer e relaxar o corpo daquele que está recebendo.\\n\\n",
      "position": 35007,
      "chapter": 4,
      "page": 88,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.4,
      "complexity_metrics": {
        "word_count": 63,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 63.0,
        "avg_word_length": 4.666666666666667,
        "unique_word_ratio": 0.8095238095238095,
        "avg_paragraph_length": 63.0,
        "punctuation_density": 0.09523809523809523,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "sentir",
          "amor",
          "sempre",
          "precisa",
          "sexual",
          "vezes",
          "precisamos",
          "companhia",
          "dormir",
          "conchinha",
          "abraçados",
          "semelhantes",
          "estarmos",
          "ventre",
          "nossa",
          "encostado",
          "certeza",
          "alguém",
          "seguro",
          "confiança"
        ],
        "entities": [
          [
            "nem sempre",
            "PERSON"
          ],
          [
            "para dormir de conchinha",
            "PERSON"
          ],
          [
            "beijar",
            "ORG"
          ],
          [
            "chupar até",
            "ORG"
          ]
        ],
        "readability_score": 67.1,
        "semantic_density": 0,
        "word_count": 63,
        "unique_words": 51,
        "lexical_diversity": 0.8095238095238095
      },
      "preservation_score": 4.087430075461283e-05
    },
    {
      "id": 144,
      "text": "Todos tem uma forma de entender e perceber o amorzinho recebido ou dado e os meus sentidos ficam mais aguçados ao fumar um baseado, sinto meu pênis entrando, ficando quentinho, todo babado e gozado de “pirapoca ao cuí” de tão gostoso e molhado que todos ficam ao fazer Amor.\\n\\n",
      "position": 35365,
      "chapter": 4,
      "page": 89,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.38367346938776,
      "complexity_metrics": {
        "word_count": 49,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 49.0,
        "avg_word_length": 4.612244897959184,
        "unique_word_ratio": 0.8367346938775511,
        "avg_paragraph_length": 49.0,
        "punctuation_density": 0.08163265306122448,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "todos",
          "ficam",
          "forma",
          "entender",
          "perceber",
          "amorzinho",
          "recebido",
          "dado",
          "meus",
          "sentidos",
          "mais",
          "aguçados",
          "fumar",
          "baseado",
          "sinto",
          "pênis",
          "entrando",
          "ficando",
          "quentinho",
          "todo"
        ],
        "entities": [
          [
            "baseado",
            "GPE"
          ],
          [
            "gozado de “pirapoca ao cuí” de tão",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "Amor",
            "ORG"
          ]
        ],
        "readability_score": 74.11632653061224,
        "semantic_density": 0,
        "word_count": 49,
        "unique_words": 41,
        "lexical_diversity": 0.8367346938775511
      },
      "preservation_score": 4.087430075461283e-05
    },
    {
      "id": 145,
      "text": "Fetiches –  Podemos fazer de tudo e ser tudo no sexo, fuder, transar, trepar, meter e amorzinho só precisamos ter imaginação, confiança, respeito e se vier com amor será melhor ainda. \\n\\n",
      "position": 35641,
      "chapter": 4,
      "page": 90,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 31.970967741935485,
      "complexity_metrics": {
        "word_count": 31,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 31.0,
        "avg_word_length": 4.903225806451613,
        "unique_word_ratio": 0.9032258064516129,
        "avg_paragraph_length": 31.0,
        "punctuation_density": 0.22580645161290322,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "tudo",
          "fetiches",
          "podemos",
          "fazer",
          "sexo",
          "fuder",
          "transar",
          "trepar",
          "meter",
          "amorzinho",
          "precisamos",
          "imaginação",
          "confiança",
          "respeito",
          "vier",
          "amor",
          "será",
          "melhor",
          "ainda"
        ],
        "entities": [
          [
            "Podemos",
            "ORG"
          ],
          [
            "confiança",
            "GPE"
          ],
          [
            "respeito",
            "GPE"
          ],
          [
            "amor será melhor ainda",
            "ORG"
          ]
        ],
        "readability_score": 83.02903225806452,
        "semantic_density": 0,
        "word_count": 31,
        "unique_words": 28,
        "lexical_diversity": 0.9032258064516129
      },
      "preservation_score": 4.768668421371498e-05
    },
    {
      "id": 146,
      "text": "Essa imaginação fértil, penetrante e molhada é um tsunami de aventuras e histórias épicas de serem contadas com orgulho para aqueles amigos que gostam de uma boa história “cultivante”, encaixada a lei da “semenadura” que me leva a pensar em quantas ideias criativas podem salvar um casamento, namoro, peguete, crush, pau amigo e todos os momentos que podemos ser feliz e triste, agressivo e carinhoso, carente e muito próximo, amado e odiado em momentos necessário ser sem perceber que está acontecendo, assim, os nossos fetiches não é algo totalmente planejado do nada, até porque, o nada é alguma coisa, e essa coisa, é relativa a o que queres ser e ao que podes ter sabendo agregar, adaptar e evoluir aquela imaginação prazerosa sem afetar o combinado faça, goze e sinta o prazer da adrenalina junto ao prazer sexual.\\n\\n",
      "position": 35827,
      "chapter": 4,
      "page": 91,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.48478260869565,
      "complexity_metrics": {
        "word_count": 138,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 138.0,
        "avg_word_length": 4.949275362318841,
        "unique_word_ratio": 0.7318840579710145,
        "avg_paragraph_length": 138.0,
        "punctuation_density": 0.13043478260869565,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "essa",
          "imaginação",
          "momentos",
          "nada",
          "coisa",
          "prazer",
          "fértil",
          "penetrante",
          "molhada",
          "tsunami",
          "aventuras",
          "histórias",
          "épicas",
          "serem",
          "contadas",
          "orgulho",
          "aqueles",
          "amigos",
          "gostam",
          "história"
        ],
        "entities": [
          [
            "Essa",
            "ORG"
          ],
          [
            "orgulho",
            "GPE"
          ],
          [
            "que gostam de uma boa história",
            "PERSON"
          ],
          [
            "encaixada",
            "ORG"
          ],
          [
            "casamento",
            "GPE"
          ],
          [
            "pau",
            "ORG"
          ],
          [
            "momentos que podemos ser",
            "ORG"
          ],
          [
            "muito próximo",
            "PERSON"
          ],
          [
            "nada",
            "ORG"
          ],
          [
            "nada",
            "ORG"
          ]
        ],
        "readability_score": 29.515217391304347,
        "semantic_density": 0,
        "word_count": 138,
        "unique_words": 101,
        "lexical_diversity": 0.7318840579710145
      },
      "preservation_score": 0.00014987243610024706
    },
    {
      "id": 147,
      "text": "Senti tanto tédio em fazer o mesmo padrão sexual que o fetiche tornou-se padrão. Não precisamos imaginar coisas absurdas ou coisas muito loucas, até porque, a loucura é relativa para quem está vivendo de qual lado está tomando, enfiando ou chupando um pirulito colorido com baba de moça e fios de ovos bem docinho e gostoso de saborear, as vezes ocorre um incomodo com os fios soltos são esses que nós faz engasgar e fazendo dar uma pequena pausa para tirar o incomodo que fica na ponta da língua, na maioria das vezes não nós importamos por estar muito gostoso e ficamos lambuzados dos cabelos da churreia aos cabelos da cabeça. \\n\\n",
      "position": 36649,
      "chapter": 4,
      "page": 92,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.4027027027027,
      "complexity_metrics": {
        "word_count": 111,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 55.5,
        "avg_word_length": 4.675675675675675,
        "unique_word_ratio": 0.7657657657657657,
        "avg_paragraph_length": 111.0,
        "punctuation_density": 0.06306306306306306,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "padrão",
          "coisas",
          "muito",
          "está",
          "fios",
          "gostoso",
          "vezes",
          "incomodo",
          "cabelos",
          "senti",
          "tanto",
          "tédio",
          "fazer",
          "mesmo",
          "sexual",
          "fetiche",
          "tornou",
          "precisamos",
          "imaginar",
          "absurdas"
        ],
        "entities": [
          [
            "mesmo padrão",
            "PERSON"
          ],
          [
            "muito loucas",
            "PERSON"
          ],
          [
            "relativa",
            "ORG"
          ],
          [
            "baba de moça",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "fazendo dar uma pequena pausa para tirar o incomodo que fica",
            "ORG"
          ],
          [
            "não nós importamos por estar muito",
            "ORG"
          ]
        ],
        "readability_score": 70.8472972972973,
        "semantic_density": 0,
        "word_count": 111,
        "unique_words": 85,
        "lexical_diversity": 0.7657657657657657
      },
      "preservation_score": 5.449906767281711e-05
    },
    {
      "id": 148,
      "text": "Uma pegada seguida com um olhar pode ser a abertura para um lindo dia em ter fetiche em um carro ou em uma mata, sei lá, sendo fora dê um padrão e hábito tudo pode ser fetiche e o dirigir carro automático a facilidade vira motivo de se transar e o não fazer muito barulho para não acordar às crianças é importante essa prevenção se por acaso forem pegos no flagrante, diga que a mamãe está cansada e ela precisava deitar para descansar.\\n\\n",
      "position": 37281,
      "chapter": 4,
      "page": 93,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.27951807228916,
      "complexity_metrics": {
        "word_count": 83,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 83.0,
        "avg_word_length": 4.265060240963855,
        "unique_word_ratio": 0.7710843373493976,
        "avg_paragraph_length": 83.0,
        "punctuation_density": 0.04819277108433735,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "pode",
          "fetiche",
          "carro",
          "pegada",
          "seguida",
          "olhar",
          "abertura",
          "lindo",
          "mata",
          "sendo",
          "fora",
          "padrão",
          "hábito",
          "tudo",
          "dirigir",
          "automático",
          "facilidade",
          "vira",
          "motivo",
          "transar"
        ],
        "entities": [
          [
            "Uma",
            "GPE"
          ],
          [
            "abertura",
            "GPE"
          ],
          [
            "sendo fora",
            "PERSON"
          ],
          [
            "hábito tudo pode ser fetiche e o",
            "PERSON"
          ],
          [
            "vira motivo de se",
            "PERSON"
          ],
          [
            "muito barulho para não acordar",
            "PERSON"
          ],
          [
            "essa prevenção",
            "FAC"
          ],
          [
            "forem",
            "PERSON"
          ]
        ],
        "readability_score": 57.22048192771084,
        "semantic_density": 0,
        "word_count": 83,
        "unique_words": 64,
        "lexical_diversity": 0.7710843373493976
      },
      "preservation_score": 2.7249533836408556e-05
    },
    {
      "id": 149,
      "text": "Capítulo 4  Histórias do começar em sexo, fuder, transar, trepar, meter e terminar no amor.\\n\\n",
      "position": 37719,
      "chapter": 5,
      "page": 1,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 24.02,
      "complexity_metrics": {
        "word_count": 15,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 15.0,
        "avg_word_length": 5.066666666666666,
        "unique_word_ratio": 1.0,
        "avg_paragraph_length": 15.0,
        "punctuation_density": 0.3333333333333333,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "capítulo",
          "histórias",
          "começar",
          "sexo",
          "fuder",
          "transar",
          "trepar",
          "meter",
          "terminar",
          "amor"
        ],
        "entities": [],
        "readability_score": 90.98,
        "semantic_density": 0,
        "word_count": 15,
        "unique_words": 15,
        "lexical_diversity": 1.0
      },
      "preservation_score": 3.406191729551069e-05
    },
    {
      "id": 150,
      "text": "Esse capítulo é o momento que eu irei escutar e contar os contos sexuais e apimentados do trajeto de maior peso no nosso sentir o amor e a causa dê nossas histerias e nossos maiores prazeres, sendo relativa e interpretativa ao sentir e ver de cada um. \\n\\n",
      "position": 37812,
      "chapter": 5,
      "page": 2,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.308510638297875,
      "complexity_metrics": {
        "word_count": 47,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 47.0,
        "avg_word_length": 4.361702127659575,
        "unique_word_ratio": 0.8297872340425532,
        "avg_paragraph_length": 47.0,
        "punctuation_density": 0.0425531914893617,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "sentir",
          "esse",
          "capítulo",
          "momento",
          "irei",
          "escutar",
          "contar",
          "contos",
          "sexuais",
          "apimentados",
          "trajeto",
          "maior",
          "peso",
          "nosso",
          "amor",
          "causa",
          "nossas",
          "histerias",
          "nossos",
          "maiores"
        ],
        "entities": [
          [
            "que eu irei escutar",
            "PERSON"
          ],
          [
            "sendo relativa e interpretativa",
            "ORG"
          ]
        ],
        "readability_score": 75.19148936170212,
        "semantic_density": 0,
        "word_count": 47,
        "unique_words": 39,
        "lexical_diversity": 0.8297872340425532
      },
      "preservation_score": 1.3624766918204278e-05
    },
    {
      "id": 151,
      "text": "Aqui irei colocar as histórias dos meus amigos, amigas, ambos, gays, heterossexual, pansexual, relacionamento aberto e muitas outras formas que irei descobrir ao decorrer, assim, vejo que é necessário termos outras visões perante ao trajeto de entender e compreender a sua própria forma de amar e ser amado, porém, ninguém nós ensina a sentar, enfiar, chupar, sentir, como apreciar, qual é a forma que eu gosto e muitas outras formas de enxergar o trajeto da vida sexual.\\n\\nQual é a diferença entre amor e amor (sexo)?\\n\\nTodos nós sentimos algo profundo quando deixamos o amor entrar, dentro desse amor, temos várias formas de fuder com os outros ou até mesmo fuder pela adrenalina perigosa em termos fetiches com aqueles que parecem fuder melhor que outros, simplesmente pelo fator de ser alguém que imaginamos ser uma melhor foda que outros pela vida extravagante e com muitas mortes nós faz pensar o quanto deve ser um fodão prazeroso e mesmo quando procuramos esse tipo de situação, acabamos viciados e em fuga, até porque, são tantos problemas rotineiros que não nós deixa termos tempo para pensar nem na solução do mesmo, imagina quando se trata das nossas melhores lembranças e mais marcantes em meio a miséria.\\n\\nVejo que a dificuldade de encontrar um amor verdadeiro não está em amar, e sim, na convivência dê um aceitar o penetrar do outro sem reclamar em uma constância de problemas necessários e motivacionais para a nossa vida, pois sem eles, quais momentos seriam marcantes e importantes? \\n\\nDevido a todos esses questionamentos incoerentes proporcionais ao nosso universo observável e imaginário, tudo dependendo de qual posição. Por muitas vezes essas posições nós faz olhar e falar:\\n\\nGatinha, assim você me assusta, com o seu capô de Fusca!!\\n\\nCabe ou não cabe?",
      "position": 38066,
      "chapter": 5,
      "page": 3,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 37.50921501706485,
      "complexity_metrics": {
        "word_count": 293,
        "sentence_count": 7,
        "paragraph_count": 7,
        "avg_sentence_length": 41.857142857142854,
        "avg_word_length": 5.030716723549488,
        "unique_word_ratio": 0.6621160409556314,
        "avg_paragraph_length": 41.857142857142854,
        "punctuation_density": 0.1296928327645051,
        "line_break_count": 12,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "amor",
          "muitas",
          "outras",
          "formas",
          "termos",
          "qual",
          "vida",
          "quando",
          "fuder",
          "outros",
          "mesmo",
          "irei",
          "assim",
          "vejo",
          "trajeto",
          "forma",
          "amar",
          "todos",
          "pela",
          "melhor"
        ],
        "entities": [
          [
            "amigas",
            "ORG"
          ],
          [
            "ambos",
            "PERSON"
          ],
          [
            "vejo que",
            "GPE"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "forma de amar",
            "PERSON"
          ],
          [
            "nós ensina",
            "ORG"
          ],
          [
            "amor e amor",
            "ORG"
          ],
          [
            "Todos",
            "ORG"
          ],
          [
            "profundo quando deixamos",
            "PERSON"
          ],
          [
            "várias formas de fuder",
            "PERSON"
          ]
        ],
        "readability_score": 77.56221355436372,
        "semantic_density": 0,
        "word_count": 293,
        "unique_words": 194,
        "lexical_diversity": 0.6621160409556314
      },
      "preservation_score": 0.011444804211291593
    }
  ],
  "book_name": "fuder ou nao fuder eis a questão.docx",
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