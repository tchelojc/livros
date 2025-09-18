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
    "total_segments": 152,
    "total_chapters": 7,
    "total_pages": 152,
    "avg_difficulty": 29.673661321842445,
    "max_difficulty": 44.45696721311475,
    "min_difficulty": 21.11875,
    "theme_distribution": {
      "arte": 89.6828752642706,
      "filosofia": 87.1938775510204,
      "ciencia": 63.23683899518076,
      "tecnologia": 39.43377148634985
    },
    "total_words": 30659,
    "avg_words_per_segment": 201.70394736842104,
    "formatting_preservation": 79.90131578947368,
    "preservation_score": 1.9076243959396702e-05,
    "book_name": "miolo_liberdade dentro do caos_17032022.pdf",
    "analysis_timestamp": "2025-09-15T18:54:08",
    "structure_preserved": false
  },
  "theme_analysis": {
    "arte": [
      {
        "segment": 1,
        "score": 100.0,
        "position": 2769,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 13696,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 36226,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 46.51162790697674,
        "position": 37601,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 46514,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 65443,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 79462,
        "chapter": 3
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 98542,
        "chapter": 4
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 103780,
        "chapter": 4
      },
      {
        "segment": 1,
        "score": 40.0,
        "position": 157843,
        "chapter": 6
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 174192,
        "chapter": 6
      }
    ],
    "filosofia": [
      {
        "segment": 1,
        "score": 100.0,
        "position": 11005,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 25690,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 32165,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 59346,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 62135,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 69426,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 70800,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 118877,
        "chapter": 4
      },
      {
        "segment": 1,
        "score": 53.57142857142857,
        "position": 136552,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 53.57142857142857,
        "position": 139287,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 53.57142857142857,
        "position": 143302,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 155251,
        "chapter": 6
      },
      {
        "segment": 1,
        "score": 60.0,
        "position": 157843,
        "chapter": 6
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 165869,
        "chapter": 6
      }
    ],
    "ciencia": [
      {
        "segment": 1,
        "score": 30.232558139534888,
        "position": 37601,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 64206,
        "chapter": 2
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 75616,
        "chapter": 3
      },
      {
        "segment": 1,
        "score": 56.52173913043479,
        "position": 81943,
        "chapter": 3
      },
      {
        "segment": 1,
        "score": 46.42857142857144,
        "position": 136552,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 46.42857142857144,
        "position": 139287,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 46.42857142857144,
        "position": 143302,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 100.0,
        "position": 147200,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 56.52173913043479,
        "position": 148632,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 56.52173913043479,
        "position": 149980,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 56.52173913043479,
        "position": 159161,
        "chapter": 6
      }
    ],
    "tecnologia": [
      {
        "segment": 1,
        "score": 23.25581395348837,
        "position": 37601,
        "chapter": 1
      },
      {
        "segment": 1,
        "score": 43.47826086956522,
        "position": 81943,
        "chapter": 3
      },
      {
        "segment": 1,
        "score": 43.47826086956522,
        "position": 148632,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 43.47826086956522,
        "position": 149980,
        "chapter": 5
      },
      {
        "segment": 1,
        "score": 43.47826086956522,
        "position": 159161,
        "chapter": 6
      }
    ]
  },
  "difficulty_map": [
    {
      "segment": 1,
      "difficulty": 23.025,
      "position": 113,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 12,
      "preservation_score": 1.276986361538898e-07
    },
    {
      "segment": 1,
      "difficulty": 21.25,
      "position": 327,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 8,
      "preservation_score": 0.0
    },
    {
      "segment": 1,
      "difficulty": 21.11875,
      "position": 516,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 16,
      "preservation_score": 3.4052969641037285e-07
    },
    {
      "segment": 1,
      "difficulty": 21.28782201405152,
      "position": 766,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 61,
      "preservation_score": 5.363342718463371e-06
    },
    {
      "segment": 1,
      "difficulty": 33.19731012658228,
      "position": 1304,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 237,
      "preservation_score": 2.6689014956162968e-05
    },
    {
      "segment": 1,
      "difficulty": 36.059288537549406,
      "position": 2769,
      "chapter": 1,
      "main_theme": "arte",
      "word_count": 253,
      "preservation_score": 1.7707544213339386e-05
    },
    {
      "segment": 1,
      "difficulty": 31.5032319391635,
      "position": 4369,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 263,
      "preservation_score": 2.1815183676289504e-05
    },
    {
      "segment": 1,
      "difficulty": 22.21818181818182,
      "position": 5887,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 11,
      "preservation_score": 1.7026484820518643e-07
    },
    {
      "segment": 1,
      "difficulty": 29.244415584415584,
      "position": 6082,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 165,
      "preservation_score": 1.1492877253850082e-05
    },
    {
      "segment": 1,
      "difficulty": 36.36126482213439,
      "position": 7138,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 253,
      "preservation_score": 2.287933897757192e-05
    },
    {
      "segment": 1,
      "difficulty": 31.447421731123388,
      "position": 8672,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 181,
      "preservation_score": 1.8729133302570503e-05
    },
    {
      "segment": 1,
      "difficulty": 28.654742547425474,
      "position": 9806,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 205,
      "preservation_score": 1.6643388912056967e-05
    },
    {
      "segment": 1,
      "difficulty": 35.37211895910781,
      "position": 11005,
      "chapter": 1,
      "main_theme": "filosofia",
      "word_count": 269,
      "preservation_score": 3.039227540462577e-05
    },
    {
      "segment": 1,
      "difficulty": 30.738423645320196,
      "position": 12523,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 203,
      "preservation_score": 1.532383633846678e-05
    },
    {
      "segment": 1,
      "difficulty": 22.414993523316063,
      "position": 13696,
      "chapter": 1,
      "main_theme": "arte",
      "word_count": 193,
      "preservation_score": 1.5323836338466775e-05
    },
    {
      "segment": 1,
      "difficulty": 35.12090592334495,
      "position": 14870,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 246,
      "preservation_score": 2.5454594806675367e-05
    },
    {
      "segment": 1,
      "difficulty": 32.74971927635683,
      "position": 16463,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 229,
      "preservation_score": 2.4475571929495542e-05
    },
    {
      "segment": 1,
      "difficulty": 37.53846153846154,
      "position": 17890,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 195,
      "preservation_score": 1.56430829288515e-05
    },
    {
      "segment": 1,
      "difficulty": 22.305855855855853,
      "position": 19222,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 222,
      "preservation_score": 1.9686873073724673e-05
    },
    {
      "segment": 1,
      "difficulty": 31.55599425699928,
      "position": 20521,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 199,
      "preservation_score": 1.5749498458979744e-05
    },
    {
      "segment": 1,
      "difficulty": 32.91265133171913,
      "position": 21744,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 236,
      "preservation_score": 1.81119232278267e-05
    },
    {
      "segment": 1,
      "difficulty": 25.344956413449566,
      "position": 23164,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 219,
      "preservation_score": 1.591976330718493e-05
    },
    {
      "segment": 1,
      "difficulty": 26.837529550827423,
      "position": 24498,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 188,
      "preservation_score": 1.2769863615388982e-05
    },
    {
      "segment": 1,
      "difficulty": 29.469730941704036,
      "position": 25690,
      "chapter": 1,
      "main_theme": "filosofia",
      "word_count": 223,
      "preservation_score": 2.1964165418469048e-05
    },
    {
      "segment": 1,
      "difficulty": 31.985714285714284,
      "position": 27023,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 175,
      "preservation_score": 1.2940128463594166e-05
    },
    {
      "segment": 1,
      "difficulty": 28.800962000962002,
      "position": 28155,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 189,
      "preservation_score": 1.404684997692788e-05
    },
    {
      "segment": 1,
      "difficulty": 27.56623188405797,
      "position": 29356,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 230,
      "preservation_score": 2.1453370873853485e-05
    },
    {
      "segment": 1,
      "difficulty": 25.7574200913242,
      "position": 30743,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 219,
      "preservation_score": 2.496508336808545e-05
    },
    {
      "segment": 1,
      "difficulty": 31.810843373493977,
      "position": 32165,
      "chapter": 1,
      "main_theme": "filosofia",
      "word_count": 249,
      "preservation_score": 2.6050521775393518e-05
    },
    {
      "segment": 1,
      "difficulty": 22.773958333333333,
      "position": 33636,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 192,
      "preservation_score": 2.553972723077796e-05
    },
    {
      "segment": 1,
      "difficulty": 31.71287726358149,
      "position": 34815,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 213,
      "preservation_score": 2.1538503297956076e-05
    },
    {
      "segment": 1,
      "difficulty": 29.52323717948718,
      "position": 36226,
      "chapter": 1,
      "main_theme": "arte",
      "word_count": 208,
      "preservation_score": 2.7902151999624914e-05
    },
    {
      "segment": 1,
      "difficulty": 39.171756978653534,
      "position": 37601,
      "chapter": 1,
      "main_theme": "arte",
      "word_count": 261,
      "preservation_score": 2.7412640561035012e-05
    },
    {
      "segment": 1,
      "difficulty": 25.885858585858585,
      "position": 39267,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 162,
      "preservation_score": 2.25175261751359e-05
    },
    {
      "segment": 1,
      "difficulty": 27.85192307692308,
      "position": 40384,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 182,
      "preservation_score": 1.4472512097440844e-05
    },
    {
      "segment": 1,
      "difficulty": 22.862175324675327,
      "position": 41596,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 176,
      "preservation_score": 1.941019269539125e-05
    },
    {
      "segment": 1,
      "difficulty": 36.493814432989694,
      "position": 42763,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 194,
      "preservation_score": 1.25144663430812e-05
    },
    {
      "segment": 1,
      "difficulty": 23.160185185185185,
      "position": 44058,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 162,
      "preservation_score": 1.6600822700005675e-05
    },
    {
      "segment": 1,
      "difficulty": 36.7188790560472,
      "position": 45086,
      "chapter": 1,
      "main_theme": "none",
      "word_count": 226,
      "preservation_score": 2.1964165418469048e-05
    },
    {
      "segment": 1,
      "difficulty": 36.05158371040724,
      "position": 46514,
      "chapter": 2,
      "main_theme": "arte",
      "word_count": 221,
      "preservation_score": 2.1453370873853485e-05
    },
    {
      "segment": 1,
      "difficulty": 36.19467787114846,
      "position": 48031,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 238,
      "preservation_score": 2.268779102334109e-05
    },
    {
      "segment": 1,
      "difficulty": 28.188031914893617,
      "position": 49484,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 188,
      "preservation_score": 1.37488864925688e-05
    },
    {
      "segment": 1,
      "difficulty": 26.436008230452675,
      "position": 50664,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 243,
      "preservation_score": 2.298575450770016e-05
    },
    {
      "segment": 1,
      "difficulty": 36.420553359683794,
      "position": 52117,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 253,
      "preservation_score": 2.5028932686162398e-05
    },
    {
      "segment": 1,
      "difficulty": 26.28019863438858,
      "position": 53706,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 179,
      "preservation_score": 1.6175160579492706e-05
    },
    {
      "segment": 1,
      "difficulty": 29.163555555555554,
      "position": 54807,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 225,
      "preservation_score": 2.341141662821313e-05
    },
    {
      "segment": 1,
      "difficulty": 34.89184782608696,
      "position": 56249,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 230,
      "preservation_score": 3.166926176616468e-05
    },
    {
      "segment": 1,
      "difficulty": 35.463461538461544,
      "position": 57726,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 260,
      "preservation_score": 3.6351545091807295e-05
    },
    {
      "segment": 1,
      "difficulty": 37.4685,
      "position": 59346,
      "chapter": 2,
      "main_theme": "filosofia",
      "word_count": 200,
      "preservation_score": 1.7452146941031606e-05
    },
    {
      "segment": 1,
      "difficulty": 27.517184035476717,
      "position": 60657,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 246,
      "preservation_score": 2.1453370873853485e-05
    },
    {
      "segment": 1,
      "difficulty": 25.36619937694704,
      "position": 62135,
      "chapter": 2,
      "main_theme": "filosofia",
      "word_count": 107,
      "preservation_score": 4.6822833256426265e-06
    },
    {
      "segment": 1,
      "difficulty": 28.06095238095238,
      "position": 62886,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 210,
      "preservation_score": 1.7877809061544572e-05
    },
    {
      "segment": 1,
      "difficulty": 23.097413127413127,
      "position": 64206,
      "chapter": 2,
      "main_theme": "ciencia",
      "word_count": 185,
      "preservation_score": 1.8771699514621802e-05
    },
    {
      "segment": 1,
      "difficulty": 44.45696721311475,
      "position": 65443,
      "chapter": 2,
      "main_theme": "arte",
      "word_count": 244,
      "preservation_score": 2.553972723077796e-05
    },
    {
      "segment": 1,
      "difficulty": 27.82977558839628,
      "position": 67007,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 203,
      "preservation_score": 1.638799163974919e-05
    },
    {
      "segment": 1,
      "difficulty": 28.335324675324678,
      "position": 68316,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 165,
      "preservation_score": 1.2344201494876015e-05
    },
    {
      "segment": 1,
      "difficulty": 36.37162162162162,
      "position": 69426,
      "chapter": 2,
      "main_theme": "filosofia",
      "word_count": 222,
      "preservation_score": 1.6856219972313452e-05
    },
    {
      "segment": 1,
      "difficulty": 28.375,
      "position": 70800,
      "chapter": 2,
      "main_theme": "filosofia",
      "word_count": 192,
      "preservation_score": 2.2006731630520344e-05
    },
    {
      "segment": 1,
      "difficulty": 35.8559585492228,
      "position": 72005,
      "chapter": 2,
      "main_theme": "none",
      "word_count": 193,
      "preservation_score": 1.8388603606160132e-05
    },
    {
      "segment": 1,
      "difficulty": 24.494841675178755,
      "position": 73334,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 178,
      "preservation_score": 1.738829762295466e-05
    },
    {
      "segment": 1,
      "difficulty": 26.248026315789474,
      "position": 74477,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 152,
      "preservation_score": 1.743086383500596e-05
    },
    {
      "segment": 1,
      "difficulty": 27.945900755124057,
      "position": 75616,
      "chapter": 3,
      "main_theme": "ciencia",
      "word_count": 206,
      "preservation_score": 2.2006731630520344e-05
    },
    {
      "segment": 1,
      "difficulty": 24.356264705882353,
      "position": 76984,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 200,
      "preservation_score": 2.298575450770016e-05
    },
    {
      "segment": 1,
      "difficulty": 36.6375,
      "position": 78278,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 192,
      "preservation_score": 9.300717333208306e-06
    },
    {
      "segment": 1,
      "difficulty": 32.58799654576856,
      "position": 79462,
      "chapter": 3,
      "main_theme": "arte",
      "word_count": 193,
      "preservation_score": 2.1453370873853485e-05
    },
    {
      "segment": 1,
      "difficulty": 27.42153846153846,
      "position": 80757,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 180,
      "preservation_score": 1.9920987240006808e-05
    },
    {
      "segment": 1,
      "difficulty": 32.539375,
      "position": 81943,
      "chapter": 3,
      "main_theme": "ciencia",
      "word_count": 160,
      "preservation_score": 1.191853937436305e-05
    },
    {
      "segment": 1,
      "difficulty": 27.59304871373837,
      "position": 83056,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 203,
      "preservation_score": 1.9814571709878563e-05
    },
    {
      "segment": 1,
      "difficulty": 23.4167348608838,
      "position": 84277,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 188,
      "preservation_score": 1.1322612405644895e-05
    },
    {
      "segment": 1,
      "difficulty": 26.857692307692307,
      "position": 85442,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 208,
      "preservation_score": 1.5664366034877146e-05
    },
    {
      "segment": 1,
      "difficulty": 26.004974160206718,
      "position": 86758,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 172,
      "preservation_score": 1.6600822700005675e-05
    },
    {
      "segment": 1,
      "difficulty": 28.766867469879518,
      "position": 87892,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 249,
      "preservation_score": 2.1964165418469048e-05
    },
    {
      "segment": 1,
      "difficulty": 25.557065706570658,
      "position": 89368,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 202,
      "preservation_score": 1.702648482051864e-05
    },
    {
      "segment": 1,
      "difficulty": 36.46938405797101,
      "position": 90630,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 207,
      "preservation_score": 1.9580457543596434e-05
    },
    {
      "segment": 1,
      "difficulty": 36.2264400921659,
      "position": 92027,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 248,
      "preservation_score": 2.656131632000908e-05
    },
    {
      "segment": 1,
      "difficulty": 22.950819672131146,
      "position": 93606,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 183,
      "preservation_score": 1.743086383500596e-05
    },
    {
      "segment": 1,
      "difficulty": 24.811303630363035,
      "position": 94808,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 202,
      "preservation_score": 1.653697338192873e-05
    },
    {
      "segment": 1,
      "difficulty": 35.05080213903743,
      "position": 96052,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 187,
      "preservation_score": 1.2769863615388982e-05
    },
    {
      "segment": 1,
      "difficulty": 28.47179487179487,
      "position": 97213,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 207,
      "preservation_score": 1.9665589967699028e-05
    },
    {
      "segment": 1,
      "difficulty": 28.680480480480483,
      "position": 98542,
      "chapter": 4,
      "main_theme": "arte",
      "word_count": 222,
      "preservation_score": 3.0136878132317994e-05
    },
    {
      "segment": 1,
      "difficulty": 27.324242424242424,
      "position": 99934,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 198,
      "preservation_score": 1.4962023536030753e-05
    },
    {
      "segment": 1,
      "difficulty": 28.827403846153846,
      "position": 101142,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 208,
      "preservation_score": 1.966558996769903e-05
    },
    {
      "segment": 1,
      "difficulty": 25.55086726998492,
      "position": 102439,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 221,
      "preservation_score": 2.6433617683855188e-05
    },
    {
      "segment": 1,
      "difficulty": 26.55552608311229,
      "position": 103780,
      "chapter": 4,
      "main_theme": "arte",
      "word_count": 261,
      "preservation_score": 2.1964165418469048e-05
    },
    {
      "segment": 1,
      "difficulty": 27.82333333333333,
      "position": 105366,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 210,
      "preservation_score": 1.4472512097440844e-05
    },
    {
      "segment": 1,
      "difficulty": 24.009590316573558,
      "position": 106601,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 179,
      "preservation_score": 1.8005507697698462e-05
    },
    {
      "segment": 1,
      "difficulty": 24.558835546475997,
      "position": 107762,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 178,
      "preservation_score": 1.3621187856414913e-05
    },
    {
      "segment": 1,
      "difficulty": 28.288655462184874,
      "position": 108914,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 238,
      "preservation_score": 2.0431781784622368e-05
    },
    {
      "segment": 1,
      "difficulty": 36.457499999999996,
      "position": 110347,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 120,
      "preservation_score": 8.045014077695056e-06
    },
    {
      "segment": 1,
      "difficulty": 26.78463855421687,
      "position": 111177,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 166,
      "preservation_score": 1.6090028155390112e-05
    },
    {
      "segment": 1,
      "difficulty": 36.40956937799043,
      "position": 112256,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 209,
      "preservation_score": 2.1070274965391818e-05
    },
    {
      "segment": 1,
      "difficulty": 35.866312056737584,
      "position": 113579,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 235,
      "preservation_score": 1.9920987240006808e-05
    },
    {
      "segment": 1,
      "difficulty": 36.250510204081635,
      "position": 114956,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 196,
      "preservation_score": 1.3855302022697046e-05
    },
    {
      "segment": 1,
      "difficulty": 31.011264822134386,
      "position": 116150,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 253,
      "preservation_score": 2.6561316320009078e-05
    },
    {
      "segment": 1,
      "difficulty": 38.44262295081967,
      "position": 117684,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 183,
      "preservation_score": 1.7367014516929012e-05
    },
    {
      "segment": 1,
      "difficulty": 38.5280701754386,
      "position": 118877,
      "chapter": 4,
      "main_theme": "filosofia",
      "word_count": 171,
      "preservation_score": 1.225906907077342e-05
    },
    {
      "segment": 1,
      "difficulty": 29.395192307692305,
      "position": 120052,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 208,
      "preservation_score": 1.591976330718493e-05
    },
    {
      "segment": 1,
      "difficulty": 29.19768115942029,
      "position": 121314,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 230,
      "preservation_score": 1.8899398150775692e-05
    },
    {
      "segment": 1,
      "difficulty": 32.143432203389835,
      "position": 122724,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 236,
      "preservation_score": 2.298575450770016e-05
    },
    {
      "segment": 1,
      "difficulty": 30.7125,
      "position": 124142,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 213,
      "preservation_score": 2.5284329958470185e-05
    },
    {
      "segment": 1,
      "difficulty": 24.752548543689322,
      "position": 125483,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 206,
      "preservation_score": 2.400734359693128e-05
    },
    {
      "segment": 1,
      "difficulty": 39.88260869565217,
      "position": 126724,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 184,
      "preservation_score": 1.7132900350646876e-05
    },
    {
      "segment": 1,
      "difficulty": 44.35537848605578,
      "position": 127890,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 251,
      "preservation_score": 2.4475571929495542e-05
    },
    {
      "segment": 1,
      "difficulty": 36.29871794871795,
      "position": 129413,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 234,
      "preservation_score": 2.7072110864624638e-05
    },
    {
      "segment": 1,
      "difficulty": 35.87307692307692,
      "position": 130795,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 234,
      "preservation_score": 2.553972723077796e-05
    },
    {
      "segment": 1,
      "difficulty": 31.064560862865946,
      "position": 132237,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 236,
      "preservation_score": 2.553972723077796e-05
    },
    {
      "segment": 1,
      "difficulty": 30.609905660377358,
      "position": 133708,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 212,
      "preservation_score": 2.553972723077796e-05
    },
    {
      "segment": 1,
      "difficulty": 23.893697478991598,
      "position": 135014,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 252,
      "preservation_score": 3.456376418565284e-05
    },
    {
      "segment": 1,
      "difficulty": 24.018410462776657,
      "position": 136552,
      "chapter": 5,
      "main_theme": "filosofia",
      "word_count": 213,
      "preservation_score": 2.1070274965391818e-05
    },
    {
      "segment": 1,
      "difficulty": 26.06297435897436,
      "position": 137900,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 225,
      "preservation_score": 3.115846722154911e-05
    },
    {
      "segment": 1,
      "difficulty": 31.111858974358974,
      "position": 139287,
      "chapter": 5,
      "main_theme": "filosofia",
      "word_count": 234,
      "preservation_score": 1.9920987240006808e-05
    },
    {
      "segment": 1,
      "difficulty": 23.727905073649755,
      "position": 140770,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 188,
      "preservation_score": 1.900581368090393e-05
    },
    {
      "segment": 1,
      "difficulty": 28.25508607198748,
      "position": 141982,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 213,
      "preservation_score": 1.7324448304877716e-05
    },
    {
      "segment": 1,
      "difficulty": 30.430574098798395,
      "position": 143302,
      "chapter": 5,
      "main_theme": "filosofia",
      "word_count": 214,
      "preservation_score": 1.617516057949271e-05
    },
    {
      "segment": 1,
      "difficulty": 26.89090909090909,
      "position": 144618,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 209,
      "preservation_score": 3.043484161667707e-05
    },
    {
      "segment": 1,
      "difficulty": 26.33299053887289,
      "position": 145931,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 221,
      "preservation_score": 2.0431781784622368e-05
    },
    {
      "segment": 1,
      "difficulty": 26.83896103896104,
      "position": 147200,
      "chapter": 5,
      "main_theme": "ciencia",
      "word_count": 231,
      "preservation_score": 2.553972723077796e-05
    },
    {
      "segment": 1,
      "difficulty": 32.73714454976303,
      "position": 148632,
      "chapter": 5,
      "main_theme": "ciencia",
      "word_count": 211,
      "preservation_score": 1.9197361635134767e-05
    },
    {
      "segment": 1,
      "difficulty": 36.385999999999996,
      "position": 149980,
      "chapter": 5,
      "main_theme": "ciencia",
      "word_count": 200,
      "preservation_score": 1.5749498458979744e-05
    },
    {
      "segment": 1,
      "difficulty": 26.744570135746606,
      "position": 151236,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 221,
      "preservation_score": 1.8963247468852635e-05
    },
    {
      "segment": 1,
      "difficulty": 36.359336099585065,
      "position": 152697,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 241,
      "preservation_score": 1.8601434666416613e-05
    },
    {
      "segment": 1,
      "difficulty": 22.941835357624832,
      "position": 154170,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 171,
      "preservation_score": 1.5664366034877146e-05
    },
    {
      "segment": 1,
      "difficulty": 29.309234411996844,
      "position": 155251,
      "chapter": 6,
      "main_theme": "filosofia",
      "word_count": 181,
      "preservation_score": 1.738829762295466e-05
    },
    {
      "segment": 1,
      "difficulty": 35.335193133047206,
      "position": 156398,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 233,
      "preservation_score": 1.715418345667253e-05
    },
    {
      "segment": 1,
      "difficulty": 25.982337662337663,
      "position": 157843,
      "chapter": 6,
      "main_theme": "filosofia",
      "word_count": 210,
      "preservation_score": 1.615387747346706e-05
    },
    {
      "segment": 1,
      "difficulty": 32.68703007518797,
      "position": 159161,
      "chapter": 6,
      "main_theme": "ciencia",
      "word_count": 228,
      "preservation_score": 2.4475571929495542e-05
    },
    {
      "segment": 1,
      "difficulty": 23.778815302344714,
      "position": 160588,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 187,
      "preservation_score": 1.6090028155390115e-05
    },
    {
      "segment": 1,
      "difficulty": 25.91923076923077,
      "position": 161824,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 208,
      "preservation_score": 2.2474959963084605e-05
    },
    {
      "segment": 1,
      "difficulty": 25.786139421117,
      "position": 163148,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 223,
      "preservation_score": 1.545153497462067e-05
    },
    {
      "segment": 1,
      "difficulty": 34.61974789915966,
      "position": 164479,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 238,
      "preservation_score": 1.6983918608467345e-05
    },
    {
      "segment": 1,
      "difficulty": 35.146950710108605,
      "position": 165869,
      "chapter": 6,
      "main_theme": "filosofia",
      "word_count": 266,
      "preservation_score": 2.5454594806675367e-05
    },
    {
      "segment": 1,
      "difficulty": 30.08875283446712,
      "position": 167487,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 245,
      "preservation_score": 2.0218950724365884e-05
    },
    {
      "segment": 1,
      "difficulty": 26.893457943925235,
      "position": 168982,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 214,
      "preservation_score": 2.324115178000794e-05
    },
    {
      "segment": 1,
      "difficulty": 27.37211111111111,
      "position": 170334,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 200,
      "preservation_score": 1.779267663744198e-05
    },
    {
      "segment": 1,
      "difficulty": 29.223399014778323,
      "position": 171592,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 203,
      "preservation_score": 1.5664366034877146e-05
    },
    {
      "segment": 1,
      "difficulty": 30.7105,
      "position": 172928,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 200,
      "preservation_score": 2.2474959963084605e-05
    },
    {
      "segment": 1,
      "difficulty": 27.849402390438247,
      "position": 174192,
      "chapter": 6,
      "main_theme": "arte",
      "word_count": 251,
      "preservation_score": 2.656131632000908e-05
    },
    {
      "segment": 1,
      "difficulty": 26.985652173913046,
      "position": 175706,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 230,
      "preservation_score": 2.287933897757192e-05
    },
    {
      "segment": 1,
      "difficulty": 31.476055760557607,
      "position": 177213,
      "chapter": 6,
      "main_theme": "none",
      "word_count": 271,
      "preservation_score": 2.643361768385519e-05
    },
    {
      "segment": 1,
      "difficulty": 31.296303501945523,
      "position": 178854,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 257,
      "preservation_score": 2.8157549271932698e-05
    },
    {
      "segment": 1,
      "difficulty": 25.314345991561183,
      "position": 180488,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 158,
      "preservation_score": 1.0854384073080632e-05
    },
    {
      "segment": 1,
      "difficulty": 23.96504854368932,
      "position": 181560,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 206,
      "preservation_score": 2.2006731630520344e-05
    },
    {
      "segment": 1,
      "difficulty": 38.4027027027027,
      "position": 182909,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 259,
      "preservation_score": 2.2474959963084605e-05
    },
    {
      "segment": 1,
      "difficulty": 28.414122533748703,
      "position": 184514,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 214,
      "preservation_score": 2.5454594806675363e-05
    },
    {
      "segment": 1,
      "difficulty": 23.920516717325228,
      "position": 185947,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 235,
      "preservation_score": 2.0942576329237928e-05
    },
    {
      "segment": 1,
      "difficulty": 30.609210526315792,
      "position": 187398,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 228,
      "preservation_score": 2.0112535194237645e-05
    },
    {
      "segment": 1,
      "difficulty": 29.893055555555556,
      "position": 188797,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 216,
      "preservation_score": 2.434787329334166e-05
    },
    {
      "segment": 1,
      "difficulty": 25.608929788684392,
      "position": 190151,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 163,
      "preservation_score": 1.2535749449106848e-05
    },
    {
      "segment": 1,
      "difficulty": 29.950369003690035,
      "position": 191290,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 271,
      "preservation_score": 2.8157549271932698e-05
    },
    {
      "segment": 1,
      "difficulty": 24.121014492753623,
      "position": 192969,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 46,
      "preservation_score": 1.1067215133337116e-06
    },
    {
      "segment": 1,
      "difficulty": 22.381818181818183,
      "position": 193364,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 11,
      "preservation_score": 1.7026484820518643e-07
    },
    {
      "segment": 1,
      "difficulty": 22.93,
      "position": 193567,
      "chapter": 7,
      "main_theme": "none",
      "word_count": 25,
      "preservation_score": 5.959269687181524e-07
    }
  ],
  "segments": [
    {
      "id": 1,
      "text": "Liberdade dentro do caos\\nSem título-1   1Sem título-1   1 17/03/2022   15:08:3417/03/2022   15:08:34",
      "position": 113,
      "chapter": 1,
      "page": 1,
      "segment_type": "page",
      "themes": {},
      "difficulty": 23.025,
      "complexity_metrics": {
        "word_count": 12,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 12.0,
        "avg_word_length": 6.75,
        "unique_word_ratio": 0.9166666666666666,
        "avg_paragraph_length": 12.0,
        "punctuation_density": 0.3333333333333333,
        "line_break_count": 1,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "título",
          "liberdade",
          "dentro",
          "caos"
        ],
        "entities": [
          [
            "Liberdade",
            "GPE"
          ],
          [
            "1Sem",
            "DATE"
          ],
          [
            "1",
            "CARDINAL"
          ],
          [
            "15:08:3417/03/2022",
            "CARDINAL"
          ],
          [
            "15:08:34",
            "PERSON"
          ]
        ],
        "readability_score": 91.975,
        "semantic_density": 0,
        "word_count": 12,
        "unique_words": 11,
        "lexical_diversity": 0.9166666666666666
      },
      "preservation_score": 1.276986361538898e-07
    },
    {
      "id": 1,
      "text": "Sem título-1   2Sem título-1   2 17/03/2022   15:08:3417/03/2022   15:08:34",
      "position": 327,
      "chapter": 1,
      "page": 2,
      "segment_type": "page",
      "themes": {},
      "difficulty": 21.25,
      "complexity_metrics": {
        "word_count": 8,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 8.0,
        "avg_word_length": 7.5,
        "unique_word_ratio": 0.875,
        "avg_paragraph_length": 8.0,
        "punctuation_density": 0.5,
        "line_break_count": 0,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "título"
        ],
        "entities": [
          [
            "2Sem",
            "CARDINAL"
          ],
          [
            "2",
            "CARDINAL"
          ],
          [
            "15:08:3417/03/2022",
            "CARDINAL"
          ],
          [
            "15:08:34",
            "PERSON"
          ]
        ],
        "readability_score": 93.75,
        "semantic_density": 0,
        "word_count": 8,
        "unique_words": 7,
        "lexical_diversity": 0.875
      },
      "preservation_score": 0.0
    },
    {
      "id": 1,
      "text": "Barcelona, 2022Marcelo J. Catharino\\nLiberdade dentro do caos\\nSem título-1   3Sem título-1   3 17/03/2022   15:08:3417/03/2022   15:08:34",
      "position": 516,
      "chapter": 1,
      "page": 3,
      "segment_type": "page",
      "themes": {},
      "difficulty": 21.11875,
      "complexity_metrics": {
        "word_count": 16,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 8.0,
        "avg_word_length": 7.0625,
        "unique_word_ratio": 0.9375,
        "avg_paragraph_length": 16.0,
        "punctuation_density": 0.375,
        "line_break_count": 2,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "título",
          "barcelona",
          "catharino",
          "liberdade",
          "dentro",
          "caos"
        ],
        "entities": [
          [
            "Barcelona",
            "GPE"
          ],
          [
            "2022Marcelo",
            "CARDINAL"
          ],
          [
            "3Sem",
            "CARDINAL"
          ],
          [
            "3",
            "CARDINAL"
          ],
          [
            "15:08:3417/03/2022",
            "CARDINAL"
          ],
          [
            "15:08:34",
            "PERSON"
          ]
        ],
        "readability_score": 93.88125,
        "semantic_density": 0,
        "word_count": 16,
        "unique_words": 15,
        "lexical_diversity": 0.9375
      },
      "preservation_score": 3.4052969641037285e-07
    },
    {
      "id": 1,
      "text": "Liberdade dentro do caos\\nMarcelo Jubilado Catharino\\nisbn: \\n1ª edição, março de 2022.\\nEditora Autografía\\nRua Mairink Veiga, 6 - 10 andar - Centro\\nRio de Janeiro, RJ - CEP: 20090-050\\nwww.autografia.com.br\\nTodos os direitos reservados.  \\nProibida a reprodução deste livro  \\npara fins comerciais sem a permissão dos autores  \\ne da Autografía Editorial.\\nSem título-1   4Sem título-1   4 17/03/2022   15:08:3417/03/2022   15:08:34",
      "position": 766,
      "chapter": 1,
      "page": 4,
      "segment_type": "page",
      "themes": {},
      "difficulty": 21.28782201405152,
      "complexity_metrics": {
        "word_count": 61,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 8.714285714285714,
        "avg_word_length": 5.721311475409836,
        "unique_word_ratio": 0.9016393442622951,
        "avg_paragraph_length": 61.0,
        "punctuation_density": 0.2459016393442623,
        "line_break_count": 12,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "autografía",
          "título",
          "liberdade",
          "dentro",
          "caos",
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
          "centro",
          "janeiro",
          "autografia",
          "todos",
          "direitos"
        ],
        "entities": [
          [
            "Liberdade",
            "GPE"
          ],
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
            "4Sem",
            "CARDINAL"
          ]
        ],
        "readability_score": 93.9264637002342,
        "semantic_density": 0,
        "word_count": 61,
        "unique_words": 55,
        "lexical_diversity": 0.9016393442622951
      },
      "preservation_score": 5.363342718463371e-06
    },
    {
      "id": 1,
      "text": "— 5 —Dedicatória\\nEsse livro é dedicado a todos que passaram em minha vida, \\npois se eu não conhecesse aquela pessoa eu não teria a minha \\nvida. Obrigado às piores pessoas que passaram pela minha \\nvida, obrigado às melhores pessoas, obrigado a todos os meus \\namigos homens, mulheres, gays, trans, lésbicas, viado, gordo, \\nmacaco, mais preto, chupeta de baleia, homossexual, surubei -\\nro, casado, solteiro, preto, branco, pobre, rico, pão duro, bêba -\\ndo, maconheiro, cachaceiro e todos aqueles que um dia vão \\npassar ou vão estar em minha vida.\\nÀ minha família eu só tenho a agradecer, por me mostrar o \\ncaminho da sabedoria paraum viver melhor, pois sem vocês eu \\nnão teria o prazer de ter uma vida, de ter um filho que não te -\\nnho como mensurar o meu amor, meu sentimento, meu cari -\\nnho, minha admiração, minha vida. De tudo que vivi, de tudo \\nque irei viver, posso dizer que eu experimentei coisas que mui -\\nta gente tem preconceito, julgamento e pensamento ruins,sem \\nsaber que o problema não é o fazer e sim o como você faz e \\ncomo continuar fazendo. Nossa vida é a nossa responsabilida -\\nde, porém quantas pessoas eu preciso para ser feliz na minha \\nvida? Eu nunca abri um sorriso que não tivesse alguém ou uma \\nlembrança de alguém. O viver é viver melhor com o mundo!\\nSem título-1   5Sem título-1   5 17/03/2022   15:08:3417/03/2022   15:08:34",
      "position": 1304,
      "chapter": 1,
      "page": 5,
      "segment_type": "page",
      "themes": {},
      "difficulty": 33.19731012658228,
      "complexity_metrics": {
        "word_count": 237,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 29.625,
        "avg_word_length": 4.616033755274262,
        "unique_word_ratio": 0.6624472573839663,
        "avg_paragraph_length": 237.0,
        "punctuation_density": 0.19831223628691982,
        "line_break_count": 22,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "minha",
          "vida",
          "viver",
          "todos",
          "obrigado",
          "pessoas",
          "como",
          "passaram",
          "pois",
          "teria",
          "preto",
          "melhor",
          "tudo",
          "nossa",
          "alguém",
          "título",
          "dedicatória",
          "esse",
          "livro",
          "dedicado"
        ],
        "entities": [
          [
            "5",
            "CARDINAL"
          ],
          [
            "Dedicatória\\nEsse",
            "ORG"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "se eu não conhecesse",
            "PERSON"
          ],
          [
            "aquela pessoa eu não teria",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "lésbicas",
            "GPE"
          ],
          [
            "viado",
            "GPE"
          ],
          [
            "macaco",
            "GPE"
          ],
          [
            "chupeta de baleia",
            "PERSON"
          ]
        ],
        "readability_score": 83.80268987341772,
        "semantic_density": 0,
        "word_count": 237,
        "unique_words": 157,
        "lexical_diversity": 0.6624472573839663
      },
      "preservation_score": 2.6689014956162968e-05
    },
    {
      "id": 1,
      "text": "— 6 —Introdução  \\nLiberdade dentro do caos\\nTodos os textos escritos foram textos sobre dificuldades de \\nviver em aceitação perante a dor do outro, em concordância \\ncom o meu outro livro,Caos do passado sendo vívido no fu -\\nturo. Esse livro é a parte filosófica do caos perante o universo.\\nSão textos “avulsos” com um seguimento de direção de um \\nentendimento em aceitar o caos, com os valores que cada um \\nde nós tem em uma propagação da sua própria energia em \\naceitar um viver melhor… não podemos controlar nada, mas \\npodemos limitar o caos para conseguirmos um viver melhor… \\nos textos que aqui contém são textos por muitas vezes agres -\\nsivos em um entendimento de ligação com um outro enten -\\ndimento, o julgar um texto não é julgar um padrão de vários \\ntextos…\\nTemos que analisar várias linhas de raciocínioperante um \\núnico texto e dentro do possível e interpretativo eu coloco al -\\nguns textos com um significado semelhante, pois nem todos \\nnós conseguimos interpretar uma frase, um texto, um livro de \\nalguém que não conhecemos ou conversámos, pois o tom, a \\nlevada da dissertação é interpretativa de cada um.\\nNão sei como você interpreta o que você enxerga, como \\nvocê enxerga o que viveu e como você enxerga a vida que você \\nviveu… então a partir desse raciocínio, prefiro por muitas ve -\\nzes transformar uma leitura rápida em uma leitura melhor in -\\nterpretada para uma maior quantidade de pessoas.\\nSem título-1   6Sem título-1   6 17/03/2022   15:08:3417/03/2022   15:08:34",
      "position": 2769,
      "chapter": 1,
      "page": 6,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 36.059288537549406,
      "complexity_metrics": {
        "word_count": 253,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 50.6,
        "avg_word_length": 4.782608695652174,
        "unique_word_ratio": 0.5849802371541502,
        "avg_paragraph_length": 253.0,
        "punctuation_density": 0.07905138339920949,
        "line_break_count": 26,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "textos",
          "caos",
          "você",
          "viver",
          "outro",
          "livro",
          "melhor",
          "texto",
          "como",
          "enxerga",
          "dentro",
          "todos",
          "perante",
          "entendimento",
          "aceitar",
          "cada",
          "podemos",
          "muitas",
          "julgar",
          "pois"
        ],
        "entities": [
          [
            "6",
            "CARDINAL"
          ],
          [
            "Introdução",
            "ORG"
          ],
          [
            "Caos",
            "ORG"
          ],
          [
            "controlar nada",
            "PERSON"
          ],
          [
            "mas \\npodemos limitar o caos",
            "PERSON"
          ],
          [
            "padrão de vários",
            "ORG"
          ],
          [
            "Temos",
            "PERSON"
          ],
          [
            "eu coloco al -\\n",
            "PERSON"
          ],
          [
            "nem todos",
            "PERSON"
          ],
          [
            "nós conseguimos interpretar uma frase",
            "ORG"
          ]
        ],
        "readability_score": 73.26521739130435,
        "semantic_density": 0,
        "word_count": 253,
        "unique_words": 148,
        "lexical_diversity": 0.5849802371541502
      },
      "preservation_score": 1.7707544213339386e-05
    },
    {
      "id": 1,
      "text": "— 7 —As frases desse livro são frases de um caos que somos obri -\\ngados a viver e nos adaptar diante de um viver, pois já nasce -\\nmos e temos que ser gratos por estarmos vivos, aqui eu coloco \\numa forma de ver o caos como necessário para nos adaptar -\\nmos em um viver melhor em uma sociedade, assim estamos \\nem um processo evolutivo e adaptativo em um viver melhor.\\nNós nascemos e não sabemos como é um viver, e escrever \\ntextos que possam vir a ajudar uma quantidade de problemas \\nque não sabemos o motivo de acontecer, isso nos faz pensar \\ne interpretar uma forma de conter o caos que é iminente a \\nacontecer.\\nMarcelo, por que você escreve esses textos?\\nSimples!!!Eu quero viver o melhor com quem me conhe -\\nce.A regra é um norte para os sábios…A regra para quem não \\nsabe oque é uma regra é uma bússola quebrada para a evo -\\nlução!!!\\nAs pessoas que leem os meus textos são pessoas próximas a \\nmim, eu não posso melhorar o mundo, mas irei fazer o melhor \\ndentro daquilo que posso fazer para o mundo.\\nNão quero ser rico, não quero ser pobre, não quero ser fa -\\nmoso, não quero ter os excessos, quero ter aquilo que é neces -\\nsário para ser feliz e viver com aqueles queamo e quero estar \\ndo lado. Se todos fizessem o melhor diante da sua própria vida, \\naté que ponto esse círculo de si próprio se propagaria para \\nquem precisa?\\nSem título-1   7Sem título-1   7 17/03/2022   15:08:3417/03/2022   15:08:34",
      "position": 4369,
      "chapter": 1,
      "page": 7,
      "segment_type": "page",
      "themes": {},
      "difficulty": 31.5032319391635,
      "complexity_metrics": {
        "word_count": 263,
        "sentence_count": 10,
        "paragraph_count": 1,
        "avg_sentence_length": 26.3,
        "avg_word_length": 4.266159695817491,
        "unique_word_ratio": 0.55893536121673,
        "avg_paragraph_length": 263.0,
        "punctuation_density": 0.11406844106463879,
        "line_break_count": 25,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "viver",
          "quero",
          "melhor",
          "caos",
          "textos",
          "quem",
          "regra",
          "frases",
          "adaptar",
          "diante",
          "forma",
          "como",
          "sabemos",
          "acontecer",
          "pessoas",
          "posso",
          "mundo",
          "fazer",
          "título",
          "desse"
        ],
        "entities": [
          [
            "7",
            "CARDINAL"
          ],
          [
            "aqui eu coloco",
            "PERSON"
          ],
          [
            "uma forma de ver",
            "PERSON"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "assim estamos",
            "PERSON"
          ],
          [
            "possam vir",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "Marcelo",
            "PERSON"
          ],
          [
            "Simples!!!Eu",
            "ORG"
          ],
          [
            "para quem não",
            "PERSON"
          ]
        ],
        "readability_score": 85.57015209125476,
        "semantic_density": 0,
        "word_count": 263,
        "unique_words": 147,
        "lexical_diversity": 0.55893536121673
      },
      "preservation_score": 2.1815183676289504e-05
    },
    {
      "id": 1,
      "text": "— 8 —\\nSem título-1   8Sem título-1   8 17/03/2022   15:08:3417/03/2022   15:08:34",
      "position": 5887,
      "chapter": 1,
      "page": 8,
      "segment_type": "page",
      "themes": {},
      "difficulty": 22.21818181818182,
      "complexity_metrics": {
        "word_count": 11,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 11.0,
        "avg_word_length": 5.7272727272727275,
        "unique_word_ratio": 0.7272727272727273,
        "avg_paragraph_length": 11.0,
        "punctuation_density": 0.36363636363636365,
        "line_break_count": 1,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "título"
        ],
        "entities": [
          [
            "8",
            "CARDINAL"
          ],
          [
            "8Sem",
            "CARDINAL"
          ],
          [
            "8",
            "CARDINAL"
          ],
          [
            "15:08:3417/03/2022",
            "CARDINAL"
          ],
          [
            "15:08:34",
            "PERSON"
          ]
        ],
        "readability_score": 92.78181818181818,
        "semantic_density": 0,
        "word_count": 11,
        "unique_words": 8,
        "lexical_diversity": 0.7272727272727273
      },
      "preservation_score": 1.7026484820518643e-07
    },
    {
      "id": 1,
      "text": "— 9 —Qual é o sentindo de viver?\\nO sentindo de viver é saber viver!\\nNós humanos descobrimos saber o sentindo de viver pro -\\ncurando no caos o sentido de viver … como assim?Meditação é \\na procura do conforto no desconforto…\\nO alpinista resolve os seus próprios problemas, indo “atrás \\nda calmaria no próprio problema” … Um esportista vai atrás \\nde superação para se sentir vivo…\\nVá atrás do seu desconforto para saber valorizar o conforto \\nque vier...\\nTodos nós queremos viver o melhor, porém para desco -\\nbrirmos o viver melhor, procuramos o nosso próprio caos, no \\nobjetivo de viver e aceitar o melhor que a vida possa nos pro -\\nporcionar!\\nNão temos uma resposta do sentido de viver, mas podemos \\nnos dar uma resposta simples, estamos vivos e precisamos sa -\\nber viver o melhor da vida, pois nenhuma resposta que eu ob -\\nter vai fazer mais sentindo do que é viver!\\nSem título-1   9Sem título-1   9 17/03/2022   15:08:3417/03/2022   15:08:34",
      "position": 6082,
      "chapter": 1,
      "page": 9,
      "segment_type": "page",
      "themes": {},
      "difficulty": 29.244415584415584,
      "complexity_metrics": {
        "word_count": 165,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 23.571428571428573,
        "avg_word_length": 4.624242424242424,
        "unique_word_ratio": 0.6181818181818182,
        "avg_paragraph_length": 165.0,
        "punctuation_density": 0.11515151515151516,
        "line_break_count": 18,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "viver",
          "sentindo",
          "melhor",
          "saber",
          "atrás",
          "resposta",
          "caos",
          "sentido",
          "conforto",
          "desconforto",
          "próprio",
          "vida",
          "título",
          "qual",
          "humanos",
          "descobrimos",
          "curando",
          "como",
          "assim",
          "meditação"
        ],
        "entities": [
          [
            "9",
            "CARDINAL"
          ],
          [
            "sentindo de viver",
            "ORG"
          ],
          [
            "descobrimos",
            "PERSON"
          ],
          [
            "sentindo de viver",
            "ORG"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "para saber",
            "PERSON"
          ],
          [
            "Todos",
            "GPE"
          ],
          [
            "para desco -\\nbrirmos",
            "PERSON"
          ],
          [
            "sentido de viver",
            "PERSON"
          ],
          [
            "mas podemos",
            "PERSON"
          ]
        ],
        "readability_score": 86.82701298701299,
        "semantic_density": 0,
        "word_count": 165,
        "unique_words": 102,
        "lexical_diversity": 0.6181818181818182
      },
      "preservation_score": 1.1492877253850082e-05
    },
    {
      "id": 1,
      "text": "— 10 —O ensinamento é um direcionamento do que é viver… se -\\nvocê vem em uma direção e precisa voltar na contramão, você \\nirá voltar na contramão? Nem sempre uns vão respeitar a fal -\\nta de respeito perante o outro, por incômodo ou por medo \\ndo incômodo… nem sempre as regras são necessárias para \\nseremcumpridas, tem momentos que precisamos fugir das re -\\ngras para conseguirmos viver…\\nNunca se ache mais inteligente ou melhor que alguém, to -\\ndos nascemos sem um objetivo, todos nascemos para viver a \\nvida e durante a vida aprendemos com as dores, com as ale -\\ngrias, com a raiva, com perdas e mesmo com tudo isso que \\npassamos, as pessoas ainda pensam que são melhores, mais \\nimportantes, sentemque têm mais direitos que outros que nas -\\nceram iguais a você. Nunca se comporte como melhor do que \\na pessoa que está à sua frente, o pensamento dela em certas \\nsituações é mais evoluído que o seu pensamento. Sempre me -\\nlhore, sempre dê o seu melhor, pois a sua vida é do tamanho \\nde uma “casa” , quando menos você espera,encontra aquela pes -\\nsoa, assim comovocê não sabe o dia de amanhã, ela também \\nnão sabe, ambos podem precisar um do outro e mesmo assim \\nas pessoas ainda continuam se achando superiores aos seus se -\\nmelhantes.\\nTodogênio tem a sua loucura…\\nE toda loucura tem a sua genialidade…\\nAté que ponto a loucura é genialidade?\\nSem título-1   10Sem título-1   10 17/03/2022   15:08:3417/03/2022   15:08:34",
      "position": 7138,
      "chapter": 1,
      "page": 10,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.36126482213439,
      "complexity_metrics": {
        "word_count": 253,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 42.166666666666664,
        "avg_word_length": 4.537549407114624,
        "unique_word_ratio": 0.6284584980237155,
        "avg_paragraph_length": 253.0,
        "punctuation_density": 0.11067193675889328,
        "line_break_count": 25,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "sempre",
          "mais",
          "viver",
          "melhor",
          "vida",
          "loucura",
          "voltar",
          "contramão",
          "outro",
          "incômodo",
          "nunca",
          "nascemos",
          "mesmo",
          "pessoas",
          "ainda",
          "pensamento",
          "assim",
          "sabe",
          "genialidade"
        ],
        "entities": [
          [
            "10",
            "CARDINAL"
          ],
          [
            "nem sempre",
            "PERSON"
          ],
          [
            "necessárias para \\nseremcumpridas",
            "PERSON"
          ],
          [
            "das re -\\ngras para conseguirmos viver",
            "PERSON"
          ],
          [
            "Nunca",
            "ORG"
          ],
          [
            "nascemos",
            "PERSON"
          ],
          [
            "todos",
            "NORP"
          ],
          [
            "nascemos para",
            "PERSON"
          ],
          [
            "Nunca",
            "ORG"
          ],
          [
            "sempre dê o seu melhor",
            "ORG"
          ]
        ],
        "readability_score": 77.55540184453228,
        "semantic_density": 0,
        "word_count": 253,
        "unique_words": 159,
        "lexical_diversity": 0.6284584980237155
      },
      "preservation_score": 2.287933897757192e-05
    },
    {
      "id": 1,
      "text": "— 11 —O ser feliz é caso do acaso, tristeza é algo dentro da norma -\\nlidade de viver… Não encontre a plenitude em viver, encontre \\no viver dentro do viver… Os problemas, as dificuldades, as co -\\nbrançastudoem sua vida é necessário para conseguirmos dar \\nvalor a sermos feliz quando se deve ser feliz!!\\nO que é o amor?\\nAmor não é aquela ilusão que nós crescemos imaginando a \\n“perfeição” de vida…\\nAmor não é tesão, muito menos paixão…\\nAmor não é só família, amigos…\\nAmor é um sentimento a qual cada um não sabe nem oque \\né amar, pois vive sonhando oque é o amor…\\nEu enxergo que quando amamos alguém o sentimento \\namor é igual, porém a forma de sentir ese relacionar um com \\no outro é diferente.\\nComo mãe e filho, proteção, carinho, família, materni -\\ndade etc.\\nMarido e mulher, proteção, família, sexo, “paixão nem sem -\\npre vai ter…nem sempre vai acontecer o melhor sexo… ” \\nIrmão e irmão\\nCompanheiros, família, estar junto etc.\\nPai e filho \\nSem título-1   11Sem título-1   11 17/03/2022   15:08:3417/03/2022   15:08:34",
      "position": 8672,
      "chapter": 1,
      "page": 11,
      "segment_type": "page",
      "themes": {},
      "difficulty": 31.447421731123388,
      "complexity_metrics": {
        "word_count": 181,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 30.166666666666668,
        "avg_word_length": 4.54696132596685,
        "unique_word_ratio": 0.6850828729281768,
        "avg_paragraph_length": 181.0,
        "punctuation_density": 0.15469613259668508,
        "line_break_count": 22,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "amor",
          "viver",
          "família",
          "feliz",
          "dentro",
          "encontre",
          "vida",
          "quando",
          "paixão",
          "sentimento",
          "oque",
          "filho",
          "proteção",
          "sexo",
          "irmão",
          "título",
          "caso",
          "acaso",
          "tristeza",
          "algo"
        ],
        "entities": [
          [
            "11",
            "CARDINAL"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "para conseguirmos dar",
            "PERSON"
          ],
          [
            "quando se deve ser feliz",
            "PERSON"
          ],
          [
            "Amor",
            "ORG"
          ],
          [
            "ilusão que",
            "ORG"
          ],
          [
            "nós crescemos",
            "ORG"
          ],
          [
            "Amor",
            "ORG"
          ],
          [
            "muito menos",
            "PERSON"
          ],
          [
            "Amor",
            "ORG"
          ]
        ],
        "readability_score": 83.55257826887662,
        "semantic_density": 0,
        "word_count": 181,
        "unique_words": 124,
        "lexical_diversity": 0.6850828729281768
      },
      "preservation_score": 1.8729133302570503e-05
    },
    {
      "id": 1,
      "text": "— 12 —Mesmo que a mãe etc.\\nAmigo e amigo\\nMesmo que o irmão etc.\\nNo final das contas, todosamamos iguais um ao outro, po -\\nrém com alguns sentimentos diferentes, nas relações as quais \\nestamos vivendo com a pessoa.\\nMas como eu irei saber se realmente amo aquela pessoa?\\nÉ simples, oque mais vale em minha vida? A minha própria \\nvida, se eu dou a minha vida por alguém, eu amo essa pessoa, \\nse eu amo essa pessoa e eu dou a minha vida por ela, o nosso \\namor é igual perante a todos que amamos.\\nNão julgue a ausência de algum sentimento que comple -\\nmenta o amora qual você vive com aquela pessoa. Cada pessoa \\ntem um relacionamento com você, a sua forma de dar a vida \\npor alguém é a mesma quevocê dá para quem você “mais” ama.\\nAmor\\nAmor pode ser a perfeição do sentimento ou a maior de -\\ncepção do sentimento…\\nAmor pode ser o seu equilíbrio ou pode ser o seu dese -\\nquilíbrio…\\nAmor você não escolhe, amor é o único sentimento que \\ntemos certeza de que temos, mas não temos marcação do sen -\\ntimento de amar…\\nSem título-1   12Sem título-1   12 17/03/2022   15:08:3417/03/2022   15:08:34",
      "position": 9806,
      "chapter": 1,
      "page": 12,
      "segment_type": "page",
      "themes": {},
      "difficulty": 28.654742547425474,
      "complexity_metrics": {
        "word_count": 205,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 22.77777777777778,
        "avg_word_length": 4.219512195121951,
        "unique_word_ratio": 0.6292682926829268,
        "avg_paragraph_length": 205.0,
        "punctuation_density": 0.11219512195121951,
        "line_break_count": 23,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "pessoa",
          "amor",
          "vida",
          "minha",
          "sentimento",
          "você",
          "pode",
          "temos",
          "mesmo",
          "amigo",
          "aquela",
          "mais",
          "alguém",
          "essa",
          "título",
          "irmão",
          "final",
          "contas",
          "todosamamos",
          "iguais"
        ],
        "entities": [
          [
            "12",
            "CARDINAL"
          ],
          [
            "Mesmo",
            "ORG"
          ],
          [
            "Mesmo",
            "PERSON"
          ],
          [
            "estamos vivendo",
            "PERSON"
          ],
          [
            "Mas como eu irei",
            "PERSON"
          ],
          [
            "aquela pessoa",
            "PERSON"
          ],
          [
            "se eu dou",
            "PERSON"
          ],
          [
            "eu",
            "PERSON"
          ],
          [
            "essa pessoa",
            "PERSON"
          ],
          [
            "se eu",
            "PERSON"
          ]
        ],
        "readability_score": 87.34525745257453,
        "semantic_density": 0,
        "word_count": 205,
        "unique_words": 129,
        "lexical_diversity": 0.6292682926829268
      },
      "preservation_score": 1.6643388912056967e-05
    },
    {
      "id": 1,
      "text": "— 13 —Amor você tem que sentir para viver o melhor do amor, \\nmas quando o amor é sentido demais e não é retribuído,você \\nse sente em um vazio…\\nAmor você tem que aprender a lhe dar, pois o amor nos \\ndeixa cegos diante do que vivemos…\\nAmor é a razão de viver, assim como é razão de não que -\\nrer viver…\\nAmor você sabe o que é, sente o que é, vive oque é, porém \\nele também te deixa cego diante dos erros do outro quevocê \\nmesmo ama…\\nAmor é algo inexplicável e muito fácil de explicar…\\nAmor é o sentido de se viver feliz e o sentido de se viver \\ntriste…\\nAmor e ódio são uma única coisa, pois para você ter ódio \\nde alguém um dia você já amou alguém…\\nAmor as pessoas confundem com “eu não gostar de al -\\nguém” por uma imagem…\\nAmor você precisa conhecer, sentir, admirar, confiar, abra -\\nçar, valorizar, compreender, brigar, dialogar, ensinar, se preo -\\ncupar; amor é tudoque háde belo, porém quandovocê perde \\nalgumas belezas do amor, ele se transforma em “ódio’ …\\nAmor não é você viver sempre, amor é caso do acaso, amor \\né a raridade de se viver a felicidade maior de umser do próprio -\\nser humano…\\nAmor não é amar uma pessoa, amor é reconhecer que aque -\\nla pessoa te faz ser uma versão melhor de si mesmo…\\nAmor pode ser de mãe, filho, irmão, esposa, amigos, pri -\\nmos, tias, avós, avôs amor é você amar o ser humano que está \\nSem título-1   13Sem título-1   13 17/03/2022   15:08:3417/03/2022   15:08:34",
      "position": 11005,
      "chapter": 1,
      "page": 13,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 35.37211895910781,
      "complexity_metrics": {
        "word_count": 269,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 269.0,
        "avg_word_length": 4.152416356877324,
        "unique_word_ratio": 0.5650557620817844,
        "avg_paragraph_length": 269.0,
        "punctuation_density": 0.13382899628252787,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "amor",
          "você",
          "viver",
          "sentido",
          "ódio",
          "sentir",
          "melhor",
          "sente",
          "pois",
          "deixa",
          "diante",
          "razão",
          "porém",
          "mesmo",
          "alguém",
          "humano",
          "amar",
          "pessoa",
          "título",
          "quando"
        ],
        "entities": [
          [
            "13",
            "CARDINAL"
          ],
          [
            "mas quando",
            "PERSON"
          ],
          [
            "amor é sentido demais",
            "ORG"
          ],
          [
            "que vivemos",
            "PERSON"
          ],
          [
            "de não",
            "PERSON"
          ],
          [
            "outro quevocê",
            "PERSON"
          ],
          [
            "sentido de se viver feliz",
            "PERSON"
          ],
          [
            "sentido de se",
            "PERSON"
          ],
          [
            "para você",
            "PERSON"
          ],
          [
            "dia",
            "ORG"
          ]
        ],
        "readability_score": 0,
        "semantic_density": 0,
        "word_count": 269,
        "unique_words": 152,
        "lexical_diversity": 0.5650557620817844
      },
      "preservation_score": 3.039227540462577e-05
    },
    {
      "id": 1,
      "text": "— 14 —ali à sua frente, fazendo exaltar o seu sentimento de amar sem \\nvocê escolher e sim sentir.\\nO que é o amor afinal?\\nAmor é você dar a vida pelo outro.\\nJesus se sacrificou porquê? Buda se separou e não se casou \\nporquê? Monges não se casam porquê?\\nMesmo quando se é casado, assassino, ditador, o seu amor \\npelo próximo é maior que o seu próprio amor…\\nHitler amava “o seu povo” …\\nGandhi amava “o seu povo” …\\nMadre Tereza “amava o seu povo” …\\nTodas as pessoas que seguiram uma pessoa foram por causa \\ndo amor; o amorque sinto é semelhante ao seu, eu te dou a \\nminha vida e você me dá a sua vida, isso se chama gerar con -\\nfiança diante daquilo que quero para mim mesmo, para um \\nbem maior…\\nAmar a maioria ama…\\nAmor é vocêentender e compreender a dor de quem \\nvocê ama…\\nAmor é você enxergar o amor através da energia quevocê \\nsente vindo de outros ou de outro…\\nNão pense que o seu amor é melhor ou pior, amor é \\nvocê querer que quem você ama tenha ou seja o mais feliz \\npossível…\\nSem título-1   14Sem título-1   14 17/03/2022   15:08:3417/03/2022   15:08:34",
      "position": 12523,
      "chapter": 1,
      "page": 14,
      "segment_type": "page",
      "themes": {},
      "difficulty": 30.738423645320196,
      "complexity_metrics": {
        "word_count": 203,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 29.0,
        "avg_word_length": 4.12807881773399,
        "unique_word_ratio": 0.6403940886699507,
        "avg_paragraph_length": 203.0,
        "punctuation_density": 0.09359605911330049,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "amor",
          "você",
          "vida",
          "porquê",
          "amava",
          "povo",
          "amar",
          "pelo",
          "outro",
          "mesmo",
          "maior",
          "quem",
          "título",
          "frente",
          "fazendo",
          "exaltar",
          "sentimento",
          "escolher",
          "sentir",
          "afinal"
        ],
        "entities": [
          [
            "14",
            "CARDINAL"
          ],
          [
            "fazendo exaltar",
            "ORG"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "de amar",
            "PERSON"
          ],
          [
            "pelo outro",
            "PERSON"
          ],
          [
            "Jesus",
            "PERSON"
          ],
          [
            "Buda",
            "PERSON"
          ],
          [
            "não se casou \\nporquê",
            "PERSON"
          ],
          [
            "Monges",
            "PERSON"
          ],
          [
            "Mesmo",
            "PERSON"
          ]
        ],
        "readability_score": 84.2615763546798,
        "semantic_density": 0,
        "word_count": 203,
        "unique_words": 130,
        "lexical_diversity": 0.6403940886699507
      },
      "preservation_score": 1.532383633846678e-05
    },
    {
      "id": 1,
      "text": "— 15 —Amor é amar o outro mais do que a si mesmo.\\nQuanto vale um sentimento?\\nQuando você está com os seus amigos, o quevocê mais pres -\\nta atenção ao viver com eles? As roupas, ocarro, a casa, a apa -\\nrência ou sentimento do momento?\\nQuando você lembra de alguma coisa com os seus amigos, \\no que vale mais?O que a pessoa estava usando ou o sentimento \\ndo momento?\\nQuando um artista começa a ser artista e pinta quadros, faz \\nmúsica, qual é o valor da arte dele?\\nDepois que ele ganha fama através da sua própria arte, \\nquanto vale um show ou a arte dele?\\nSentimento não tem valor a ser medido, sentimento é algo \\nimpagável diante da importância do próprio sentimento!!!\\nVocê pensa em sexo acima de tudo?Como você trata o sexo? \\nVocê respeita a pessoa ao seu lado? Atéque ponto o sexo para \\nvocê tem que ter confiança para ter amor ao invés de sexo? O \\nque é sexo para você?\\nResponda para si mesmo essas perguntas e veja como você \\nenxerga a confiança diante do sexoe daprópria vida!\\nSem título-1   15Sem título-1   15 17/03/2022   15:08:3417/03/2022   15:08:34",
      "position": 13696,
      "chapter": 1,
      "page": 15,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 22.414993523316063,
      "complexity_metrics": {
        "word_count": 193,
        "sentence_count": 16,
        "paragraph_count": 1,
        "avg_sentence_length": 12.0625,
        "avg_word_length": 4.404145077720207,
        "unique_word_ratio": 0.6113989637305699,
        "avg_paragraph_length": 193.0,
        "punctuation_density": 0.15544041450777202,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "sentimento",
          "sexo",
          "mais",
          "vale",
          "quando",
          "arte",
          "amor",
          "mesmo",
          "quanto",
          "seus",
          "amigos",
          "momento",
          "pessoa",
          "artista",
          "valor",
          "dele",
          "diante",
          "como",
          "confiança"
        ],
        "entities": [
          [
            "15",
            "CARDINAL"
          ],
          [
            "Quanto",
            "PRODUCT"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "quevocê mais",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "lembra de alguma",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "faz \\nmúsica",
            "ORG"
          ],
          [
            "da sua própria arte",
            "ORG"
          ],
          [
            "Sentimento",
            "NORP"
          ]
        ],
        "readability_score": 92.64750647668394,
        "semantic_density": 0,
        "word_count": 193,
        "unique_words": 118,
        "lexical_diversity": 0.6113989637305699
      },
      "preservation_score": 1.5323836338466775e-05
    },
    {
      "id": 1,
      "text": "— 16 —Não confundam saudade com tesão!!\\nSaudade (família, amigos) você tem daquela pessoa que \\nmesmo longe de você lembra com felicidade, carinho, admi -\\nração. Sempre quando está junto àquela saudade parece que \\nnem aconteceu, simplesmente a história continuou de onde \\nparou da última vez…\\nTesão é você perder a noção entre o certo e o errado diante \\nda sua própria necessidade…\\nTesão é quando você quer fazer sexo com a pessoa, mesmo \\nsabendo que não tem afeto quase nenhum…\\nTesão é ohomem acordar parecendo um pau-brasil, a mu -\\nlher acordar toda molhada por uma lembrança sexual e não \\ncontextual (pode acontecer por amor, tem que se entender) …\\nTesão é algo que você sobe pelas paredes e quandovocê \\nquer fazer… Sai da frente, pois você vai dar um jeito de fazer.\\nTesão não é algo quevocê não tem que usar e sim saber \\nusar… suas necessidades corpóreas são tão necessáriasquanto \\na necessidade de comer, dormir, respirar.Nós humanos precisa -\\nmos fazer sexo por toda história evolutiva do humano sempre \\nser feito para combater o estresse, mauhumor, liberar endorfi -\\nna, satisfação corporal…\\nNão prejudique alguém pela sua necessidade, não engane \\nalguém por você precisar acabar com o seu tesão, fale a ver -\\ndade, assim comovocê quer, a outra pessoa também quer. O \\naconteceu, o sentimento, o amar, o se conhecer não é necessa -\\nriamente restrição e sim aprender a apreciar o trajeto. Nesse \\nSem título-1   16Sem título-1   16 17/03/2022   15:08:3417/03/2022   15:08:34",
      "position": 14870,
      "chapter": 1,
      "page": 16,
      "segment_type": "page",
      "themes": {},
      "difficulty": 35.12090592334495,
      "complexity_metrics": {
        "word_count": 246,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 35.142857142857146,
        "avg_word_length": 4.926829268292683,
        "unique_word_ratio": 0.6707317073170732,
        "avg_paragraph_length": 246.0,
        "punctuation_density": 0.12601626016260162,
        "line_break_count": 26,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "tesão",
          "você",
          "quer",
          "fazer",
          "saudade",
          "pessoa",
          "necessidade",
          "mesmo",
          "sempre",
          "quando",
          "aconteceu",
          "história",
          "sexo",
          "acordar",
          "toda",
          "algo",
          "usar",
          "alguém",
          "título",
          "confundam"
        ],
        "entities": [
          [
            "16",
            "CARDINAL"
          ],
          [
            "daquela",
            "PERSON"
          ],
          [
            "mesmo longe de você lembra com",
            "ORG"
          ],
          [
            "nem aconteceu",
            "PERSON"
          ],
          [
            "história continuou de",
            "PERSON"
          ],
          [
            "última vez",
            "PERSON"
          ],
          [
            "Tesão",
            "GPE"
          ],
          [
            "Tesão",
            "GPE"
          ],
          [
            "quando você quer",
            "ORG"
          ],
          [
            "fazer",
            "PERSON"
          ]
        ],
        "readability_score": 80.95052264808362,
        "semantic_density": 0,
        "word_count": 246,
        "unique_words": 165,
        "lexical_diversity": 0.6707317073170732
      },
      "preservation_score": 2.5454594806675367e-05
    },
    {
      "id": 1,
      "text": "— 17 —trajeto tem um início e muitas vezes esse mesmo início come -\\nça com um tesão fora de controle… não se prive de fazer, se \\nprive de se entender antes de querer mais e mais.\\n“A mulher tem o poder de destruir o homem ou erguer o \\nhomem. ”\\nMeu ponto de vista diante dessa frase é: “O homem perante \\no querer fazer sexo é muito mais fraco que a mulher. ”\\nComo assim? A mulher consegue ser mais independente \\nque o homem por conseguir segurar os seus próprios desejos \\nsexuais (a maioria das mulheres) …\\nO homem não consegue ser mais independente por sem -\\npre querer mais sexo, chegando ao ponto de não se controlar e \\nver os seus benefícios e malefícios diante da sua própria neces -\\nsidade, os tornando cegos diante da sua necessidade evolutiva \\n(maioria dos homens) …\\nO homem (mulher) quando casa e arruma uma mulher ou \\num homem (relacionamento)que ambosvão confiar, somar, \\nagregar, crescer, amar, apoiar, evoluir junto, qual é a chance \\ndesses dois indivíduos conseguirem uma vida melhor?\\nUm homem solteiro, sem ninguém, sem limites, sem al -\\nguém para apoiá-lo, tendo só a obrigação de “viver” , quais são \\nas chances desse mesmo homem ter uma vida melhor? O sexo \\nnos move em uma direção, se vocênão conseguir enxergar qual \\nSem título-1   17Sem título-1   17 17/03/2022   15:08:3417/03/2022   15:08:34",
      "position": 16463,
      "chapter": 1,
      "page": 17,
      "segment_type": "page",
      "themes": {},
      "difficulty": 32.74971927635683,
      "complexity_metrics": {
        "word_count": 229,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 32.714285714285715,
        "avg_word_length": 4.641921397379913,
        "unique_word_ratio": 0.6550218340611353,
        "avg_paragraph_length": 229.0,
        "punctuation_density": 0.11790393013100436,
        "line_break_count": 23,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "homem",
          "mais",
          "mulher",
          "querer",
          "diante",
          "sexo",
          "início",
          "mesmo",
          "prive",
          "fazer",
          "ponto",
          "consegue",
          "independente",
          "conseguir",
          "seus",
          "maioria",
          "qual",
          "vida",
          "melhor",
          "título"
        ],
        "entities": [
          [
            "17",
            "CARDINAL"
          ],
          [
            "prive de fazer",
            "ORG"
          ],
          [
            "Meu",
            "ORG"
          ],
          [
            "querer fazer",
            "PERSON"
          ],
          [
            "muito mais fraco",
            "PERSON"
          ],
          [
            "Como",
            "ORG"
          ],
          [
            "desejos \\nsexuais",
            "PERSON"
          ],
          [
            "diante da sua própria",
            "PERSON"
          ],
          [
            "quando",
            "PERSON"
          ],
          [
            "amar",
            "PERSON"
          ]
        ],
        "readability_score": 82.25028072364317,
        "semantic_density": 0,
        "word_count": 229,
        "unique_words": 150,
        "lexical_diversity": 0.6550218340611353
      },
      "preservation_score": 2.4475571929495542e-05
    },
    {
      "id": 1,
      "text": "— 18 —direção o sexo está te levando, você pode viver à procura de \\nalgo quevocê nunca vai achar a sua própria direção!!\\nA preocupação em fazer sexo é tão grande que esquecemos \\ndo sentimento que precisamos ter para ter um bom sexo… A \\nfelicidade em ter uma aparência, ter mais dinheiro, ter muito \\nmais coisas materiais está valendo muito mais que o sentimen -\\nto, pois até o sexo está sendo feito pela necessidade material e \\nnão pela vontade sentimental!!!\\nDeixamos de ver as consequências em volta de nossa vida \\npelo simples fator do sexo ser“mais importante” que as demais \\ncoisas…Seja conhecendo alguém, namorando alguém, casado \\ncom alguém, solteiro só viveà procura…\\nDeixamos de dar prioridade para um estar com um amigo, \\nestar com o filho, estar com a mulher/homemquevocê ama, \\nestar vivendo e não focando a sua vida toda em prol do sexo… \\nValores estão sendo destoados, nossas prioridades estão sendo \\ndesignadas de uma única formade prazer,que depois de um \\ntempo você nem lembra desse prazer…\\nDeixamos de construir casa, deixamos famílias, deixamos \\nde trabalhar, deixamos de viver para apenas viver uma única \\ncoisa, sexo!!!\\nSem título-1   18Sem título-1   18 17/03/2022   15:08:3417/03/2022   15:08:34",
      "position": 17890,
      "chapter": 1,
      "page": 18,
      "segment_type": "page",
      "themes": {},
      "difficulty": 37.53846153846154,
      "complexity_metrics": {
        "word_count": 195,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 48.75,
        "avg_word_length": 5.128205128205129,
        "unique_word_ratio": 0.6461538461538462,
        "avg_paragraph_length": 195.0,
        "punctuation_density": 0.14358974358974358,
        "line_break_count": 21,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "sexo",
          "deixamos",
          "mais",
          "está",
          "viver",
          "sendo",
          "alguém",
          "direção",
          "você",
          "procura",
          "muito",
          "coisas",
          "pela",
          "vida",
          "estão",
          "única",
          "prazer",
          "título",
          "levando",
          "pode"
        ],
        "entities": [
          [
            "18",
            "CARDINAL"
          ],
          [
            "levando",
            "GPE"
          ],
          [
            "procura de \\nalgo",
            "PERSON"
          ],
          [
            "uma aparência",
            "PERSON"
          ],
          [
            "muito \\nmais coisas materiais está",
            "PERSON"
          ],
          [
            "muito mais que",
            "PERSON"
          ],
          [
            "Deixamos de dar",
            "ORG"
          ],
          [
            "estar",
            "PRODUCT"
          ],
          [
            "designadas de uma única formade",
            "ORG"
          ],
          [
            "nem lembra",
            "PERSON"
          ]
        ],
        "readability_score": 74.08653846153845,
        "semantic_density": 0,
        "word_count": 195,
        "unique_words": 126,
        "lexical_diversity": 0.6461538461538462
      },
      "preservation_score": 1.56430829288515e-05
    },
    {
      "id": 1,
      "text": "— 19 —Qual é a importância do sexo em sua vida?\\nQual é a quantidade de malefícios que você tem para ter \\num bom sexo?\\nQual é o grau de prioridade do sexo?\\nQuanto tempo você fica pensando em sexo?\\nQuanto tempo você se dedica para ter sexo?\\nQuanto você gasta (dinheiro) para ter sexo?\\nNa sua vida, qual é a escala de importância do sexo perante \\noutras coisas?\\nVocê conseguiria viver sem sexo?\\nO que é sexo para você é amor ou é algo a ser feito por pra -\\nzer próprio ou vontade?\\nO sexo quandovocê namora ou é casado tem que ser só \\ncom você ou pode ser um relacionamento aberto?\\nPorque o relacionamento é monogamia?\\nQual é a forma certa de ver o sexo perante ao seu compa -\\nnheiro (a)?\\nSão muitos questionamentos que temos perante ao sexo \\npor não entender o que é o sexo para a nossa própria vida… \\nConheça os seus valorespara entender o valor do sexo para \\nvocê, se você gosta de uma suruba, orgia, relacionamento aber -\\nto viva dessa forma. Se você gosta de sexo com amor, viva des -\\nsa forma.\\nSexo é algo que temos que sentir prazer, vontade, pois nem \\nsempre teremos amor e um bom sexo… Assim como não \\nSem título-1   19Sem título-1   19 17/03/2022   15:08:3417/03/2022   15:08:34",
      "position": 19222,
      "chapter": 1,
      "page": 19,
      "segment_type": "page",
      "themes": {},
      "difficulty": 22.305855855855853,
      "complexity_metrics": {
        "word_count": 222,
        "sentence_count": 15,
        "paragraph_count": 1,
        "avg_sentence_length": 14.8,
        "avg_word_length": 4.2657657657657655,
        "unique_word_ratio": 0.545045045045045,
        "avg_paragraph_length": 222.0,
        "punctuation_density": 0.11261261261261261,
        "line_break_count": 25,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "sexo",
          "você",
          "qual",
          "vida",
          "quanto",
          "perante",
          "amor",
          "relacionamento",
          "forma",
          "importância",
          "tempo",
          "algo",
          "vontade",
          "temos",
          "entender",
          "gosta",
          "viva",
          "título",
          "quantidade",
          "malefícios"
        ],
        "entities": [
          [
            "19",
            "CARDINAL"
          ],
          [
            "Quanto",
            "PRODUCT"
          ],
          [
            "fica pensando",
            "ORG"
          ],
          [
            "Quanto",
            "PRODUCT"
          ],
          [
            "Quanto",
            "PRODUCT"
          ],
          [
            "para você",
            "PERSON"
          ],
          [
            "quandovocê namora",
            "PERSON"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "gosta de uma suruba",
            "ORG"
          ],
          [
            "gosta de sexo",
            "ORG"
          ]
        ],
        "readability_score": 91.32027027027027,
        "semantic_density": 0,
        "word_count": 222,
        "unique_words": 121,
        "lexical_diversity": 0.545045045045045
      },
      "preservation_score": 1.9686873073724673e-05
    },
    {
      "id": 1,
      "text": "— 20 —teremos sempre uma ótima comida, ótima casa, ótima vida… \\nSexo é sexo. Sexo é para se fazer e não para viver em pró do \\nsexo!!!\\nQuer entender sobre o perder tempo de vida estudando, vi -\\nvendo uma vida em que você faz o bem, porém não faz bem \\npara si próprio, viver uma vida dedicada aos outros e não ten -\\ndo reconhecimento, viver uma vida quevocê possa vir morrer \\na qualquer momento e deixou de viver pelo simples fator de \\neu estudo, eu conheço, eu sou o melhor? Ver esse filme vai te \\najudar a decifrar e mostrar quena vida é preciso viver!!\\nFilme: Adeus, Professor.\\nA minha maior preocupação perante a sociedade é a falta \\nde saber viver…\\nEu não entendo a monotonia de se viver, pois se você está \\nvivo,porque não vive?\\nNão vejo nenhum grito de uma mãe escandalosa, não vejo \\nnenhuma criança brigando com a outra, não vejo nenhuma \\nbola caindo no quintal do vizinho, não vejo os velhos jogando \\ndominó, não vejo os adultos sendo felizes com as suas mulhe -\\nres, família e amigos… Só vejo os valores da necessidade de \\nSem título-1   20Sem título-1   20 17/03/2022   15:08:3417/03/2022   15:08:34",
      "position": 20521,
      "chapter": 1,
      "page": 20,
      "segment_type": "page",
      "themes": {},
      "difficulty": 31.55599425699928,
      "complexity_metrics": {
        "word_count": 199,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 28.428571428571427,
        "avg_word_length": 4.472361809045226,
        "unique_word_ratio": 0.6683417085427136,
        "avg_paragraph_length": 199.0,
        "punctuation_density": 0.1507537688442211,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "viver",
          "vida",
          "vejo",
          "sexo",
          "ótima",
          "você",
          "filme",
          "nenhuma",
          "título",
          "teremos",
          "sempre",
          "comida",
          "casa",
          "fazer",
          "quer",
          "entender",
          "perder",
          "tempo",
          "estudando",
          "vendo"
        ],
        "entities": [
          [
            "20",
            "CARDINAL"
          ],
          [
            "sempre uma ótima comida",
            "ORG"
          ],
          [
            "casa",
            "GPE"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "aos outros e não",
            "ORG"
          ],
          [
            "ten",
            "CARDINAL"
          ],
          [
            "fator de \\neu",
            "PERSON"
          ],
          [
            "eu conheço",
            "PERSON"
          ],
          [
            "eu sou o melhor",
            "PERSON"
          ]
        ],
        "readability_score": 84.44400574300072,
        "semantic_density": 0,
        "word_count": 199,
        "unique_words": 133,
        "lexical_diversity": 0.6683417085427136
      },
      "preservation_score": 1.5749498458979744e-05
    },
    {
      "id": 1,
      "text": "— 21 —se criar um filho, valores de se trabalhar, trabalhar, trabalhar e \\nfazer aquilo que se tem “obrigação” de se fazer, sem saber viver \\naquilo que se tem para viver, pois nunca viveu não sabendo \\nviver sem aquilo, quepoderia ter o feito feliz por nunca ter \\nvivido aquilo que ele poderia ter vivido que ele poderia ter \\nsido feliz…\\nRegras são para conter a merda de quem faz merda…\\nRegras não são feitas para deixarmos de viver!!!\\nNós não sabemos como viver, não viemos com manual de \\ninstrução, estamos em uma evolução e adaptação de como se \\nviver… Os erros são para serem consertados e não repetidos, se \\nnão conseguimos viver e perceber que estamos em um trajeto \\nde adaptação e evolução junto ao mundo, nunca vamos conse -\\nguir viver em harmonia de um viver!!!\\nVocê vê a realidade do jeito quevocê quer ver?\\nTodos nós não sabemos como o outro é, pois assim como as \\npessoas não sabem da sua vida, das suas dores você não sabe da \\nvida do outro e nem das dores do outro.\\nSe eu não temo a verdade, se eu não temo pelo o que eu \\nsou, porque esconder sobre o que sou e me omitir diante da \\nverdade?\\nNós queremos julgar e não queremos ser julgados. Antes \\nde falar de esquerda, direita e qualquer outra coisa, avalia a sua \\nSem título-1   21Sem título-1   21 17/03/2022   15:08:3417/03/2022   15:08:34",
      "position": 21744,
      "chapter": 1,
      "page": 21,
      "segment_type": "page",
      "themes": {},
      "difficulty": 32.91265133171913,
      "complexity_metrics": {
        "word_count": 236,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 33.714285714285715,
        "avg_word_length": 4.436440677966102,
        "unique_word_ratio": 0.5889830508474576,
        "avg_paragraph_length": 236.0,
        "punctuation_density": 0.1271186440677966,
        "line_break_count": 23,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "viver",
          "aquilo",
          "como",
          "trabalhar",
          "nunca",
          "outro",
          "fazer",
          "pois",
          "feliz",
          "vivido",
          "poderia",
          "regras",
          "merda",
          "sabemos",
          "estamos",
          "evolução",
          "adaptação",
          "você",
          "vida",
          "dores"
        ],
        "entities": [
          [
            "21",
            "CARDINAL"
          ],
          [
            "de se trabalhar",
            "PERSON"
          ],
          [
            "não sabendo",
            "GPE"
          ],
          [
            "quepoderia",
            "GPE"
          ],
          [
            "Regras",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "merda",
            "PERSON"
          ],
          [
            "Regras",
            "PERSON"
          ],
          [
            "para deixarmos de viver",
            "PERSON"
          ],
          [
            "adaptação de como se \\nviver",
            "ORG"
          ]
        ],
        "readability_score": 81.8119249394673,
        "semantic_density": 0,
        "word_count": 236,
        "unique_words": 139,
        "lexical_diversity": 0.5889830508474576
      },
      "preservation_score": 1.81119232278267e-05
    },
    {
      "id": 1,
      "text": "— 22 —própria vida e os seus erros, para ver que a sua vida é de maior \\nexemplo daqueles quevocêesperavaser maior exemplo…\\nO que é confiança?\\nQuantos “tipos” de confiança existem? Você é perfeito?\\nVocê confia em você para fazer tudo?\\nSe você precisa de algo, você confia no profissional que es -\\ntudou ou você confia em quem você confia?\\nConfiança quando não se tem é um sinônimo da falta de \\nconfiança em si próprio… pois todos nós erramos e apren -\\ndemos, a confiança é uma conquista, não pelo erroe sim por \\nentender que aquela pessoavai me direcionar melhor do \\nque eu quando eu precisar dentro daquilo que ele me fez ter \\nconfiança.\\nSe você não confia em ninguém, se você não enxerga a con -\\nfiança, será que todos não são de confiança ou vocêestá inter -\\npretando errado oque é confiança?\\nSe vocêestá interpretando errado a confiança, quem não é \\nde confiança – você ou as pessoas quevocê não confia?\\nSe você é assaltante e vai assaltar algo em quem você vai \\nconfiar, em alguém que nunca assaltou ou em quem tem ex -\\nperiência? Se você precisa de um médico, em quem você vai \\nconfiar – no médico ou na sua mãe que faz simpatia? Kkkkkk\\nSem título-1   22Sem título-1   22 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 23164,
      "chapter": 1,
      "page": 22,
      "segment_type": "page",
      "themes": {},
      "difficulty": 25.344956413449566,
      "complexity_metrics": {
        "word_count": 219,
        "sentence_count": 11,
        "paragraph_count": 1,
        "avg_sentence_length": 19.90909090909091,
        "avg_word_length": 4.497716894977169,
        "unique_word_ratio": 0.5616438356164384,
        "avg_paragraph_length": 219.0,
        "punctuation_density": 0.1050228310502283,
        "line_break_count": 22,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "confiança",
          "confia",
          "quem",
          "vida",
          "maior",
          "exemplo",
          "precisa",
          "algo",
          "quando",
          "todos",
          "vocêestá",
          "errado",
          "confiar",
          "médico",
          "título",
          "própria",
          "seus",
          "erros",
          "daqueles"
        ],
        "entities": [
          [
            "22",
            "CARDINAL"
          ],
          [
            "para ver",
            "PERSON"
          ],
          [
            "perfeito",
            "PERSON"
          ],
          [
            "para fazer tudo",
            "PERSON"
          ],
          [
            "Se",
            "PERSON"
          ],
          [
            "precisa de algo",
            "ORG"
          ],
          [
            "Confiança",
            "GPE"
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
            "nós erramos",
            "FAC"
          ]
        ],
        "readability_score": 88.69613947696139,
        "semantic_density": 0,
        "word_count": 219,
        "unique_words": 123,
        "lexical_diversity": 0.5616438356164384
      },
      "preservation_score": 1.591976330718493e-05
    },
    {
      "id": 1,
      "text": "— 23 —Confiança não é um todo, confiança se conquista devido \\naquela pessoa sempre me mostrar confiança em ser aquilo que \\nprecisava quando precisei daquela pessoa.\\nNão generaliza a todos pela sua falta de confiança em um \\nviver com valores diferentes da sua própria confiança…\\nQual legado você irá deixar? Você se importa com a vida \\nquevocê tem? Quem te fez ter essa vida?\\nA sua vida importa para quem você se importa, pois o ama -\\nnhã quem irá pagar pela sua falta de importância serão as pes -\\nsoas quevocê ama.\\nNão deixe de viver uma vida mais digna possível, pois se \\nvocê se importa com quem você ama, o seu legado irá benefi -\\nciar ou prejudicar as pessoas com as quais você foi mais feliz \\nem sua vida!\\nTemos dois tipos de percepção perante a vida, temos o ra -\\ncional e o sentimental.\\nSentimental – aquele(a) que não consegue se controlar \\ndiante da energia que ele mais se importa (absorção da sua \\nprópria necessidade ou de um contexto), as tornando pessoas \\nfracas diante do sentimento.\\nSem título-1   23Sem título-1   23 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 24498,
      "chapter": 1,
      "page": 23,
      "segment_type": "page",
      "themes": {},
      "difficulty": 26.837529550827423,
      "complexity_metrics": {
        "word_count": 188,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 20.88888888888889,
        "avg_word_length": 4.6436170212765955,
        "unique_word_ratio": 0.6382978723404256,
        "avg_paragraph_length": 188.0,
        "punctuation_density": 0.09574468085106383,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "vida",
          "confiança",
          "importa",
          "quem",
          "mais",
          "pessoa",
          "pela",
          "falta",
          "viver",
          "própria",
          "legado",
          "quevocê",
          "pois",
          "pessoas",
          "temos",
          "sentimental",
          "diante",
          "título",
          "todo"
        ],
        "entities": [
          [
            "23",
            "CARDINAL"
          ],
          [
            "Confiança",
            "GPE"
          ],
          [
            "aquela pessoa sempre",
            "PERSON"
          ],
          [
            "mostrar confiança",
            "PERSON"
          ],
          [
            "quando precisei daquela pessoa",
            "PERSON"
          ],
          [
            "todos",
            "NORP"
          ],
          [
            "própria confiança",
            "ORG"
          ],
          [
            "Qual legado",
            "PERSON"
          ],
          [
            "irá deixar",
            "PERSON"
          ],
          [
            "Você se importa",
            "PERSON"
          ]
        ],
        "readability_score": 88.16247044917257,
        "semantic_density": 0,
        "word_count": 188,
        "unique_words": 120,
        "lexical_diversity": 0.6382978723404256
      },
      "preservation_score": 1.2769863615388982e-05
    },
    {
      "id": 1,
      "text": "— 24 —Racional – aquele(a) que não consegue ou tem dificulda -\\ndes em entender o sentimento do outro, as tornando pessoas \\ncalculistas, sem erros, confiança acima da maioria, prepotentes \\ncom a sua razão.\\nNão irei falar de qualidades, pois ambos os lados têm qua -\\nlidades e ambos os lados têm defeitos, nenhum lado é melhor \\nou pior… o melhor lado é saber administrar ambos os lados. \\nAnalogia – pega uma balança, coloca de um lado o sen -\\ntimento e do outro a razão…qual é o lado que tem um pe -\\nsar maior?\\nA sua preocupação é tão relativa …\\nUm fio pegando fogo para um eletricista, como ele irá rea -\\ngir perante o momento?\\nUma pessoa que sempre usou arma, como irá agir com \\numa arma?\\nUma pessoa que se sente?\\nUma pessoa que sempre teve “tudo”?\\nUma pessoa que nunca teve nada?\\nTodos nós temos percepções de acordo com a nossa necessi -\\ndade, o seu preconceito é tão ruim para os outros tanto quanto \\npara você, pois alguém pode estar te julgando da mesma for -\\nma quevocê o está julgando diante da sua própria vivência!!!\\nSão tantas obrigações que nos delegamos, que não con -\\nseguimos ter tempo para pensar em outra coisa a não ser no \\nSem título-1   24Sem título-1   24 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 25690,
      "chapter": 1,
      "page": 24,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 29.469730941704036,
      "complexity_metrics": {
        "word_count": 223,
        "sentence_count": 10,
        "paragraph_count": 1,
        "avg_sentence_length": 22.3,
        "avg_word_length": 4.3991031390134525,
        "unique_word_ratio": 0.6636771300448431,
        "avg_paragraph_length": 223.0,
        "punctuation_density": 0.1210762331838565,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "lado",
          "pessoa",
          "ambos",
          "lados",
          "outro",
          "razão",
          "pois",
          "melhor",
          "como",
          "sempre",
          "arma",
          "teve",
          "julgando",
          "título",
          "racional",
          "aquele",
          "consegue",
          "dificulda",
          "entender",
          "sentimento"
        ],
        "entities": [
          [
            "24",
            "CARDINAL"
          ],
          [
            "sem erros",
            "ORG"
          ],
          [
            "confiança",
            "GPE"
          ],
          [
            "acima da maioria",
            "PERSON"
          ],
          [
            "nenhum",
            "ORG"
          ],
          [
            "administrar ambos",
            "PERSON"
          ],
          [
            "Analogia",
            "GPE"
          ],
          [
            "coloca de um lado o",
            "ORG"
          ],
          [
            "lado",
            "PERSON"
          ],
          [
            "tão relativa",
            "PRODUCT"
          ]
        ],
        "readability_score": 87.53026905829597,
        "semantic_density": 0,
        "word_count": 223,
        "unique_words": 148,
        "lexical_diversity": 0.6636771300448431
      },
      "preservation_score": 2.1964165418469048e-05
    },
    {
      "id": 1,
      "text": "— 25 —próprio sistema padrão de viver, que não consigo entender por \\nqual motivo nos obrigamostanto em pensar…\\n“Aprenda a economizar hoje, para não economizar \\namanhã… ”\\nNeymar, Bill Gates, Whindersson Nunes, Anita… todos são \\ncapitalistas?\\nTodos trabalham e ganham seu dinheiro?\\nSe você for chamado para uma festa dessas pessoas, sendo \\n“contra o capitalismo” , você ia e ainda falava que era o seu me -\\nlhor amigo… vê a vida de outros não vivendo a vida de outros \\né fácil… difícil é vivermos e reconhecermosque o nosso mere -\\ncimento é simplesmente o nosso.\\nNão pense que o fulano deu sorte… não pense que a vida \\ndo outro é melhor ou pior que a sua, pensa que o capitalismo, \\nsocialismo etc.É necessário para todos nós termos uma aceita -\\nção de viver. Tudo no mundo é necessário, desde o mendigo e \\na pessoa mais rica do mundo, pois todos aprendemos uns com \\nos outros e iremos lutar uns pelos outros de acordo com nosso \\nmerecimento.\\nSem título-1   25Sem título-1   25 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 27023,
      "chapter": 1,
      "page": 25,
      "segment_type": "page",
      "themes": {},
      "difficulty": 31.985714285714284,
      "complexity_metrics": {
        "word_count": 175,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 25.0,
        "avg_word_length": 4.714285714285714,
        "unique_word_ratio": 0.6971428571428572,
        "avg_paragraph_length": 175.0,
        "punctuation_density": 0.12,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "todos",
          "outros",
          "vida",
          "nosso",
          "viver",
          "economizar",
          "você",
          "capitalismo",
          "pense",
          "necessário",
          "mundo",
          "título",
          "próprio",
          "sistema",
          "padrão",
          "consigo",
          "entender",
          "qual",
          "motivo",
          "obrigamostanto"
        ],
        "entities": [
          [
            "25",
            "CARDINAL"
          ],
          [
            "Aprenda",
            "ORG"
          ],
          [
            "para não",
            "PERSON"
          ],
          [
            "Neymar",
            "PERSON"
          ],
          [
            "Bill Gates",
            "PERSON"
          ],
          [
            "Whindersson Nunes",
            "ORG"
          ],
          [
            "Anita",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "ganham seu",
            "PERSON"
          ],
          [
            "Se",
            "PERSON"
          ]
        ],
        "readability_score": 86.08571428571429,
        "semantic_density": 0,
        "word_count": 175,
        "unique_words": 122,
        "lexical_diversity": 0.6971428571428572
      },
      "preservation_score": 1.2940128463594166e-05
    },
    {
      "id": 1,
      "text": "— 26 —Oque é capitalismo? Se você trabalha, ganha seu dinheiro \\nvocê é capitalista?\\nSe trabalhar ganhar o seu dinheiro é capitalismo, existe \\numa sociedade sem capitalismo? Se existisse uma sociedade a \\nqual não fosse capitalista, como seria? \\nMinha forma de ver o que é capitalismo: capitalismo é o \\nexcesso do consumo.\\nExemplo: o sistema do nosso mundo funciona através de \\ntrabalhar, ganhar o dinheiro de acordo com o seu trabalho e \\nviver de acordo com o nosso ganho… porque isso é capitalis -\\nmo e não um sistema que é necessário termos, para tentar vi -\\nver em paz com o merecimento de acordo com o seu mérito.\\nObservação: se nós humanos não sabemos viver, de quem é \\no problema, do capitalismo ou da falta de respeito perante um \\nao outro?\\nMaior problema do ser humano é o próprio ser humano… \\nsevocê pensa em algo, quem pensa por você? O maior proble -\\nma do ser humano é oquevocê mesmo pensa.\\nTrabalho para viver e não viver para o trabalho, porém para \\nse ter uma vida digna é necessário trabalhar.\\nSem título-1   26Sem título-1   26 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 28155,
      "chapter": 1,
      "page": 26,
      "segment_type": "page",
      "themes": {},
      "difficulty": 28.800962000962002,
      "complexity_metrics": {
        "word_count": 189,
        "sentence_count": 11,
        "paragraph_count": 1,
        "avg_sentence_length": 17.181818181818183,
        "avg_word_length": 4.650793650793651,
        "unique_word_ratio": 0.5925925925925926,
        "avg_paragraph_length": 189.0,
        "punctuation_density": 0.13756613756613756,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "capitalismo",
          "viver",
          "você",
          "dinheiro",
          "trabalhar",
          "acordo",
          "trabalho",
          "humano",
          "pensa",
          "capitalista",
          "ganhar",
          "sociedade",
          "sistema",
          "nosso",
          "necessário",
          "quem",
          "problema",
          "maior",
          "título",
          "oque"
        ],
        "entities": [
          [
            "26",
            "CARDINAL"
          ],
          [
            "capitalista",
            "PERSON"
          ],
          [
            "Se",
            "PERSON"
          ],
          [
            "fosse",
            "ORG"
          ],
          [
            "como seria",
            "ORG"
          ],
          [
            "Minha forma de ver",
            "PERSON"
          ],
          [
            "dinheiro de acordo",
            "ORG"
          ],
          [
            "necessário termos",
            "ORG"
          ],
          [
            "para tentar vi -\\n",
            "PERSON"
          ],
          [
            "merecimento de acordo",
            "ORG"
          ]
        ],
        "readability_score": 90.01385281385281,
        "semantic_density": 0,
        "word_count": 189,
        "unique_words": 112,
        "lexical_diversity": 0.5925925925925926
      },
      "preservation_score": 1.404684997692788e-05
    },
    {
      "id": 1,
      "text": "— 27 —Até que ponto você precisa ter uma vida perante a quan -\\ntidade ou qualidade do trabalho? Até que ponto é necessário \\nvocê ter algo perante um viver?\\nEuMarcelo vejo da seguinte forma: tenho uma casa, comi -\\nda, família, amigos, uma boa cama, uma boa TV , carro.\\nOque é mais necessário na vida?A partir desse ponto o que \\neu preciso mais?\\nVocê precisa de mais dinheiro ou mais tempo? Você ga -\\nnhando mais dinheiro, o quevocê terá de mais valor ou mais \\nfelicidade do quevocê já tem?\\nHoje eu penso que a minha maior evolução é ter mais tem -\\npo para viver.\\nDe que adianta eu querer mais sem saber viver com mais?O \\ncrescer na vida é involuntário a partir do momento em que \\nvocê para de pensar na fome (estrutura familiar), só assimvocê \\npensa em evoluir o seu melhor viver!!!\\nJá parou para pensar o quanto você já estudou, o quanto \\nvocê esqueceu o que já estudou, que às vezes do nada você \\nlembra que já estudou, voltando a perceber o quanto você não \\npercebeu sobre o quevocêmesmo jáestudou?\\nResumo de tanto estudo…\\nNinguém sabe o que o outro sabe, ninguém sabe o quanto \\no outro é bom ou ruim, ninguém sabe o quanto as pessoas \\nsabem sobre um viver, pois ninguém lembra do queestudou \\nSem título-1   27Sem título-1   27 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 29356,
      "chapter": 1,
      "page": 27,
      "segment_type": "page",
      "themes": {},
      "difficulty": 27.56623188405797,
      "complexity_metrics": {
        "word_count": 230,
        "sentence_count": 12,
        "paragraph_count": 1,
        "avg_sentence_length": 19.166666666666668,
        "avg_word_length": 4.447826086956522,
        "unique_word_ratio": 0.5826086956521739,
        "avg_paragraph_length": 230.0,
        "punctuation_density": 0.1391304347826087,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "você",
          "viver",
          "quanto",
          "ninguém",
          "sabe",
          "ponto",
          "vida",
          "estudou",
          "precisa",
          "perante",
          "necessário",
          "partir",
          "dinheiro",
          "quevocê",
          "pensar",
          "lembra",
          "outro",
          "título",
          "quan"
        ],
        "entities": [
          [
            "27",
            "CARDINAL"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "EuMarcelo",
            "PERSON"
          ],
          [
            "da seguinte forma",
            "PERSON"
          ],
          [
            "mais necessário",
            "PERSON"
          ],
          [
            "Você ga -\\nnhando mais dinheiro",
            "PERSON"
          ],
          [
            "quevocê terá de mais",
            "PERSON"
          ],
          [
            "quevocê já tem",
            "PERSON"
          ],
          [
            "Hoje eu",
            "PERSON"
          ],
          [
            "eu querer mais sem",
            "PERSON"
          ]
        ],
        "readability_score": 89.08231884057972,
        "semantic_density": 0,
        "word_count": 230,
        "unique_words": 134,
        "lexical_diversity": 0.5826086956521739
      },
      "preservation_score": 2.1453370873853485e-05
    },
    {
      "id": 1,
      "text": "— 28 —(o acessar não quer dizer que você compreendeu) … Você acha \\nque na vida (viver) você vai ser diferente?\\nVivemos e não compreendemos,pois não compreendemos \\no que é viver, pois estamos tão focados em nosso querer, por \\nmal conseguir compreender o nosso próprio querer viver, es -\\nquecendo o querer viverem um contexto!!\\nCuriosidades da vida!!!\\nSe você não resolveu um problema quevocê achou que ti -\\nnha “resolvido” ou deixou o “tempo resolver” , porém futura -\\nmente esse mesmo problema aconteceu com o seu filho, como \\nvocê irá ajudar se você mesmo ficou omisso com o mesmo \\nproblema quevocêteve? Como vocêo ajuda a resolver?\\nDá a “solução” do problema igual ao que você fez?Apren -\\nde junto com ele?Briga pela situação e tenta resolver?Conversa \\ncom ele e conversa com todos os envolvidos?Luta pelos seus \\ndireitos de acordo com o que a sociedade impõe como certo?\\nTodas essas variações, devido a você não limitar ou resolver \\no problema que aconteceu com você mesmo, pois se você en -\\nsinar a quem você ama a não sofrer pelo mesmo, porque ele \\niria sofrer?\\nBullying, racismo, gordofobia, homofobia, tudo que en -\\ngloba o menosprezo do mesmo quevocê ama poderia ser \\nevitado por vocêao ensinar como agir diante do mesmo \\nSem título-1   28Sem título-1   28 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 30743,
      "chapter": 1,
      "page": 28,
      "segment_type": "page",
      "themes": {},
      "difficulty": 25.7574200913242,
      "complexity_metrics": {
        "word_count": 219,
        "sentence_count": 12,
        "paragraph_count": 1,
        "avg_sentence_length": 18.25,
        "avg_word_length": 4.885844748858448,
        "unique_word_ratio": 0.6484018264840182,
        "avg_paragraph_length": 219.0,
        "punctuation_density": 0.1415525114155251,
        "line_break_count": 23,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "mesmo",
          "problema",
          "resolver",
          "como",
          "viver",
          "pois",
          "querer",
          "vida",
          "compreendemos",
          "nosso",
          "quevocê",
          "aconteceu",
          "conversa",
          "sofrer",
          "título",
          "acessar",
          "quer",
          "dizer",
          "compreendeu"
        ],
        "entities": [
          [
            "28",
            "CARDINAL"
          ],
          [
            "acessar não quer",
            "ORG"
          ],
          [
            "Você acha \\nque",
            "PERSON"
          ],
          [
            "Vivemos",
            "PERSON"
          ],
          [
            "querer viverem",
            "PERSON"
          ],
          [
            "Se",
            "PERSON"
          ],
          [
            "resolver?Conversa",
            "ORG"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "pelos",
            "PERSON"
          ],
          [
            "Todas",
            "PERSON"
          ]
        ],
        "readability_score": 89.40924657534246,
        "semantic_density": 0,
        "word_count": 219,
        "unique_words": 142,
        "lexical_diversity": 0.6484018264840182
      },
      "preservation_score": 2.496508336808545e-05
    },
    {
      "id": 1,
      "text": "— 29 —ocorrido, quevocê mesmo não teve iniciativa e sabedoria pa -\\nradar ou resolver quando era para ser resolvido com a sua pró -\\npria pessoa!!!\\nSe nós não aprendemos a viver no mundo, o mundo irá te \\nengolir.\\nNão adianta dar a “melhor criação” se você não sabe ensi -\\nnar a melhor criação que é necessária para o mundo. O mun -\\ndo não vai se adaptar a vocêporquevocê quer, o mundo vai \\ncontinuar sendo o que é independente de você… faça diferen -\\nte, lute para viver melhor, ensine as pessoas a viverem melhor, \\npois assim como você não sabe a solução, “o outro não sabe o \\nque está fazendo… ” .\\nAs pessoas estão tão preocupadas com a sua vida que o vi -\\nver do outro está errado perante o meu viver…\\nTá chato, preocupante, caótico,prepotente, falso moralismo, \\nhipócrita tudo é errado, tudo não pode, tudo tem que ser de \\numa forma que não possa incomodar ninguém…quer viver \\nperfeitamente? Morra e vá para o céu… lá ninguém vai ter \\nsexo, não vai ter roubo, não vai ter disputa, não vai ter confli -\\ntos… Se eu tivesse tudoque eu quero eu não saberia dar valor \\npara o que é bom para mim mesmo.\\nSe você não quer barulho, não quer crianças brincando, \\nnão quer festa, não quer beber, não quer futebol só por achar \\nque o estudar ou ser “inteligente” o torna melhor a alguém? \\nSem título-1   29Sem título-1   29 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 32165,
      "chapter": 1,
      "page": 29,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 31.810843373493977,
      "complexity_metrics": {
        "word_count": 249,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 31.125,
        "avg_word_length": 4.3694779116465865,
        "unique_word_ratio": 0.6104417670682731,
        "avg_paragraph_length": 249.0,
        "punctuation_density": 0.13654618473895583,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quer",
          "melhor",
          "viver",
          "mundo",
          "você",
          "sabe",
          "tudo",
          "mesmo",
          "criação",
          "pessoas",
          "outro",
          "está",
          "errado",
          "ninguém",
          "título",
          "ocorrido",
          "quevocê",
          "teve",
          "iniciativa",
          "sabedoria"
        ],
        "entities": [
          [
            "29",
            "CARDINAL"
          ],
          [
            "quevocê mesmo",
            "ORG"
          ],
          [
            "pria",
            "GPE"
          ],
          [
            "Se",
            "PERSON"
          ],
          [
            "ensi -\\n",
            "PERSON"
          ],
          [
            "outro",
            "ORG"
          ],
          [
            "tão",
            "ORG"
          ],
          [
            "preocupadas",
            "ORG"
          ],
          [
            "Morra",
            "PERSON"
          ],
          [
            "Se eu",
            "PERSON"
          ]
        ],
        "readability_score": 83.12665662650602,
        "semantic_density": 0,
        "word_count": 249,
        "unique_words": 152,
        "lexical_diversity": 0.6104417670682731
      },
      "preservation_score": 2.6050521775393518e-05
    },
    {
      "id": 1,
      "text": "— 30 —Está fudido!!!Pois sua energia se propaga em uma forma cons -\\ntante sem retorno, se você não souber viver o que adianta es -\\ntar vivo?\\nSe não sabe viver e pensa que o seu jeito de viver é o me -\\nlhor, viva sozinho sem perturbar ninguém, pois ninguém quer \\nfalar com você se você não quiser falar com ninguém.\\nBeber uma cerveja com amigos, vendo o jogo, fumando um \\nbaseado, rindo à beçacom todos e talvez fazer um churrasco… \\nIsso é merecimento devido ao meu trabalho, que eu usufruo \\nde benefício para o meu melhor viver.\\nRegra da vida!!\\nTrabalhar, ganhar dinheiro e viver sem prejudicar a \\nninguém!!!\\nSe você está vendo que o seu viver tá atrapalhando alguém \\nou incomodando alguém, avalie as suas ações, pois nem sem -\\npre o seu viver é certo e nem sempre o seu incômodo é o certo.\\nAprendi…\\nA dizer não!!\\nNão posso!!\\nAmanhã eu faço!!!\\nMe afastar!!\\nA limitar!!!\\nSua vida é sua. Suas consequências são suas. Ninguém sa -\\nberá o quevocê ou eu estamos passando, não somos o centro \\nSem título-1   30Sem título-1   30 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 33636,
      "chapter": 1,
      "page": 30,
      "segment_type": "page",
      "themes": {},
      "difficulty": 22.773958333333333,
      "complexity_metrics": {
        "word_count": 192,
        "sentence_count": 15,
        "paragraph_count": 1,
        "avg_sentence_length": 12.8,
        "avg_word_length": 4.46875,
        "unique_word_ratio": 0.6875,
        "avg_paragraph_length": 192.0,
        "punctuation_density": 0.21354166666666666,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "viver",
          "ninguém",
          "você",
          "pois",
          "suas",
          "está",
          "falar",
          "vendo",
          "vida",
          "alguém",
          "certo",
          "título",
          "fudido",
          "energia",
          "propaga",
          "forma",
          "cons",
          "tante",
          "retorno",
          "souber"
        ],
        "entities": [
          [
            "30",
            "CARDINAL"
          ],
          [
            "você não",
            "ORG"
          ],
          [
            "Se",
            "PERSON"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "jeito de viver",
            "PERSON"
          ],
          [
            "viva",
            "ORG"
          ],
          [
            "Beber",
            "PERSON"
          ],
          [
            "jogo",
            "GPE"
          ],
          [
            "beçacom",
            "ORG"
          ],
          [
            "todos",
            "CARDINAL"
          ]
        ],
        "readability_score": 92.259375,
        "semantic_density": 0,
        "word_count": 192,
        "unique_words": 132,
        "lexical_diversity": 0.6875
      },
      "preservation_score": 2.553972723077796e-05
    },
    {
      "id": 1,
      "text": "— 31 —do universo para brigar, exigir, gritar, estressar com quem nem \\nsabe oquevocêpossa estar passando ou eu estou passando, se -\\njamos racionais perante a situação, não desconte sua dor…sua \\ncompreensão diante do momento, pensando no momento em \\nque o outro não estava, pensa, repense, avalie e aja para sempre \\nvoltar aquela energia quevocê mandou necessária no momen -\\nto necessário… Um dia aquela mesma pessoa que brigou, gri -\\ntou, agrediu vai entender que aquela energia quevocê enviou \\npara elevai retornar para você, e aquela energia que ele enviou \\npara você irá retornar para ele.\\nDeus existe?\\nDeus existe para si próprio…\\nComo assim? Deus é uma energia, ele sendo uma energia \\nlogo eu penso em energia.\\nSe Deus é energia e nós temos uma energia de contenção \\ndo caos gerado pelo próprio caos, que o próprio universo cau -\\nsa (movimento, buraco negro, explosão solares, encontro de \\ngaláxias…) em adaptação de si próprio, gerando uma energia \\nonipresente, e sentida por tudo quehá no universo, na forma \\nde um se adaptar à energia do outro, em constante adaptação \\ne evolução… Sim, Deus existe perante a sua própria interpreta -\\nção e a bíblia é oensinamento de saber movimen tar-se.\\nDeus existe para você.\\nSem título-1   31Sem título-1   31 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 34815,
      "chapter": 1,
      "page": 31,
      "segment_type": "page",
      "themes": {},
      "difficulty": 31.71287726358149,
      "complexity_metrics": {
        "word_count": 213,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 30.428571428571427,
        "avg_word_length": 4.995305164319249,
        "unique_word_ratio": 0.6666666666666666,
        "avg_paragraph_length": 213.0,
        "punctuation_density": 0.15023474178403756,
        "line_break_count": 23,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "deus",
          "aquela",
          "existe",
          "próprio",
          "universo",
          "você",
          "passando",
          "perante",
          "momento",
          "outro",
          "quevocê",
          "enviou",
          "retornar",
          "caos",
          "adaptação",
          "título",
          "brigar",
          "exigir",
          "gritar"
        ],
        "entities": [
          [
            "31",
            "CARDINAL"
          ],
          [
            "universo para brigar",
            "PERSON"
          ],
          [
            "exigir",
            "GPE"
          ],
          [
            "quem nem",
            "PERSON"
          ],
          [
            "oquevocêpossa estar",
            "ORG"
          ],
          [
            "eu estou passando",
            "PERSON"
          ],
          [
            "situação",
            "GPE"
          ],
          [
            "não desconte sua dor…",
            "PERSON"
          ],
          [
            "outro não estava",
            "PRODUCT"
          ],
          [
            "para sempre",
            "PERSON"
          ]
        ],
        "readability_score": 83.28712273641851,
        "semantic_density": 0,
        "word_count": 213,
        "unique_words": 142,
        "lexical_diversity": 0.6666666666666666
      },
      "preservation_score": 2.1538503297956076e-05
    },
    {
      "id": 1,
      "text": "— 32 —Para outros, Deus existe de acordo com o seu próprio caos \\na se adaptar ao caos do universo!!!Deus é a energia quevocê \\nconsegue acessar perante o caos quevocê mesmo vive!!!\\nPalavras de um ATEU perante a Deus.\\nNão é porque sou ATEUque não irei compreender você!!!\\nNão é porque sou ATEUque serei uma pessoa ruim!!\\nNão é porque sou ATEU que não irei amar!! \\nNão é porque sou ATEU que não saberei respeitar!!\\nO ateu ama, fica triste, fica feliz, trabalha, curte, vive, briga, \\nerra igual a todos que seguem aqualquer entidade ou a Deus!!!\\nPreconceito racial!!\\nEstamos em evolução, nosso pensamento pode ser mais \\nevoluído do que o outro, em alguns aspectos que eu vivi pe -\\nrante o caos quevocê viveu. O seu pensamento diante da sua \\ndor é muito mais revoltante do que quem não sofreu com essa \\nmesma dor…\\nPrimeira pergunta que se deve fazer é:oque é preciso para \\numa família ter uma estrutura familiar?Como se consegue ter \\numa estrutura familiar?\\nAntes de “abolir” a escravidão, como os negros viviam na \\narte, escrita, história, poder na sociedade, marketing perante \\na sociedade, visual perante a sociedade?Após o “término” da \\nescravidão, como os negros arrumaram empregos?\\nSem título-1   32Sem título-1   32 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 36226,
      "chapter": 1,
      "page": 32,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 29.52323717948718,
      "complexity_metrics": {
        "word_count": 208,
        "sentence_count": 15,
        "paragraph_count": 1,
        "avg_sentence_length": 13.866666666666667,
        "avg_word_length": 4.966346153846154,
        "unique_word_ratio": 0.6394230769230769,
        "avg_paragraph_length": 208.0,
        "punctuation_density": 0.23076923076923078,
        "line_break_count": 23,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "deus",
          "caos",
          "perante",
          "ateu",
          "porque",
          "quevocê",
          "como",
          "sociedade",
          "consegue",
          "vive",
          "ateuque",
          "irei",
          "fica",
          "pensamento",
          "mais",
          "estrutura",
          "familiar",
          "escravidão",
          "negros",
          "título"
        ],
        "entities": [
          [
            "32",
            "CARDINAL"
          ],
          [
            "Para",
            "PRODUCT"
          ],
          [
            "Deus",
            "PERSON"
          ],
          [
            "Palavras",
            "PERSON"
          ],
          [
            "fica",
            "GPE"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "Preconceito",
            "PERSON"
          ],
          [
            "Estamos",
            "PERSON"
          ],
          [
            "que eu vivi",
            "PERSON"
          ],
          [
            "diante da sua",
            "PERSON"
          ]
        ],
        "readability_score": 91.57676282051283,
        "semantic_density": 0,
        "word_count": 208,
        "unique_words": 133,
        "lexical_diversity": 0.6394230769230769
      },
      "preservation_score": 2.7902151999624914e-05
    },
    {
      "id": 1,
      "text": "— 33 —Para você melhorar seu valor monetário, como você vai \\nnegociar valores maiores com quem não confia em você?Ao \\ndecorrer do fim da escravidão, como os negros conseguiram \\nevoluir na sociedade?\\nHoje, negros estão começando a usufruir de uma estrutu -\\nra familiar, devido a nunca conseguir ter poder ou mesmo ter \\nabertura no meio social necessário para ter uma vida melhor, \\ne conseguir proporcionar uma vida melhor para quem está à \\nsua volta (negros).\\nDurante séculos nós fomos criados com artes de pessoas \\nbrancas (racistas) que exaltavama cor branca pela necessidade \\nde ter e ser melhor (época)que os negros… na entrada do sé -\\nculo 20 nós começamos a era do início da tecnologia, abrindo \\ne expandindo o marketing e a publicidade, gerando mais con -\\nforto visual do que tínhamos antes devido só ter arte branca \\n(Cristo Redentor), gerando um conforto visual perante a cor \\nbranca.\\nNão temos como brigar com todos, no final todos nós te -\\nmos o racismo involuntário dentro de nós mesmos sem perce -\\nbermos… O filho de rico branco não tem culpa de o passado \\npelo passado ter dado uma melhor estrutura familiar. Nenhu -\\nma pessoa que ama o próximo vai ter racismo perante o outro, \\nassim como ele não tem culpa do racismo o colocar na socie -\\ndade onde ele está!!\\nO lutar contra racismo, feminismos, gênero, religioso, so -\\ncial pode te transformar em uma pessoa mais preconceituosa, \\no preconceito quevocê mesmo está lutando contra para o seu \\npróprio benefício…\\nSem título-1   33Sem título-1   33 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 37601,
      "chapter": 1,
      "page": 33,
      "segment_type": "page",
      "themes": {
        "ciencia": 30.232558139534888,
        "arte": 46.51162790697674,
        "tecnologia": 23.25581395348837
      },
      "difficulty": 39.171756978653534,
      "complexity_metrics": {
        "word_count": 261,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 37.285714285714285,
        "avg_word_length": 4.85823754789272,
        "unique_word_ratio": 0.6551724137931034,
        "avg_paragraph_length": 261.0,
        "punctuation_density": 0.09961685823754789,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "como",
          "negros",
          "melhor",
          "racismo",
          "você",
          "está",
          "branca",
          "quem",
          "familiar",
          "devido",
          "conseguir",
          "mesmo",
          "vida",
          "gerando",
          "mais",
          "visual",
          "perante",
          "todos",
          "culpa",
          "passado"
        ],
        "entities": [
          [
            "33",
            "CARDINAL"
          ],
          [
            "Para",
            "PRODUCT"
          ],
          [
            "monetário",
            "PERSON"
          ],
          [
            "Hoje",
            "PERSON"
          ],
          [
            "começando",
            "PRODUCT"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "Durante",
            "PERSON"
          ],
          [
            "exaltavama",
            "GPE"
          ],
          [
            "cor",
            "ORG"
          ],
          [
            "20",
            "CARDINAL"
          ]
        ],
        "readability_score": 79.89967159277504,
        "semantic_density": 0,
        "word_count": 261,
        "unique_words": 171,
        "lexical_diversity": 0.6551724137931034
      },
      "preservation_score": 2.7412640561035012e-05
    },
    {
      "id": 1,
      "text": "— 34 —Todos nós sabemos que é errado o julgamento preconcei -\\ntuoso, você lutar dessa forma na década de90 para trás, de uma \\nforma mais agressiva é uma coisa, você lutar de uma forma ra -\\ncional nos tempos modernos, onde todos nós sabemos o que é \\nerrado perante ao preconceito é outra!!!\\nQuando você encontra alguém muito inteligente, burro, \\nfamoso, rico, pobre, culto, “família tradicional” , como você se \\ncomporta no modo de falar, no modo de se sentir à vontade \\ncom o outro, como você fica?\\nDiante dessa pergunta e perante a sua resposta, você sabia \\nquetodo mundo pode ter a resposta sobre “tudo”?\\nQuandovocê quer fazer alguma comida, onde você \\nprocura?\\nMexer no carro?\\nTelefone? \\nPlantar?\\nConstruir?\\nDemolir?\\nDestruir?\\nGoogle, basta você ter interesse e aprender, pois, através do \\nseu próprio interesse você entenderá (de acordo com o meio \\nem quevocê vive) as suas respostas diante das suas próprias \\nperguntas…\\nSem título-1   34Sem título-1   34 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 39267,
      "chapter": 1,
      "page": 34,
      "segment_type": "page",
      "themes": {},
      "difficulty": 25.885858585858585,
      "complexity_metrics": {
        "word_count": 162,
        "sentence_count": 11,
        "paragraph_count": 1,
        "avg_sentence_length": 14.727272727272727,
        "avg_word_length": 5.074074074074074,
        "unique_word_ratio": 0.7345679012345679,
        "avg_paragraph_length": 162.0,
        "punctuation_density": 0.20987654320987653,
        "line_break_count": 23,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "forma",
          "todos",
          "sabemos",
          "errado",
          "lutar",
          "dessa",
          "onde",
          "perante",
          "como",
          "modo",
          "diante",
          "resposta",
          "interesse",
          "suas",
          "título",
          "julgamento",
          "preconcei",
          "tuoso",
          "década"
        ],
        "entities": [
          [
            "34",
            "CARDINAL"
          ],
          [
            "Todos",
            "ORG"
          ],
          [
            "julgamento",
            "ORG"
          ],
          [
            "de90",
            "PRODUCT"
          ],
          [
            "você lutar de uma forma",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "nós sabemos o que",
            "ORG"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "muito inteligente",
            "PERSON"
          ],
          [
            "rico",
            "LAW"
          ]
        ],
        "readability_score": 91.11414141414141,
        "semantic_density": 0,
        "word_count": 162,
        "unique_words": 119,
        "lexical_diversity": 0.7345679012345679
      },
      "preservation_score": 2.25175261751359e-05
    },
    {
      "id": 1,
      "text": "— 35 —Nem todos conseguem interpretar e compreender uma \\nfrase, um texto, uma imagem… nem todos têm a sua mente \\nque criou aquela frase, texto, uma imagem, pois foi você quem \\ncriou, tem um sentimento perante aquilo quevocê mesmo fez, \\nnem todos viveram um mundo parecido ao seu, porém todos \\npodem se perguntar no Google oque é certo ou errado diante \\nda sua própria vida e a vida do outro!!!\\nApós ler esse texto, como você se comporta perante o seu \\nincômodo diante do outro?\\nVocê tem medo de se comportar e falar do jeito quevocê já \\né acostumado de viver na frente de todos? Quem está errado -\\nvocê ou a pessoa que nem teconhece?\\nPor muitas vezes essa pessoa é“maisimportantena socie -\\ndade” , perante oquevocê mesmo julgou no seu pensamento, \\nafetando o seu comportamento em uma forma de incômodo \\nperante ao outro quevocê nem conhece…\\nOque mais causa doenças na sociedade ao ser ingerido?\\nSalgadinhos de pacote. Salgadinhos de pacote geralmente \\nsão ricos em gorduras do tipo vegetal hidrogenada (gordura \\ntrans).\\nSem título-1   35Sem título-1   35 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 40384,
      "chapter": 1,
      "page": 35,
      "segment_type": "page",
      "themes": {},
      "difficulty": 27.85192307692308,
      "complexity_metrics": {
        "word_count": 182,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 22.75,
        "avg_word_length": 4.923076923076923,
        "unique_word_ratio": 0.6813186813186813,
        "avg_paragraph_length": 182.0,
        "punctuation_density": 0.13186813186813187,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "todos",
          "você",
          "perante",
          "texto",
          "quevocê",
          "outro",
          "frase",
          "imagem",
          "criou",
          "quem",
          "mesmo",
          "oque",
          "errado",
          "diante",
          "vida",
          "incômodo",
          "pessoa",
          "salgadinhos",
          "pacote",
          "título"
        ],
        "entities": [
          [
            "35",
            "CARDINAL"
          ],
          [
            "nem todos",
            "PERSON"
          ],
          [
            "aquela frase",
            "PERSON"
          ],
          [
            "quevocê mesmo",
            "PERSON"
          ],
          [
            "fez",
            "DATE"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "Google",
            "ORG"
          ],
          [
            "Após",
            "PERSON"
          ],
          [
            "medo de se",
            "PERSON"
          ],
          [
            "jeito quevocê já",
            "PERSON"
          ]
        ],
        "readability_score": 87.14807692307693,
        "semantic_density": 0,
        "word_count": 182,
        "unique_words": 124,
        "lexical_diversity": 0.6813186813186813
      },
      "preservation_score": 1.4472512097440844e-05
    },
    {
      "id": 1,
      "text": "— 36 —Bolacha recheada.\\nEmbutidos.\\nRefrigerante.\\nMacarrão instantâneo.\\nSódio, açúcar e gordura…\\nQual droga faz mais mal?\\nNão confundam drogas ilícitas como maior fazedor de mal \\nao seu corpo e ao seu viver…\\nQualquer droga, seja ela ilícita ou lícita, se você não souber \\nusar irá te fazer mal.\\nVocê mesmo irá julgar a maconha perante o salgadinho, re -\\nfrigerante, miojo…\\nPor qual motivo a maconha não é liberado?Qual foi o moti -\\nvo da maconha ser uma droga ilícita?A maconha faz bem para \\nalguma coisa?A maconha trata de doenças?\\nFaça essas mesmas perguntasao sódio, açúcar e gordura…\\nNunca subjugar a felicidade de alguém perante a sua fe -\\nlicidade…\\nPobre, rico, homem, mulher, casado, solteiro, todos nós so -\\nmos felizes de acordo com o que vivemos, não pense que todos \\ntêm que ser felizes da forma quevocê pensa que é a forma certa \\nde ser feliz.\\nFelicidade está em viver. Se você almeja o viver de outro \\nalguém será realmente quevocê está vivendo ou sobrevivendo? \\nSem título-1   36Sem título-1   36 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 41596,
      "chapter": 1,
      "page": 36,
      "segment_type": "page",
      "themes": {},
      "difficulty": 22.862175324675327,
      "complexity_metrics": {
        "word_count": 176,
        "sentence_count": 14,
        "paragraph_count": 1,
        "avg_sentence_length": 12.571428571428571,
        "avg_word_length": 4.8977272727272725,
        "unique_word_ratio": 0.7272727272727273,
        "avg_paragraph_length": 176.0,
        "punctuation_density": 0.17045454545454544,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "maconha",
          "qual",
          "droga",
          "viver",
          "você",
          "sódio",
          "açúcar",
          "gordura",
          "ilícita",
          "perante",
          "felicidade",
          "alguém",
          "todos",
          "felizes",
          "forma",
          "quevocê",
          "está",
          "título",
          "bolacha",
          "recheada"
        ],
        "entities": [
          [
            "36",
            "CARDINAL"
          ],
          [
            "Refrigerante",
            "PERSON"
          ],
          [
            "Macarrão",
            "ORG"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "Qualquer",
            "PERSON"
          ],
          [
            "você não",
            "ORG"
          ],
          [
            "mal",
            "PERSON"
          ],
          [
            "irá julgar",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "Faça",
            "GPE"
          ]
        ],
        "readability_score": 92.24496753246753,
        "semantic_density": 0,
        "word_count": 176,
        "unique_words": 128,
        "lexical_diversity": 0.7272727272727273
      },
      "preservation_score": 1.941019269539125e-05
    },
    {
      "id": 1,
      "text": "— 37 —Tudo na vida tem algo que se possa aproveitar, se você não \\nenxerga dessa forma, você nunca será feliz vivendo a vida de \\noutro, muito menos a sua própria vida… veja os valores ne -\\ncessários dentro do quevocê viveu, pois se você não viveu, \\ncomo você saberá que a felicidade em viver aquilo quevocê \\nnão viveu?\\nTodos nós deveríamos conseguir compreender Maquiavel e \\nWiliamShakespeare, pois tudo quehá amor há ódio…\\nMaquiavel passou a visão da dor perante vocêpara não ter \\nnecessidade de sentir a dor (contexto)… Shakespeare explicou \\no amor com muito amor sem o caos de um contexto e sim de \\nsi próprio… Quem ensinou mais sobre o amor, Maquiavel ou \\nShakespeare?\\nSou perfeccionista nas coisas que são irreparáveis…\\nTem sentimentos por coisas materiais irreparáveis… Tem \\nsentimentos por coisas sentimentais irreparáveis…\\nA sua importância é relativa de acordo com o quevocê vi -\\nveu, como você viveu, como você enxergou o quevocê viveu e \\ncomo você absorveu tudoquevocê viveu… Cada um tem a sua \\nimportância diante de um viver, se o seu viver não prejudica o \\nseu viver e o outro viver,viva!!!\\nSem título-1   37Sem título-1   37 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 42763,
      "chapter": 1,
      "page": 37,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.493814432989694,
      "complexity_metrics": {
        "word_count": 194,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 48.5,
        "avg_word_length": 4.979381443298969,
        "unique_word_ratio": 0.634020618556701,
        "avg_paragraph_length": 194.0,
        "punctuation_density": 0.10309278350515463,
        "line_break_count": 21,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "viveu",
          "viver",
          "quevocê",
          "como",
          "amor",
          "vida",
          "maquiavel",
          "coisas",
          "irreparáveis",
          "tudo",
          "outro",
          "muito",
          "pois",
          "contexto",
          "shakespeare",
          "sentimentos",
          "importância",
          "título",
          "algo"
        ],
        "entities": [
          [
            "37",
            "CARDINAL"
          ],
          [
            "dessa forma",
            "PERSON"
          ],
          [
            "muito menos",
            "PERSON"
          ],
          [
            "sua própria",
            "ORG"
          ],
          [
            "quevocê viveu",
            "PERSON"
          ],
          [
            "Todos",
            "GPE"
          ],
          [
            "WiliamShakespeare",
            "ORG"
          ],
          [
            "tudo quehá",
            "PERSON"
          ],
          [
            "Shakespeare",
            "PERSON"
          ],
          [
            "muito amor sem",
            "PERSON"
          ]
        ],
        "readability_score": 74.2561855670103,
        "semantic_density": 0,
        "word_count": 194,
        "unique_words": 123,
        "lexical_diversity": 0.634020618556701
      },
      "preservation_score": 1.25144663430812e-05
    },
    {
      "id": 1,
      "text": "— 38 —Qual é a sua maior conquista?\\nA minha maior conquista são as pessoas que estão em mi -\\nnha vida.\\nPensa comigo: qual é o preço da confiança de uma pessoa?\\nA minha maior conquista éter o amor de quem eu amo!!!\\nSe você me matar, eu te perdoo..., porém tem uma regra: \\nviva melhor do que vocêvive…\\nOs nossos erros vêm de uma conduta, que vem de outra \\nconduta,que“perdemos” de onde viemos…Tudoque vivemos é \\numa imaginação que nós mesmos criamos e queremos, dentro \\ndaquilo que nós mesmos nos importamos…\\nComo você pensa diante dê…\\nComo você pensa quando olha para algo?\\nComo você pensa ao ouvir algo?\\nComo você pensa ao sentir algum cheiro?\\nComo você pensa quando toca em algo?\\nComo você pensa ao comer?\\nQual é o “sentido” mais importante, são os cinco senti -\\ndos ou é o sentido de como você vive a sua própria captação \\n(energia)?\\nSem título-1   38Sem título-1   38 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 44058,
      "chapter": 1,
      "page": 38,
      "segment_type": "page",
      "themes": {},
      "difficulty": 23.160185185185185,
      "complexity_metrics": {
        "word_count": 162,
        "sentence_count": 12,
        "paragraph_count": 1,
        "avg_sentence_length": 13.5,
        "avg_word_length": 4.561728395061729,
        "unique_word_ratio": 0.654320987654321,
        "avg_paragraph_length": 162.0,
        "punctuation_density": 0.16666666666666666,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "pensa",
          "como",
          "qual",
          "maior",
          "conquista",
          "algo",
          "minha",
          "conduta",
          "mesmos",
          "quando",
          "sentido",
          "título",
          "pessoas",
          "estão",
          "vida",
          "comigo",
          "preço",
          "confiança",
          "pessoa"
        ],
        "entities": [
          [
            "38",
            "CARDINAL"
          ],
          [
            "preço da confiança de uma pessoa",
            "ORG"
          ],
          [
            "amor de quem eu",
            "ORG"
          ],
          [
            "Se",
            "PERSON"
          ],
          [
            "eu",
            "PERSON"
          ],
          [
            "que vem de outra",
            "ORG"
          ],
          [
            "Tudoque",
            "ORG"
          ],
          [
            "nós mesmos criamos",
            "ORG"
          ],
          [
            "queremos",
            "GPE"
          ],
          [
            "mesmos",
            "PERSON"
          ]
        ],
        "readability_score": 91.88148148148149,
        "semantic_density": 0,
        "word_count": 162,
        "unique_words": 106,
        "lexical_diversity": 0.654320987654321
      },
      "preservation_score": 1.6600822700005675e-05
    },
    {
      "id": 1,
      "text": "— 39 —Frase de um bilionário brasileiro: “Quanto mais dinheiro \\neu ganhar, mais pessoas eu posso ajudar… ”\\nPrimeira pergunta: até que ponto eu preciso de mais di -\\nnheiro ao invés de distribuir mais o dinheiro?\\nQuanto mais dinheiro eu tenho, o que ocorre de caos pe -\\nrante ao excesso do meu capitalismo perante ao mundo (caos \\ngerado devido ao seu próprio consumo)?\\nAnalogia\\nPrimeira questão da Analogia é uma pergunta… O ser hu -\\nmano é o centro do universo ou do mundo?\\nNesse tipo de pensamento vamos colocar o nosso corpo (ta -\\nmanho) diante de uma bactéria proporcional ao nosso corpo \\n(terra)… se nosso corpo pega uma superbactéria, o que aconte -\\nce com o nosso corpo?\\nNós criamos um caos no nosso corpo para curar aquela su -\\nperbactéria, nós fazemos mitose (processo de divisão e mul -\\ntiplicação celular) sobre mitose, fazendo o nosso corpo gerar \\nmais células para proteger o nosso corpo, superaquecendo e \\nsaturando (gasto de energia) o nosso próprio corpo, para uma \\nsuperbactéria retirar mais do que o necessário para a sua pró -\\npria sobrevivência…\\nO que nós fazemos ao mundo quando retiramos mais do \\nque o necessário é a mesma coisa.Nós retiramos do mundo \\no que é necessário para vivermos, se nós tiramos mais do que \\nSem título-1   39Sem título-1   39 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 45086,
      "chapter": 1,
      "page": 39,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.7188790560472,
      "complexity_metrics": {
        "word_count": 226,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 37.666666666666664,
        "avg_word_length": 4.738938053097345,
        "unique_word_ratio": 0.5752212389380531,
        "avg_paragraph_length": 226.0,
        "punctuation_density": 0.084070796460177,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "nosso",
          "corpo",
          "mundo",
          "dinheiro",
          "caos",
          "necessário",
          "quanto",
          "primeira",
          "pergunta",
          "próprio",
          "analogia",
          "superbactéria",
          "fazemos",
          "mitose",
          "retiramos",
          "título",
          "frase",
          "bilionário",
          "brasileiro"
        ],
        "entities": [
          [
            "39",
            "CARDINAL"
          ],
          [
            "eu ganhar",
            "PERSON"
          ],
          [
            "mais pessoas eu",
            "PERSON"
          ],
          [
            "posso ajudar",
            "ORG"
          ],
          [
            "Analogia",
            "GPE"
          ],
          [
            "Analogia",
            "GPE"
          ],
          [
            "Nesse",
            "ORG"
          ],
          [
            "nosso corpo",
            "PERSON"
          ],
          [
            "diante de uma bactéria",
            "PERSON"
          ],
          [
            "aquela su -\\nperbactéria",
            "PERSON"
          ]
        ],
        "readability_score": 79.74498525073747,
        "semantic_density": 0,
        "word_count": 226,
        "unique_words": 130,
        "lexical_diversity": 0.5752212389380531
      },
      "preservation_score": 2.1964165418469048e-05
    },
    {
      "id": 1,
      "text": "— 40 —o necessário, como o mundo faz“mitose” para sobreviver aos \\nnossos excessos (bactéria)?\\nO nosso corpo quando se cura fica cicatrizes, feridas, seque -\\nlas… Imagina o corpo do planeta Terra perantevárias “super -\\nbactérias” (humanos) atingindo o seu corpo, fazendo outras \\nbactérias (humanos) dentro do seu corpo (Terra), com menos \\nrecursos por eu retirar mais do que o necessário, fazendo você \\nsobreviver com menos recursos quevocê precisa por eu tirar \\nmais do que o necessário, desestabilizando o corpo, diminuin -\\ndo a quantidade de recursos e centralizando todos os recursos \\npara uma parte específica do corpo, danificando os recursos \\nnecessários de outra parte do corpo (Terra), o deixando fora \\nde equilíbrio e saturando essas outras partes do corpo por não \\nter recursos suficientes para sobreviver, fazendo você entrar \\nem um estado caótico por causa deoutras bactérias necessárias \\npara o seu próprio corpo não tendo o necessário e afetando \\noutras parte do seu próprio corpo (Terra)…\\nNão adianta querermos muito, não adianta vivermos com \\npouco, temos que ter uma balança de nós mesmos peran -\\nte uma balança de contexto proporcional ao meio em que \\nvivemos…\\nSaber até que ponto é necessário eu ter para fazer um bem \\nnecessáriopara um contexto maior do que o dano colateral \\nque eu mesmo estou causando…\\nSem título-1   40Sem título-1   40 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 46514,
      "chapter": 2,
      "page": 40,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 36.05158371040724,
      "complexity_metrics": {
        "word_count": 221,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 110.5,
        "avg_word_length": 5.239819004524887,
        "unique_word_ratio": 0.579185520361991,
        "avg_paragraph_length": 221.0,
        "punctuation_density": 0.08144796380090498,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "corpo",
          "recursos",
          "necessário",
          "terra",
          "sobreviver",
          "bactérias",
          "fazendo",
          "outras",
          "parte",
          "humanos",
          "menos",
          "mais",
          "você",
          "próprio",
          "adianta",
          "balança",
          "contexto",
          "título",
          "como",
          "mundo"
        ],
        "entities": [
          [
            "40",
            "CARDINAL"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "cura",
            "ORG"
          ],
          [
            "fica cicatrizes",
            "PERSON"
          ],
          [
            "Imagina",
            "NORP"
          ],
          [
            "Terra",
            "PERSON"
          ],
          [
            "atingindo",
            "PERSON"
          ],
          [
            "seu corpo",
            "GPE"
          ],
          [
            "eu retirar mais",
            "PERSON"
          ],
          [
            "necessário",
            "GPE"
          ]
        ],
        "readability_score": 43.178054298642536,
        "semantic_density": 0,
        "word_count": 221,
        "unique_words": 128,
        "lexical_diversity": 0.579185520361991
      },
      "preservation_score": 2.1453370873853485e-05
    },
    {
      "id": 1,
      "text": "— 41 —Se você fizer uma comida e falar para os outros, você pre -\\njudica a sua comida ao mostrar como fazer? Aomostrar para \\nos outros a comida do seu restaurante, você prejudica o seu \\nnegócio?\\nFrases:\\nQuanto menos pessoas souberem, mais feliz você será…\\nNão conte sobre a sua vida, quase ninguém está torcendo \\npor você…\\nDo meu ponto de vista, essa visão e essas frases são horríveis \\npara quem quer acreditar que o mal está nos outros e não em \\nsi próprio.\\nNinguém te afeta se você não se permitir (caso do acaso \\nnão conta, atropelamento, bala perdida, dano colateral), nos -\\nsos problemas são normais, nossas dificuldades são normais, o \\nanormal é você pensar que os seus planos, sua vida será afetada \\npor outro, por ele falar de você…\\nSe você vai montar um negócio e ninguém sabe, como irá \\nter clientes, contatos, parcerias?\\n“Sua vida pessoal é diferente da sua vida profissional” , mas \\na sua vida profissional afeta a sua vida pessoal e a sua vida pes -\\nsoal afeta a sua profissional…\\nO não contar sobre a sua vida é a omissão de você ensinar a \\nalguém a viver uma vida que talvez você tenha a resposta para \\najudar aquele alguém.\\nO não falar você está generalizando, discriminando, se iso -\\nlando e você mesmo deixa de ser confiável por não crer em \\nSem título-1   41Sem título-1   41 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 48031,
      "chapter": 2,
      "page": 41,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.19467787114846,
      "complexity_metrics": {
        "word_count": 238,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 39.666666666666664,
        "avg_word_length": 4.53781512605042,
        "unique_word_ratio": 0.6092436974789915,
        "avg_paragraph_length": 238.0,
        "punctuation_density": 0.12184873949579832,
        "line_break_count": 26,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "vida",
          "comida",
          "falar",
          "outros",
          "ninguém",
          "está",
          "afeta",
          "profissional",
          "como",
          "negócio",
          "frases",
          "será",
          "normais",
          "pessoal",
          "alguém",
          "título",
          "fizer",
          "judica",
          "mostrar"
        ],
        "entities": [
          [
            "41",
            "CARDINAL"
          ],
          [
            "outros",
            "GPE"
          ],
          [
            "mostrar como fazer",
            "PERSON"
          ],
          [
            "Aomostrar",
            "PERSON"
          ],
          [
            "você prejudica o",
            "ORG"
          ],
          [
            "Quanto",
            "PRODUCT"
          ],
          [
            "souberem",
            "GPE"
          ],
          [
            "mais feliz você será",
            "PERSON"
          ],
          [
            "essa visão",
            "ORG"
          ],
          [
            "para quem",
            "PERSON"
          ]
        ],
        "readability_score": 78.80532212885154,
        "semantic_density": 0,
        "word_count": 238,
        "unique_words": 145,
        "lexical_diversity": 0.6092436974789915
      },
      "preservation_score": 2.268779102334109e-05
    },
    {
      "id": 1,
      "text": "— 42 —outros. Se você não crê em pessoas ou está generalizando as \\npessoas, onde está o erro, em você ou nos outros quevocê mes -\\nmo colocou na sua vida?\\nSe você não confia nas pessoas com o seu pensamento ge -\\nneralizando a tudo e a todos, porque irei confiar em você se \\nvocê não me passa confiança por não confiar em ninguém?\\nSua vida é uma escola da vida para outros, assim como a \\nvida de outros é uma escola da vida para você!!!\\nVocê ter ideia de negócio é uma coisa totalmente diferente \\nde dar certo…\\nExemplo: escrevi um livro… sou bom em gramática e orto -\\ngrafia?Sou bom em colocar a dissertação do livro em uma boa \\nlinha de raciocínio?\\nQuandovocê vai fazer algo, você precisa de outras pessoas \\npara melhorar e aprimorar aquele algo, por mais quevocê te -\\nnha tido uma ideia excelente, você não é bom administrador, \\ncontador, líder, organizador…você pode se destacar em algu -\\nma coisa, mas você não estudou tudo o que é necessário para \\nsaber diante daquilo quevocêprecisa.\\nSem título-1   42Sem título-1   42 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 49484,
      "chapter": 2,
      "page": 42,
      "segment_type": "page",
      "themes": {},
      "difficulty": 28.188031914893617,
      "complexity_metrics": {
        "word_count": 188,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 23.5,
        "avg_word_length": 4.585106382978723,
        "unique_word_ratio": 0.6436170212765957,
        "avg_paragraph_length": 188.0,
        "punctuation_density": 0.13297872340425532,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "vida",
          "outros",
          "pessoas",
          "está",
          "quevocê",
          "tudo",
          "confiar",
          "escola",
          "ideia",
          "coisa",
          "livro",
          "algo",
          "título",
          "generalizando",
          "onde",
          "erro",
          "colocou",
          "confia",
          "pensamento"
        ],
        "entities": [
          [
            "42",
            "CARDINAL"
          ],
          [
            "Se",
            "PERSON"
          ],
          [
            "ge",
            "ORG"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "passa",
            "GPE"
          ],
          [
            "Sua",
            "PERSON"
          ],
          [
            "para outros",
            "PERSON"
          ],
          [
            "grafia?Sou",
            "NORP"
          ],
          [
            "Quandovocê",
            "GPE"
          ],
          [
            "precisa de outras",
            "PERSON"
          ]
        ],
        "readability_score": 86.87446808510639,
        "semantic_density": 0,
        "word_count": 188,
        "unique_words": 121,
        "lexical_diversity": 0.6436170212765957
      },
      "preservation_score": 1.37488864925688e-05
    },
    {
      "id": 1,
      "text": "— 43 —Não adianta ensinar, direcionar, educar, mostrar… não \\nadianta fazer nada se a pessoa não consegue ver a sua própria \\nvida e os seus próprios valores.\\nPara você aprender a fazer alguma coisa o quevocê tem que \\nfazer? Tem que praticar, errar, executar, “aprender” , errar, prati -\\ncar, executar, “aprender” … Nunca aprendemos nada, sempre \\ntemos algo a aprender ou aprimorar, nunca deixe de ver que \\nna sua própria vida “você sempre está errado” …\\nO seu melhor ou o seu pior são relativos de acordo com \\noque você sabe fazer… Quem sabe fazer alguma coisa que \\nnunca fez?\\nComo vamos ensinar alguém a ser bom se ele nunca foi? \\nComo vamos ensinar alguém a ser matador se ele nunca ma -\\ntou?Como vamos ensinar alguém a pensar melhor se ele nun -\\nca pensou?Como vamos ensinar alguém a pensar e a melhorar \\nde vida se ele nunca enxergou a vida dele como ruim?\\nO ensinamento vem de um contexto e não só de si, se você \\nnão consegue enxergar a sua vida, como alguém vai fazer você \\nenxergar a sua própria vida?\\nSua vida, minha vida, qualquer vida vive aquilo que cada \\npessoa viveu de acordo com o seu pensamento de vida, peran -\\nte a sua importância e forma de ver o que é melhor para si \\npróprio, de acordo com o quevocê viveu e como viveu a sua \\nprópria vida.\\nSem título-1   43Sem título-1   43 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 50664,
      "chapter": 2,
      "page": 43,
      "segment_type": "page",
      "themes": {},
      "difficulty": 26.436008230452675,
      "complexity_metrics": {
        "word_count": 243,
        "sentence_count": 10,
        "paragraph_count": 1,
        "avg_sentence_length": 24.3,
        "avg_word_length": 4.419753086419753,
        "unique_word_ratio": 0.51440329218107,
        "avg_paragraph_length": 243.0,
        "punctuation_density": 0.12757201646090535,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "vida",
          "como",
          "fazer",
          "nunca",
          "ensinar",
          "você",
          "alguém",
          "própria",
          "aprender",
          "vamos",
          "melhor",
          "acordo",
          "viveu",
          "adianta",
          "nada",
          "pessoa",
          "consegue",
          "alguma",
          "coisa",
          "quevocê"
        ],
        "entities": [
          [
            "43",
            "CARDINAL"
          ],
          [
            "mostrar",
            "PERSON"
          ],
          [
            "nada se",
            "PERSON"
          ],
          [
            "Para",
            "PRODUCT"
          ],
          [
            "quevocê tem",
            "ORG"
          ],
          [
            "Nunca",
            "GPE"
          ],
          [
            "aprendemos nada",
            "PERSON"
          ],
          [
            "sua própria",
            "ORG"
          ],
          [
            "Quem",
            "GPE"
          ],
          [
            "Como",
            "ORG"
          ]
        ],
        "readability_score": 86.52407407407408,
        "semantic_density": 0,
        "word_count": 243,
        "unique_words": 125,
        "lexical_diversity": 0.51440329218107
      },
      "preservation_score": 2.298575450770016e-05
    },
    {
      "id": 1,
      "text": "— 44 —Não adianta falar, falar, falar… escrever, escrever, escrever… \\nestudar, estudar, estudar… sevocê não se estudar, você não vai \\nchegar a lugar algum.\\nNão ensinamos alguém a melhorar, nós direcionamos al -\\nguém para melhora se ele quiser melhorar…\\nSe você não consegue ser jogador de futebol, você vai con -\\ntinuar jogando? Isso é mais ou menos uma pessoa que quer \\naprender a ser melhor, porém não consegue enxergar o que ele \\nfez de pior, continuando vivendo e querendo viver os mesmos \\nerros que ele mesmo acha queé o “melhor” para ele mesmo…\\nPosso escrever milhões de coisas, posso direcionar milhões \\nde coisas, posso mostrar e descrever milhões de coisas, pois eu \\nvivi, sofri, errei, acertei e isso me faz pensar sempre em evoluir, \\naprender e agregar tudo aquilo que é melhor em um valor de \\ncontexto de felicidade para aqueles que eu amo.\\nO viver no Rio de Janeiro é lindo, épico, lendário e único, \\nnós lidamos com situações de todos os tipos, quem chega não \\nquer ir embora e quem vive não quer estar… o Rio de Janeiro é \\na cidade dos opostos, onde o corrupto, traficante, matador está \\ncom pessoas medrosas, policiais, criados juntos… O Rio de Ja -\\nneiro tem a favela e tem paisagens que só temos aqui. Temos \\nmontanhas, temos praias com formatos raros no mundo…\\nRio de Janeiro tem o malandro que é maneiro, porém 171 \\nnato, tem aquele carioca que gosta da praia, garotão, temos \\nSem título-1   44Sem título-1   44 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 52117,
      "chapter": 2,
      "page": 44,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.420553359683794,
      "complexity_metrics": {
        "word_count": 253,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 50.6,
        "avg_word_length": 4.735177865612648,
        "unique_word_ratio": 0.6482213438735178,
        "avg_paragraph_length": 253.0,
        "punctuation_density": 0.15810276679841898,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "escrever",
          "estudar",
          "temos",
          "falar",
          "você",
          "quer",
          "melhor",
          "posso",
          "milhões",
          "coisas",
          "janeiro",
          "melhorar",
          "consegue",
          "isso",
          "aprender",
          "porém",
          "viver",
          "mesmo",
          "quem",
          "título"
        ],
        "entities": [
          [
            "44",
            "CARDINAL"
          ],
          [
            "estudar",
            "PERSON"
          ],
          [
            "você não vai \\n",
            "PERSON"
          ],
          [
            "direcionamos al -\\n",
            "PERSON"
          ],
          [
            "melhora se ele quiser melhorar",
            "PERSON"
          ],
          [
            "Se",
            "PERSON"
          ],
          [
            "mesmos \\nerros",
            "PERSON"
          ],
          [
            "para ele mesmo",
            "PERSON"
          ],
          [
            "Posso",
            "PERSON"
          ],
          [
            "posso mostrar",
            "PERSON"
          ]
        ],
        "readability_score": 73.27944664031621,
        "semantic_density": 0,
        "word_count": 253,
        "unique_words": 164,
        "lexical_diversity": 0.6482213438735178
      },
      "preservation_score": 2.5028932686162398e-05
    },
    {
      "id": 1,
      "text": "— 45 —todos os tipos de personalidade, desde a mais autêntica e a pes -\\nsoa mais ignorante… o Rio de Janeiro não tem um padrão, o \\nRio de Janeiro é o Rio de Janeiro! \\nSomos exclusivos nesse vasto mundo, somos únicos e au -\\ntênticos para o mundo, o ser carioca não é algo quevocê con -\\nquista, é algo que nasce em você, pois até pessoas que nascem \\nfora do Rio, seja lá aonde for, se chegaremao Rio e se identifi -\\ncarem… virou carioca e carioca se permanecerá…Cariocas,ca -\\npítulo 4, versículo 3.\\nFelicidade não é palpável ou comprada e sim sentida!\\nFelicidade vem de você, vem de mim, vem de reconhe -\\ncimento!\\nFelicidade é reconhecer valores e viver!\\nFelicidade é viver o melhor que a vida pode te proporcio -\\nnar sentimentalmente!\\nNão precisa de dinheiro para ser feliz… mentira da por -\\nra! Kkkkkk\\nNão tenha dinheiro para ter comida em casa, não tenha di -\\nnheiro para pagar a sua luz, água, aluguel etc.\\nSem título-1   45Sem título-1   45 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 53706,
      "chapter": 2,
      "page": 45,
      "segment_type": "page",
      "themes": {},
      "difficulty": 26.28019863438858,
      "complexity_metrics": {
        "word_count": 179,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 19.88888888888889,
        "avg_word_length": 4.4525139664804465,
        "unique_word_ratio": 0.6368715083798883,
        "avg_paragraph_length": 179.0,
        "punctuation_density": 0.15083798882681565,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "felicidade",
          "janeiro",
          "carioca",
          "mais",
          "somos",
          "mundo",
          "algo",
          "você",
          "viver",
          "dinheiro",
          "tenha",
          "título",
          "todos",
          "tipos",
          "personalidade",
          "desde",
          "autêntica",
          "ignorante",
          "padrão",
          "exclusivos"
        ],
        "entities": [
          [
            "45",
            "CARDINAL"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "Rio de Janeiro",
            "GPE"
          ],
          [
            "Rio de Janeiro",
            "GPE"
          ],
          [
            "Somos",
            "PERSON"
          ],
          [
            "somos únicos",
            "PERSON"
          ],
          [
            "tênticos",
            "NORP"
          ],
          [
            "quista",
            "NORP"
          ],
          [
            "pois até pessoas que",
            "ORG"
          ],
          [
            "Rio",
            "ORG"
          ]
        ],
        "readability_score": 88.71980136561142,
        "semantic_density": 0,
        "word_count": 179,
        "unique_words": 114,
        "lexical_diversity": 0.6368715083798883
      },
      "preservation_score": 1.6175160579492706e-05
    },
    {
      "id": 1,
      "text": "— 46 —Não precisa de muito dinheiro para ser feliz! Isso é verdade \\nno meu ponto de vista.Se você junta 10 amigos, cada um dá \\n20 reais, fazemos um churrasco com aquela carne elástica, lin -\\nguiça cheia de gordura, aquele fígado sem estar limpo e aquela \\ncerveja que te dá uma ressaca absurda no outro dia… isso é \\nlendário!!!!Isso é ser feliz não pelo dinheiro e sim pelo contex -\\nto de sentimento, energia, confiança, amizade, brincadeiras…\\nPega um milhão, vai viajar o mundo todo sozinho, sem \\nninguém mesmo, será quevocê vai ser mais feliz do que eu que \\ngastei 20 reais com 10 amigos?Pega esse mesmo um milhão \\ne viaje com a mulher quevocê ama, família ou amigos, será \\nmais feliz?\\nO dinheiro não compra a felicidade, porém sem dinheiro \\nnenhum vocêestáferrado!!!Trabalhe, conquiste, viva, sinta a \\nenergia de quandovocê é feliz e aceite a felicidade que as pes -\\nsoas podem te proporcionar, a felicidade não está na quantida -\\nde e sim na qualidade sentimental do quevocê vive!\\nNão importa o valor gasto, importa a proporção de gastos \\ndiante da quantidade de felicidade que irei receber de volta \\n(custo-benefício), se for com pessoas quevocê ama, você pode \\ngastar 20 a um milhão de reais… agora se você não souber ser \\nfeliz, você não será.\\nSem título-1   46Sem título-1   46 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 54807,
      "chapter": 2,
      "page": 46,
      "segment_type": "page",
      "themes": {},
      "difficulty": 29.163555555555554,
      "complexity_metrics": {
        "word_count": 225,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 25.0,
        "avg_word_length": 4.804444444444444,
        "unique_word_ratio": 0.6444444444444445,
        "avg_paragraph_length": 225.0,
        "punctuation_density": 0.17333333333333334,
        "line_break_count": 22,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "feliz",
          "dinheiro",
          "você",
          "quevocê",
          "felicidade",
          "isso",
          "amigos",
          "reais",
          "milhão",
          "será",
          "aquela",
          "pelo",
          "energia",
          "pega",
          "mesmo",
          "mais",
          "importa",
          "título",
          "precisa",
          "muito"
        ],
        "entities": [
          [
            "46",
            "CARDINAL"
          ],
          [
            "para ser feliz",
            "PERSON"
          ],
          [
            "10",
            "CARDINAL"
          ],
          [
            "20",
            "CARDINAL"
          ],
          [
            "aquela carne elástica",
            "PERSON"
          ],
          [
            "lin",
            "PERSON"
          ],
          [
            "estar",
            "PRODUCT"
          ],
          [
            "aquela",
            "GPE"
          ],
          [
            "ressaca absurda",
            "PERSON"
          ],
          [
            "dia",
            "ORG"
          ]
        ],
        "readability_score": 86.05866666666667,
        "semantic_density": 0,
        "word_count": 225,
        "unique_words": 145,
        "lexical_diversity": 0.6444444444444445
      },
      "preservation_score": 2.341141662821313e-05
    },
    {
      "id": 1,
      "text": "— 47 —Eu não gosto da maconha do morro, porém é a única forma \\nde eu ter acesso, queria plantar para o meu próprio consumo.\\nVocê bebe uma cerveja Antarctica, Brahma, Stella, Heineken…\\nWhisky Red Label, White Horse, Blue Label, Johnny Wal -\\nker… a maconha também tem variedades, porém é cara e difí -\\ncil de se achar e cada tipo de planta dá um tipo de maconha. \\nEla traz benefícios de acordo com a sua necessidade: contra \\ninsônia, Parkinson, depressão, anticonvulsivo, relaxamen -\\nto, sexo…\\nQuais são os benefícios do álcool, cigarro, remédios de far -\\nmácia, comida?Pela falta de acesso você come o que vem… se \\nquiser continuar com o seu pensamento preconceituoso, dian -\\nte de algo que foi proibido por questões raciais (escravos fuma -\\nvam para relaxar após um dia de“trabalho” , negros fumavam \\npara se divertir),você continua com ele para você, pois para \\nmim que estudei pra caralho antes mesmo de começar a fumar \\n(30 anos), acho um dos maiores preconceitos que vivemos, só \\nperdendo para macumba, criado-mudo e “outros preconceitos \\ndiante da minha certeza ser melhor que a sua. ”\\nMarcelo, você fuma maconha? Sim.\\nMarcelo, não gosto quevocê fume maconha, fale baixo que -\\nvocê faz isso…\\nNão irei omitir algo (semelhante a omitir que sou negro), \\neu sou a favor da liberação.\\nSem título-1   47Sem título-1   47 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 56249,
      "chapter": 2,
      "page": 47,
      "segment_type": "page",
      "themes": {},
      "difficulty": 34.89184782608696,
      "complexity_metrics": {
        "word_count": 230,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 28.75,
        "avg_word_length": 4.8478260869565215,
        "unique_word_ratio": 0.7260869565217392,
        "avg_paragraph_length": 230.0,
        "punctuation_density": 0.17391304347826086,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "maconha",
          "gosto",
          "porém",
          "acesso",
          "label",
          "tipo",
          "benefícios",
          "algo",
          "fuma",
          "preconceitos",
          "marcelo",
          "omitir",
          "título",
          "morro",
          "única",
          "forma",
          "queria",
          "plantar",
          "próprio"
        ],
        "entities": [
          [
            "47",
            "CARDINAL"
          ],
          [
            "Eu",
            "PERSON"
          ],
          [
            "queria plantar",
            "PERSON"
          ],
          [
            "Antarctica",
            "LOC"
          ],
          [
            "Heineken",
            "ORG"
          ],
          [
            "Whisky Red Label",
            "PERSON"
          ],
          [
            "Johnny Wal -\\nker",
            "PERSON"
          ],
          [
            "Ela traz",
            "PERSON"
          ],
          [
            "de acordo",
            "PERSON"
          ],
          [
            "contra",
            "NORP"
          ]
        ],
        "readability_score": 84.17065217391304,
        "semantic_density": 0,
        "word_count": 230,
        "unique_words": 167,
        "lexical_diversity": 0.7260869565217392
      },
      "preservation_score": 3.166926176616468e-05
    },
    {
      "id": 1,
      "text": "— 48 —Marcelo, isso é uma droga vai te fazer mal…\\nCanabidiol (CBD) funciona como analgésico, sedativo e \\nanticonvulsivo e é usado no tratamento de doenças como es -\\nclerose múltipla, epilepsia, mal de Parkinson, esquizofrenia e \\ndores crônicas. Todo o sistema nervoso se acalma com a ma -\\nconha, por isso se você não tem uma vida estável, uma direção \\na ser seguida, um trabalho, se você não tiver um conforto de \\nvida, não use.\\nMarcelo, isso vai te tornar um drogado!\\nNão vai. Você come açúcar, carboidratos, toma remé -\\ndios, bebe cerveja, malha igual louco, come 10 kg de comida \\npor dia…\\nMarcelo, isso é contra lei, você financia o tráfico!\\nNós financiamos o tráfico pagando impostos, nós financia -\\nmos o tráfico jogando, nós financiamos o tráfico por não ter \\num país onde todos podem ter chance de uma boa educação, \\nestrutura familiar, cheios de preconceitos, com arma de fogo \\nem casa (eu nunca peguei em uma arma) …\\nQuando alguém vier falar comigo sobre a maconha, vê o \\nmotivo da lei ser formada, depois quevocê descobrir isso,vo -\\ncê vem falar comigo com argumentos de malefícios peran -\\nte a maconha, se os seus argumentos são coerentes, eu paro \\nde fumar.\\n“Não atire pedra no telhado dos outros, pois o seu telhado \\ntambém é de vidro!”\\nSe não sabe a diferença entre usuário, dependente e vicia -\\ndo,porquevocê quer argumentar sobre algo quevocê não sabe? \\nNem tudoque faz mal ou bem para você faz para mim. Minha \\nSem título-1   48Sem título-1   48 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 57726,
      "chapter": 2,
      "page": 48,
      "segment_type": "page",
      "themes": {},
      "difficulty": 35.463461538461544,
      "complexity_metrics": {
        "word_count": 260,
        "sentence_count": 10,
        "paragraph_count": 1,
        "avg_sentence_length": 26.0,
        "avg_word_length": 4.711538461538462,
        "unique_word_ratio": 0.6807692307692308,
        "avg_paragraph_length": 260.0,
        "punctuation_density": 0.16923076923076924,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "isso",
          "você",
          "tráfico",
          "marcelo",
          "como",
          "vida",
          "come",
          "financia",
          "financiamos",
          "arma",
          "falar",
          "comigo",
          "maconha",
          "quevocê",
          "argumentos",
          "telhado",
          "sabe",
          "título",
          "droga",
          "fazer"
        ],
        "entities": [
          [
            "48",
            "CARDINAL"
          ],
          [
            "Marcelo",
            "ORG"
          ],
          [
            "mal",
            "PERSON"
          ],
          [
            "epilepsia",
            "GPE"
          ],
          [
            "mal de Parkinson",
            "ORG"
          ],
          [
            "Marcelo",
            "PERSON"
          ],
          [
            "10 kg de",
            "QUANTITY"
          ],
          [
            "dia",
            "ORG"
          ],
          [
            "Marcelo",
            "PERSON"
          ],
          [
            "contra",
            "NORP"
          ]
        ],
        "readability_score": 85.58653846153847,
        "semantic_density": 0,
        "word_count": 260,
        "unique_words": 177,
        "lexical_diversity": 0.6807692307692308
      },
      "preservation_score": 3.6351545091807295e-05
    },
    {
      "id": 1,
      "text": "— 49 —mente, meu corpo, minha vida sãodiferentes da sua, não ge -\\nneraliza uma ou várias situações quevocê tem como exemplo, \\nvocê já procurou os exemplos bons diante da maconha? \\nNão entenda a sua interpretação como a melhor interpre -\\ntação… interprete como melhor interpretação, um estudo de \\nmelhor interpretação diante do mesmo que você está interpre -\\ntando… Antes de julgarmos algo ou alguém, interprete a vida, \\na situação em quevocê se encontra e o contexto quevocê está \\ninterpretando, sua razão não é o padrão da sociedade, sua ra -\\nzão é o seu padrão de interpretação…\\nInterpretar é um contexto da maioria, não de todos, até por -\\nque nem Deus (tudoque é bom agradecemos aDeus) agrada a \\ntodos e tem a aceitação de todos, você, uma simples pessoa, é \\nperfeita para interpretar e entender a todos?\\nA vida é muito curta para não ser vivida!\\nPorém, o que é viver?\\nEu penso que viver é abrir sorrisos, ver as pessoas contando \\nhistórias e interagindo uma com a outra, tendo boas conversas, \\nfalando como foram felizes, como aconteceram coisas engra -\\nçadas, aquele dia quevocê passou um perrengue sensacional, \\nSem título-1   49Sem título-1   49 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 59346,
      "chapter": 2,
      "page": 49,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 37.4685,
      "complexity_metrics": {
        "word_count": 200,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 40.0,
        "avg_word_length": 4.895,
        "unique_word_ratio": 0.66,
        "avg_paragraph_length": 200.0,
        "punctuation_density": 0.145,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "como",
          "quevocê",
          "interpretação",
          "todos",
          "vida",
          "você",
          "melhor",
          "diante",
          "interpre",
          "interprete",
          "está",
          "contexto",
          "padrão",
          "interpretar",
          "viver",
          "título",
          "mente",
          "corpo",
          "minha",
          "sãodiferentes"
        ],
        "entities": [
          [
            "49",
            "CARDINAL"
          ],
          [
            "ge",
            "ORG"
          ],
          [
            "Antes de julgarmos",
            "ORG"
          ],
          [
            "sua ra -\\n",
            "PERSON"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "de interpretação",
            "PERSON"
          ],
          [
            "não de todos",
            "ORG"
          ],
          [
            "nem Deus",
            "PERSON"
          ],
          [
            "muito curta",
            "ORG"
          ],
          [
            "para não ser vivida",
            "PERSON"
          ]
        ],
        "readability_score": 78.5315,
        "semantic_density": 0,
        "word_count": 200,
        "unique_words": 132,
        "lexical_diversity": 0.66
      },
      "preservation_score": 1.7452146941031606e-05
    },
    {
      "id": 1,
      "text": "— 50 —aquele dia quevocê ficou bêbado com seus amigos, aquele dia \\nquevocê foi a um culto e teve uma revelação, aquele dia que -\\nvocê conheceu a pessoa da sua vida… para mim o viver é viver \\ncom os melhores sorrisos que eu já vivi, viver é algo que não \\npercebemos que estamos sendo felizes, o viver é algo de cada \\num… porém, como iremos saber viver se não aprendemos o \\nque é viver?\\nO viver é sentir a emoção e saber viver aquela emoção.\\nViver é você sentir a energia que está à sua volta.\\nViver é ser feliz com a maior quantidade de sorrisos quevo -\\ncê possa ter ao seu lado.\\nViver é você ver felicidade em viver!\\nEntendam uma coisa, Collor, Fernando Henrique, Lula, \\nDilma, Bolsonaro – o que você etodos têm em comum?\\nTodos têm amigos que fazem coisas erradas e não podemos \\nfazer nada! Infelizmente por mais que eu veja que é errado, o \\nque eu irei fazer?\\nSe você conhece um traficante, miliciano, político, contra -\\nventor e qualquer pessoa que sabe que está errado, o quevocê \\npode fazer? Hipocrisia e falta de entendimento diante de um \\nviver, pois eu penso igual a você, queria o melhor para todos, \\nporém nem todos merecem o melhor. Aprenda algo, se você \\nnão pode fazer algo contra os erros, ensina à próxima geração \\na não cometer os mesmos, pois assim comoteve roubos em \\nSem título-1   50Sem título-1   50 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 60657,
      "chapter": 2,
      "page": 50,
      "segment_type": "page",
      "themes": {},
      "difficulty": 27.517184035476717,
      "complexity_metrics": {
        "word_count": 246,
        "sentence_count": 11,
        "paragraph_count": 1,
        "avg_sentence_length": 22.363636363636363,
        "avg_word_length": 4.451219512195122,
        "unique_word_ratio": 0.6097560975609756,
        "avg_paragraph_length": 246.0,
        "punctuation_density": 0.14227642276422764,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "viver",
          "você",
          "algo",
          "fazer",
          "aquele",
          "quevocê",
          "todos",
          "amigos",
          "pessoa",
          "sorrisos",
          "porém",
          "saber",
          "sentir",
          "emoção",
          "está",
          "errado",
          "contra",
          "pode",
          "pois",
          "melhor"
        ],
        "entities": [
          [
            "50",
            "CARDINAL"
          ],
          [
            "dia",
            "ORG"
          ],
          [
            "dia",
            "ORG"
          ],
          [
            "dia",
            "ORG"
          ],
          [
            "para mim",
            "PERSON"
          ],
          [
            "que eu já vivi",
            "QUANTITY"
          ],
          [
            "Collor",
            "PERSON"
          ],
          [
            "Fernando Henrique",
            "PERSON"
          ],
          [
            "Lula",
            "PERSON"
          ],
          [
            "Bolsonaro",
            "PERSON"
          ]
        ],
        "readability_score": 87.48281596452328,
        "semantic_density": 0,
        "word_count": 246,
        "unique_words": 150,
        "lexical_diversity": 0.6097560975609756
      },
      "preservation_score": 2.1453370873853485e-05
    },
    {
      "id": 1,
      "text": "— 51 —todos os mandatos de presidente, você achava quealgum seria \\ndiferente? Parem de criticar um ao outro por presidentes que \\nnós mesmos colocamos e critiquem a falta de evolução de nós \\nmesmos e dos presidentes, até porque,você nasceu sabendo an -\\ndar? Imagina lidar com 200 milhões de pessoas, você saberia -\\nlidar? Temos que aprender a não ter a nossa razão como certa.\\n A dificuldade está para todos e todos estamos na dificulda -\\nde, como aprendemos se não sabemos e nem temos um bom \\nparâmetro de aprendizado em ser algo que ninguém conse -\\ngue ser?\\nSem título-1   51Sem título-1   51 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 62135,
      "chapter": 2,
      "page": 51,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 25.36619937694704,
      "complexity_metrics": {
        "word_count": 107,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 17.833333333333332,
        "avg_word_length": 4.831775700934579,
        "unique_word_ratio": 0.7757009345794392,
        "avg_paragraph_length": 107.0,
        "punctuation_density": 0.1308411214953271,
        "line_break_count": 10,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "todos",
          "você",
          "presidentes",
          "mesmos",
          "lidar",
          "temos",
          "como",
          "título",
          "mandatos",
          "presidente",
          "achava",
          "quealgum",
          "seria",
          "diferente",
          "parem",
          "criticar",
          "outro",
          "colocamos",
          "critiquem",
          "falta"
        ],
        "entities": [
          [
            "51",
            "CARDINAL"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "de presidente",
            "GPE"
          ],
          [
            "você achava",
            "PERSON"
          ],
          [
            "seria \\ndiferente",
            "ORG"
          ],
          [
            "Parem de",
            "PERSON"
          ],
          [
            "mesmos colocamos",
            "PERSON"
          ],
          [
            "você nasceu sabendo",
            "PERSON"
          ],
          [
            "Imagina",
            "PERSON"
          ],
          [
            "200",
            "CARDINAL"
          ]
        ],
        "readability_score": 89.63380062305296,
        "semantic_density": 0,
        "word_count": 107,
        "unique_words": 83,
        "lexical_diversity": 0.7757009345794392
      },
      "preservation_score": 4.6822833256426265e-06
    },
    {
      "id": 1,
      "text": "— 52 —O maior fracassado é aquele que não reconhece o próprio \\nfracasso! Sua vida, suas escolhas, sua direção, sua estrada, seu \\ncaminho, suas decisões, suasoportunidades… só você pode sa -\\nber o valorquevocê enxerga de acordo com a sua necessidade. \\nNão culpe alguém por não conseguir atingir o quevocê alme -\\njava, pois enquanto você escolheu uma estrada sem buraco por \\nser mais fácil, o outro escolheu uma direção em que ele seguiu \\no melhor destino e não a melhor estrada!\\nPara se viver uma vida digna, não tenha lacunas em sua \\nvida!!!!\\nO que são lacunas em sua vida? Mentiras contadas, intri -\\ngas e brigas mal resolvidas, fugir dos problemas, omissão dian -\\nte dos problemas, falta de postura diante de algo que vai te \\nincomodar … tudoaquilo que possa vir te ocasionar um mal \\namanhã é uma lacuna pendente em sua vida, sem data para \\no mesmo retornar. Faça regresso, tire as lacunas de sua vida, \\nresolva as suas próprias mentiras para se viver uma vida que se \\né para viver.\\nO reclamar de hoje é falha do seu próprio passado… fracas -\\nsado não é aquele que fracassa e sim aquele que não reconhece \\no próprio fracasso!\\nSem título-1   52Sem título-1   52 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 62886,
      "chapter": 2,
      "page": 52,
      "segment_type": "page",
      "themes": {},
      "difficulty": 28.06095238095238,
      "complexity_metrics": {
        "word_count": 210,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 23.333333333333332,
        "avg_word_length": 4.647619047619048,
        "unique_word_ratio": 0.6238095238095238,
        "avg_paragraph_length": 210.0,
        "punctuation_density": 0.14761904761904762,
        "line_break_count": 21,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "vida",
          "aquele",
          "próprio",
          "suas",
          "estrada",
          "viver",
          "lacunas",
          "reconhece",
          "fracasso",
          "direção",
          "você",
          "escolheu",
          "melhor",
          "mentiras",
          "problemas",
          "título",
          "maior",
          "fracassado",
          "escolhas",
          "caminho"
        ],
        "entities": [
          [
            "52",
            "CARDINAL"
          ],
          [
            "Sua",
            "PERSON"
          ],
          [
            "suas escolhas",
            "PERSON"
          ],
          [
            "sua direção",
            "PERSON"
          ],
          [
            "sua estrada",
            "ORG"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "suas decisões",
            "PERSON"
          ],
          [
            "quevocê alme -\\njava",
            "PERSON"
          ],
          [
            "escolheu",
            "GPE"
          ],
          [
            "uma estrada sem",
            "ORG"
          ]
        ],
        "readability_score": 86.93904761904761,
        "semantic_density": 0,
        "word_count": 210,
        "unique_words": 131,
        "lexical_diversity": 0.6238095238095238
      },
      "preservation_score": 1.7877809061544572e-05
    },
    {
      "id": 1,
      "text": "— 53 —Quando você vai ser empreendedor, qual é a sua prioridade \\ncom o cliente, satisfação do cliente ou o valor monetário de \\nretorno?\\nVocê, sendo cliente, ficaria satisfeito em pagar “caro” por \\naquilo quevocê precisa ou quer pagar o preço justo?\\nHoje temos internet. Com a internet todos se informam de \\nacordo com a sua necessidade. Quando você vai adquirir algo, \\nvocê pesquisa sobre?\\nNinguém é burro, ninguém quer perder dinheiro. Diante \\ndessas perguntas, como você faria para abrir um empreendi -\\nmento? Temos que ter noção das nossas falhas e nossas quali -\\ndades. Por mais que eu queira ter um empreendimento, sou \\ncapaz de proporcionar a qualidade necessária para ter um bom \\ncusto-benefício?\\nSeus elogios recebidos é uma direção para um futuro... Se \\nvocê não reconhece a si mesmo, como irá reconhecer o que \\noutras pessoas necessitam?\\nNão somos os melhores, não somos os mais fortes, não so -\\nmos nada se não deixarmos o nosso egoísmo, nosso egocen -\\ntrismo. Não somos os mais inteligentes ao ponto de sermos \\ntudo para nós mesmos!\\nSem título-1   53Sem título-1   53 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 64206,
      "chapter": 2,
      "page": 53,
      "segment_type": "page",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 23.097413127413127,
      "complexity_metrics": {
        "word_count": 185,
        "sentence_count": 14,
        "paragraph_count": 1,
        "avg_sentence_length": 13.214285714285714,
        "avg_word_length": 4.967567567567568,
        "unique_word_ratio": 0.7135135135135136,
        "avg_paragraph_length": 185.0,
        "punctuation_density": 0.16756756756756758,
        "line_break_count": 21,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "cliente",
          "mais",
          "somos",
          "quando",
          "pagar",
          "quer",
          "temos",
          "internet",
          "ninguém",
          "como",
          "nossas",
          "nosso",
          "título",
          "empreendedor",
          "qual",
          "prioridade",
          "satisfação",
          "valor",
          "monetário"
        ],
        "entities": [
          [
            "Quando",
            "PERSON"
          ],
          [
            "valor monetário de \\nretorno",
            "PERSON"
          ],
          [
            "ficaria satisfeito",
            "PERSON"
          ],
          [
            "quevocê precisa",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "Ninguém",
            "ORG"
          ],
          [
            "Diante",
            "PERSON"
          ],
          [
            "dessas perguntas",
            "PERSON"
          ],
          [
            "como você faria para",
            "ORG"
          ],
          [
            "das nossas",
            "ORG"
          ]
        ],
        "readability_score": 91.90258687258688,
        "semantic_density": 0,
        "word_count": 185,
        "unique_words": 132,
        "lexical_diversity": 0.7135135135135136
      },
      "preservation_score": 1.8771699514621802e-05
    },
    {
      "id": 1,
      "text": "— 54 —Quando se vai fazer um filme, temos um diretor de criação, \\ndiretor de fotografia, diretor de roteiro, diretor de cena… no \\nfutebol, temos os jogadores, cada um na sua posição, temos o \\ntécnico, médico, auxiliares, preparadores, fisioterapeuta…\\nPrecisamos nos descobrir, precisamos ser humildes e reco -\\nnhecer a necessidade que nos falta, para evoluirmos e fazer o \\nmelhor para nós mesmos, que consequentemente melhora o \\noutro, que é “melhor” que você em outra coisa. Nossa men -\\nte cria, nossa mente constrói, nossa mente desenvolve, nossa \\nmente é nossa. Nós somos parte de um sistema de colabora -\\nção que retorna para si próprio, seja amanhã ou o agoratudo \\ndepende de como vocêviveu, para saber o legado que você vai \\ndeixar… estudeo que nós já vivemos que você entenderá o sig -\\nnificadode um legado estrutural, educacional, racial e outros \\ntipos de legados.\\nTrabalho – minhas dificuldades durante a trajetória – me \\nfez perceber as dificuldades de ser ter comida, um bom rela -\\ncionamento, ser um bom pai,aí você entende a necessidade de \\nse ter um bom emprego…\\nSer solteiro – você só pensa em viver, curtir, ninguém man -\\nda em você, gasta tudoque tem… estilo de vida diferente, po -\\nrémquando se adapta eu acho que é a melhor vida para mim.\\nDepressão – aprendi que não há diferença de dorquando \\nse trata de importância diante de um sonho quevocê mesmo \\nSem título-1   54Sem título-1   54 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 65443,
      "chapter": 2,
      "page": 54,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 44.45696721311475,
      "complexity_metrics": {
        "word_count": 244,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 48.8,
        "avg_word_length": 4.85655737704918,
        "unique_word_ratio": 0.6352459016393442,
        "avg_paragraph_length": 244.0,
        "punctuation_density": 0.15163934426229508,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "nossa",
          "diretor",
          "temos",
          "melhor",
          "mente",
          "fazer",
          "precisamos",
          "necessidade",
          "legado",
          "dificuldades",
          "vida",
          "título",
          "quando",
          "filme",
          "criação",
          "fotografia",
          "roteiro",
          "cena",
          "futebol"
        ],
        "entities": [
          [
            "54",
            "CARDINAL"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "diretor de criação",
            "PERSON"
          ],
          [
            "de cena",
            "PERSON"
          ],
          [
            "temos os jogadores",
            "PERSON"
          ],
          [
            "Precisamos",
            "PERSON"
          ],
          [
            "precisamos ser",
            "PERSON"
          ],
          [
            "para evoluirmos",
            "PERSON"
          ],
          [
            "nós mesmos",
            "ORG"
          ],
          [
            "melhora",
            "PERSON"
          ]
        ],
        "readability_score": 74.14303278688524,
        "semantic_density": 0,
        "word_count": 244,
        "unique_words": 155,
        "lexical_diversity": 0.6352459016393442
      },
      "preservation_score": 2.553972723077796e-05
    },
    {
      "id": 1,
      "text": "— 55 —criou como sonho, cada pessoa tem uma importância para o \\nque vive, cada um tem a sua própria dor.\\nTudo que aprendi de ruim e de bom, eu ensino e aprendo \\ncom todos.\\nTodas as coisas ruins e feliz que vivisão necessárias para re -\\npassar, pois a sua felicidade é a minha.Quando estivermos ao \\nlado um do outro, quero quevocê sorria junto comigo, quero \\nquevocê seja feliz junto comigo. Na minha vida e em minha \\nvolta só quero felicidade, quanto mais eu puder ensinar para as \\npessoas à minha volta, mais feliz eu serei!\\nEstamos sempre fugindo de alguma coisa…\\nQuando crianças, fugimos dos nossos pais…\\nQuando adolescentes, fugimos das responsabilidades…\\nQuando adultos, fugimos do que é viver… como assim?Se \\ntrabalhamos muito, queremos fugir do excesso de trabalho…\\nQuando ficamos muito em casa, queremos fugir do excesso \\nda monotonia… quando queremos fugir dos nossos sentimen -\\ntos, queremos extravasar…\\nQuando vamos aprender a viver o melhor que cada situa -\\nção nos proporciona ao invés de fugir do que é viver? Aprovei -\\nta a sua vida, pois o seu fugir é fugir da sua própria forma de \\nviver a sua vida.\\nSem título-1   55Sem título-1   55 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 67007,
      "chapter": 2,
      "page": 55,
      "segment_type": "page",
      "themes": {},
      "difficulty": 27.82977558839628,
      "complexity_metrics": {
        "word_count": 203,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 22.555555555555557,
        "avg_word_length": 4.802955665024631,
        "unique_word_ratio": 0.6157635467980296,
        "avg_paragraph_length": 203.0,
        "punctuation_density": 0.1330049261083744,
        "line_break_count": 22,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quando",
          "fugir",
          "minha",
          "viver",
          "queremos",
          "cada",
          "feliz",
          "quero",
          "vida",
          "fugimos",
          "como",
          "própria",
          "pois",
          "felicidade",
          "quevocê",
          "junto",
          "comigo",
          "volta",
          "mais",
          "nossos"
        ],
        "entities": [
          [
            "55",
            "CARDINAL"
          ],
          [
            "eu ensino",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "Todas",
            "PERSON"
          ],
          [
            "coisas",
            "ORG"
          ],
          [
            "necessárias para re -\\n",
            "PERSON"
          ],
          [
            "Quando estivermos",
            "PERSON"
          ],
          [
            "quevocê sorria junto comigo",
            "ORG"
          ],
          [
            "quanto mais eu",
            "PERSON"
          ],
          [
            "Estamos",
            "PERSON"
          ]
        ],
        "readability_score": 87.28133552271483,
        "semantic_density": 0,
        "word_count": 203,
        "unique_words": 125,
        "lexical_diversity": 0.6157635467980296
      },
      "preservation_score": 1.638799163974919e-05
    },
    {
      "id": 1,
      "text": "— 56 —Referência sobre como armazenamentos e a importância \\nde cada memória…\\nFilme – Quem quer ser um milionário?\\nMinha vida – proporção e importância de acordo com o \\nque vou vivendo.\\nQuando eu vivi…\\nPassei fome durante um bom período quando criança– não \\ndesejo que ninguém passe, estudei para melhor interpretar e \\npoder ensinar e estimular a quem ao mesmo tempo passa por \\nessa mesma dificuldade.\\nPai ausente – referência para ser o melhor pai que eu posso \\nser, oposto. \\nCasamento – durante um período, vivi um sonho de casa -\\nmento, após o nosso filho nascer não fomos maduros o sufi -\\nciente para obedecer a quarentena após o parto, pois meu filho \\nnasceu com4kg e 130g, parto normal, a mãe do meu filho teve \\num corte grande e muitos pontos, ocasionando dificuldades \\npara cicatrização.Ao fazermos sexo gerou um trauma (sensa -\\nção de estupro) nela, criando um afastamento e consequente -\\nmente outras brigas.\\nSem título-1   56Sem título-1   56 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 68316,
      "chapter": 2,
      "page": 56,
      "segment_type": "page",
      "themes": {},
      "difficulty": 28.335324675324678,
      "complexity_metrics": {
        "word_count": 165,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 23.571428571428573,
        "avg_word_length": 4.927272727272728,
        "unique_word_ratio": 0.7272727272727273,
        "avg_paragraph_length": 165.0,
        "punctuation_density": 0.11515151515151516,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "filho",
          "referência",
          "importância",
          "quem",
          "quando",
          "vivi",
          "durante",
          "período",
          "melhor",
          "após",
          "parto",
          "título",
          "como",
          "armazenamentos",
          "cada",
          "memória",
          "filme",
          "quer",
          "milionário",
          "minha"
        ],
        "entities": [
          [
            "56",
            "CARDINAL"
          ],
          [
            "Referência",
            "PERSON"
          ],
          [
            "Filme",
            "PERSON"
          ],
          [
            "Quem",
            "PERSON"
          ],
          [
            "vou",
            "ORG"
          ],
          [
            "Quando eu",
            "PERSON"
          ],
          [
            "quando criança",
            "PERSON"
          ],
          [
            "para melhor interpretar",
            "ORG"
          ],
          [
            "passa",
            "GPE"
          ],
          [
            "referência para ser o melhor pai",
            "PERSON"
          ]
        ],
        "readability_score": 86.7361038961039,
        "semantic_density": 0,
        "word_count": 165,
        "unique_words": 120,
        "lexical_diversity": 0.7272727272727273
      },
      "preservation_score": 1.2344201494876015e-05
    },
    {
      "id": 1,
      "text": "— 57 —Reclamamos tanto das perdas de uma pessoa que amamos, \\nde um machucado, de um amor não correspondido, reclama -\\nmos, reclamamos, reclamamos até quando iremos reclamar e \\nnão enxergamosqueo que nos faz ser o que somos não é o vi -\\nver e sim o valor de viver…\\nTodas as nossas reclamações nos fazem ver valores que nos \\nfazem enxergar a grandeza de estarmos vivos, de termos pro -\\nblemas, termos a morte, termos a perda… até porque nem \\ntoda escuridão é ruim, se você enxergar a luz na escuridão de \\numa forma evolutiva, iremos conseguir enxergar o pior para \\nvivermos melhor. \\nMinha vida, sua vida não é tão pior ou melhor que a mi -\\nnha, minha vida e a sua vida é uma constância em evolução \\npara aprendermos e ensinarmos aos nossos filhos, aos nossos \\nnetos, para nossa existência ser digna diante de um mundo \\nmelhor para todos nós. Nossa vida só vale apenas se fizermos \\nela valer apena, o seu tempo é único para você, cada segundo \\nquevocêperde,você está perdendo tempo de vida, perdendo \\ntempo que pode te ocasionar um dano futuro, pois qualquer \\ntempo de vida quevocê perde, você está perdendo o trajeto até \\na sua morte!\\nO seu caos do passado será o seu dano no futuro!\\nSem título-1   57Sem título-1   57 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 69426,
      "chapter": 2,
      "page": 57,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 36.37162162162162,
      "complexity_metrics": {
        "word_count": 222,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 44.4,
        "avg_word_length": 4.572072072072072,
        "unique_word_ratio": 0.6171171171171171,
        "avg_paragraph_length": 222.0,
        "punctuation_density": 0.12612612612612611,
        "line_break_count": 22,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "vida",
          "você",
          "tempo",
          "reclamamos",
          "enxergar",
          "termos",
          "melhor",
          "perdendo",
          "iremos",
          "fazem",
          "morte",
          "escuridão",
          "pior",
          "minha",
          "nossos",
          "nossa",
          "está",
          "dano",
          "futuro",
          "título"
        ],
        "entities": [
          [
            "57",
            "CARDINAL"
          ],
          [
            "das perdas de uma pessoa",
            "ORG"
          ],
          [
            "quando iremos reclamar e \\nnão",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "Todas",
            "PERSON"
          ],
          [
            "iremos conseguir enxergar",
            "ORG"
          ],
          [
            "para aprendermos",
            "PERSON"
          ],
          [
            "para nossa existência",
            "PERSON"
          ],
          [
            "digna diante de",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ]
        ],
        "readability_score": 76.42837837837838,
        "semantic_density": 0,
        "word_count": 222,
        "unique_words": 137,
        "lexical_diversity": 0.6171171171171171
      },
      "preservation_score": 1.6856219972313452e-05
    },
    {
      "id": 1,
      "text": "— 58 —“O lado bom de se viver… ”\\nO ser bom é relativo, nem sempre o que é bom para mim é \\nbom para você.\\nTem o lado bom, porém sombrio e tem o lado sombrio, \\nporém bom…\\nExemplos: você trabalha investigandomortes, nessas investi -\\ngações, como você vai saber interpretar se você não enxerga o \\nlado sombrio?\\nVocê tem um filho, você o cria dando tudo de “bom” , du -\\nrante toda essa criação ele teve tudo, quando ele ficar mais ve -\\nlho, qual vai ser o respeito por outros que não tiveramtudo de \\n“bom” igual ele teve?\\n Quem tem mais empatia e compaixão pelo próximo, o \\nbom sombrio ou o sombrio bom?\\nPreciso ter compaixão e razão.\\n“Ter compaixão sem razão é sofrimento para sipróprio. ”\\nQuando somos crianças não entendemos os motivos das \\nbrigas, das exigências, os motivos daquelas pessoas que nos \\namam fazerem aquelas situações, até porque se a pessoa que \\nme ama está fazendo isso, elame ama?\\nNão somos perfeitos, não sabemos de tudo, aprendemos \\ncom a vida, aprendemos com as conquistas, as perdas, o amor, \\nSem título-1   58Sem título-1   58 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 70800,
      "chapter": 2,
      "page": 58,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 28.375,
      "complexity_metrics": {
        "word_count": 192,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 24.0,
        "avg_word_length": 4.583333333333333,
        "unique_word_ratio": 0.671875,
        "avg_paragraph_length": 192.0,
        "punctuation_density": 0.16666666666666666,
        "line_break_count": 22,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "sombrio",
          "lado",
          "tudo",
          "compaixão",
          "porém",
          "teve",
          "quando",
          "mais",
          "razão",
          "somos",
          "motivos",
          "aprendemos",
          "título",
          "viver",
          "relativo",
          "sempre",
          "exemplos",
          "trabalha",
          "investigandomortes"
        ],
        "entities": [
          [
            "58",
            "CARDINAL"
          ],
          [
            "nem sempre o que",
            "ORG"
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
            "lado sombrio",
            "PERSON"
          ],
          [
            "dando tudo de “",
            "PERSON"
          ],
          [
            "toda essa criação ele teve tudo",
            "ORG"
          ],
          [
            "quando ele ficar mais",
            "PERSON"
          ],
          [
            "por outros que",
            "ORG"
          ],
          [
            "pelo próximo",
            "PERSON"
          ]
        ],
        "readability_score": 86.625,
        "semantic_density": 0,
        "word_count": 192,
        "unique_words": 129,
        "lexical_diversity": 0.671875
      },
      "preservation_score": 2.2006731630520344e-05
    },
    {
      "id": 1,
      "text": "— 59 —a dor… aprendemos quena vida não temos muitas escolhas, \\n“porém temos como evitar a maioria dos buracos, um sinal \\navançado, uma seta esquecida, um motoqueiro, uma árvore \\ncaída… ”\\nA vida é semelhante, pois temos uma noção da estrada \\nque iremos enfrentar, porém não sabemos as dificuldades que \\nessa mesma estrada irá nos proporcionar, mas podemos andar \\nde uma forma cautelosa que, mesmo caindo em buracos, so -\\nfrendo pequenos acidentes, temos como nos recuperar e nos \\nconsertar…\\nQuero trabalhar!\\nVocê quer trabalhar ou um emprego?\\nTrabalhar é você conquistar um emprego a base do seu \\nesforço… dar prioridade para o seu trabalho acima de quase \\ntudo…você percebe quevocê trabalha e não participa de mo -\\nmentos que vale mais à pena do que qualquer dinheiro… Você \\nperdeaniversários, diversão, carinho, sexo…\\nEmprego é você atingir uma qualidade de vida, quando \\ncolocamos em uma balança trabalho e necessidade sentimen -\\ntal, conseguimos tempo e o dinheiro suficiente para ter uma \\nvida digna.\\nCasa própria!\\nÉ um custo tão alto para ter quevocê nunca ficará satisfei -\\nto, sempre terá algo que possa melhorar…tudoque quebra, \\nSem título-1   59Sem título-1   59 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 72005,
      "chapter": 2,
      "page": 59,
      "segment_type": "page",
      "themes": {},
      "difficulty": 35.8559585492228,
      "complexity_metrics": {
        "word_count": 193,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 38.6,
        "avg_word_length": 5.186528497409326,
        "unique_word_ratio": 0.7357512953367875,
        "avg_paragraph_length": 193.0,
        "punctuation_density": 0.13471502590673576,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "vida",
          "temos",
          "trabalhar",
          "emprego",
          "porém",
          "como",
          "buracos",
          "estrada",
          "trabalho",
          "quevocê",
          "dinheiro",
          "título",
          "aprendemos",
          "quena",
          "muitas",
          "escolhas",
          "evitar",
          "maioria",
          "sinal"
        ],
        "entities": [
          [
            "59",
            "CARDINAL"
          ],
          [
            "motoqueiro",
            "ORG"
          ],
          [
            "da estrada",
            "ORG"
          ],
          [
            "porém não sabemos",
            "ORG"
          ],
          [
            "essa mesma",
            "ORG"
          ],
          [
            "estrada irá",
            "PERSON"
          ],
          [
            "mas podemos",
            "ORG"
          ],
          [
            "mesmo",
            "ORG"
          ],
          [
            "Quero",
            "PERSON"
          ],
          [
            "Trabalhar",
            "GPE"
          ]
        ],
        "readability_score": 79.1440414507772,
        "semantic_density": 0,
        "word_count": 193,
        "unique_words": 142,
        "lexical_diversity": 0.7357512953367875
      },
      "preservation_score": 1.8388603606160132e-05
    },
    {
      "id": 1,
      "text": "— 60 —estraga, arrumar mão de obra decente, garantia, calcular valo -\\nres… na maioria das vezes você tem um custo maior que mo -\\nrar de aluguel!\\nNós queremos uma vida que não sabemos o motivo pela -\\nqual queremos, pois imaginamos algo que não sabemos as di -\\nficuldades queexistem para termosos nossos próprios sonhos!\\nSonhos que podem se tomar pesadelos!\\nQuero ter um filho!\\nVocê quer ser pai (mãe) ou ter um filho? Ser pai (mãe) é \\num estilo vida, nunca mais terá só a sua vida. O que acontecer \\ncom o seu filho o efeito será diretamente em você, custos de \\numa vida, educação… minha opinião: não tenha filhos, se tiver \\nassuma a sua responsabilidade, pois tudo em sua vida será você \\ne seu filho. Se você não tiver, você não sabe os benefícios e os \\nmalefícios, é outra linha de tempo, é outro estilo de vida! \\nVocê quer trabalhar para ter dinheiro ou quer ter dinheiro \\nsem trabalhar?\\nTer dinheiro sem trabalhar:você é vagabundo,(rico) \\nplayboy. \\nSem título-1   60Sem título-1   60 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 73334,
      "chapter": 3,
      "page": 60,
      "segment_type": "page",
      "themes": {},
      "difficulty": 24.494841675178755,
      "complexity_metrics": {
        "word_count": 178,
        "sentence_count": 11,
        "paragraph_count": 1,
        "avg_sentence_length": 16.181818181818183,
        "avg_word_length": 4.679775280898877,
        "unique_word_ratio": 0.6853932584269663,
        "avg_paragraph_length": 178.0,
        "punctuation_density": 0.16292134831460675,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "vida",
          "filho",
          "quer",
          "trabalhar",
          "dinheiro",
          "queremos",
          "sabemos",
          "pois",
          "sonhos",
          "estilo",
          "será",
          "tiver",
          "título",
          "estraga",
          "arrumar",
          "obra",
          "decente",
          "garantia",
          "calcular"
        ],
        "entities": [
          [
            "60",
            "CARDINAL"
          ],
          [
            "arrumar mão de obra decente",
            "PERSON"
          ],
          [
            "garantia",
            "PERSON"
          ],
          [
            "pois imaginamos algo que",
            "PERSON"
          ],
          [
            "para termosos",
            "PERSON"
          ],
          [
            "se tomar",
            "PERSON"
          ],
          [
            "Quero",
            "PERSON"
          ],
          [
            "custos de \\numa vida",
            "PERSON"
          ],
          [
            "Se você não tiver",
            "PERSON"
          ],
          [
            "outra",
            "NORP"
          ]
        ],
        "readability_score": 90.50515832482125,
        "semantic_density": 0,
        "word_count": 178,
        "unique_words": 122,
        "lexical_diversity": 0.6853932584269663
      },
      "preservation_score": 1.738829762295466e-05
    },
    {
      "id": 1,
      "text": "— 61 —Ter dinheiro trabalhando:você não terá tempo para curtir \\no seu próprio dinheiro…você terá mais funcionários, fazendo \\nvocê ter mais preocupações diante da quantidade de pessoas \\nquevocê irá ter como responsabilidade….Irá chamar atenção \\npara situações inconvenientes, roubo, inveja, falsidade, ter me -\\nnos confiança, mudança do seu estilo de vida…\\nEstou trabalhando, coloque uma música que desperte uma \\nboa lembrança!\\nEstou em casa, coloque uma música que desperte uma boa \\nlembrança! \\nEstou sem comida, coloque umamúsica que desperte uma \\nboa lembrança!\\nEstamos em guerra, coloque uma música que desperte uma \\nboa lembrança!\\nEstou morrendo, coloque uma música que desperte uma \\nboa lembrança!\\nColoque cheiros agradáveis, um conforto visual, uma boa \\ncomida, ouvir bons sons, abrace,beije, toque em quemvo -\\ncê ama, pois você usando os cincosentidos, você saberá sen -\\ntir o melhor que cada momento da nossa vidapode nos pro -\\nporcionar!\\nSem título-1   61Sem título-1   61 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 74477,
      "chapter": 3,
      "page": 61,
      "segment_type": "page",
      "themes": {},
      "difficulty": 26.248026315789474,
      "complexity_metrics": {
        "word_count": 152,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 19.0,
        "avg_word_length": 5.618421052631579,
        "unique_word_ratio": 0.625,
        "avg_paragraph_length": 152.0,
        "punctuation_density": 0.20394736842105263,
        "line_break_count": 21,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "coloque",
          "você",
          "desperte",
          "lembrança",
          "estou",
          "música",
          "dinheiro",
          "trabalhando",
          "terá",
          "mais",
          "comida",
          "título",
          "tempo",
          "curtir",
          "próprio",
          "funcionários",
          "fazendo",
          "preocupações",
          "diante",
          "quantidade"
        ],
        "entities": [
          [
            "61",
            "CARDINAL"
          ],
          [
            "para curtir \\n",
            "PERSON"
          ],
          [
            "seu próprio dinheiro",
            "ORG"
          ],
          [
            "você terá mais funcionários",
            "PERSON"
          ],
          [
            "quevocê irá",
            "PERSON"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "Estamos",
            "PERSON"
          ],
          [
            "61Sem",
            "CARDINAL"
          ],
          [
            "61",
            "CARDINAL"
          ],
          [
            "15:08:3517/03/2022",
            "CARDINAL"
          ]
        ],
        "readability_score": 88.81447368421053,
        "semantic_density": 0,
        "word_count": 152,
        "unique_words": 95,
        "lexical_diversity": 0.625
      },
      "preservation_score": 1.743086383500596e-05
    },
    {
      "id": 1,
      "text": "— 62 —A vida é um “eterno desconforto” … se você não aprender a \\nviver no desconforto, você nunca irá reconhecer o que é con -\\nfortável!\\nExemplos de caos que fazem você encontrar a sua paz! \\nMeditação – você fica em posição desconfortável para en -\\ncontrar o conforto.\\nAtleta – resistência, empenho, esforço, paciência, dor física.\\nConquista – conquistar algo através da sua própria capaci -\\ndade (casamento:conquista diária, filho: conquista diária, tra -\\nbalho: conquista diária, amigos: conquista diária, carro, casa, \\ndinheiro…). Conquistar algo requer a maior sabedoria que é \\nsaber lidar com as situações adversas.\\nFelicidade – para você entender a sua felicidade,você tem \\nque entender sobre o que é ser triste, pois nós não conhece -\\nmos algo sem saber o motivo daquele conhecimento diante \\nde ser feliz… só sabemos o que nos faz felizquando sabemos o \\nque nos deixa triste, pois através dessa sabedoria podemos dar \\nvalor para o que realmente nos deixa felizes!\\nQueremos ter paz no nosso próprio caos! Na história, te -\\nmos os maiores exemplos de aceitar o caos, nos adaptar ao caos \\nou fazer o caos para conseguirmos evoluir a ponto de conse -\\nguirmos viver melhor…\\nSem título-1   62Sem título-1   62 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 75616,
      "chapter": 3,
      "page": 62,
      "segment_type": "page",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 27.945900755124057,
      "complexity_metrics": {
        "word_count": 206,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 22.88888888888889,
        "avg_word_length": 5.004854368932039,
        "unique_word_ratio": 0.6601941747572816,
        "avg_paragraph_length": 206.0,
        "punctuation_density": 0.1553398058252427,
        "line_break_count": 22,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "caos",
          "conquista",
          "diária",
          "algo",
          "desconforto",
          "viver",
          "exemplos",
          "conquistar",
          "através",
          "sabedoria",
          "saber",
          "felicidade",
          "entender",
          "triste",
          "pois",
          "sabemos",
          "deixa",
          "título",
          "vida"
        ],
        "entities": [
          [
            "62",
            "CARDINAL"
          ],
          [
            "Exemplos de caos",
            "ORG"
          ],
          [
            "Conquista",
            "NORP"
          ],
          [
            "dade",
            "GPE"
          ],
          [
            "diária",
            "GPE"
          ],
          [
            "diária",
            "GPE"
          ],
          [
            "diária",
            "GPE"
          ],
          [
            "diária",
            "GPE"
          ],
          [
            "casa",
            "ORG"
          ],
          [
            "faz",
            "ORG"
          ]
        ],
        "readability_score": 87.05409924487594,
        "semantic_density": 0,
        "word_count": 206,
        "unique_words": 136,
        "lexical_diversity": 0.6601941747572816
      },
      "preservation_score": 2.2006731630520344e-05
    },
    {
      "id": 1,
      "text": "— 63 —O Egito antigo era a maior potência.\\nOs mongóis eram a maior potência.\\nRoma era a maior potência.\\nPortugal era a maior potência.\\nEspanha era a maior potência.\\nInglaterra era a maior potência.\\nFrança era a maior potência.\\nAlemanha era a maior potência.\\nEstados Unidos é a maior potência. China, como o excesso \\nde população se adaptou, está virando a maior economia.\\nJapão se adaptou ao caos e criou um país com melhor in -\\nfraestrutura. “Não encontre a paz, encontre o conforto no seu \\npróprio caos!” \\nA nossa evolução não está em viver melhor, está em quem \\nse adapta em viver melhor, não controlamos as ações à nossa \\nvolta, não conseguimos controlar nem os nossos sentimentos, \\ncomo iremos controlar o que nós mesmos criamos desde o iní -\\ncio da humanidade?\\nMarcelo, você ultimamente mudou muito, está mais inteli -\\ngente, mais sábio… Você não era assim, o que aconteceu?\\nDeixei de pensar na fome, no caos, na necessidade básica, \\nabrindo espaço para pensar na evolução, felicidade e em viver \\nmelhor. Você não encontrará sua zona de conforto no meio do \\ncaos se você não se adaptar ao caos!!\\nSem título-1   63Sem título-1   63 17/03/2022   15:08:3517/03/2022   15:08:35",
      "position": 76984,
      "chapter": 3,
      "page": 63,
      "segment_type": "page",
      "themes": {},
      "difficulty": 24.356264705882353,
      "complexity_metrics": {
        "word_count": 200,
        "sentence_count": 17,
        "paragraph_count": 1,
        "avg_sentence_length": 11.764705882352942,
        "avg_word_length": 4.815,
        "unique_word_ratio": 0.605,
        "avg_paragraph_length": 200.0,
        "punctuation_density": 0.18,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "maior",
          "potência",
          "caos",
          "está",
          "melhor",
          "você",
          "viver",
          "como",
          "adaptou",
          "encontre",
          "conforto",
          "nossa",
          "evolução",
          "controlar",
          "mais",
          "pensar",
          "título",
          "egito",
          "antigo",
          "mongóis"
        ],
        "entities": [
          [
            "63",
            "CARDINAL"
          ],
          [
            "Egito",
            "PERSON"
          ],
          [
            "Portugal",
            "GPE"
          ],
          [
            "França",
            "GPE"
          ],
          [
            "China",
            "GPE"
          ],
          [
            "excesso \\nde população",
            "ORG"
          ],
          [
            "Japão",
            "PERSON"
          ],
          [
            "nós mesmos criamos",
            "ORG"
          ],
          [
            "Marcelo",
            "PERSON"
          ],
          [
            "mudou muito",
            "PERSON"
          ]
        ],
        "readability_score": 92.67314705882353,
        "semantic_density": 0,
        "word_count": 200,
        "unique_words": 121,
        "lexical_diversity": 0.605
      },
      "preservation_score": 2.298575450770016e-05
    },
    {
      "id": 1,
      "text": "— 64 —Lembra, os países que mais causaram o caos e se adaptaram \\nao caos no mundo são os países mais desenvolvidos.\\nTodos nós temos problemas, o problema não está em resol -\\nver o problema e sim em quanto tempo você perde pensando \\nou tentando resolver algo que não vai ser solucionado e sim \\nterque aceitar e pensar menos possível nele… quanto mais \\ntempo você perde tempo pensando nele, mais tempo você vai \\nperdendo de vida,simplesmente pela sua própria importância \\ndiante do mesmo!\\nO ser humano está se acostumando tanto com o caos que \\nquando vem uma lembrança ou uma solução diante de algo a \\nprimeira resposta que vem na maioria das vezes é o lado ruim \\nda solução…\\nTia, estou preocupado com meu filho, ele é muito satisfeito \\ncom a vida dele, ele não sabe o que vai ser na vida e ele tem 11 \\nanos.Tem que começar a pensar no amanhã… como vocêlidou \\ncom isso?\\nMeu filho, olha à sua volta; veja seus irmãos e seus primos, \\neu e sua mãe só fizemos o melhor que podíamos fazer e a vida \\nSem título-1   64Sem título-1   64 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 78278,
      "chapter": 3,
      "page": 64,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.6375,
      "complexity_metrics": {
        "word_count": 192,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 38.4,
        "avg_word_length": 4.458333333333333,
        "unique_word_ratio": 0.6302083333333334,
        "avg_paragraph_length": 192.0,
        "punctuation_density": 0.09375,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "tempo",
          "vida",
          "caos",
          "você",
          "países",
          "problema",
          "está",
          "quanto",
          "perde",
          "pensando",
          "algo",
          "pensar",
          "nele",
          "diante",
          "solução",
          "filho",
          "seus",
          "título",
          "lembra"
        ],
        "entities": [
          [
            "64",
            "CARDINAL"
          ],
          [
            "Lembra",
            "PERSON"
          ],
          [
            "Todos",
            "GPE"
          ],
          [
            "nós temos problemas",
            "ORG"
          ],
          [
            "você perde pensando",
            "ORG"
          ],
          [
            "nele",
            "PERSON"
          ],
          [
            "quanto mais",
            "PERSON"
          ],
          [
            "pensando nele",
            "PERSON"
          ],
          [
            "simplesmente pela",
            "PERSON"
          ],
          [
            "sua própria",
            "FAC"
          ]
        ],
        "readability_score": 79.4625,
        "semantic_density": 0,
        "word_count": 192,
        "unique_words": 121,
        "lexical_diversity": 0.6302083333333334
      },
      "preservation_score": 9.300717333208306e-06
    },
    {
      "id": 1,
      "text": "— 65 —de vocêsforamacontecendo as coisas dentro do tempo de cada \\num de vocês!\\nSabedoria não está só na leitura, vídeos, áudios e sim na \\nmaior parte do tempo sempre esteve à sua volta,basta vocêape -\\nnas saber interpretar o quevocê quer de melhor para simesmo, \\ndiante de sua própria vida!\\nCuriosidade!\\nVocê trabalha, conquista uma independência financeira, \\ntem um carro, uma casa bacana, um dinheiro na conta, aí eu \\nte pergunto: se você conquistou tudoquevocê tem através das \\nsuas conquistas, você conquista homem ou mulher através do \\nseu carro, sua casa, seu dinheiro, isso é interesse do outro ou \\na oportunidade de ter com o outro o que ele não tinha, uma \\naparência para ter aquela outra pessoa,que através das suas \\nconquistas consegue ter alguém mais novo(a), bonito(a), gos -\\ntoso(a), isso é conquista ou o quê?\\nMinha opinião: eu vejo que independente de qualquer \\ncoisa, é uma conquista, pois quem está entrando no relaciona -\\nmento já está entrando sabendo da sua limitação!\\nA anormalidade é tão normal que, mesmo quando acon -\\ntece alguma coisa com você, anormal, esse mesmo anormal já \\nSem título-1   65Sem título-1   65 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 79462,
      "chapter": 3,
      "page": 65,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 32.58799654576856,
      "complexity_metrics": {
        "word_count": 193,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 32.166666666666664,
        "avg_word_length": 5.015544041450777,
        "unique_word_ratio": 0.7098445595854922,
        "avg_paragraph_length": 193.0,
        "punctuation_density": 0.17616580310880828,
        "line_break_count": 21,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "conquista",
          "está",
          "através",
          "tempo",
          "carro",
          "casa",
          "dinheiro",
          "suas",
          "conquistas",
          "isso",
          "outro",
          "coisa",
          "entrando",
          "mesmo",
          "anormal",
          "título",
          "vocêsforamacontecendo",
          "coisas",
          "dentro"
        ],
        "entities": [
          [
            "65",
            "CARDINAL"
          ],
          [
            "coisas",
            "NORP"
          ],
          [
            "basta",
            "NORP"
          ],
          [
            "quevocê quer de melhor",
            "ORG"
          ],
          [
            "para simesmo",
            "PERSON"
          ],
          [
            "diante de sua própria",
            "PERSON"
          ],
          [
            "independência financeira",
            "PERSON"
          ],
          [
            "aí eu \\nte",
            "PERSON"
          ],
          [
            "aparência para",
            "PERSON"
          ],
          [
            "aquela",
            "PERSON"
          ]
        ],
        "readability_score": 82.41200345423144,
        "semantic_density": 0,
        "word_count": 193,
        "unique_words": 137,
        "lexical_diversity": 0.7098445595854922
      },
      "preservation_score": 2.1453370873853485e-05
    },
    {
      "id": 1,
      "text": "— 66 —aconteceu com outro alguém normal…anormalidade é algo \\nfora do padrão e não algo para você se julgar como pior ou \\nmelhor.\\nViva, sinta e deixe o próprio tempo direcionar a sua pró -\\npria vida.\\nO sentir compaixão por alguém é você sentir falta de com -\\npaixão para si mesmo… sua vida tem dor, felicidade, batalhas, \\namor, diversidade, acaso, foco, determinação…você tem com -\\npaixão por si mesmo diante da sua própria vida? Compaixão \\ntemos que usar para entender e melhorar a vida, e não um ga -\\ntilho emocional parasofrermoscom a compaixão que nós mes -\\nmos criamos!\\nQuanto mais problemas temos, menos tempo temos para \\npensar em resolver os nossos próprios problemas…\\nComo assim?Quanto tempo você gasta pensando em traba -\\nlhar para ter o que comer?\\nPagar as contas?\\nAluguel?\\nEscola? \\nCarro?\\nSe você tem uma estrutura familiar que faça você não se \\nimportar com esses problemas, como vocêusaria o seu tempo? -\\nSe você é criado com essa estrutura familiar, como seria o seu \\npensamento?\\nSem título-1   66Sem título-1   66 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 80757,
      "chapter": 3,
      "page": 66,
      "segment_type": "page",
      "themes": {},
      "difficulty": 27.42153846153846,
      "complexity_metrics": {
        "word_count": 180,
        "sentence_count": 13,
        "paragraph_count": 1,
        "avg_sentence_length": 13.846153846153847,
        "avg_word_length": 4.866666666666666,
        "unique_word_ratio": 0.6833333333333333,
        "avg_paragraph_length": 180.0,
        "punctuation_density": 0.15555555555555556,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "como",
          "tempo",
          "vida",
          "compaixão",
          "temos",
          "problemas",
          "alguém",
          "algo",
          "sentir",
          "paixão",
          "mesmo",
          "quanto",
          "estrutura",
          "familiar",
          "título",
          "aconteceu",
          "outro",
          "normal",
          "anormalidade"
        ],
        "entities": [
          [
            "66",
            "CARDINAL"
          ],
          [
            "julgar como",
            "ORG"
          ],
          [
            "Viva",
            "ORG"
          ],
          [
            "pria",
            "GPE"
          ],
          [
            "mesmo",
            "ORG"
          ],
          [
            "diversidade",
            "GPE"
          ],
          [
            "foco",
            "ORG"
          ],
          [
            "ga",
            "ORG"
          ],
          [
            "Quanto mais problemas temos",
            "PERSON"
          ],
          [
            "Pagar",
            "PERSON"
          ]
        ],
        "readability_score": 91.61692307692307,
        "semantic_density": 0,
        "word_count": 180,
        "unique_words": 123,
        "lexical_diversity": 0.6833333333333333
      },
      "preservation_score": 1.9920987240006808e-05
    },
    {
      "id": 1,
      "text": "— 67 —Assim funciona a qualidade de vida nos países desenvol -\\nvidos, criando mais tempo para estudar, evoluir a tecnologia, \\nevoluir o nosso conforto, evoluir a mente humana lparater \\nmais tempo de sobra para pensar em algomelhor para uma \\nsociedade!\\nO que é mais fácil?\\nCurar um ser humano cheios de erros ou curar os erros do \\nser humano?\\nNossa vida, nossas escolhas, nossa direção, nossa estrada, \\nnosso caminho = malefícios ou benefícios de acordo com o \\nmeu querer viver!\\nQueremos tanto uma vida que não vivemos…\\nVivemos em boates, putaria, curtição e queremos um bom \\nrelacionamento… vivemos gastando dinheiro em coisas desne -\\ncessárias e queremos ter uma boa vida financeira…\\nQueremos pessoas felizes à nossa volta, porém não somos \\nfelizes o suficiente…\\nQueremos viver, porém não sabemos o que vivemos…\\nNós sempre queremos mais, sem fazer o necessário \\nque possa nos proporcionar o que queremos a mais, se não \\nSem título-1   67Sem título-1   67 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 81943,
      "chapter": 3,
      "page": 67,
      "segment_type": "page",
      "themes": {
        "ciencia": 56.52173913043479,
        "tecnologia": 43.47826086956522
      },
      "difficulty": 32.539375,
      "complexity_metrics": {
        "word_count": 160,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 32.0,
        "avg_word_length": 5.13125,
        "unique_word_ratio": 0.675,
        "avg_paragraph_length": 160.0,
        "punctuation_density": 0.1375,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "queremos",
          "mais",
          "vida",
          "nossa",
          "vivemos",
          "evoluir",
          "tempo",
          "nosso",
          "curar",
          "humano",
          "erros",
          "viver",
          "felizes",
          "porém",
          "título",
          "assim",
          "funciona",
          "qualidade",
          "países",
          "desenvol"
        ],
        "entities": [
          [
            "67",
            "CARDINAL"
          ],
          [
            "para estudar",
            "PERSON"
          ],
          [
            "evoluir",
            "PERSON"
          ],
          [
            "Nossa",
            "PERSON"
          ],
          [
            "nossas escolhas",
            "PERSON"
          ],
          [
            "nossa direção",
            "PERSON"
          ],
          [
            "nossa estrada",
            "PERSON"
          ],
          [
            "Queremos",
            "PERSON"
          ],
          [
            "Vivemos",
            "PERSON"
          ],
          [
            "vivemos gastando dinheiro",
            "PERSON"
          ]
        ],
        "readability_score": 82.460625,
        "semantic_density": 0,
        "word_count": 160,
        "unique_words": 108,
        "lexical_diversity": 0.675
      },
      "preservation_score": 1.191853937436305e-05
    },
    {
      "id": 1,
      "text": "— 68 —enxergamos o que vem à nossa frente, como queremos enxer -\\ngar o que pode vir mais à frente?\\nFiquei em depressão muitos anos por julgar erros de ou -\\ntros, até porque quando você não está feliz, não está se achan -\\ndo na vida, qual é a sua fuga? Falar de “erros” de uma pessoa é \\nfácil, difícil é entender o motivo.\\nTodos nós temos problemas, dificuldades, decepção e por \\nmuitas vezes não sabemos em qual direção ir, nos fazendo ir \\nem uma direção que talvez seja julgada como desnecessária!\\nAs pessoas se preocupam muito com o erro dos outros…\\nSe alguém erra, e ele sendo o maior prejudicado, o proble -\\nma é dele.\\nSe um funcionário falta o trabalho, a culpa é de quem?\\nSe um jogador de futebol, lutador, artista, médico, advoga -\\ndo, pedreiro, faxineiro… falha com a sua obrigação, o proble -\\nma é de cada um, pois plantamos e iremos ter uma colheita, \\nqual colheita você quer ter? Foda-se que ele foi ao bingo, night, \\ndrogas, bebida e ele errou diante do seu trabalho e da sua vida, \\nnão sou eu que irei me preocupar.\\nSem título-1   68Sem título-1   68 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 83056,
      "chapter": 3,
      "page": 68,
      "segment_type": "page",
      "themes": {},
      "difficulty": 27.59304871373837,
      "complexity_metrics": {
        "word_count": 203,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 22.555555555555557,
        "avg_word_length": 4.384236453201971,
        "unique_word_ratio": 0.6945812807881774,
        "avg_paragraph_length": 203.0,
        "punctuation_density": 0.17733990147783252,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "qual",
          "frente",
          "como",
          "erros",
          "você",
          "está",
          "vida",
          "direção",
          "proble",
          "trabalho",
          "colheita",
          "título",
          "enxergamos",
          "nossa",
          "queremos",
          "enxer",
          "pode",
          "mais",
          "fiquei",
          "depressão"
        ],
        "entities": [
          [
            "68",
            "CARDINAL"
          ],
          [
            "vir mais",
            "PERSON"
          ],
          [
            "Fiquei",
            "GPE"
          ],
          [
            "julgar erros de ou -\\n",
            "ORG"
          ],
          [
            "quando você não",
            "PERSON"
          ],
          [
            "Todos",
            "GPE"
          ],
          [
            "nós temos problemas",
            "ORG"
          ],
          [
            "direção ir",
            "PERSON"
          ],
          [
            "que",
            "CARDINAL"
          ],
          [
            "talvez seja",
            "ORG"
          ]
        ],
        "readability_score": 87.40695128626163,
        "semantic_density": 0,
        "word_count": 203,
        "unique_words": 141,
        "lexical_diversity": 0.6945812807881774
      },
      "preservation_score": 1.9814571709878563e-05
    },
    {
      "id": 1,
      "text": "— 69 —Eu sei quais são as minhas obrigações, se você não cumpriu \\ncom a sua, o problema é seu.\\nNão julgue todos por um. Nem todos que moram na favela \\nsão bandidos, nem todos os ricos são pessoas fechadas, nem to -\\ndos os famosos são inteligentes, nem todos sabem o benefício \\ne o malefício diante da sua própria vida!\\nQual é o valor monetário para se viver com dignidade? Até -\\nque ponto é necessário ganhar mais dinheiro para se viver?\\nColoca na balança e analisa até que ponto eu deixo de viver \\npara ganhar mais dinheiro.\\nQual é o maior valor monetário para eu viver o melhor que \\na vida possa me dar?Qual é a quantidade de esforço necessário \\npara se ter um valor monetário de acordo com o seu desejo de \\nviver o melhor que a vida pode lhe proporcionar? Qual é a sua \\nreferência monetária diante da sua necessidade financeira?\\nA maior certeza que eu tenho na vida são os meus erros, \\nporém quais são eles?\\nEu não tenho certeza.Meu julgamento sempre vai estar \\nerrado.\\nSem título-1   69Sem título-1   69 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 84277,
      "chapter": 3,
      "page": 69,
      "segment_type": "page",
      "themes": {},
      "difficulty": 23.4167348608838,
      "complexity_metrics": {
        "word_count": 188,
        "sentence_count": 13,
        "paragraph_count": 1,
        "avg_sentence_length": 14.461538461538462,
        "avg_word_length": 4.49468085106383,
        "unique_word_ratio": 0.5904255319148937,
        "avg_paragraph_length": 188.0,
        "punctuation_density": 0.11702127659574468,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "viver",
          "todos",
          "vida",
          "qual",
          "valor",
          "monetário",
          "quais",
          "diante",
          "ponto",
          "necessário",
          "ganhar",
          "mais",
          "dinheiro",
          "maior",
          "melhor",
          "certeza",
          "tenho",
          "título",
          "minhas",
          "obrigações"
        ],
        "entities": [
          [
            "69",
            "CARDINAL"
          ],
          [
            "Eu",
            "PERSON"
          ],
          [
            "nem todos",
            "PERSON"
          ],
          [
            "ricos são pessoas fechadas",
            "ORG"
          ],
          [
            "nem todos",
            "PERSON"
          ],
          [
            "benefício \\ne",
            "PERSON"
          ],
          [
            "malefício diante da sua própria",
            "PERSON"
          ],
          [
            "valor monetário para se viver com",
            "PERSON"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "ganhar mais dinheiro",
            "PERSON"
          ]
        ],
        "readability_score": 91.42082651391162,
        "semantic_density": 0,
        "word_count": 188,
        "unique_words": 111,
        "lexical_diversity": 0.5904255319148937
      },
      "preservation_score": 1.1322612405644895e-05
    },
    {
      "id": 1,
      "text": "— 70 —Como eu sei dos meus próprios erros?O maior aprendizado \\nda vida é sempre aprender.\\nNão sou o melhor advogado, médico, físico, químico … po -\\nrém, posso entender um pouco melhor, perguntando os por -\\nquês necessários de acordo com a minha necessidade!\\nTodos acertamos e erramos, até que ponto eu estou certo \\ndiante da sua certeza?\\nPergunte os porquês ao invés de pensar que os porquêsque -\\nvocê perguntou diante da situação é a melhor direção…\\nSua mente só absorve aquilo que ela dá importância.\\nVocê só deixa de gostar de alguém quando percebe que não \\nprecisa se importar mais com aquele alguém.\\nVocê só melhora na escola e em seu trabalhoquando você \\nse importa em melhorar.\\nVocê só consegue administrar melhor seu financeiro quan -\\ndo você gasta com o que importa para melhorar a sua vida \\namanhã.\\nVocê só: melhora a sua vida quando você se importa com a \\nsua própria vida.\\nO principal problema da importância é você entender que \\nvocêé o que importa, pois se você não se conhece, como sa -\\nberá reconhecer o seu caráter e  nãoreconhecer o seu caráter \\né desconhecer a sua maior qualidade e o seu maior defeito, \\nSem título-1   70Sem título-1   70 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 85442,
      "chapter": 3,
      "page": 70,
      "segment_type": "page",
      "themes": {},
      "difficulty": 26.857692307692307,
      "complexity_metrics": {
        "word_count": 208,
        "sentence_count": 10,
        "paragraph_count": 1,
        "avg_sentence_length": 20.8,
        "avg_word_length": 4.6923076923076925,
        "unique_word_ratio": 0.625,
        "avg_paragraph_length": 208.0,
        "punctuation_density": 0.11057692307692307,
        "line_break_count": 23,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "vida",
          "melhor",
          "importa",
          "maior",
          "como",
          "entender",
          "diante",
          "importância",
          "alguém",
          "quando",
          "melhora",
          "melhorar",
          "caráter",
          "título",
          "meus",
          "próprios",
          "erros",
          "aprendizado",
          "sempre"
        ],
        "entities": [
          [
            "70",
            "CARDINAL"
          ],
          [
            "Como eu",
            "PRODUCT"
          ],
          [
            "físico",
            "GPE"
          ],
          [
            "químico",
            "GPE"
          ],
          [
            "pouco melhor",
            "PERSON"
          ],
          [
            "Todos",
            "GPE"
          ],
          [
            "erramos",
            "GPE"
          ],
          [
            "até que",
            "ORG"
          ],
          [
            "eu estou",
            "PERSON"
          ],
          [
            "Pergunte",
            "PERSON"
          ]
        ],
        "readability_score": 88.1923076923077,
        "semantic_density": 0,
        "word_count": 208,
        "unique_words": 130,
        "lexical_diversity": 0.625
      },
      "preservation_score": 1.5664366034877146e-05
    },
    {
      "id": 1,
      "text": "— 71 —como você vai saber as principais lembranças quevocê tem, \\ndiante daquilo que é importante para você?\\nO valor da importância não está em algo quevocê não co -\\nnhece, o valor da importância está naquilo quevocê se importa \\nem querer viver!\\nQuase todos os problemas em sua vida acontecemde acordo \\ncom a importância que você dá diante do mesmo, pois aquele \\nproblema do seu amigo, irmão, mãe, pai, filho, conhecido, ve -\\nlho, adulto, criança, gay, mulher, homem, todas as pessoas, só \\nte trazem problema na mesma proporção da sua importância!\\nAção e reação!\\nVento que venta lá, venta cá!\\nCausa e efeito!\\nSua expectativa é a mesma proporção da decepção diante \\nda sua própria expectativa e quando se gera muita expectativa \\npode se transformar em depressão!\\nSe eu não me importar, eu me transformo em uma pessoa \\nsem sentimento, como irei viver sem me importar?\\nPara eu viver o melhor da vida eu tenho que aceitar o pior \\nda vida (morte)…\\nSem título-1   71Sem título-1   71 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 86758,
      "chapter": 3,
      "page": 71,
      "segment_type": "page",
      "themes": {},
      "difficulty": 26.004974160206718,
      "complexity_metrics": {
        "word_count": 172,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 19.11111111111111,
        "avg_word_length": 4.8313953488372094,
        "unique_word_ratio": 0.686046511627907,
        "avg_paragraph_length": 172.0,
        "punctuation_density": 0.18023255813953487,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "importância",
          "você",
          "quevocê",
          "diante",
          "viver",
          "vida",
          "expectativa",
          "como",
          "valor",
          "está",
          "problema",
          "mesma",
          "proporção",
          "venta",
          "importar",
          "título",
          "saber",
          "principais",
          "lembranças",
          "daquilo"
        ],
        "entities": [
          [
            "71",
            "CARDINAL"
          ],
          [
            "lembranças quevocê",
            "PERSON"
          ],
          [
            "importante para você",
            "PERSON"
          ],
          [
            "importa",
            "GPE"
          ],
          [
            "problemas em sua vida acontecemde",
            "ORG"
          ],
          [
            "todas",
            "PERSON"
          ],
          [
            "Sua",
            "PERSON"
          ],
          [
            "quando se gera muita",
            "PERSON"
          ],
          [
            "transformar em depressão",
            "ORG"
          ],
          [
            "Se eu",
            "PERSON"
          ]
        ],
        "readability_score": 88.99502583979329,
        "semantic_density": 0,
        "word_count": 172,
        "unique_words": 118,
        "lexical_diversity": 0.686046511627907
      },
      "preservation_score": 1.6600822700005675e-05
    },
    {
      "id": 1,
      "text": "— 72 —Como eu aceito a morte?\\nSe o mundo do jeito que está já está com excesso de huma -\\nnos, imagina se não tem morte?\\nO maior egoísmo seria não perceber que é necessário, ou -\\ntras pessoas morrerem para nascerem outras pessoas… eu nas -\\nci e tenho uma vida, meu filho nasceu e tem uma vida… como \\nseriam as nossas vidas se outras pessoas não tivessem morrido \\ne deixado um legado, seja ele ruim ou bom?\\nTodos os dias morrem pais, mães, filhos, primos, amigos de \\ntodas as formas, a vida só tem valor por termos uma só vida. \\nSe eu não viver a minha vida, como posso melhorar a vida de \\noutros, qual vai ser o meu legado? Eu não posso fazer você se \\nimportar pela sua vida, pois você já está com uma idade cheias \\nde costumes, vícios, conclusões, caráter, certezas… eu só posso \\nte ensinar algo se você se importa com aquilo que estou te en -\\nsinando e assim o mesmo serve para mim.\\nCoisas que a Covid-19está acabando com o ser humano …\\nDesde que a espécie humana existe, nós temos contatos um \\ncom o outro, fomos acostumados a deitarmos um com o outro \\npara nos aquecermos. Nesse contato passamos sentimentos, \\ndesejos, sensações que venho junto com a evolução de um sen -\\ntir o outro.\\nA não aproximação de pessoas está nos transformando em \\npessoas mais distantes do que já somos!\\nSem título-1   72Sem título-1   72 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 87892,
      "chapter": 3,
      "page": 72,
      "segment_type": "page",
      "themes": {},
      "difficulty": 28.766867469879518,
      "complexity_metrics": {
        "word_count": 249,
        "sentence_count": 10,
        "paragraph_count": 1,
        "avg_sentence_length": 24.9,
        "avg_word_length": 4.389558232931727,
        "unique_word_ratio": 0.642570281124498,
        "avg_paragraph_length": 249.0,
        "punctuation_density": 0.13253012048192772,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "vida",
          "pessoas",
          "está",
          "como",
          "posso",
          "você",
          "outro",
          "morte",
          "outras",
          "legado",
          "título",
          "aceito",
          "mundo",
          "jeito",
          "excesso",
          "huma",
          "imagina",
          "maior",
          "egoísmo",
          "seria"
        ],
        "entities": [
          [
            "72",
            "CARDINAL"
          ],
          [
            "Como eu",
            "PRODUCT"
          ],
          [
            "Se",
            "PERSON"
          ],
          [
            "excesso de huma -\\n",
            "PERSON"
          ],
          [
            "imagina se não",
            "PERSON"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "morrerem para nascerem outras pessoas",
            "PERSON"
          ],
          [
            "eu nas -\\nci",
            "PERSON"
          ],
          [
            "seriam",
            "GPE"
          ],
          [
            "nossas vidas",
            "PERSON"
          ]
        ],
        "readability_score": 86.23313253012049,
        "semantic_density": 0,
        "word_count": 249,
        "unique_words": 160,
        "lexical_diversity": 0.642570281124498
      },
      "preservation_score": 2.1964165418469048e-05
    },
    {
      "id": 1,
      "text": "— 73 —“Extinção do ser humano e estamos nos transformando em \\nHUMANOS. ”\\nPorque uma pessoa mata? Porque uma pessoa assalta?\\nUma mãe que usa crack tem um filho, essa mesma mãe usa \\nesse mesmo filho para ganhar dinheiro para “comer” … Nesse \\nmomento entra um dilema, se eu ajudar, irei sustentar o vício \\ndo crack, porém se eu não ajudar aquela criança pode morrer \\nde fome…\\nEssa mesma criança cresce com a mãe viciada, pedindo di -\\nnheiro através daquela criança. Após um tempo, ele mesmo \\ncomeça a pedir dinheiro para sustentar o vício da mãe e talvez \\no dele, quando essa mesma criança te pede dinheiro, como é a \\nsua reação? Como você acha que essa criança foi criada a vida \\ntoda, vivendo nessa vida? Alguma vez você deu um abraço em \\numa criança dessas? Um beijo? Um olhar de amor? Quando \\npensamos no início da vida, pensamos em como a vida faz sen -\\ntindo diante das nossas próprias falhas!\\nSe todo mundo que estuda fosse inteligente, nós só tería -\\nmos Leonardo daVinci, Tesla, Pitágoras, Einstein… não con -\\nfundem uma pessoa que tem um estudo como se o estudo \\nSem título-1   73Sem título-1   73 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 89368,
      "chapter": 3,
      "page": 73,
      "segment_type": "page",
      "themes": {},
      "difficulty": 25.557065706570658,
      "complexity_metrics": {
        "word_count": 202,
        "sentence_count": 11,
        "paragraph_count": 1,
        "avg_sentence_length": 18.363636363636363,
        "avg_word_length": 4.584158415841584,
        "unique_word_ratio": 0.698019801980198,
        "avg_paragraph_length": 202.0,
        "punctuation_density": 0.13861386138613863,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "criança",
          "essa",
          "como",
          "vida",
          "pessoa",
          "mesma",
          "dinheiro",
          "porque",
          "crack",
          "filho",
          "mesmo",
          "ajudar",
          "sustentar",
          "vício",
          "quando",
          "você",
          "pensamos",
          "estudo",
          "título",
          "extinção"
        ],
        "entities": [
          [
            "73",
            "CARDINAL"
          ],
          [
            "HUMANOS",
            "ORG"
          ],
          [
            "Uma mãe que usa",
            "ORG"
          ],
          [
            "essa mesma mãe usa",
            "ORG"
          ],
          [
            "ganhar dinheiro",
            "PERSON"
          ],
          [
            "Nesse",
            "ORG"
          ],
          [
            "se eu ajudar",
            "PERSON"
          ],
          [
            "se eu não ajudar",
            "PERSON"
          ],
          [
            "aquela criança pode morrer \\nde fome",
            "PERSON"
          ],
          [
            "Essa",
            "ORG"
          ]
        ],
        "readability_score": 89.44293429342935,
        "semantic_density": 0,
        "word_count": 202,
        "unique_words": 141,
        "lexical_diversity": 0.698019801980198
      },
      "preservation_score": 1.702648482051864e-05
    },
    {
      "id": 1,
      "text": "— 74 —dele sempre estivesse certo… Se todos os estudiosos tivessem \\nacertado, porque temos que reestudar o estudo da pessoa que \\nacha que chegou a um estudo concreto?\\nSempre temos que evoluir, não fique cego diante daqui -\\nlo que um especialista diz, pois assim como grandes filóso -\\nfos, cientistas, médicos e etecetera erraram,porquevocê acha \\nquehoje será diferente dos anos anteriores? Todos nós erramos, \\ntodos nós acertamos, basta termos a sabedoria de reconhecer \\nque sempre podemos melhorar algo que imaginamos ser“im -\\npossível de melhorar!” .\\nDiferença entre preconceito e estereótipo preconceituoso!\\nPreconceito – pessoas que não enxergam a dor ou a dificul -\\ndade do outro, tornando uma pessoa egoísta a ponto de pensar \\nque a sua cor, seu sexo, sua raça, sua religião, sua vida é a forma \\nmelhor para se viver.\\nExemplo: aqueles homens estão se pegando, que horrível, \\nDeus não aceita isso e ainda são pretos…\\nEstereótipo preconceituoso – é aquele preconceito que es -\\ntamos vivendo e nem percebemos que temos, devido a criação \\nque tivemos.\\nExemplo: um jogador de futebol preto ficou rico e namora \\numa loira de olhos claros… um empresário rico de cor branca \\nnão se relaciona com uma negra…\\nSem título-1   74Sem título-1   74 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 90630,
      "chapter": 3,
      "page": 74,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.46938405797101,
      "complexity_metrics": {
        "word_count": 207,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 25.875,
        "avg_word_length": 5.106280193236715,
        "unique_word_ratio": 0.714975845410628,
        "avg_paragraph_length": 207.0,
        "punctuation_density": 0.14009661835748793,
        "line_break_count": 23,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "sempre",
          "todos",
          "temos",
          "preconceito",
          "estudo",
          "pessoa",
          "acha",
          "melhorar",
          "estereótipo",
          "preconceituoso",
          "exemplo",
          "rico",
          "título",
          "dele",
          "estivesse",
          "certo",
          "estudiosos",
          "tivessem",
          "acertado",
          "porque"
        ],
        "entities": [
          [
            "74",
            "CARDINAL"
          ],
          [
            "Se",
            "PERSON"
          ],
          [
            "Sempre",
            "ORG"
          ],
          [
            "cientistas",
            "ORG"
          ],
          [
            "médicos",
            "ORG"
          ],
          [
            "etecetera erraram",
            "ORG"
          ],
          [
            "porquevocê acha \\nquehoje",
            "PERSON"
          ],
          [
            "Todos",
            "GPE"
          ],
          [
            "nós erramos",
            "GPE"
          ],
          [
            "todos",
            "CARDINAL"
          ]
        ],
        "readability_score": 85.53061594202899,
        "semantic_density": 0,
        "word_count": 207,
        "unique_words": 148,
        "lexical_diversity": 0.714975845410628
      },
      "preservation_score": 1.9580457543596434e-05
    },
    {
      "id": 1,
      "text": "— 75 —Vendedor de shopping negro quase não se vê devido ao \\nconforto de uma imagem de aceitação diante da cor (70 a 80 \\nporcento das favelas são negros, nessa mesma favela tem tráfi -\\nco, tiros, assaltos).Como você enxerga uma cor predominante, \\ndiante de viver em um local que ele não teve escolha e sim \\njulgamento devido a sua cor ser maioria, no caso de noticiários \\ncriminosos, assaltos, traficantes… isso é o preconceito que a \\nsociedade impôs.\\nPorque os negros são a maioria nas favelas?\\nEm 1888 foi criada a lei Áurea. Quando ela foi criada, os \\nnegros que eram escravos nas fazendas, nas casas, deixaram de \\nser escravos e viraram “trabalhadores” sem trabalho… quan -\\ndo“extinguiu” a escravidão, nenhum empresário, fazendeiro, \\npolítico, pessoas que tinham condições de empregar alguém \\nnão empregavam, pois o custo era mais alto e “você é negro \\nnão condiz com o valor que eu estou pagando” , fazendo os ne -\\ngros ocuparem lugares quehoje se chamam favelas!\\nNós estamos acostumados a viver em um mundo machista, \\nonde nesse mesmo mundo a mulher era tratada como obje -\\nto,  tornando uma pessoa “inferior” , devido ao homem ter mais \\nforça, ser visto como base da família, a pessoa que tem direito \\nao dinheiro da família. Hojeainda temos mulheres que saem \\ncom homens e falam que os homens são obrigados a pagar a \\nconta, tenho que cuidar da casa, sou mãe (sou pai igual você \\nSem título-1   75Sem título-1   75 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 92027,
      "chapter": 3,
      "page": 75,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.2264400921659,
      "complexity_metrics": {
        "word_count": 248,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 35.42857142857143,
        "avg_word_length": 4.80241935483871,
        "unique_word_ratio": 0.6895161290322581,
        "avg_paragraph_length": 248.0,
        "punctuation_density": 0.13306451612903225,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "devido",
          "favelas",
          "negros",
          "como",
          "você",
          "negro",
          "diante",
          "assaltos",
          "viver",
          "maioria",
          "criada",
          "escravos",
          "mais",
          "mundo",
          "pessoa",
          "família",
          "homens",
          "título",
          "vendedor",
          "shopping"
        ],
        "entities": [
          [
            "75",
            "CARDINAL"
          ],
          [
            "Vendedor de shopping negro",
            "ORG"
          ],
          [
            "70",
            "CARDINAL"
          ],
          [
            "80",
            "CARDINAL"
          ],
          [
            "das",
            "ORG"
          ],
          [
            "cor ser maioria",
            "PRODUCT"
          ],
          [
            "1888",
            "DATE"
          ],
          [
            "Áurea",
            "GPE"
          ],
          [
            "Quando ela",
            "PERSON"
          ],
          [
            "nas fazendas",
            "PERSON"
          ]
        ],
        "readability_score": 80.84498847926267,
        "semantic_density": 0,
        "word_count": 248,
        "unique_words": 171,
        "lexical_diversity": 0.6895161290322581
      },
      "preservation_score": 2.656131632000908e-05
    },
    {
      "id": 1,
      "text": "— 76 —que é mãe), coisas que as mulheres foram acostumadas a viver \\npor serem “inferiores” . \\nAté que ponto estamos vivendo uma farsa que se chama \\nsociedade? Vamos enxergar o início para compreendermos o \\nque estamos vivendo hoje e amanhã!\\nQual é a diferença entre vício, usuário e dependente?\\nVício – algo que você usa prejudicando o que é necessário \\npara a sua vida!\\nUsuário – algo quevocê usa sem prejudicar sua vida!\\nDependente – algo quevocê usa por depender de usar para \\nviver melhor!\\nNão confunda alcoólatracom beber.\\nNão confunda viciado em maconha com maconheiro.\\nNão confunda o viciado em malhar com a necessidade de \\nmalhar. Tudo na vida tem vício, usuário e dependente.\\nTudo na vida só depende de como você usa e como você \\ncontrola, pois assim como existe o viciado em comer, fumar, \\nbeber, malhar e etecetera existe também a pessoa que usa para \\nser mais feliz, por diversão, por conforto ou pela necessidade. “ \\nRico se suicida pela tristeza e o pobre se mata (drogas) pela \\nfelicid ade... ”\\nSem título-1   76Sem título-1   76 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 93606,
      "chapter": 3,
      "page": 76,
      "segment_type": "page",
      "themes": {},
      "difficulty": 22.950819672131146,
      "complexity_metrics": {
        "word_count": 183,
        "sentence_count": 14,
        "paragraph_count": 1,
        "avg_sentence_length": 13.071428571428571,
        "avg_word_length": 4.836065573770492,
        "unique_word_ratio": 0.6174863387978142,
        "avg_paragraph_length": 183.0,
        "punctuation_density": 0.15300546448087432,
        "line_break_count": 21,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "vida",
          "vício",
          "usuário",
          "dependente",
          "algo",
          "você",
          "confunda",
          "viciado",
          "malhar",
          "como",
          "pela",
          "viver",
          "estamos",
          "vivendo",
          "quevocê",
          "beber",
          "necessidade",
          "tudo",
          "existe",
          "título"
        ],
        "entities": [
          [
            "76",
            "CARDINAL"
          ],
          [
            "estamos",
            "PERSON"
          ],
          [
            "Vamos",
            "PERSON"
          ],
          [
            "para compreendermos",
            "PERSON"
          ],
          [
            "que estamos",
            "PERSON"
          ],
          [
            "hoje e amanhã!",
            "PERSON"
          ],
          [
            "Vício",
            "GPE"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "Usuário",
            "PERSON"
          ],
          [
            "Dependente",
            "PERSON"
          ]
        ],
        "readability_score": 92.01346604215456,
        "semantic_density": 0,
        "word_count": 183,
        "unique_words": 113,
        "lexical_diversity": 0.6174863387978142
      },
      "preservation_score": 1.743086383500596e-05
    },
    {
      "id": 1,
      "text": "— 77 —Aos 16 anos comecei a lavar carro e aprender a aplicar in -\\nsulfilm.\\nCom 19 anos virei supervisor.\\nCom 21 anos virei supervisor em outra empresa.\\nApós o meu filho nascer, percebi que eu trabalhava muito \\ne não conseguia dar o suporte necessário para a família, pois \\néramos um casal muito jovem e precisávamos um do outro.\\nSeparei com 24 anos e fiquei sete anos em depressão, não \\nentendia o motivo, comecei a estudar comportamento huma -\\nno, melhorando meu relacionamento com o cliente.\\nMorava em uma quitinetecom meu filho que eu paguei \\nR$ 400,00 durante cinco anos. Quitei todas as minhas dívidas \\nativas e com R$ 8.500,00 na conta comecei a construir mi -\\nnha casa.\\nConstruí em cima da casa da minha mãe, mas teve uma \\nchuva de 45 dias e tive que correr com a obra, pois infiltrou \\ntoda a casa da minha mãe, me fazendo trabalhar de 7 da ma -\\nnhã à 23 danoitedurante seis meses. Cheguei a pesar 77 kg an -\\ntes pesava 86 kg. Hoje ainda pago reforma, melhoria, resíduo \\nde cartão da obra… a vida tem dificuldades, como você faz \\npara melhorar?\\nSem título-1   77Sem título-1   77 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 94808,
      "chapter": 3,
      "page": 77,
      "segment_type": "page",
      "themes": {},
      "difficulty": 24.811303630363035,
      "complexity_metrics": {
        "word_count": 202,
        "sentence_count": 12,
        "paragraph_count": 1,
        "avg_sentence_length": 16.833333333333332,
        "avg_word_length": 4.50990099009901,
        "unique_word_ratio": 0.7079207920792079,
        "avg_paragraph_length": 202.0,
        "punctuation_density": 0.13861386138613863,
        "line_break_count": 21,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "anos",
          "comecei",
          "casa",
          "virei",
          "supervisor",
          "filho",
          "muito",
          "pois",
          "minha",
          "obra",
          "título",
          "lavar",
          "carro",
          "aprender",
          "aplicar",
          "sulfilm",
          "outra",
          "empresa",
          "após",
          "nascer"
        ],
        "entities": [
          [
            "Aos 16",
            "PERSON"
          ],
          [
            "19",
            "CARDINAL"
          ],
          [
            "21",
            "CARDINAL"
          ],
          [
            "Após",
            "PERSON"
          ],
          [
            "percebi que eu trabalhava muito \\ne não conseguia dar",
            "ORG"
          ],
          [
            "suporte necessário",
            "PERSON"
          ],
          [
            "muito jovem",
            "PERSON"
          ],
          [
            "Separei",
            "ORG"
          ],
          [
            "24",
            "CARDINAL"
          ],
          [
            "depressão",
            "GPE"
          ]
        ],
        "readability_score": 90.23036303630363,
        "semantic_density": 0,
        "word_count": 202,
        "unique_words": 143,
        "lexical_diversity": 0.7079207920792079
      },
      "preservation_score": 1.653697338192873e-05
    },
    {
      "id": 1,
      "text": "— 78 —Eu sou tão egoístaque só faço aquilo que quero de volta \\npara mim…\\nEu não quero a mesma troca monetária, eu quero a mesma \\ntroca sentimental diante daquilo que fiz por você.\\nPorque pessoas independentes não são boas para se re -\\nlacionar?\\nIndependente é independente, pois até quando ela depen -\\nde de alguém, ela acha que não depende…\\nMesmo quando eu erro eu estou certo, atéporque a minha \\nvida é minha, ela é independente…\\nAh, eu sou independente e tenho muitos amigos, minha \\nfamília… por isso você não é bom de se relacionar, pois a sua \\nvida de independente é sua. Sendo assim, se você quiser sair, \\nse divertir, ficar com a sua família é mais importante do que \\ndeixar de ser independente…\\nTudo em nossa vida tem que ser balanceado, não se pode \\npesar mais para um lado e nem para o outro, temos que en -\\nxergar e dar valor em ser dependente de alguém, atéporque eu \\nnunca fui feliz sozinho, sempre tive alguém do meu lado que \\neu dependia para ser feliz!\\nSem título-1   78Sem título-1   78 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 96052,
      "chapter": 3,
      "page": 78,
      "segment_type": "page",
      "themes": {},
      "difficulty": 35.05080213903743,
      "complexity_metrics": {
        "word_count": 187,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 37.4,
        "avg_word_length": 4.502673796791444,
        "unique_word_ratio": 0.6256684491978609,
        "avg_paragraph_length": 187.0,
        "punctuation_density": 0.12299465240641712,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "independente",
          "quero",
          "você",
          "alguém",
          "minha",
          "vida",
          "mesma",
          "troca",
          "pois",
          "quando",
          "atéporque",
          "família",
          "mais",
          "lado",
          "feliz",
          "título",
          "egoístaque",
          "faço",
          "aquilo",
          "volta"
        ],
        "entities": [
          [
            "78",
            "CARDINAL"
          ],
          [
            "Eu",
            "PERSON"
          ],
          [
            "para mim",
            "PERSON"
          ],
          [
            "Eu",
            "PERSON"
          ],
          [
            "troca monetária",
            "PERSON"
          ],
          [
            "eu",
            "PERSON"
          ],
          [
            "boas",
            "ORG"
          ],
          [
            "para se re -\\n",
            "PERSON"
          ],
          [
            "até quando ela",
            "PERSON"
          ],
          [
            "ela acha que",
            "PERSON"
          ]
        ],
        "readability_score": 79.94919786096257,
        "semantic_density": 0,
        "word_count": 187,
        "unique_words": 117,
        "lexical_diversity": 0.6256684491978609
      },
      "preservation_score": 1.2769863615388982e-05
    },
    {
      "id": 1,
      "text": "— 79 —Olhe para a tv e veja:\\nQuantos “programas de pessoas de pele branca existem?” . \\nQuando se trata do âncora do programa(clipe, programas, ci -\\nnema, cotidiano etc.) ser branco, quantas pessoas negrasháem \\nvolta do âncora do programa?\\nAgora repara o contrário… quantos programas de pessoas \\nde pele negra existem e quantas pessoas de pele branca existem \\nem volta?Repara isso quevocê vai entender o que eu falo de \\nconforto visual perante o pré-conceito ou o preconceito…\\nImportância!\\nPor qual motivo você trabalha para ganhar dinheiro?\\nImagina os seguintes fatores: eu trabalho para dar o me -\\nlhor para meu filho, família, amigos e viver o melhor que eu \\nposso me proporcionar. Eu trabalho para ter uma vida melhor \\npara mim.\\nAtéque ponto a pessoa que trabalha pensando em si mes -\\nma respeita ao outro que trabalha em prol de um todo?\\nNossa importância nos mostra as nossas ambições, ganân -\\ncia e atéque ponto eu respeito a ausência de algo na vida do \\noutro perante a minha? Como assim? Atéque ponto eu não \\nirei pagar você para pagar um carro novo, uma casa nova, um \\niate, comer em restaurantes caros… eu te devo R$ 100,00 e \\nSem título-1   79Sem título-1   79 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 97213,
      "chapter": 3,
      "page": 79,
      "segment_type": "page",
      "themes": {},
      "difficulty": 28.47179487179487,
      "complexity_metrics": {
        "word_count": 207,
        "sentence_count": 13,
        "paragraph_count": 1,
        "avg_sentence_length": 15.923076923076923,
        "avg_word_length": 4.777777777777778,
        "unique_word_ratio": 0.6618357487922706,
        "avg_paragraph_length": 207.0,
        "punctuation_density": 0.14009661835748793,
        "line_break_count": 22,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "pessoas",
          "programas",
          "pele",
          "existem",
          "trabalha",
          "atéque",
          "ponto",
          "quantos",
          "branca",
          "âncora",
          "programa",
          "quantas",
          "volta",
          "repara",
          "perante",
          "importância",
          "você",
          "trabalho",
          "melhor",
          "vida"
        ],
        "entities": [
          [
            "79",
            "CARDINAL"
          ],
          [
            "Olhe",
            "ORG"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "ci -\\nnema",
            "PERSON"
          ],
          [
            "ser branco",
            "PERSON"
          ],
          [
            "quantas",
            "GPE"
          ],
          [
            "Agora",
            "PERSON"
          ],
          [
            "contrário",
            "ORG"
          ],
          [
            "quantas",
            "GPE"
          ],
          [
            "volta?Repara",
            "GPE"
          ]
        ],
        "readability_score": 90.60512820512821,
        "semantic_density": 0,
        "word_count": 207,
        "unique_words": 137,
        "lexical_diversity": 0.6618357487922706
      },
      "preservation_score": 1.9665589967699028e-05
    },
    {
      "id": 1,
      "text": "— 80 —estou sem dinheiro para te pagar, porém eu tenho minha vi -\\nda,que é mais importante que a sua, pois esses R$100,00 “é \\npouco, não vai te fazer falta… ” . O que é pouco para uns é mui -\\nto para outros!\\nEu acredito em uma vida quevocê precisa fazer por \\nmerecer!\\nMarcelo, esse questionamento é muito vago, como eu sei \\nquefiz por merecer?\\n Eu recebo tantos benefícios, que me enxergo não merece -\\ndor de ter uma vida tão boa.\\nQuantos benefícios você faz por alguém e quantos benefí -\\ncios as pessoas fazem por você?\\nQuero que todos que façam por merecer tenham aquilo \\nque merecem. Como nem tudo é perfeito, inclusive essa re -\\ngra, por muitas vezes por você ser fruto do meio, seja ele fa -\\nvelado, religioso, macumbeiro, rico, pobre…você não percebe \\no seu merecimento diante da sua vida, pois não entendemos \\nos motivos de cada pessoa matar, roubar, esquartejar, machu -\\ncar, trair…\\nEntenda o seu merecimento da seguinte forma: faça tudo \\naquilo quevocê deseja receber de volta. A vida é uma troca, seja \\nela sentimental (carinho, abraço, beijo, educação…) ou mate -\\nrial (doar, trabalho, fazer, melhorar tudo que está em volta…)\\nSua vida pertence a você, porém a sua vida tem consequências \\nSem título-1   80Sem título-1   80 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 98542,
      "chapter": 4,
      "page": 80,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 28.680480480480483,
      "complexity_metrics": {
        "word_count": 222,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 24.666666666666668,
        "avg_word_length": 4.675675675675675,
        "unique_word_ratio": 0.7342342342342343,
        "avg_paragraph_length": 222.0,
        "punctuation_density": 0.18468468468468469,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "vida",
          "você",
          "fazer",
          "merecer",
          "tudo",
          "porém",
          "pois",
          "pouco",
          "quevocê",
          "como",
          "benefícios",
          "quantos",
          "aquilo",
          "seja",
          "merecimento",
          "volta",
          "título",
          "estou",
          "dinheiro",
          "pagar"
        ],
        "entities": [
          [
            "80",
            "CARDINAL"
          ],
          [
            "porém eu",
            "PERSON"
          ],
          [
            "pouco",
            "ORG"
          ],
          [
            "para outros!",
            "PERSON"
          ],
          [
            "Eu",
            "PERSON"
          ],
          [
            "Marcelo",
            "PERSON"
          ],
          [
            "muito vago",
            "PERSON"
          ],
          [
            "como eu sei",
            "PERSON"
          ],
          [
            "Quantos",
            "GPE"
          ],
          [
            "faz",
            "ORG"
          ]
        ],
        "readability_score": 86.26396396396396,
        "semantic_density": 0,
        "word_count": 222,
        "unique_words": 163,
        "lexical_diversity": 0.7342342342342343
      },
      "preservation_score": 3.0136878132317994e-05
    },
    {
      "id": 1,
      "text": "— 81 —em outras vidas. Faça por merecer todos que estão àsua volta \\nestar com você.\\nJá parou para reparar o quanto você fica incomodado com \\no incômodo que o seu amigo vai sentir, diante do incômodo \\nquevocê imagina estar incomodando, e o seu amigo por sua \\nvez, fica incomodado por você não ter ido ou ter feito o que \\nera para ser feito? Loucuras dos seres humanos! \\nMarcelo,você é ateu, o que a Bíblia significa para você? \\nEu vejo a Bíblia igual eu vejo a vida…você lê Paulo, Moisés, \\nGênesis, Jesus… eu vejo você, converso com você, sinto o senti -\\nmento quevocê tem perante a mim… a Bíblia para mim é um \\nlivro que nos dá uma direção, igual à sua vida, a minha vida, a \\nvida de todos nós dá uma direção a ser seguida ou não ser se -\\nguida. Você é meu profeta, você é meu Messias assim como eu \\ntambém sou para você.\\nNascemos e não sabemos o que iremos viver, precisamos \\nsemprenos aperfeiçoar, melhorando,pois, a vida não veio com \\num manual de instruções a ser seguido, porém sabemos o final \\nque iremos ter!\\nSem título-1   81Sem título-1   81 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 99934,
      "chapter": 4,
      "page": 81,
      "segment_type": "page",
      "themes": {},
      "difficulty": 27.324242424242424,
      "complexity_metrics": {
        "word_count": 198,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 22.0,
        "avg_word_length": 4.414141414141414,
        "unique_word_ratio": 0.6161616161616161,
        "avg_paragraph_length": 198.0,
        "punctuation_density": 0.15656565656565657,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "vida",
          "bíblia",
          "vejo",
          "todos",
          "fica",
          "incomodado",
          "incômodo",
          "amigo",
          "quevocê",
          "feito",
          "igual",
          "direção",
          "sabemos",
          "iremos",
          "título",
          "outras",
          "vidas",
          "faça",
          "merecer"
        ],
        "entities": [
          [
            "81",
            "CARDINAL"
          ],
          [
            "Já parou",
            "PERSON"
          ],
          [
            "quanto você fica",
            "PERSON"
          ],
          [
            "quevocê imagina estar",
            "PERSON"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "sua \\nvez",
            "ORG"
          ],
          [
            "fica",
            "GPE"
          ],
          [
            "feito",
            "PERSON"
          ],
          [
            "Marcelo",
            "PERSON"
          ],
          [
            "Bíblia",
            "GPE"
          ]
        ],
        "readability_score": 87.67575757575757,
        "semantic_density": 0,
        "word_count": 198,
        "unique_words": 122,
        "lexical_diversity": 0.6161616161616161
      },
      "preservation_score": 1.4962023536030753e-05
    },
    {
      "id": 1,
      "text": "— 82 —Mas quem criou nós, seres humanos, se não foi Deus, foi o \\nBig Bang?\\nEu não sei essa resposta, você não sabe essa resposta, você \\ntem uma crença que foi Deus, outros Brahma, outros Odin, \\noutros Big Bang… eu não tenho a menor ideia, pois todos es -\\nses “fatos” são comprovados de acordo com o quevocê quer \\naceitar, é fruto da sua imaginação crer no quevocê quiser crer.\\nSe te faz bem fico feliz por você, pois a minha forma de \\npensar me faz bem.\\nA maioria das guerras que tivemos foi por causa dessa per -\\ngunta, você acha que eu quero perguntar sobre isso ou falar \\nsobre isso? Não quero criar guerra com você, quero amar você!\\nSuzane von Richthofen… mãe e padrasto de Henry…você \\nnão vê uma mãe favelada matando a própria família!Porque \\nisso acontece em família “bem estruturada”? \\nTese: o excesso de poder junto com o excesso de luxo faz \\nvocê não ter uma conquista, transformando esse seu sentimen -\\nto de querer conquistar algo acima (fui criado para ser melhor \\nque os meus pais – decepção não conquistar), racional.\\n“Excesso de problemas na vida menos tempo temos para \\nmelhorar a vida. ”\\nSem título-1   82Sem título-1   82 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 101142,
      "chapter": 4,
      "page": 82,
      "segment_type": "page",
      "themes": {},
      "difficulty": 28.827403846153846,
      "complexity_metrics": {
        "word_count": 208,
        "sentence_count": 10,
        "paragraph_count": 1,
        "avg_sentence_length": 20.8,
        "avg_word_length": 4.591346153846154,
        "unique_word_ratio": 0.7355769230769231,
        "avg_paragraph_length": 208.0,
        "punctuation_density": 0.13942307692307693,
        "line_break_count": 21,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "outros",
          "quero",
          "isso",
          "excesso",
          "deus",
          "bang",
          "essa",
          "resposta",
          "pois",
          "quevocê",
          "crer",
          "família",
          "conquistar",
          "vida",
          "título",
          "quem",
          "criou",
          "seres",
          "humanos"
        ],
        "entities": [
          [
            "82",
            "CARDINAL"
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
            "Eu",
            "PERSON"
          ],
          [
            "sei essa resposta",
            "ORG"
          ],
          [
            "você não",
            "ORG"
          ],
          [
            "essa resposta",
            "ORG"
          ],
          [
            "Deus",
            "PERSON"
          ],
          [
            "Odin",
            "ORG"
          ],
          [
            "eu",
            "PERSON"
          ]
        ],
        "readability_score": 88.22259615384615,
        "semantic_density": 0,
        "word_count": 208,
        "unique_words": 153,
        "lexical_diversity": 0.7355769230769231
      },
      "preservation_score": 1.966558996769903e-05
    },
    {
      "id": 1,
      "text": "— 83 —“Menos problemas na vida mais dificuldade em organizar \\na vida. ”\\nExemplo: eu posso fazer tal coisa e você não, eu posso ma -\\ntar, roubar, agredir, pois eu tenho mais direito quevocê por ter \\nmais dinheiro e mais poder que você.\\nIsso é o dia a dia das nossas vidas, são tantas regras, tan -\\ntas leis, que até que ponto essas regras e essas leis são boas \\npara todos?\\nHátantas leis preconceituosas, ruins, hipócritas, leis de be -\\nnefício para quem quer ser beneficiado. Hátantas regras reli -\\ngiosas que servem para quando você erra diante do ser huma -\\nno, porém Deus te salva…Resumo, o ser humano só quer ver \\no lado que te faz bem. Atéque ponto o que te faz bemfaz mal \\npara o outro?\\nPorque o ser humano sente empatia, energia ou alma?\\nPara entender, temos quecompreenderque nosso corpo é \\nformado de átomos, o que seria um átomo e porque tem aver?\\nPensa na física, quando cai uma pedra na água (ação), ela \\npropaga ondas como se fosse uma energia (reação), o átomo \\né semelhante, porém invisível aos nossos olhos, ele tem dois \\ntipos de núcleos, negativo e positivo. Os átomos não se encos -\\ntam, eles se repelem.\\nMas o que seria o átomo?\\nSem título-1   83Sem título-1   83 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 102439,
      "chapter": 4,
      "page": 83,
      "segment_type": "page",
      "themes": {},
      "difficulty": 25.55086726998492,
      "complexity_metrics": {
        "word_count": 221,
        "sentence_count": 12,
        "paragraph_count": 1,
        "avg_sentence_length": 18.416666666666668,
        "avg_word_length": 4.475113122171946,
        "unique_word_ratio": 0.6877828054298643,
        "avg_paragraph_length": 221.0,
        "punctuation_density": 0.17194570135746606,
        "line_break_count": 23,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "leis",
          "você",
          "regras",
          "átomo",
          "vida",
          "posso",
          "ponto",
          "essas",
          "hátantas",
          "quer",
          "quando",
          "porém",
          "humano",
          "porque",
          "energia",
          "átomos",
          "seria",
          "título",
          "menos"
        ],
        "entities": [
          [
            "83",
            "CARDINAL"
          ],
          [
            "eu posso",
            "PERSON"
          ],
          [
            "fazer tal coisa",
            "PRODUCT"
          ],
          [
            "eu posso ma -\\ntar",
            "PERSON"
          ],
          [
            "agredir",
            "PERSON"
          ],
          [
            "eu",
            "PERSON"
          ],
          [
            "dia",
            "ORG"
          ],
          [
            "dia",
            "ORG"
          ],
          [
            "das nossas vidas",
            "PRODUCT"
          ],
          [
            "boas",
            "ORG"
          ]
        ],
        "readability_score": 89.44913273001508,
        "semantic_density": 0,
        "word_count": 221,
        "unique_words": 152,
        "lexical_diversity": 0.6877828054298643
      },
      "preservation_score": 2.6433617683855188e-05
    },
    {
      "id": 1,
      "text": "— 84 —Pensa em um pó de café quevocê compra no mercado, ele \\nvem só café ou vem cheio de outras coisas que nem sabemos? \\nAgora você pensa em separar o que realmente é café, depois \\nsepara a cafeína do café, pega a cafeína e divide até você não \\nconseguir dividir e pegar só a parte da cafeína que te deixa \\nacordado. Como seria uma colher cheia de cafeína só com o \\nátomo que te deixa acordado?Potencializa. Imagina o nosso \\ncorpo em pequenos átomos afastando outros átomos, qual é a \\nenergiaquerepelimos ao outro átomo?\\nTudo em nossa volta emite uma energia, tudo à nossa volta \\nnos faz sentir uma energia, pois tudo na vida contém átomos.\\nSabe quando você pensa que algo vai cair,você coloca a sua \\nmão para não deixar e você acaba derrubando? Na vida é mais \\nou menos assim, quanto mais você não deixe as pessoas caí -\\nrem, mais você está protegendo-as,o queàs vezes e fazpara pro -\\nteger acaba pordeixar cair…\\nTemos tanta certeza da nossa certeza que esquecemos que \\na nossa certeza pode estar tão errada quanto a do outro, por -\\nque a sua certeza é mais certa que a dos outros? Você viveu \\nmais?Você aprendeu mais?Você é melhor?O quevocê é diante \\ndo outro para ter mais certeza ou ser maior exemplo? Nin -\\nguém sabe viver, ninguém sabe ser mãe, ninguém sabe ser pai, \\nninguém sabe ser amigo, ninguém sabe nada da vida, a única \\ncoisa que sabemos é que iremos morrer, quando não sabemos, \\nSem título-1   84Sem título-1   84 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 103780,
      "chapter": 4,
      "page": 84,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 26.55552608311229,
      "complexity_metrics": {
        "word_count": 261,
        "sentence_count": 13,
        "paragraph_count": 1,
        "avg_sentence_length": 20.076923076923077,
        "avg_word_length": 4.5440613026819925,
        "unique_word_ratio": 0.6168582375478927,
        "avg_paragraph_length": 261.0,
        "punctuation_density": 0.13026819923371646,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "mais",
          "sabe",
          "certeza",
          "café",
          "cafeína",
          "nossa",
          "ninguém",
          "pensa",
          "sabemos",
          "átomos",
          "outro",
          "tudo",
          "vida",
          "quevocê",
          "deixa",
          "acordado",
          "átomo",
          "outros",
          "volta"
        ],
        "entities": [
          [
            "84",
            "CARDINAL"
          ],
          [
            "café",
            "PERSON"
          ],
          [
            "nem sabemos",
            "PERSON"
          ],
          [
            "Agora",
            "LOC"
          ],
          [
            "café",
            "PERSON"
          ],
          [
            "café",
            "PERSON"
          ],
          [
            "Como",
            "ORG"
          ],
          [
            "cheia de cafeína",
            "PERSON"
          ],
          [
            "Imagina",
            "PERSON"
          ],
          [
            "outros átomos",
            "PERSON"
          ]
        ],
        "readability_score": 88.59832007073386,
        "semantic_density": 0,
        "word_count": 261,
        "unique_words": 161,
        "lexical_diversity": 0.6168582375478927
      },
      "preservation_score": 2.1964165418469048e-05
    },
    {
      "id": 1,
      "text": "— 85 —porém podemos aproveitar e deixar a vida nos mostrar como \\nse deve viver!\\nQual é a maior loucura financeira de um ser humano?\\nViver uma vida em prol de morar em um local, que faz você \\nsobreviver por consumir quase todo o seu dinheiro, ter um \\ncarro que chama a atenção a ponto de ser roubado, se preocu -\\npar tanto com o amanhã é esquecer de viver o hoje…\\nOu viver pensando no amanhã, se planejando para viver \\nmais feliz o amanhã… qual é a sua felicidade diante dos seus \\ngastos?\\nQual é a sua prioridade financeira? Como você distribui o \\nseu dinheiro diante da sua necessidade em viver melhor?\\nO que é viver melhor para você?\\nO tempo é contínuo e cada tempo que passa para mim pas -\\nsa para você, para ele, para nós, para eles, o tempo é o mesmo \\nvalor para todos. O tempo é aproveitado de acordo com o que \\ncondiz como você quer usá-lo, respeite o tempo que cada pes -\\nsoa dedica a você, pois assim como vocêperde o seu tempo, \\na pessoa que está à sua frente, longe, em qualquer lugar, está \\npassando no mesmo valor que o seu tempo.\\nSem título-1   85Sem título-1   85 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 105366,
      "chapter": 4,
      "page": 85,
      "segment_type": "page",
      "themes": {},
      "difficulty": 27.82333333333333,
      "complexity_metrics": {
        "word_count": 210,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 23.333333333333332,
        "avg_word_length": 4.252380952380952,
        "unique_word_ratio": 0.5952380952380952,
        "avg_paragraph_length": 210.0,
        "punctuation_density": 0.12380952380952381,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "viver",
          "tempo",
          "você",
          "como",
          "qual",
          "amanhã",
          "vida",
          "financeira",
          "dinheiro",
          "diante",
          "melhor",
          "cada",
          "mesmo",
          "valor",
          "está",
          "título",
          "porém",
          "podemos",
          "aproveitar",
          "deixar"
        ],
        "entities": [
          [
            "85",
            "CARDINAL"
          ],
          [
            "porém podemos aproveitar e deixar",
            "ORG"
          ],
          [
            "loucura financeira de um",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "Ou",
            "PERSON"
          ],
          [
            "financeira",
            "PERSON"
          ],
          [
            "diante da sua",
            "PERSON"
          ],
          [
            "mim",
            "PERSON"
          ],
          [
            "para você",
            "PERSON"
          ],
          [
            "para ele",
            "PERSON"
          ]
        ],
        "readability_score": 87.05761904761906,
        "semantic_density": 0,
        "word_count": 210,
        "unique_words": 125,
        "lexical_diversity": 0.5952380952380952
      },
      "preservation_score": 1.4472512097440844e-05
    },
    {
      "id": 1,
      "text": "— 86 —Viva o melhor a cada momento, aprecie o trajeto, pois o \\nfinal é a morte. Creio euquevocê não deseja chegar ao final ou \\nvocê quer?\\nTodas as pessoas que passam pela sua vida te fazem adquirir \\nalgo.Atéque ponto você adquiriu o suficiente daquela pessoa?\\nNinguém está fazendo mal para você (caso do acaso não \\nconta, matar, roubar etc.)… ninguém está fazendo o bem para \\nvocê…você enxerga o quevocê deseja enxergar, suas expectati -\\nvas, suas decepções, sua felicidade, sua vida são suas! Sabe aque -\\nle ditado: só conhecemos a pessoa quando nos separamos?\\nVocê não enxergou por estar próximo do problema ouvocê \\nnão quis enxergar por imaginar quevocê estava vivendo o “me -\\nlhor da vida”?\\nO ensinamento está no erro e não no acerto. Se você não \\ndeixar o seu filho, mãe, pai, irmão, amigo, cachorro, gato, papa -\\ngaio … como vão saber que cair e se machucar é ruim?Quantas \\nvezes um atleta, um escultor, uma mãe, um pai, um filho erra \\npara saber acertar amanhã?\\nSem título-1   86Sem título-1   86 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 106601,
      "chapter": 4,
      "page": 86,
      "segment_type": "page",
      "themes": {},
      "difficulty": 24.009590316573558,
      "complexity_metrics": {
        "word_count": 179,
        "sentence_count": 12,
        "paragraph_count": 1,
        "avg_sentence_length": 14.916666666666666,
        "avg_word_length": 4.754189944134078,
        "unique_word_ratio": 0.7430167597765364,
        "avg_paragraph_length": 179.0,
        "punctuation_density": 0.19553072625698323,
        "line_break_count": 18,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "vida",
          "está",
          "suas",
          "final",
          "deseja",
          "pessoa",
          "ninguém",
          "fazendo",
          "quevocê",
          "enxergar",
          "filho",
          "saber",
          "título",
          "viva",
          "melhor",
          "cada",
          "momento",
          "aprecie",
          "trajeto"
        ],
        "entities": [
          [
            "86",
            "CARDINAL"
          ],
          [
            "Viva o melhor",
            "PRODUCT"
          ],
          [
            "Creio",
            "ORG"
          ],
          [
            "Todas",
            "PERSON"
          ],
          [
            "passam pela sua vida",
            "PERSON"
          ],
          [
            "Ninguém",
            "ORG"
          ],
          [
            "quevocê deseja enxergar",
            "ORG"
          ],
          [
            "suas expectati -\\n",
            "PERSON"
          ],
          [
            "suas decepções",
            "PERSON"
          ],
          [
            "separamos",
            "PERSON"
          ]
        ],
        "readability_score": 91.11540968342645,
        "semantic_density": 0,
        "word_count": 179,
        "unique_words": 133,
        "lexical_diversity": 0.7430167597765364
      },
      "preservation_score": 1.8005507697698462e-05
    },
    {
      "id": 1,
      "text": "— 87 —Para vivermos os nossos sonhos, precisamos deixar de viver \\nem prol deles, para conseguirmos nos planejar, conquistar e \\nvivenciar os nossos próprios sonhos…\\nEu não vivo um sonho de vida.Eu transformei a vida que \\nme veio em um sonho de vida!\\nPorque eu me importo tanto com as pessoas?\\nPorque eu não desejo que ninguém passe pelo que eu pas -\\nsei de ruim na vida? \\nPorque sempre quero estar rodeado de pessoas?\\nOnde foi o início do meu caráter?\\nQuando eu era criança, passei por muitas dificuldades, \\nfome foia maior delas.\\nA dor que se sente pelaimpotência, diante da necessidade \\nde se ter comida e não ter é umsintoma junto ao meu próprio \\nsentimentoque não tem como mensurar,explicare medir.\\nMesmo passando por tudo isso, eu vivia sempre feliz, sim -\\nplesmente pelo fator de ter amigos que me mostravam felici -\\ndades e companheiros naquela situação em que eu me encon -\\ntrava. Se eu fui feliz mesmo nesse estado, como você acha que \\neu quero viver?\\nSem título-1   87Sem título-1   87 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 107762,
      "chapter": 4,
      "page": 87,
      "segment_type": "page",
      "themes": {},
      "difficulty": 24.558835546475997,
      "complexity_metrics": {
        "word_count": 178,
        "sentence_count": 11,
        "paragraph_count": 1,
        "avg_sentence_length": 16.181818181818183,
        "avg_word_length": 4.741573033707865,
        "unique_word_ratio": 0.7191011235955056,
        "avg_paragraph_length": 178.0,
        "punctuation_density": 0.1348314606741573,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "vida",
          "porque",
          "nossos",
          "sonhos",
          "viver",
          "sonho",
          "pessoas",
          "pelo",
          "sempre",
          "quero",
          "como",
          "mesmo",
          "feliz",
          "título",
          "vivermos",
          "precisamos",
          "deixar",
          "prol",
          "deles",
          "conseguirmos"
        ],
        "entities": [
          [
            "87",
            "CARDINAL"
          ],
          [
            "precisamos deixar de viver",
            "PERSON"
          ],
          [
            "para conseguirmos",
            "PERSON"
          ],
          [
            "Eu",
            "PERSON"
          ],
          [
            "Eu transformei",
            "PERSON"
          ],
          [
            "Porque eu",
            "PERSON"
          ],
          [
            "Porque eu",
            "PERSON"
          ],
          [
            "pelo que eu pas -\\nsei de ruim",
            "PERSON"
          ],
          [
            "Quando eu",
            "PERSON"
          ],
          [
            "Mesmo",
            "ORG"
          ]
        ],
        "readability_score": 90.48661899897854,
        "semantic_density": 0,
        "word_count": 178,
        "unique_words": 128,
        "lexical_diversity": 0.7191011235955056
      },
      "preservation_score": 1.3621187856414913e-05
    },
    {
      "id": 1,
      "text": "— 88 —Dê valor à vida, viva a vida, pois amanhã você vai ser retri -\\nbuído.Tenho exposto a minha vida para você entender que a \\nsua vida é tão complicada quanto a minha.\\nEu presto serviço para uma empresa X, essa empresa X pres -\\nta serviço para uma empresa Y , essa empresa Y me chamou \\npara conversar para prestar serviço para eles, devido a um bom \\nserviço que eu presto para empresa X, fechei uma parceria de \\nserviço com a empresa Y junto com empresa X. Os serviços da \\nempresa Y eu efetuo o serviço para eles na empresa X.\\nA empresa X me comunicou que tinha um retorno de um \\nserviço malfeito, eu fui avaliar o serviço e percebi que não ha -\\nvia sidoeu que tinha executadoo serviço (tem outra empresa \\nque presta serviço na empresa Y , que só aplica insufilm nos car -\\nros sem serem blindados). A empresa X pediu para eu refazer o \\nserviço, pois eles pagariam pelo serviço.\\nEu: Não irei fazer, pois combinei que todos os carros blin -\\ndados seria eu quem faria. \\nResultado – a empresa Y quase não estava fazendo serviço \\ncomigo, mês passado aplicou insulfilm em um carro, esse mês \\nforam cinco\\nSe você não se dá valor, ninguém vai te valorizar.\\nEu sei que sou seu amigo(a).\\nNós brigávamos muito quandoéramos crianças…\\nSou homossexual…\\nSem título-1   88Sem título-1   88 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 108914,
      "chapter": 4,
      "page": 88,
      "segment_type": "page",
      "themes": {},
      "difficulty": 28.288655462184874,
      "complexity_metrics": {
        "word_count": 238,
        "sentence_count": 10,
        "paragraph_count": 1,
        "avg_sentence_length": 23.8,
        "avg_word_length": 4.46218487394958,
        "unique_word_ratio": 0.6134453781512605,
        "avg_paragraph_length": 238.0,
        "punctuation_density": 0.1134453781512605,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "empresa",
          "serviço",
          "vida",
          "pois",
          "você",
          "eles",
          "valor",
          "minha",
          "presto",
          "essa",
          "tinha",
          "título",
          "viva",
          "amanhã",
          "retri",
          "buído",
          "tenho",
          "exposto",
          "entender",
          "complicada"
        ],
        "entities": [
          [
            "88",
            "CARDINAL"
          ],
          [
            "amanhã você vai",
            "PERSON"
          ],
          [
            "Tenho",
            "ORG"
          ],
          [
            "tão complicada quanto",
            "ORG"
          ],
          [
            "Eu",
            "PERSON"
          ],
          [
            "para prestar",
            "PERSON"
          ],
          [
            "para eles",
            "PERSON"
          ],
          [
            "que eu presto",
            "PERSON"
          ],
          [
            "X.",
            "PERSON"
          ],
          [
            "eu",
            "PERSON"
          ]
        ],
        "readability_score": 86.76134453781512,
        "semantic_density": 0,
        "word_count": 238,
        "unique_words": 146,
        "lexical_diversity": 0.6134453781512605
      },
      "preservation_score": 2.0431781784622368e-05
    },
    {
      "id": 1,
      "text": "— 89 —Me mudei para longe…\\nArrumei um emprego,trabalho e faculdade…\\nNem me chamou para a sua festa…\\nCasei…\\nTive filhos…\\nSeparei…\\nEstou sem dinheiro…\\nEstou com dinheiro…\\nPreciso de um abraço…\\nPreciso conversar…\\nNossa amizade só é amizade, pois criamos confiança um \\npara com o outro, as situações “normais” da vida não nos afas -\\ntam, se nos afastamos é porque nunca fomos amigos!\\nQuanto mais você se aproxima do problema menos vocêo \\nenxerga… Pega um objeto, aproxime dos seus olhos, ele perde \\no foco, o afaste até a posição ideal para melhor o enxergar… na \\nvida é assim, temos que ampliar a nossa vista e não aproximar \\na nossa visão!\\nSem título-1   89Sem título-1   89 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 110347,
      "chapter": 4,
      "page": 89,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.457499999999996,
      "complexity_metrics": {
        "word_count": 120,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 40.0,
        "avg_word_length": 4.858333333333333,
        "unique_word_ratio": 0.7833333333333333,
        "avg_paragraph_length": 120.0,
        "punctuation_density": 0.11666666666666667,
        "line_break_count": 18,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "nossa",
          "estou",
          "dinheiro",
          "preciso",
          "amizade",
          "vida",
          "título",
          "mudei",
          "longe",
          "arrumei",
          "emprego",
          "trabalho",
          "faculdade",
          "chamou",
          "festa",
          "casei",
          "tive",
          "filhos",
          "separei",
          "abraço"
        ],
        "entities": [
          [
            "89",
            "CARDINAL"
          ],
          [
            "Casei",
            "ORG"
          ],
          [
            "Tive",
            "ORG"
          ],
          [
            "Separei",
            "ORG"
          ],
          [
            "Nossa",
            "PERSON"
          ],
          [
            "Pega",
            "PERSON"
          ],
          [
            "89Sem",
            "CARDINAL"
          ],
          [
            "89",
            "CARDINAL"
          ],
          [
            "17/03/2022",
            "DATE"
          ],
          [
            "15:08:3617/03/2022",
            "CARDINAL"
          ]
        ],
        "readability_score": 78.5425,
        "semantic_density": 0,
        "word_count": 120,
        "unique_words": 94,
        "lexical_diversity": 0.7833333333333333
      },
      "preservation_score": 8.045014077695056e-06
    },
    {
      "id": 1,
      "text": "— 90 —Nossos problemas são nossos.\\nPensa no amanhã para poder planejar melhor o amanhã, \\npara conseguir viver melhor o amanhã! Se você, por acaso, não \\nconseguiu se planejar uma, duas, três, quatrovezes, onde está \\no erro?\\nEm você, por falta de planejamento, em quem te ajudou ou \\nem alguém quevocê culpou por estar passando por isso?\\nGratidão!!!\\nSou eternamente grato por ter você em minha vida, até \\no ponto em quevocê é eternamente grato por eu estar em \\nsua vida.\\nGratidão é ser grato por ter aquela pessoa quevocê vai po -\\nder confiar, conversar, abraçar, amar, beijar, confidenciar, ser \\ncúmplice… Aquela pessoa que é grata por você, e você por ela, \\nnunca irá te cobrar o valor de algo que fez por você ou por \\nela(e), por ter feito algo por você… pois só por você estar em \\nminha vida ou eu estar na sua vida é o suficiente para sermos \\neternamente gratos em estarmos juntos!!!!\\nSem título-1   90Sem título-1   90 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 111177,
      "chapter": 4,
      "page": 90,
      "segment_type": "page",
      "themes": {},
      "difficulty": 26.78463855421687,
      "complexity_metrics": {
        "word_count": 166,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 20.75,
        "avg_word_length": 4.698795180722891,
        "unique_word_ratio": 0.6325301204819277,
        "avg_paragraph_length": 166.0,
        "punctuation_density": 0.21084337349397592,
        "line_break_count": 18,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "vida",
          "amanhã",
          "quevocê",
          "eternamente",
          "grato",
          "nossos",
          "planejar",
          "melhor",
          "gratidão",
          "minha",
          "aquela",
          "pessoa",
          "algo",
          "título",
          "problemas",
          "pensa",
          "poder",
          "conseguir",
          "viver"
        ],
        "entities": [
          [
            "90",
            "CARDINAL"
          ],
          [
            "para conseguir",
            "PERSON"
          ],
          [
            "Se você",
            "PERSON"
          ],
          [
            "estar passando",
            "PERSON"
          ],
          [
            "Gratidão",
            "PERSON"
          ],
          [
            "eu estar",
            "PERSON"
          ],
          [
            "Gratidão",
            "PERSON"
          ],
          [
            "aquela pessoa quevocê",
            "PERSON"
          ],
          [
            "amar",
            "PERSON"
          ],
          [
            "beijar",
            "ORG"
          ]
        ],
        "readability_score": 88.21536144578313,
        "semantic_density": 0,
        "word_count": 166,
        "unique_words": 105,
        "lexical_diversity": 0.6325301204819277
      },
      "preservation_score": 1.6090028155390112e-05
    },
    {
      "id": 1,
      "text": "— 91 —Inflação!!!\\nÉ semelhante a viver em um outro país com uma moeda \\nmais valorizada ganhando em real…hoje, se você ganha R$ \\n1000,00 para manter o padrão de vida proporcional ao de cos -\\ntume dos mesmos R$ 1000,00 você tem que ganhar no míni -\\nmo R$ 1400,00…\\nTodos nós fazemos contas e estipulamos metas proporcio -\\nnais ao viver de um contexto de si próprio. Dentro desse con -\\ntexto você evolui de acordo com o aumento monetário, fazen -\\ndo contas proporcionais ao que ganhamos.\\nSe você não tá entendendo como está a situação no Brasil \\ne eu acho que no mundo… veja as ruas em quevocêestá acos -\\ntumado a andar e vê a quantidade de carros… Vê onde você \\ncome, vê a quantidade de pessoas que estão comendo… Vê as \\nconcessionárias, mercado (carrinhos vazios ou produtos mais \\nbaratos)… Se você não entende de mercado financeiro, polí -\\ntica, comportamento, venda, compra, administração de uma \\nforma fora do normal (pensar acima da maioria),você não vive, \\nvocê sobrevive!!!\\n“Pais e mães que deixam de viver devido as obrigações de \\nter tido filho(s) não sabem o motivo dos seus pais deixarem de \\nviver para você poder viver… ”\\nSem título-1   91Sem título-1   91 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 112256,
      "chapter": 4,
      "page": 91,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.40956937799043,
      "complexity_metrics": {
        "word_count": 209,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 41.8,
        "avg_word_length": 4.698564593301436,
        "unique_word_ratio": 0.6698564593301436,
        "avg_paragraph_length": 209.0,
        "punctuation_density": 0.12440191387559808,
        "line_break_count": 22,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "viver",
          "mais",
          "contas",
          "quantidade",
          "mercado",
          "pais",
          "título",
          "inflação",
          "semelhante",
          "outro",
          "país",
          "moeda",
          "valorizada",
          "ganhando",
          "real",
          "hoje",
          "ganha",
          "manter",
          "padrão"
        ],
        "entities": [
          [
            "91",
            "CARDINAL"
          ],
          [
            "valorizada",
            "GPE"
          ],
          [
            "1000,00",
            "CARDINAL"
          ],
          [
            "para manter",
            "PERSON"
          ],
          [
            "padrão de vida",
            "ORG"
          ],
          [
            "mesmos",
            "PERSON"
          ],
          [
            "1000,00",
            "DATE"
          ],
          [
            "Todos",
            "GPE"
          ],
          [
            "Dentro",
            "LOC"
          ],
          [
            "aumento monetário",
            "PERSON"
          ]
        ],
        "readability_score": 77.69043062200957,
        "semantic_density": 0,
        "word_count": 209,
        "unique_words": 140,
        "lexical_diversity": 0.6698564593301436
      },
      "preservation_score": 2.1070274965391818e-05
    },
    {
      "id": 1,
      "text": "— 92 —A forma mais fácil de descobrir o quevocê deve fazer ou \\nnão diante de ser exemplo para o seu filho é se perguntando \\ncomo você é feliz…Se eu deixo de viver uma vida para dar o \\nmelhor para o meu filho, eu estou fazendo o mesmo que o \\nmeu pai e minha mãe fizeram por mim, como eu queria que \\no meu pai e minha mãe vivessem as suas próprias vidas me \\ncriando?\\nSe não percebemos os “erros” dos nossos pais, o que adian -\\ntou os“erros” que eles tiveram que viver para te ensinar e você \\nnão aprender?\\nMomento descontração\\nUm grande sábio amigo me falou uma vez…você acha que \\nvai conseguir beber e trabalhar, espera passar dos 30 anos para \\nvocê entender o que é ressaca…\\nPqp!!! Hoje eu, com 35 anos, interpreto esse meu amigo \\ncomo gênio!!!!\\nNão sei mais o que fazer para melhorar algo queestou sen -\\ntindo, que não é possível ser ressaca, isso é algo muito maior \\nque uma ressaca, não estou conseguindo ficar de pé de tan -\\nta cachaça de ontem, meu pai do céu, meu grande Buda, com \\na sabedoria e divindade de Alá, com o Universo conspirando \\npara esse meu caos interno como punição por beber como se \\nnão houvesse o amanhã, e o amanhã chegou me fudendo à \\nbeça… Isso que é vida.\\nSem título-1   92Sem título-1   92 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 113579,
      "chapter": 4,
      "page": 92,
      "segment_type": "page",
      "themes": {},
      "difficulty": 35.866312056737584,
      "complexity_metrics": {
        "word_count": 235,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 39.166666666666664,
        "avg_word_length": 4.276595744680851,
        "unique_word_ratio": 0.6127659574468085,
        "avg_paragraph_length": 235.0,
        "punctuation_density": 0.11914893617021277,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "como",
          "você",
          "ressaca",
          "mais",
          "fazer",
          "filho",
          "viver",
          "vida",
          "estou",
          "minha",
          "erros",
          "grande",
          "amigo",
          "beber",
          "anos",
          "esse",
          "algo",
          "isso",
          "amanhã",
          "título"
        ],
        "entities": [
          [
            "92",
            "CARDINAL"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "Se eu",
            "PERSON"
          ],
          [
            "eu estou fazendo",
            "PERSON"
          ],
          [
            "mim",
            "PERSON"
          ],
          [
            "como eu queria que",
            "PERSON"
          ],
          [
            "Se",
            "PERSON"
          ],
          [
            "adian",
            "NORP"
          ],
          [
            "ensinar e você \\nnão aprender",
            "ORG"
          ],
          [
            "você acha que",
            "PERSON"
          ]
        ],
        "readability_score": 79.13368794326242,
        "semantic_density": 0,
        "word_count": 235,
        "unique_words": 144,
        "lexical_diversity": 0.6127659574468085
      },
      "preservation_score": 1.9920987240006808e-05
    },
    {
      "id": 1,
      "text": "— 93 —Porra nenhuma, isso é um desespero pela felicidade que \\nchega a ser bom à beça naquele momento de pura “riqueza” , \\ndança, abraços, azaração, uma loucura viciante com muitos \\ngastos. Kkkkkk esse é um depoimento de uma grande ressa -\\nca!!! Kkkkk\\nTemos que mostrar a evolução do corpo humano… Kkkkk\\nO ser altruísta entende que a sua conquista não é sua…\\nO ser altruísta nos faz pensar em um contexto de benefício \\ne não só de si…\\nO ser altruísta é você fazendo o melhor como se fosse “nor -\\nmal” , pois aquilo é o quevocê quer de volta…\\nO ser altruísta não quer dizer ser um idiota ou um babaca, \\nquer dizer quevocê vai saber limitar no momento certo, pois \\naquilo queaconteceuvocê não faria o mesmo…\\nAltruísta é você “amar” sem ver a quem…\\nAltruísta quer dizer amar a si próprio com o benefício de \\noutros amores…\\nAltruísta é você enxergar o amor perante ao seu lado do \\nseu próprio amor…Se você não consegue enxergar o seu \\namor para outros, como você vai enxergar o que é o seu pró -\\nprio amor?\\nSem título-1   93Sem título-1   93 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 114956,
      "chapter": 4,
      "page": 93,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.250510204081635,
      "complexity_metrics": {
        "word_count": 196,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 49.0,
        "avg_word_length": 4.423469387755102,
        "unique_word_ratio": 0.5969387755102041,
        "avg_paragraph_length": 196.0,
        "punctuation_density": 0.09183673469387756,
        "line_break_count": 21,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "altruísta",
          "você",
          "quer",
          "amor",
          "dizer",
          "enxergar",
          "momento",
          "kkkkk",
          "benefício",
          "como",
          "pois",
          "aquilo",
          "quevocê",
          "amar",
          "próprio",
          "outros",
          "título",
          "porra",
          "nenhuma",
          "isso"
        ],
        "entities": [
          [
            "desespero pela felicidade",
            "PERSON"
          ],
          [
            "beça naquele momento de",
            "ORG"
          ],
          [
            "abraços",
            "PERSON"
          ],
          [
            "azaração",
            "ORG"
          ],
          [
            "Kkkkk\\nTemos",
            "PERSON"
          ],
          [
            "corpo humano",
            "PERSON"
          ],
          [
            "Kkkkk",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "você fazendo o melhor como se fosse",
            "ORG"
          ],
          [
            "quevocê quer de volta",
            "PERSON"
          ]
        ],
        "readability_score": 74.17295918367347,
        "semantic_density": 0,
        "word_count": 196,
        "unique_words": 117,
        "lexical_diversity": 0.5969387755102041
      },
      "preservation_score": 1.3855302022697046e-05
    },
    {
      "id": 1,
      "text": "— 94 —Nós trabalhamos, trabalhamos, trabalhamos… Por qual in -\\ntuito? Por qual motivo precisamos ter ou ser mais?\\nHoje eu, Marcelo, percebo que o meu cansaço perante a \\nminha necessidade de ter uma qualidade de vida em viver está \\npesando.\\nO corpo e a mente estão ficando gastos, estão ficando exaus -\\ntoscom a necessidade de pagar contas, metas, obrigações e \\nquando será o final dessas obrigações para conseguirmos real -\\nmente viver?\\nSerá que a minha casa um dia será suficiente?\\nSerá que o meu carro um dia será suficiente?\\nSerá que algum dia o viver será o suficiente?\\nA quantidade de malefícios perante aos benefícios que se \\ntêm ao viver em uma loucura de obrigações ou metas… nos \\ntornamos escravos de um sistema de necessidade evolutiva im -\\nposta pela ganância de ter ou ser mais e mais!!!\\nEu pago contas todos os dias 5, 10, 13,15, 20, 23, 24 fora \\npagar toda semana material que usa para o trabalho e mão de \\nobra… O querer ter mais fará com que você queira muito mais \\noutras coisas quevocê não queria ter…\\nVocê não vê um cara rico (a exceção da regra) acima de 30 \\nanos, solteiro, saindo todos os dias, com um vigor de atleta, tra -\\nbalhando, cuidando de sicom frequência em uma noitada… \\nNoitada para esse mesmo cara rico é quando se separa, vive um \\ntempo como se não houvesse o amanhã, depois casa ou namo -\\nra, porque isso?\\nSem título-1   94Sem título-1   94 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 116150,
      "chapter": 4,
      "page": 94,
      "segment_type": "page",
      "themes": {},
      "difficulty": 31.011264822134386,
      "complexity_metrics": {
        "word_count": 253,
        "sentence_count": 10,
        "paragraph_count": 1,
        "avg_sentence_length": 25.3,
        "avg_word_length": 4.537549407114624,
        "unique_word_ratio": 0.6324110671936759,
        "avg_paragraph_length": 253.0,
        "punctuation_density": 0.1422924901185771,
        "line_break_count": 26,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "será",
          "mais",
          "viver",
          "trabalhamos",
          "necessidade",
          "obrigações",
          "suficiente",
          "qual",
          "perante",
          "minha",
          "mente",
          "estão",
          "ficando",
          "pagar",
          "contas",
          "metas",
          "quando",
          "casa",
          "todos",
          "dias"
        ],
        "entities": [
          [
            "94",
            "CARDINAL"
          ],
          [
            "Hoje eu",
            "PERSON"
          ],
          [
            "Marcelo",
            "PERSON"
          ],
          [
            "quando",
            "PERSON"
          ],
          [
            "dessas",
            "GPE"
          ],
          [
            "para conseguirmos",
            "PERSON"
          ],
          [
            "dia",
            "ORG"
          ],
          [
            "dia",
            "ORG"
          ],
          [
            "Será",
            "PERSON"
          ],
          [
            "dia",
            "ORG"
          ]
        ],
        "readability_score": 85.9887351778656,
        "semantic_density": 0,
        "word_count": 253,
        "unique_words": 160,
        "lexical_diversity": 0.6324110671936759
      },
      "preservation_score": 2.6561316320009078e-05
    },
    {
      "id": 1,
      "text": "— 95 —Cansaço corpóreo e mental!!!\\nNossos corpos são semelhantes, nossos corpos têm muita \\nmeta, preocupação, obrigações…quando percebemos o valor \\npara aquilo que é necessário para a nossa própria vida peran -\\nte ao nosso próprio corpo, começamos a entender que as nos -\\nsasvidas cheias de conquistas são vazias a ponto de entender \\nquetudo aquilo que fizemos como melhorfoi a nossa pior es -\\ncolha perante um viver melhor a nossa própria vida cheia de \\nregras…\\nTemos que ter e não ter, temos que ser e não ser, temos que \\nser tudo e nada, temos que entender que os nossos excessos e a \\nnossa falta de ter nos faz viver uma vida pior do queter,o que é \\nnecessário para si próprio!!!\\nTempo é a propagação da energia…\\nTudo que contém átomos (energia) tem uma marcação de \\npropagação da mesma, e essa marcação é de sipróprio!!\\nExemplo: universo tem uma energia que se propaga duran -\\nte trilhões de anos (tempo)…\\nGaláxia tem uma energia que se propaga…\\nSistema solar…\\nTerra…\\nSeres humanos…\\nCarro…\\nCasa…\\nSem título-1   95Sem título-1   95 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 117684,
      "chapter": 4,
      "page": 95,
      "segment_type": "page",
      "themes": {},
      "difficulty": 38.44262295081967,
      "complexity_metrics": {
        "word_count": 183,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 45.75,
        "avg_word_length": 4.808743169398907,
        "unique_word_ratio": 0.6174863387978142,
        "avg_paragraph_length": 183.0,
        "punctuation_density": 0.12021857923497267,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "nossa",
          "temos",
          "energia",
          "nossos",
          "vida",
          "entender",
          "corpos",
          "aquilo",
          "necessário",
          "própria",
          "próprio",
          "pior",
          "viver",
          "tudo",
          "tempo",
          "propagação",
          "marcação",
          "propaga",
          "título",
          "cansaço"
        ],
        "entities": [
          [
            "95",
            "CARDINAL"
          ],
          [
            "quando percebemos",
            "PERSON"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "vida peran -\\n",
            "PERSON"
          ],
          [
            "que",
            "CARDINAL"
          ],
          [
            "cheia de \\nregras",
            "PERSON"
          ],
          [
            "Temos",
            "PERSON"
          ],
          [
            "nada",
            "GPE"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "necessário",
            "GPE"
          ]
        ],
        "readability_score": 75.68237704918033,
        "semantic_density": 0,
        "word_count": 183,
        "unique_words": 113,
        "lexical_diversity": 0.6174863387978142
      },
      "preservation_score": 1.7367014516929012e-05
    },
    {
      "id": 1,
      "text": "— 96 —Mosquito…\\nBarata…\\nVírus…\\nBactéria…\\nO que adianta não percebermos quais são os nossos gastos \\nde energia perante ao tempo que temos?\\nTudo e todos nós temos uma energia que afeta a outras \\nenergias, se estamos em uma frequência diferente da energia \\ndo universo (Deus, Buda, Alá…), galáxia, sistema solar, Terra, \\nnós e tudoque contém átomos, estamos disputando e afetando \\no tempo de existência da outra energia que precisamos estar \\nna mesma frequência!!!\\nNão adianta você ler todos os livros sobre ganhar \\ndinheiro…\\nNão adianta seguir vários influenciadores financeiros…\\nNão adianta você querer algo se você não sabe como iniciar \\nesse mesmo algo…\\nNão adianta você querer ganhar dinheiro se você nem sabe \\ncomo viver…\\nNão adianta você dar mais valor ao dinheiro se você não \\nsabe o motivo de como gastar o dinheiro…\\nEm nossas maiores felicidades houvedinheiro, mas o quefoi \\nmais importante foram as pessoas e o momento a qual viven -\\nciamos com o dinheiro ou sem o dinheiro…\\nSem título-1   96Sem título-1   96 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 118877,
      "chapter": 4,
      "page": 96,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 38.5280701754386,
      "complexity_metrics": {
        "word_count": 171,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 57.0,
        "avg_word_length": 5.093567251461988,
        "unique_word_ratio": 0.6549707602339181,
        "avg_paragraph_length": 171.0,
        "punctuation_density": 0.09941520467836257,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "adianta",
          "dinheiro",
          "energia",
          "sabe",
          "como",
          "tempo",
          "temos",
          "todos",
          "estamos",
          "frequência",
          "ganhar",
          "querer",
          "algo",
          "mais",
          "título",
          "mosquito",
          "barata",
          "vírus",
          "bactéria"
        ],
        "entities": [
          [
            "96",
            "CARDINAL"
          ],
          [
            "Mosquito",
            "PERSON"
          ],
          [
            "Barata",
            "PERSON"
          ],
          [
            "Bactéria",
            "PERSON"
          ],
          [
            "nós temos uma energia",
            "ORG"
          ],
          [
            "se estamos",
            "PERSON"
          ],
          [
            "galáxia",
            "PERSON"
          ],
          [
            "Terra",
            "PERSON"
          ],
          [
            "estamos disputando",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ]
        ],
        "readability_score": 69.9719298245614,
        "semantic_density": 0,
        "word_count": 171,
        "unique_words": 112,
        "lexical_diversity": 0.6549707602339181
      },
      "preservation_score": 1.225906907077342e-05
    },
    {
      "id": 1,
      "text": "— 97 —Não adianta você querer viver algo se você não sabe nem \\nviver a sua própria vida…Antes de pensar em ganhar dinhei -\\nro, pensa em como eu quero viver com o quanto eu quero \\nganhar…\\nA vida dos outros não é a sua vida, você fica cansado, estres -\\nsado, exausto, dificuldades iguais a todas as classes sociais…\\nSe você não sabe viver com o dinheiro quevocê ganha, \\ncomo você quer viver com mais dinheiro quevocê está viven -\\ndo?O administrar o dinheiro não é a quantidade e sim saber \\nviver com o que se tem…\\nQuando você aprender a viver com o quevocê tem você será \\ncapaz de ter muito mais, pois assim você terá tempo para pen -\\nsar em como ganhar dinheiro para viver melhor a sua vida!!!\\nMais um momento descontração\\nEstou preparado para ser um vagabundo…\\nO que se precisa para ser um vagabundo? Ficar sem fazer \\nnada? Posso, pois não sei o que é fazer nada, seria uma expe -\\nriência nova para o meu curriculum…\\nNão trabalhar? Trabalhei muito a minha vida toda, já posso \\nficar sem fazer nada…\\nFicar sentado conversando? Isso eu sou bom à beça, falo \\nmuita coisa!!\\nSem título-1   97Sem título-1   97 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 120052,
      "chapter": 4,
      "page": 97,
      "segment_type": "page",
      "themes": {},
      "difficulty": 29.395192307692305,
      "complexity_metrics": {
        "word_count": 208,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 26.0,
        "avg_word_length": 4.4423076923076925,
        "unique_word_ratio": 0.6298076923076923,
        "avg_paragraph_length": 208.0,
        "punctuation_density": 0.1201923076923077,
        "line_break_count": 22,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "viver",
          "vida",
          "dinheiro",
          "ganhar",
          "como",
          "quevocê",
          "mais",
          "ficar",
          "fazer",
          "nada",
          "sabe",
          "quero",
          "muito",
          "pois",
          "vagabundo",
          "posso",
          "título",
          "adianta",
          "querer"
        ],
        "entities": [
          [
            "97",
            "CARDINAL"
          ],
          [
            "Antes de pensar",
            "PERSON"
          ],
          [
            "ganhar dinhei -\\nro",
            "PERSON"
          ],
          [
            "como eu quero",
            "PERSON"
          ],
          [
            "quanto eu quero",
            "PERSON"
          ],
          [
            "fica",
            "GPE"
          ],
          [
            "Se",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "muito mais",
            "PERSON"
          ],
          [
            "Estou",
            "GPE"
          ]
        ],
        "readability_score": 85.66730769230769,
        "semantic_density": 0,
        "word_count": 208,
        "unique_words": 131,
        "lexical_diversity": 0.6298076923076923
      },
      "preservation_score": 1.591976330718493e-05
    },
    {
      "id": 1,
      "text": "— 98 —Jogar baralho ou dominó sentado com um shortinho curti -\\nnho? Sei contar todas as cartas e peças de quase todos os jogos, \\nnão sou o melhor, porém sou uma boa dupla nos jogos…\\nContador de história? Ah irmão, eu tenho história para o \\nresto da vida de vagabundo, momentos queirei lembrar e falar \\nassim: na minha época…kkkk\\nCheguei à conclusão de que o trabalho da vida de um ho -\\nmem, mulher ou sei lá tudo em quevocê quiser ser ou se en -\\nquadrar, sua intenção no final é se aposentar. Me sinto total -\\nmente preparado, sou capacitado, sou correria, sou dedicado, \\nse alguém quiser me contratar estou disponível no mercado \\npara ser um vagabundo nato. Minha contratação para ser um \\nvagabundo é um shortinho curto, uma mesa com tabuleiro, \\nBrahma no copo de milho e um dinheiro todo mês para pagar \\nminhas contas…\\nQuer me ter como vagabundo ao seu lado?Aqui estão todos \\nos requisitos e todas as necessidades básicas para ser um dos \\nmelhores vagabundos da história!!! Kkkkkk\\nO dinheiro não é o problema… Dinheiro também não é a \\nsolução…\\nO maior problema do dinheiro é quem está com o \\ndinheiro…\\nSer casado sem e com dinheiro, o que se tem para fazer?\\nSer solteiro sem e com dinheiro, o que se tem para fazer?\\nSem título-1   98Sem título-1   98 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 121314,
      "chapter": 4,
      "page": 98,
      "segment_type": "page",
      "themes": {},
      "difficulty": 29.19768115942029,
      "complexity_metrics": {
        "word_count": 230,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 25.555555555555557,
        "avg_word_length": 4.547826086956522,
        "unique_word_ratio": 0.6478260869565218,
        "avg_paragraph_length": 230.0,
        "punctuation_density": 0.12608695652173912,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "dinheiro",
          "vagabundo",
          "história",
          "shortinho",
          "todas",
          "todos",
          "jogos",
          "vida",
          "minha",
          "quiser",
          "problema",
          "fazer",
          "título",
          "jogar",
          "baralho",
          "dominó",
          "sentado",
          "curti",
          "contar",
          "cartas"
        ],
        "entities": [
          [
            "98",
            "CARDINAL"
          ],
          [
            "Jogar",
            "PERSON"
          ],
          [
            "Contador de história",
            "ORG"
          ],
          [
            "eu",
            "PERSON"
          ],
          [
            "para o \\n",
            "PERSON"
          ],
          [
            "Cheguei à conclusão de que",
            "ORG"
          ],
          [
            "quevocê quiser",
            "PERSON"
          ],
          [
            "sou capacitado",
            "GPE"
          ],
          [
            "sou",
            "GPE"
          ],
          [
            "correria",
            "GPE"
          ]
        ],
        "readability_score": 85.85787439613526,
        "semantic_density": 0,
        "word_count": 230,
        "unique_words": 149,
        "lexical_diversity": 0.6478260869565218
      },
      "preservation_score": 1.8899398150775692e-05
    },
    {
      "id": 1,
      "text": "— 99 —O nosso problema não é o dinheiro, nosso problema é a \\nforma como vemos o dinheiro…\\nVocê trabalha a semana toda, o mês todo, o ano todo, a vida \\ntoda para quê?\\nEu trabalho para viver, o meu viver é ser feliz, pois o viver \\nno caos é o normal perante a um viver uma vida, a nossa felici -\\ndade é uma colheita da nossa própria vida, se você não semear \\no ser feliz, como você irá saber ser feliz?\\nO que é felicidade?\\nAquela lembrança quevocê não esquece da sensação de feli -\\ncidade do momento, ocasião e local… não deixe de viver com \\nas melhores coisas que passaram em sua vida.Ao invés disso, \\naprenda a agregar os valores para as coisas boas que você já \\nviveu em sua vida!!!\\nNada é bom o suficiente que não possa melhorar…\\nO comprar algo quevocê acha caroé agregar em você não \\nperder tempo e nem dinheiro, com algo que vai sair mais caro \\nqueo quevocê acha caro… todos nós iremos gastar dinheiro, \\ncomo vamos investir esse dinheiro perante a nossa felicidade \\ne tempo? Planejar, parcelar, programar a compra de um video -\\ngame, uma televisão, uma cama, uma boa cozinha, o investi -\\nmento para um “básico” confortável em nossas vidas é neces -\\nsário para conseguirmos enfrentar o caos do nosso próprio dia \\na dia!!!\\nSem título-1   99Sem título-1   99 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 122724,
      "chapter": 4,
      "page": 99,
      "segment_type": "page",
      "themes": {},
      "difficulty": 32.143432203389835,
      "complexity_metrics": {
        "word_count": 236,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 29.5,
        "avg_word_length": 4.436440677966102,
        "unique_word_ratio": 0.614406779661017,
        "avg_paragraph_length": 236.0,
        "punctuation_density": 0.1440677966101695,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "dinheiro",
          "você",
          "vida",
          "viver",
          "nosso",
          "como",
          "feliz",
          "nossa",
          "quevocê",
          "problema",
          "toda",
          "todo",
          "caos",
          "perante",
          "felicidade",
          "coisas",
          "agregar",
          "algo",
          "acha",
          "tempo"
        ],
        "entities": [
          [
            "99",
            "CARDINAL"
          ],
          [
            "para quê",
            "PERSON"
          ],
          [
            "Eu",
            "PERSON"
          ],
          [
            "uma colheita",
            "PERSON"
          ],
          [
            "Aquela",
            "GPE"
          ],
          [
            "coisas boas",
            "PERSON"
          ],
          [
            "Nada",
            "PERSON"
          ],
          [
            "quevocê acha caroé",
            "FAC"
          ],
          [
            "nem dinheiro",
            "PERSON"
          ],
          [
            "quevocê acha caro",
            "PERSON"
          ]
        ],
        "readability_score": 83.91906779661016,
        "semantic_density": 0,
        "word_count": 236,
        "unique_words": 145,
        "lexical_diversity": 0.614406779661017
      },
      "preservation_score": 2.298575450770016e-05
    },
    {
      "id": 1,
      "text": "— 100 —Não entendocomo alguém pode errar e o humano achar \\nmaneiro…Isso se chama efeito fã!!!\\nQuando você vira FÃ de alguém quer dizer quevocê gosta \\ntanto da pessoa que esquece de ver os valores da própria pes -\\nsoa…O efeito FÃ transforma as pessoas em menos amor por si \\npróprio e mais amor por quem é fã…\\nQuando se ocorre o efeito FÃ, qualquer coisa no ouvido \\ndessa pessoa é semelhante ao comercial da Whiskas sachê. \\nComo assim? Era um comercial que o gato só entendia o dono \\nfalando Whiskas sachê, pois era a única coisa que ele precisava \\nentender… Assim é o efeito FÃ!!!\\nComercial – blá,blá,blá,blá, blá Whiskas sachê (Lula, Bolso -\\nnaro), blá, blá, blá, blá, blá, Whiskas sachê\\n(Lula, Bolsonaro)… Julgue as ações, não julgue o seu pró -\\nprio sentimento…\\nO que nós perdemos mais tempo em nossas vidas?\\nA maioria tem uma rotina de acordar, tomar café da ma -\\nnhã, alguns vão malhar (à noite), outros vão direto para o tra -\\nbalho, após o trabalho vão encontrar amigos, cuidar da casa, \\nestudar… Independente do quevocê esteja fazendo, você está \\npensando em alguma coisa, o quevocê pensa o dia todo? Isso é \\no quevocê mais perde tempo!!\\nSem título-1   100Sem título-1   100 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 124142,
      "chapter": 5,
      "page": 100,
      "segment_type": "page",
      "themes": {},
      "difficulty": 30.7125,
      "complexity_metrics": {
        "word_count": 213,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 26.625,
        "avg_word_length": 4.666666666666667,
        "unique_word_ratio": 0.7136150234741784,
        "avg_paragraph_length": 213.0,
        "punctuation_density": 0.18309859154929578,
        "line_break_count": 22,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "efeito",
          "quevocê",
          "whiskas",
          "sachê",
          "mais",
          "coisa",
          "comercial",
          "alguém",
          "isso",
          "quando",
          "você",
          "pessoa",
          "amor",
          "assim",
          "lula",
          "julgue",
          "tempo",
          "título",
          "entendocomo",
          "pode"
        ],
        "entities": [
          [
            "100",
            "CARDINAL"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "FÃ de alguém quer",
            "ORG"
          ],
          [
            "dizer quevocê gosta",
            "PERSON"
          ],
          [
            "tanto da pessoa",
            "ORG"
          ],
          [
            "da própria",
            "PERSON"
          ],
          [
            "FÃ",
            "ORG"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "FÃ",
            "ORG"
          ],
          [
            "qualquer coisa",
            "PERSON"
          ]
        ],
        "readability_score": 85.2875,
        "semantic_density": 0,
        "word_count": 213,
        "unique_words": 152,
        "lexical_diversity": 0.7136150234741784
      },
      "preservation_score": 2.5284329958470185e-05
    },
    {
      "id": 1,
      "text": "— 101 —O nosso tempo perdido não é o corpo físico, o nosso tem -\\npo perdido é o que a nossa mente pensa diante da minha ne -\\ncessidade, pois se eu penso eu executo e não ao contrário. Se \\neu penso nos meus problemas o dia todo, qual é a diferença de \\npensar ou não pensar?\\nSexo?\\nFutebol?\\nTrabalho?\\nComida?\\nAcademia?\\nEstudo?\\nCom o quevocê “perde” o seu tempo o dia todo? Sua mente \\né a sua forma de ver e agir, como você pensa ao ver ou o agir \\nde você ou de outro alguém? Nossas ações não estão no ato do \\nacontecimento, nossas ações estão no ato de se pensar!!!\\nVocê que briga com tudo e todos falando de política… con -\\ntinue votando e brigando com todos pelo poder de quem se \\nbeneficia a quem não precisa ser beneficiado… falar, discutir, \\ndebater perante o erro,você está sendo a favor de outros er -\\nros… ninguém sabe viver e conforme vamos vivendo, vamos \\naprendendo com os nossos erros… se o seu filho faz algo erra -\\ndo,o quevocê faz?\\nSe você faz algo errado,o quevocê faz? Vamos parar com o \\npreconceito “preconceituoso”!!! Como assim?\\nSem título-1   101Sem título-1   101 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 125483,
      "chapter": 5,
      "page": 101,
      "segment_type": "page",
      "themes": {},
      "difficulty": 24.752548543689322,
      "complexity_metrics": {
        "word_count": 206,
        "sentence_count": 16,
        "paragraph_count": 1,
        "avg_sentence_length": 12.875,
        "avg_word_length": 4.383495145631068,
        "unique_word_ratio": 0.6407766990291263,
        "avg_paragraph_length": 206.0,
        "punctuation_density": 0.1650485436893204,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "pensar",
          "quevocê",
          "vamos",
          "nosso",
          "tempo",
          "perdido",
          "mente",
          "pensa",
          "penso",
          "todo",
          "agir",
          "como",
          "nossas",
          "ações",
          "estão",
          "todos",
          "quem",
          "algo",
          "título"
        ],
        "entities": [
          [
            "101",
            "CARDINAL"
          ],
          [
            "perdido não",
            "PERSON"
          ],
          [
            "corpo físico",
            "PERSON"
          ],
          [
            "se eu penso eu",
            "PERSON"
          ],
          [
            "Se \\neu penso",
            "PERSON"
          ],
          [
            "dia",
            "ORG"
          ],
          [
            "Futebol",
            "GPE"
          ],
          [
            "Trabalho",
            "PERSON"
          ],
          [
            "Comida",
            "GPE"
          ],
          [
            "Academia",
            "ORG"
          ]
        ],
        "readability_score": 92.24745145631069,
        "semantic_density": 0,
        "word_count": 206,
        "unique_words": 132,
        "lexical_diversity": 0.6407766990291263
      },
      "preservation_score": 2.400734359693128e-05
    },
    {
      "id": 1,
      "text": "— 102 —Um amigo me falou:\\n– Se eu pudesse tatuar uma folha de maconha na cara eu \\ntatuava…\\nEu:\\n– É igual eu tatuar que sou preto…\\nNão precisamos lutar de uma forma preconceituosa por \\nmuitas vezes não ter ocorrido o próprio preconceito.O pensa -\\nmento extremista diante da minha certeza, diante de uma vida \\ncheia de erros e acertosonde às vezes o próprio acerto é erroo \\nque na sua visão foi acerto por ter algum ganho,o faz pensar \\nque os seus próprios erros sempre vão estar certosperantesua \\nprópria certeza com cada um de seus acertos e seus próprios \\nerros!!!\\nSermos omissos diante do preconceito nos faz entender \\nque o preconceito “não existe” …\\n“Aquela mulher é uma puta por ficar com vários homens. ”\\n“Vem duas pessoas atrás de você, um branco e um negro, \\nqual vai te roubar?”\\n“Como um homem vem e me azara, ele é maluco, dei logo \\num soco… ”\\n“Gordo tem pau pequeno, pois ele tem uma barriga maior \\nque o próprio pau… ”\\nEntenderam porque o preconceito existe?\\nSem título-1   102Sem título-1   102 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 126724,
      "chapter": 5,
      "page": 102,
      "segment_type": "page",
      "themes": {},
      "difficulty": 39.88260869565217,
      "complexity_metrics": {
        "word_count": 184,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 30.666666666666668,
        "avg_word_length": 4.608695652173913,
        "unique_word_ratio": 0.7010869565217391,
        "avg_paragraph_length": 184.0,
        "punctuation_density": 0.10869565217391304,
        "line_break_count": 23,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "preconceito",
          "próprio",
          "diante",
          "erros",
          "seus",
          "tatuar",
          "vezes",
          "certeza",
          "acerto",
          "próprios",
          "existe",
          "título",
          "amigo",
          "falou",
          "pudesse",
          "folha",
          "maconha",
          "cara",
          "tatuava",
          "igual"
        ],
        "entities": [
          [
            "102",
            "CARDINAL"
          ],
          [
            "Se eu",
            "PERSON"
          ],
          [
            "cara eu \\ntatuava",
            "PERSON"
          ],
          [
            "Eu",
            "PERSON"
          ],
          [
            "eu tatuar que",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "Aquela",
            "PERSON"
          ],
          [
            "Gordo tem pau pequeno",
            "WORK_OF_ART"
          ],
          [
            "pau",
            "ORG"
          ]
        ],
        "readability_score": 83.28405797101449,
        "semantic_density": 0,
        "word_count": 184,
        "unique_words": 129,
        "lexical_diversity": 0.7010869565217391
      },
      "preservation_score": 1.7132900350646876e-05
    },
    {
      "id": 1,
      "text": "— 103 —O não falar, pensar e agir é pior que aceitar os nossos erros e \\nconsertar os nossos próprios erros…\\nPara descobrirmos como temos que viver, temos que des -\\ncobrir os nossos erros, pois do que adianta você achar certo e \\noutros não? O que adianta você ganhar e não ter ninguém para \\ncomemorar junto?\\nO preconceito existe para todos (há uma dificuldade maior \\nno racismo) perante a forma que você lida com ele e o que \\nfaz você não ter o mesmo preconceito que todos nós fomos \\ncriados?\\nAo chamar um amigo de viado, galinha, gordo, negão isso \\nnão quer dizer quevocê esteja sendo preconceituoso, o maior \\npreconceito é você se sentir ofendido pelo preconceito sofri -\\ndo, pois aquele que faz isso não tem que ser exaltado (vai na \\npolícia), pois assim como temos cachorros que mordem, te -\\nmos“humanos” que matam, mordem, ferem, agridem, machu -\\ncam e fazem coisas muito piores que qualquer outro animal \\nirracional. Ao exaltar o caos criam-se novos fãs para se gerar \\nmais caos, pois você vê o caos dos outros como ruim e outros \\nveem o caos de outro como bom, pois se eu vivo no caos eu ad -\\nmiro esse mesmo caos… nem sempre as regras são exatas, nem \\nsempre as regras são a favor para a maioria, mas um padrão é \\npara quase todos…\\nNão temos um número de aceitação para todos, temos um \\npadrão de aceitação para todos!!!\\nSem título-1   103Sem título-1   103 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 127890,
      "chapter": 5,
      "page": 103,
      "segment_type": "page",
      "themes": {},
      "difficulty": 44.35537848605578,
      "complexity_metrics": {
        "word_count": 251,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 41.833333333333336,
        "avg_word_length": 4.51792828685259,
        "unique_word_ratio": 0.6055776892430279,
        "avg_paragraph_length": 251.0,
        "punctuation_density": 0.11952191235059761,
        "line_break_count": 25,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "caos",
          "temos",
          "pois",
          "todos",
          "como",
          "preconceito",
          "nossos",
          "erros",
          "outros",
          "adianta",
          "maior",
          "mesmo",
          "isso",
          "mordem",
          "outro",
          "sempre",
          "regras",
          "padrão",
          "aceitação"
        ],
        "entities": [
          [
            "103",
            "CARDINAL"
          ],
          [
            "Para",
            "PRODUCT"
          ],
          [
            "lida",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "mesmo",
            "ORG"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "nós fomos",
            "GPE"
          ],
          [
            "negão",
            "ORG"
          ],
          [
            "dizer quevocê",
            "PERSON"
          ],
          [
            "pelo preconceito sofri -\\n",
            "PERSON"
          ]
        ],
        "readability_score": 77.72795484727756,
        "semantic_density": 0,
        "word_count": 251,
        "unique_words": 152,
        "lexical_diversity": 0.6055776892430279
      },
      "preservation_score": 2.4475571929495542e-05
    },
    {
      "id": 1,
      "text": "— 104 —Período da Primeira Guerra e Segunda Guerra, analogia em \\num pensamento!!!\\n“Foram as guerras das armas criadas pela sabedoria dos \\nsábios, que se tornou a sabedoria da destruição para os tolos \\n(amor é ódio, porém amor e ódio tem que ter um sincro -\\nnismo) … ”\\n“Adolfo Hitler foi um gênio do mal, pelo seu próprio \\ncaos ser semelhante à sua dor, eu entendo o quanto você está \\nem caos… ”\\n“A sua luxúria o faz gerar o caos de quem não tem nada \\naver com sua própria luxúria… ”\\nA melhor forma de se viver a vida é se adaptar ao que tem \\nque se adaptar…\\nEssa frase vem de suas próprias perguntas e ações, se você \\nfizer algo que você não irá se adaptar,porque irá fazer?\\nEstou aqui pensando…\\nEu já nasci, e nessa vivência temos situações que aconte -\\ncem, que talvez seja muito bom do ponto de vista de viver…\\nComo assim?Minha família já teve dinheiro (não lembro, \\npois era novo), ficou pobre (foi pica, porém me ensinou valo -\\nres), entrei para a escola e era ruim (só era bom em matemá -\\ntica), passei fome (o normal na vida do ser humano é sempre \\nter tudo), fiquei sem luz (teve várias brincadeiras e lembranças \\nboas e ruins pornão ter luz), andei de skate (não era o melhor, \\nSem título-1   104Sem título-1   104 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 129413,
      "chapter": 5,
      "page": 104,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.29871794871795,
      "complexity_metrics": {
        "word_count": 234,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 58.5,
        "avg_word_length": 4.329059829059829,
        "unique_word_ratio": 0.7222222222222222,
        "avg_paragraph_length": 234.0,
        "punctuation_density": 0.1111111111111111,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "caos",
          "você",
          "adaptar",
          "guerra",
          "sabedoria",
          "amor",
          "ódio",
          "porém",
          "luxúria",
          "melhor",
          "viver",
          "vida",
          "teve",
          "título",
          "período",
          "primeira",
          "segunda",
          "analogia",
          "pensamento",
          "guerras"
        ],
        "entities": [
          [
            "104",
            "CARDINAL"
          ],
          [
            "Guerra",
            "ORG"
          ],
          [
            "analogia",
            "GPE"
          ],
          [
            "Hitler",
            "PERSON"
          ],
          [
            "pelo seu",
            "PERSON"
          ],
          [
            "eu entendo",
            "PERSON"
          ],
          [
            "quanto você está \\n",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "nada",
            "GPE"
          ],
          [
            "sua própria luxúria",
            "ORG"
          ]
        ],
        "readability_score": 69.45128205128205,
        "semantic_density": 0,
        "word_count": 234,
        "unique_words": 169,
        "lexical_diversity": 0.7222222222222222
      },
      "preservation_score": 2.7072110864624638e-05
    },
    {
      "id": 1,
      "text": "— 105 —mas tinha minhas habilidades), lavei carro(terminava rápido \\npara aprender a colocar Insulfilm), amei (foi uma das melho -\\nres coisas que eu vivi), magoei pessoas (aprendi a dar valor ao \\nsentimento do outro devido a ter ocorrido comigo), trabalho \\n(aprendi que as dificuldades são semelhantes, porém necessi -\\ndades diferentes e objetivos), tenho família e amigos que me \\nfazem viver uma vida que só tenho a agradecer. \\nMeu aniversário não é algo que comemoro em vão… meu \\naniversário é algo único para mim, pois nasci nesse ciclo infi -\\nnito de tempo, e esse dia para mim é o dia mais especial que \\ntenho, pois me fez viver tudona minha vida que posso viver \\njunto com todos que me fizeram ser o que eu sou, o que eu \\nvivo, o que eu amo, o queme faz feliz, o queme faz triste, o que -\\nsinto veio de um viver. Obrigado a todos por sempre aceitarem \\nas minhas loucuras, as minhas extravagâncias, minha forma \\nsistemática, meu mundo, minha vida!!!\\nO gostar não quer dizer que somos bons…\\nNós gostamos de várias coisas, porém nem sempre eu sou \\nbom no que gosto…\\nDito popular: \\nFaça aquilo que te faz feliz ou o quevocê gosta de fazer…\\nFaça e passa fome, você vai estar feliz?\\nAquilo quevocê foi criado para ser, nem sempre é para \\nvocê ser.\\nSem título-1   105Sem título-1   105 17/03/2022   15:08:3617/03/2022   15:08:36",
      "position": 130795,
      "chapter": 5,
      "page": 105,
      "segment_type": "page",
      "themes": {},
      "difficulty": 35.87307692307692,
      "complexity_metrics": {
        "word_count": 234,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 39.0,
        "avg_word_length": 4.576923076923077,
        "unique_word_ratio": 0.6666666666666666,
        "avg_paragraph_length": 234.0,
        "punctuation_density": 0.14102564102564102,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "viver",
          "minhas",
          "tenho",
          "vida",
          "minha",
          "feliz",
          "sempre",
          "coisas",
          "aprendi",
          "porém",
          "aniversário",
          "algo",
          "pois",
          "todos",
          "queme",
          "faça",
          "aquilo",
          "quevocê",
          "você",
          "título"
        ],
        "entities": [
          [
            "105",
            "CARDINAL"
          ],
          [
            "carro(terminava",
            "GPE"
          ],
          [
            "para aprender",
            "PERSON"
          ],
          [
            "Insulfilm",
            "PERSON"
          ],
          [
            "que eu vivi",
            "PERSON"
          ],
          [
            "único",
            "NORP"
          ],
          [
            "para mim",
            "PERSON"
          ],
          [
            "dia",
            "ORG"
          ],
          [
            "para mim",
            "PERSON"
          ],
          [
            "dia",
            "ORG"
          ]
        ],
        "readability_score": 79.12692307692308,
        "semantic_density": 0,
        "word_count": 234,
        "unique_words": 156,
        "lexical_diversity": 0.6666666666666666
      },
      "preservation_score": 2.553972723077796e-05
    },
    {
      "id": 1,
      "text": "— 106 —Dom é algo particular de cada um.\\nAnalogia da evolução do seu próprio comportamento!!!\\nPensa na sua vida em uma escola, na escola temos o diretor, \\ncoordenador, professor e alunos.\\nProfessor – semelhante a uma mãe, um pai, as pessoas à sua \\nvolta que são a maior referência para você. Há bons professo -\\nres e professores ruins.\\nDiretor – é a comunidade, estado, país é a regra que direcio -\\nna o “melhor” para se viver em conjunto com a sociedade. Há \\nbons diretores e diretores ruins.\\nCoordenador – são aquelas pessoas quepassam em sua vida, \\nte orientando, coordenando, instruindo, guiando…Há coorde -\\nnadores bons e coordenadores ruins.\\nAluno – somos nós que estamos na escola da vida, à pro -\\ncura de aprender, melhorar, aprimorar e enxergando aquilo \\nou algo que achamos que é necessário para vivermos melhor, \\ndiante daquilo ou de algo que os nossos professores ensinaram \\ncomo melhor para nós mesmos ou para uma escola melhor. \\nHá alunos bons e alunos ruins.\\nNós não sabemos nada, não sabemos oque é a vida, não sa -\\nbemos oque é certo ou errado, não sabemos oque a outra pes -\\nsoa está pensando e muito menos como ela viveu e como ela \\nabsorveu a vida, sua crítica, seu julgamento tem que ser ensi -\\nnamento junto com a seu próprio aprendizado, pois em nosso \\nSem título-1   106Sem título-1   106 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 132237,
      "chapter": 5,
      "page": 106,
      "segment_type": "page",
      "themes": {},
      "difficulty": 31.064560862865946,
      "complexity_metrics": {
        "word_count": 236,
        "sentence_count": 11,
        "paragraph_count": 1,
        "avg_sentence_length": 21.454545454545453,
        "avg_word_length": 4.669491525423729,
        "unique_word_ratio": 0.597457627118644,
        "avg_paragraph_length": 236.0,
        "punctuation_density": 0.15677966101694915,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "vida",
          "escola",
          "bons",
          "ruins",
          "melhor",
          "algo",
          "alunos",
          "como",
          "sabemos",
          "oque",
          "próprio",
          "diretor",
          "coordenador",
          "professor",
          "pessoas",
          "professores",
          "diretores",
          "título",
          "particular",
          "cada"
        ],
        "entities": [
          [
            "106",
            "CARDINAL"
          ],
          [
            "Analogia",
            "GPE"
          ],
          [
            "referência para você",
            "PERSON"
          ],
          [
            "para se",
            "PERSON"
          ],
          [
            "Coordenador",
            "ORG"
          ],
          [
            "orientando",
            "ORG"
          ],
          [
            "coordenando",
            "ORG"
          ],
          [
            "Aluno",
            "ORG"
          ],
          [
            "cura de aprender",
            "ORG"
          ],
          [
            "melhorar",
            "GPE"
          ]
        ],
        "readability_score": 87.87187981510016,
        "semantic_density": 0,
        "word_count": 236,
        "unique_words": 141,
        "lexical_diversity": 0.597457627118644
      },
      "preservation_score": 2.553972723077796e-05
    },
    {
      "id": 1,
      "text": "— 107 —próprio mundo nós somos a escola, diretor, coordenador, alu -\\nnos, nós somos o nosso viver!!!\\nCoisas que nós conversamos e não percebemos que esta -\\nmos conversando, e quando estamos conversando brigamos \\npor não lembrar oque nós mesmos estávamos conversando!!!\\nPessoa\\nEstou conhecendo uma pessoa, não irei no lugar, pois eu \\nnão sei se ela gosta que fumem maconha perto dela, pois ela é \\nmeio careta!!!\\nEu:\\nPeraí, você é meu amigo há quantos anos? E outra,você vai \\ndeixar de fazer algo que raramente fazemos para dar priorida -\\nde a ficar com uma mulherque você está conhecendo, deixan -\\ndo de fazer algo que você é feliz com os seus amigos, ver o jogo \\ndo Flamengo,fumar um baseado após o trabalho e você está \\ndando prioridade para uma pessoa?\\nPessoa:\\n– Se eu deixar de fumar maconha para ficar com uma pes -\\nsoa eu faço, você acha que todo mundo tem que aceitar a ma -\\nconha, pois você usa, tem gente que não gosta e eu respeito!! \\nEu:\\n– Também respeito. Mas estou na minha casa com meus \\namigos, eu não fumo no meu trabalho, não fumo sempre, \\nfumo para dormir meio baseado e quando estou com meus \\nSem título-1   107Sem título-1   107 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 133708,
      "chapter": 5,
      "page": 107,
      "segment_type": "page",
      "themes": {},
      "difficulty": 30.609905660377358,
      "complexity_metrics": {
        "word_count": 212,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 26.5,
        "avg_word_length": 4.533018867924528,
        "unique_word_ratio": 0.6179245283018868,
        "avg_paragraph_length": 212.0,
        "punctuation_density": 0.18867924528301888,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "pessoa",
          "conversando",
          "estou",
          "pois",
          "fumo",
          "mundo",
          "somos",
          "quando",
          "conhecendo",
          "gosta",
          "maconha",
          "meio",
          "deixar",
          "fazer",
          "algo",
          "ficar",
          "está",
          "amigos",
          "fumar"
        ],
        "entities": [
          [
            "107",
            "CARDINAL"
          ],
          [
            "Coisas",
            "NORP"
          ],
          [
            "não percebemos que",
            "ORG"
          ],
          [
            "quando estamos",
            "PERSON"
          ],
          [
            "conversando brigamos",
            "GPE"
          ],
          [
            "mesmos estávamos",
            "PERSON"
          ],
          [
            "eu \\nnão sei",
            "PERSON"
          ],
          [
            "ela gosta",
            "PERSON"
          ],
          [
            "Eu",
            "PERSON"
          ],
          [
            "Peraí",
            "ORG"
          ]
        ],
        "readability_score": 85.39009433962264,
        "semantic_density": 0,
        "word_count": 212,
        "unique_words": 131,
        "lexical_diversity": 0.6179245283018868
      },
      "preservation_score": 2.553972723077796e-05
    },
    {
      "id": 1,
      "text": "— 108 —amigos e pessoas que amo não irei deixar de fazer algo que me \\ndeixa feliz com pessoas que eu amo, por uma pessoa que eu \\nestou conhecendo!!!\\nPessoa:\\nVocêé você, a maconha você aceita, nem todos aceitam, \\nnem todos conseguem fazer oque você faz, sua mãe aceita, seu \\nfilho aceita, para você é normal.Não pense que todos vão ter \\nesse pensamento de liberdade perante a maconha!!\\nEu:\\nVocêbebe todos os dias? Fuma cigarro todos os dias? Como \\nos negros conquistaram a liberdade? Como as mulheres con -\\nquistaram a liberdade? Os gays? Temos que lutar contra aquilo \\nque eu acho errado de ser proibido. Como irei lutar se eu ficar \\nomisso?\\n“Outra coisa acontece quando o assunto é política, maco -\\nnha, respeito, legislação ou a sua prioridade em dar priorida -\\nde para uma pessoa que vocêestá conhecendo, que não gosta \\nde algo que te faz feliz com os seus amigos.Tem uma semana \\nque você está conhecendo-a, ao invés de você ficar com os seus \\namigos que você quase não vê, que você conhece há mais de \\n30 anos, você não quer ir por ela não gostar? Eu não irei ficar \\ncom uma pessoa, que não aceita a minha felicidade. Aceito a \\nsua felicidade e ela aceita a minha.Se não for para somar, eu \\nnão quero!!!”\\n“Suas prioridades o faz pagar um preço futuro sem saber o \\nmotivo… ”\\nNão reclame do seu presente, pois ele é fruto do seu \\npassado!!!\\nSem título-1   108Sem título-1   108 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 135014,
      "chapter": 5,
      "page": 108,
      "segment_type": "page",
      "themes": {},
      "difficulty": 23.893697478991598,
      "complexity_metrics": {
        "word_count": 252,
        "sentence_count": 17,
        "paragraph_count": 1,
        "avg_sentence_length": 14.823529411764707,
        "avg_word_length": 4.5476190476190474,
        "unique_word_ratio": 0.6150793650793651,
        "avg_paragraph_length": 252.0,
        "punctuation_density": 0.18253968253968253,
        "line_break_count": 28,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "aceita",
          "todos",
          "pessoa",
          "amigos",
          "irei",
          "conhecendo",
          "liberdade",
          "como",
          "ficar",
          "pessoas",
          "fazer",
          "algo",
          "feliz",
          "maconha",
          "dias",
          "lutar",
          "seus",
          "minha",
          "felicidade"
        ],
        "entities": [
          [
            "108",
            "CARDINAL"
          ],
          [
            "deixar de fazer",
            "PERSON"
          ],
          [
            "que eu",
            "PERSON"
          ],
          [
            "Vocêé",
            "PERSON"
          ],
          [
            "nem todos",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "sua mãe aceita",
            "ORG"
          ],
          [
            "filho aceita",
            "PERSON"
          ],
          [
            "para você",
            "PERSON"
          ]
        ],
        "readability_score": 91.22394957983194,
        "semantic_density": 0,
        "word_count": 252,
        "unique_words": 155,
        "lexical_diversity": 0.6150793650793651
      },
      "preservation_score": 3.456376418565284e-05
    },
    {
      "id": 1,
      "text": "— 109 —O maior problema do ser humano é não reconhecer o pró -\\nprio erro!!!\\nO ser humano, se reconhecesse o seu próprio erro, não iria \\ndiscutir pelo mesmo. O assumir que as suas ações são erradas \\ndiante da sua própria certeza é raro!!!\\nOs atos de pedir desculpas, reconhecer algo fora de um \\ncontexto pessoal perante o melhor para uma sociedade não \\nestá escrito como“princípio” . Se você não reconhecer como ne -\\ncessário, de nada vale!!!\\nSe só os outros reconhecerem e você não, de que adianta?\\nA sua prepotência diante da sua razão nunca irá ser reco -\\nnhecida por você mesmo, pois você viveu uma vida de valores \\nproporcionais à vida a qual você vive. Se todas as vidas fossem \\nsemelhantes ou iguais, por que teríamos nossas diferenças, \\nevolução, amor, vontades e muitas outras coisas que você re -\\nclama e não percebe a importância de se viver as diferenças de \\ncada um?Isso é necessário para o valor de si próprio!\\nO nosso subconsciente é o organizador da nossa cons -\\nciência…\\nNossos pensamentos vêm de algo, de onde vem esse algo? \\nQuem organiza oque iremos pensar? Quem diz oque iremos \\npensar? Quem consegue captar oque está à nossa volta?\\nSem título-1   109Sem título-1   109 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 136552,
      "chapter": 5,
      "page": 109,
      "segment_type": "page",
      "themes": {
        "filosofia": 53.57142857142857,
        "ciencia": 46.42857142857144
      },
      "difficulty": 24.018410462776657,
      "complexity_metrics": {
        "word_count": 213,
        "sentence_count": 14,
        "paragraph_count": 1,
        "avg_sentence_length": 15.214285714285714,
        "avg_word_length": 4.704225352112676,
        "unique_word_ratio": 0.6901408450704225,
        "avg_paragraph_length": 213.0,
        "punctuation_density": 0.1596244131455399,
        "line_break_count": 22,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "reconhecer",
          "algo",
          "quem",
          "oque",
          "humano",
          "erro",
          "próprio",
          "mesmo",
          "diante",
          "está",
          "como",
          "vida",
          "diferenças",
          "nossa",
          "iremos",
          "pensar",
          "título",
          "maior",
          "problema"
        ],
        "entities": [
          [
            "109",
            "CARDINAL"
          ],
          [
            "pelo mesmo",
            "PERSON"
          ],
          [
            "suas ações",
            "PERSON"
          ],
          [
            "diante da sua própria",
            "PERSON"
          ],
          [
            "Se você não reconhecer",
            "PERSON"
          ],
          [
            "de nada",
            "PERSON"
          ],
          [
            "prepotência diante da sua",
            "PERSON"
          ],
          [
            "irá ser reco -\\n",
            "PERSON"
          ],
          [
            "Se todas",
            "PERSON"
          ],
          [
            "necessário",
            "GPE"
          ]
        ],
        "readability_score": 90.98158953722334,
        "semantic_density": 0,
        "word_count": 213,
        "unique_words": 147,
        "lexical_diversity": 0.6901408450704225
      },
      "preservation_score": 2.1070274965391818e-05
    },
    {
      "id": 1,
      "text": "— 110 —Quem é mais importante: quem organiza ou quem executa?\\n“Mente vazia é oficina do diabo… ”\\nOque seria o diabo nessa frase? O diabo são as suas próprias \\nfraquezas!!\\nOque seria mente vazia? Mente vazia é aquela mente que \\nnão consegue produzir, estudar, criar, assimilar, evoluir, só pen -\\nsando no seu “benefício” de não saber fazer algo no seu tempo \\n“livre”!!!\\nOque seria a oficina nessa frase? Oficina é ausência de \\nnão saber oque fazer, com o tempo “livre” diante da sua pró -\\npria vida!!\\nEx.: você está em casa após trabalho, com a casa arrumada, \\nsem dinheiro, já viu todas as séries e filmes e, entediado, oque \\nvocê faria para passar o seu tempo “livre”? A maioria vai à pro -\\ncura de fugir de estar sozinho, entrando em um ciclo vicioso \\nda necessidade de ter alguma companhia a seu lado, o limitan -\\ndo em fazer algo melhor para si mesmo, levando você a ir para \\na rua ficar com os amigos, sair para beber com os amigos ou \\npara ficar com alguém ou mesmo indo para rua gastar dinhei -\\nro desnecessário, pelo simples fator de ter oque fazer.\\nQuando não se tem obrigações, oque acontece com essa \\npessoa?\\nQuando se tem muito problema (mendigo), oque acontece \\ncom essa pessoa?\\nSem título-1   110Sem título-1   110 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 137900,
      "chapter": 5,
      "page": 110,
      "segment_type": "page",
      "themes": {},
      "difficulty": 26.06297435897436,
      "complexity_metrics": {
        "word_count": 225,
        "sentence_count": 13,
        "paragraph_count": 1,
        "avg_sentence_length": 17.307692307692307,
        "avg_word_length": 4.568888888888889,
        "unique_word_ratio": 0.6488888888888888,
        "avg_paragraph_length": 225.0,
        "punctuation_density": 0.17777777777777778,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "oque",
          "mente",
          "fazer",
          "quem",
          "vazia",
          "oficina",
          "diabo",
          "seria",
          "tempo",
          "livre",
          "você",
          "nessa",
          "frase",
          "saber",
          "algo",
          "casa",
          "mesmo",
          "ficar",
          "amigos",
          "quando"
        ],
        "entities": [
          [
            "110",
            "CARDINAL"
          ],
          [
            "Mente",
            "PRODUCT"
          ],
          [
            "aquela mente que",
            "PERSON"
          ],
          [
            "benefício” de não",
            "PERSON"
          ],
          [
            "Oficina é ausência de \\nnão",
            "PERSON"
          ],
          [
            "pria",
            "GPE"
          ],
          [
            "casa",
            "ORG"
          ],
          [
            "de fugir de estar",
            "PERSON"
          ],
          [
            "mesmo",
            "ORG"
          ],
          [
            "levando você a ir",
            "ORG"
          ]
        ],
        "readability_score": 89.97548717948717,
        "semantic_density": 0,
        "word_count": 225,
        "unique_words": 146,
        "lexical_diversity": 0.6488888888888888
      },
      "preservation_score": 3.115846722154911e-05
    },
    {
      "id": 1,
      "text": "— 111 — Quando não se está feliz, oque acontece com essa pessoa?\\nA mente vazia tem vários sentidos, mas o maior sentido da \\nmente vazia,e que émaléfico, é o medo da solidão em não sa -\\nber lidar com a própria solidão!!\\nNão confundam uma mente cheias de “problemas” com \\numa mente cheia de pensamentos… Uma mente cheia de pro -\\nblemas ocorre pela ausência de se pensar corretamente diante \\ndo problema, nos tornando pessoas com mais problemas por \\nnão conseguirmos resolver nosso próprio problema por não \\nconseguir ocupar a mente corretamente.\\nFalta de organização mental o faz ter prioridades para que \\nseu subconsciente mande para sua consciência…\\nReferência – analogia\\nSemelhante a desfragmentar um computador, relocar a \\nsua memória de acordo com a importância de necessidade \\nfutura!!!\\nA vida é feita de altos e baixos, certo e errado, bom e ruim, \\npois é necessário para sabermos oque é felicidade… pensa em \\numa vida, ondevocê tem tudo sem saber oque é não ter algo. \\nQual seria a graça de viver tendo tudo sem as adversidades, \\nsem as loucuras que acontecem do nada em sua vida?São pes -\\nsoas que você não encontra há anos que te beijam, pessoas que \\nestão ao seu lado te ouvindo, na felicidade e na tristeza, tudo \\nem prol de quê? Em prol de ser feliz, não em prol da tristeza, \\nSem título-1   111Sem título-1   111 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 139287,
      "chapter": 5,
      "page": 111,
      "segment_type": "page",
      "themes": {
        "filosofia": 53.57142857142857,
        "ciencia": 46.42857142857144
      },
      "difficulty": 31.111858974358974,
      "complexity_metrics": {
        "word_count": 234,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 29.25,
        "avg_word_length": 4.747863247863248,
        "unique_word_ratio": 0.6452991452991453,
        "avg_paragraph_length": 234.0,
        "punctuation_density": 0.1282051282051282,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "mente",
          "oque",
          "vida",
          "tudo",
          "prol",
          "feliz",
          "vazia",
          "solidão",
          "problemas",
          "cheia",
          "corretamente",
          "problema",
          "pessoas",
          "felicidade",
          "tristeza",
          "título",
          "quando",
          "está",
          "acontece",
          "essa"
        ],
        "entities": [
          [
            "111",
            "CARDINAL"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "essa pessoa",
            "PERSON"
          ],
          [
            "sentido da \\nmente vazia",
            "PERSON"
          ],
          [
            "medo da solidão",
            "PERSON"
          ],
          [
            "ausência de se pensar corretamente diante",
            "PERSON"
          ],
          [
            "Falta de organização mental",
            "ORG"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "para sua consciência",
            "PERSON"
          ],
          [
            "Referência",
            "PERSON"
          ]
        ],
        "readability_score": 83.95064102564103,
        "semantic_density": 0,
        "word_count": 234,
        "unique_words": 151,
        "lexical_diversity": 0.6452991452991453
      },
      "preservation_score": 1.9920987240006808e-05
    },
    {
      "id": 1,
      "text": "— 112 —da dor.A vida é uma palavra feliz e não de tristeza (morte). \\nOlhe em sua volta, pois há energia das pessoas ao redor. O sen -\\ntir é pessoal, não ensinamos a alguém a ser melhor, ensinamos \\nque ele tem que ser melhor para simesmo, pois enxergamos \\ndefeitosque nós mesmos não enxergamos sobre nós mesmos. \\nSomos feitos de erros, pois quandovem a felicidade é algo úni -\\nco, cada momento de felicidade é único. Como podemos que -\\nrer sermos sempre feliz se nenhum animal na natureza tem \\nesse privilégio? Todos os seres vivos são felizes dentro do seu \\npróprio mundo!!!\\nAnalogia\\nO leão quandopega uma presa é feliz. Após se alimentar do \\nque ele caçou, ele é feliz. Quanto tempo demora na vida de um \\nleão para ele ser feliz?\\nTodos os animais são assim, ensinam, aprendem, evoluem, \\nresolvem e absorvem aquilo que eu fiz por merecer!!!!\\nNão pense no ganho de vida em contexto monetário, pois \\nesse ganho pode vir por motivos eorigemerradas, “nem todos \\nque têm dinheiro são felizes e nem todo pobre é triste!!!”\\nSem título-1   112Sem título-1   112 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 140770,
      "chapter": 5,
      "page": 112,
      "segment_type": "page",
      "themes": {},
      "difficulty": 23.727905073649755,
      "complexity_metrics": {
        "word_count": 188,
        "sentence_count": 13,
        "paragraph_count": 1,
        "avg_sentence_length": 14.461538461538462,
        "avg_word_length": 4.73404255319149,
        "unique_word_ratio": 0.6914893617021277,
        "avg_paragraph_length": 188.0,
        "punctuation_density": 0.19148936170212766,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "feliz",
          "pois",
          "vida",
          "todos",
          "ensinamos",
          "melhor",
          "enxergamos",
          "mesmos",
          "felicidade",
          "esse",
          "felizes",
          "leão",
          "ganho",
          "título",
          "palavra",
          "tristeza",
          "morte",
          "olhe",
          "volta",
          "energia"
        ],
        "entities": [
          [
            "112",
            "CARDINAL"
          ],
          [
            "para simesmo",
            "PERSON"
          ],
          [
            "defeitosque",
            "NORP"
          ],
          [
            "mesmos não enxergamos",
            "PERSON"
          ],
          [
            "nós mesmos",
            "PERSON"
          ],
          [
            "Somos",
            "PERSON"
          ],
          [
            "úni",
            "ORG"
          ],
          [
            "único",
            "GPE"
          ],
          [
            "nenhum",
            "ORG"
          ],
          [
            "Analogia",
            "GPE"
          ]
        ],
        "readability_score": 91.34901800327333,
        "semantic_density": 0,
        "word_count": 188,
        "unique_words": 130,
        "lexical_diversity": 0.6914893617021277
      },
      "preservation_score": 1.900581368090393e-05
    },
    {
      "id": 1,
      "text": "— 113 —Não confundam o querer ter com o poder ter… nem tudo \\nque eu quero eu posso dentro da minha realidade de vida.\\nTemos que entender que o mundo não acontece apenas ao \\nnosso redor.O mundo é formado de várias linhas de tempos \\ndistintas de cada um, da junção de acordo com a necessida -\\nde de cada necessidade, devido a sua linha de tempo coincidir \\ncom a outra e sua demandamomentânea ou de acordo com o \\nmeio em quevivo!!\\nAté que ponto você tem que ser pai ou mãe e criar o seu \\nfilho para o mundo?\\nMeu filho de 12 anos:\\n– Pai, quase ninguém da minha escola vai embora sozinho, \\npor que isso? Quando você era mais novo também era assim?\\nEu:\\n– Não era assim!! Pois na minha época tinha traficantes, \\nbandidos, brigas quase todos os dias, a violência e o ensino \\neram piores do que o seu, porém não tínhamos tantas infor -\\nmações sobre tudo oque acontecia, as nossas informações \\neram locais, nem sempre oque acontecia em outros lugares \\nnós sabíamos. Hoje as pessoas têm muito mais informações de \\ntodos os lugares, e essas informações vêm sempre com maior \\nconstância e dor, sofrimento, erros, roubos, tudo oque causa \\nSem título-1   113Sem título-1   113 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 141982,
      "chapter": 5,
      "page": 113,
      "segment_type": "page",
      "themes": {},
      "difficulty": 28.25508607198748,
      "complexity_metrics": {
        "word_count": 213,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 23.666666666666668,
        "avg_word_length": 4.553990610328638,
        "unique_word_ratio": 0.6807511737089202,
        "avg_paragraph_length": 213.0,
        "punctuation_density": 0.14553990610328638,
        "line_break_count": 22,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "tudo",
          "minha",
          "mundo",
          "oque",
          "informações",
          "cada",
          "acordo",
          "você",
          "filho",
          "quase",
          "mais",
          "assim",
          "todos",
          "eram",
          "acontecia",
          "sempre",
          "lugares",
          "título",
          "confundam",
          "querer"
        ],
        "entities": [
          [
            "113",
            "CARDINAL"
          ],
          [
            "nem tudo \\nque eu quero eu posso",
            "PERSON"
          ],
          [
            "Temos",
            "PERSON"
          ],
          [
            "necessida",
            "GPE"
          ],
          [
            "filho para",
            "ORG"
          ],
          [
            "Meu filho de 12",
            "ORG"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "novo também era",
            "PERSON"
          ],
          [
            "Eu",
            "PERSON"
          ],
          [
            "nem sempre",
            "PERSON"
          ]
        ],
        "readability_score": 86.80046948356808,
        "semantic_density": 0,
        "word_count": 213,
        "unique_words": 145,
        "lexical_diversity": 0.6807511737089202
      },
      "preservation_score": 1.7324448304877716e-05
    },
    {
      "id": 1,
      "text": "— 114 —mal para alguém, gerando uma preocupação muito maior que \\né para ser gerada, transformando as crianças com medo de sair, \\nmedo de conversar, cheias de julgamento, cheias de manias, \\ncheias de não me toques e amanhã não sabendo viver por nun -\\nca conseguirem viver pelo medo que as pessoas em sua vol -\\nta passavam para elas mesmas, transformando-as em pessoas \\ncheias de medo do mundoque você terá que viver amanhã!!!\\nAté que ponto você cria o seu filho para você ao invés de \\ncriar para o amanhã, para que o mundo não possa o destruir?\\n“A sua consciência é o maior problema da sua própria cons -\\nciência… ” Oque a sua consciência absorve afeta o seu subcons -\\nciente, absorve oque é necessário para se ter a razão de se viver \\numa vida digna, entrando em ciclos da sua própria absorção \\ndiante da sua própria consciência que não sabe oque é necessá -\\nrio e absorve perante sua própria necessidade!!!\\nQual é o seu valor?\\nVocê deseja conhecer alguém, você chega até esse alguém, \\naté que ponto você tem que ir até esse alguém?\\nAté que ponto o valor que você dá para conhecer aquela \\npessoa não o faz se desmerecer?\\nSem título-1   114Sem título-1   114 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 143302,
      "chapter": 5,
      "page": 114,
      "segment_type": "page",
      "themes": {
        "filosofia": 53.57142857142857,
        "ciencia": 46.42857142857144
      },
      "difficulty": 30.430574098798395,
      "complexity_metrics": {
        "word_count": 214,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 30.571428571428573,
        "avg_word_length": 4.5327102803738315,
        "unique_word_ratio": 0.5514018691588785,
        "avg_paragraph_length": 214.0,
        "punctuation_density": 0.12149532710280374,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "alguém",
          "medo",
          "cheias",
          "viver",
          "própria",
          "amanhã",
          "ponto",
          "consciência",
          "oque",
          "absorve",
          "maior",
          "transformando",
          "pessoas",
          "valor",
          "conhecer",
          "esse",
          "título",
          "gerando",
          "preocupação"
        ],
        "entities": [
          [
            "114",
            "CARDINAL"
          ],
          [
            "para ser gerada",
            "PRODUCT"
          ],
          [
            "medo de sair",
            "PERSON"
          ],
          [
            "medo de conversar",
            "PERSON"
          ],
          [
            "pelo medo que",
            "PERSON"
          ],
          [
            "para elas mesmas",
            "PERSON"
          ],
          [
            "de medo",
            "PERSON"
          ],
          [
            "mundoque você terá que",
            "ORG"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "para você ao",
            "PERSON"
          ]
        ],
        "readability_score": 83.35447263017356,
        "semantic_density": 0,
        "word_count": 214,
        "unique_words": 118,
        "lexical_diversity": 0.5514018691588785
      },
      "preservation_score": 1.617516057949271e-05
    },
    {
      "id": 1,
      "text": "— 115 —Até que ponto você está valorizando mais a pessoa do que a \\npessoa está te valorizando?\\nMeu ponto de vista!!!\\nSe eu fizer mais por alguém, automaticamente estou me \\ncolocando como inferior à outra pessoa. Qualquer relaciona -\\nmento, seja ele qual for, tem que ser via de mão dupla, pois eu \\nnão sei oque você pensa, eu não sei como você vive, como eu \\nirei te dar um valor seeu não sei se você merece?\\nVeja oque você é, veja como você vive, veja até que ponto \\nvocê merece aquele amigo (a), namorada (o), filho (a), irmão \\n(a), mãe, pai, qualquer pessoa, pois assim como temos pessoas \\nruins no mundo, essas mesmas pessoas são pais, mães, irmãos, \\nfilhos, namoradas e etc.\\nLimita as pessoas para que você não seja limitado por não \\ndar limites a quem não merece, por você ficar preocupado \\ncom oque vão pensar, pelo oque eu quero “conquistar” , pelo \\noque eu preciso ser amanhã para ser melhor para quem real -\\nmente merece o meu valor!!!\\nCoisas que eu escuto!!!\\n“Todas as pessoas são ruins!!!”\\nQuandovocê pensa assim você está se incluindo, incluindo \\nseu filho, sua mãe, seus amigos e todos os seres humanos.\\nSem título-1   115Sem título-1   115 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 144618,
      "chapter": 5,
      "page": 115,
      "segment_type": "page",
      "themes": {},
      "difficulty": 26.89090909090909,
      "complexity_metrics": {
        "word_count": 209,
        "sentence_count": 10,
        "paragraph_count": 1,
        "avg_sentence_length": 20.9,
        "avg_word_length": 4.636363636363637,
        "unique_word_ratio": 0.6507177033492823,
        "avg_paragraph_length": 209.0,
        "punctuation_density": 0.22488038277511962,
        "line_break_count": 22,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "como",
          "oque",
          "pessoa",
          "merece",
          "pessoas",
          "ponto",
          "está",
          "veja",
          "valorizando",
          "mais",
          "qualquer",
          "seja",
          "pois",
          "pensa",
          "vive",
          "valor",
          "filho",
          "assim",
          "ruins"
        ],
        "entities": [
          [
            "115",
            "CARDINAL"
          ],
          [
            "Meu",
            "ORG"
          ],
          [
            "Se eu",
            "PERSON"
          ],
          [
            "Qualquer relaciona -\\n",
            "PERSON"
          ],
          [
            "eu \\nnão",
            "PERSON"
          ],
          [
            "eu não",
            "PERSON"
          ],
          [
            "como eu \\nirei te",
            "PERSON"
          ],
          [
            "namorada",
            "ORG"
          ],
          [
            "qualquer pessoa",
            "PERSON"
          ],
          [
            "preocupado",
            "GPE"
          ]
        ],
        "readability_score": 88.1590909090909,
        "semantic_density": 0,
        "word_count": 209,
        "unique_words": 136,
        "lexical_diversity": 0.6507177033492823
      },
      "preservation_score": 3.043484161667707e-05
    },
    {
      "id": 1,
      "text": "— 116 —Se você pensa que não existem pessoas boas, são porque to -\\ndos são ruins, é porque você é ruim ou é porque você só vê \\ncoisas ruins?\\nNós sabemos oque é bom e oque é ruim.\\nExemplos: \\nJesus (Palestina) foi uma pessoa boa ou ruim?\\nHitler (Alemanha) uma pessoa boa ou ruim?\\nTodos nós temos noção da merda que estamos fazendo, o \\nmedo de estarmos errados te move ao erro pior ainda…\\nAnalogia\\nOque é um peido para quem já está todo cagado?\\nMerdas cagadas não voltam ao rabo…\\nSe está no inferno, abraça o capeta…\\nÉ assim que as pessoas pensam quando sabem que estão \\nerradas, pois o seu benefício diante do erro que já está ocor -\\nrendo será o “mesmo”!!! \\nO entender o lado ruim do ser humano não quer dizer que \\nvocê seja ruim.O entender o lado bom do ser humano não \\nquer dizer que você seja bom.\\nA falta de conversar, a falta de ensinar, a falta de compreen -\\nsão perante o outro o faz ter um julgamento da sua certeza, da \\nsua felicidade e da sua dor. Não pense que a sua forma de ver \\no certo ou o errado é a forma correta de ver a vida de todosque \\nvivem no mundo!!!\\nSem título-1   116Sem título-1   116 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 145931,
      "chapter": 5,
      "page": 116,
      "segment_type": "page",
      "themes": {},
      "difficulty": 26.33299053887289,
      "complexity_metrics": {
        "word_count": 221,
        "sentence_count": 11,
        "paragraph_count": 1,
        "avg_sentence_length": 20.09090909090909,
        "avg_word_length": 4.14027149321267,
        "unique_word_ratio": 0.6153846153846154,
        "avg_paragraph_length": 221.0,
        "punctuation_density": 0.12217194570135746,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "ruim",
          "você",
          "porque",
          "oque",
          "está",
          "falta",
          "pessoas",
          "ruins",
          "pessoa",
          "erro",
          "entender",
          "lado",
          "humano",
          "quer",
          "dizer",
          "seja",
          "forma",
          "título",
          "pensa",
          "existem"
        ],
        "entities": [
          [
            "116",
            "CARDINAL"
          ],
          [
            "Jesus",
            "PERSON"
          ],
          [
            "Hitler",
            "PERSON"
          ],
          [
            "Todos",
            "GPE"
          ],
          [
            "da merda",
            "PERSON"
          ],
          [
            "que",
            "CARDINAL"
          ],
          [
            "fazendo",
            "ORG"
          ],
          [
            "medo de estarmos",
            "PERSON"
          ],
          [
            "ainda",
            "PERSON"
          ],
          [
            "Analogia",
            "GPE"
          ]
        ],
        "readability_score": 88.71246400658165,
        "semantic_density": 0,
        "word_count": 221,
        "unique_words": 136,
        "lexical_diversity": 0.6153846153846154
      },
      "preservation_score": 2.0431781784622368e-05
    },
    {
      "id": 1,
      "text": "— 117 —Com quem você gostaria de ter uma conversa: Jesus, Hitler, \\nEinstein, Tesla, Leonardo da Vinci? Todos esses têm o seu bene -\\nfício diante de uma forma de ver a vida. Por mais que a maio -\\nria fale Jesus eu, Marcelo, provavelmente não teria paciência \\npara conversar com Jesus, não seria a minha prioridade dessa \\nlista. Do meu ponto de vista, Jesus é muito passivo e nem sem -\\npre o ser passivo é a solução!!!\\nO maior aprendizado do ser humano é na dificuldade do \\nser humano!!!\\nO que é um bom professor??\\nMeu ponto de vista:\\nBom professor é aquele que consegue ensinar as dificulda -\\ndes para outros com uma maior facilidade.\\nSer inteligente é semelhante, pois ele pode ser um gênio \\npara fazer algo, porém nem sempre o “melhor guerreiro é o \\nmelhor general… ” . A sabedoria em viver é aquele “melhor vive \\nquem tem o equilíbrio entre ter algo e entre ser algo” …Sabe -\\ndoria de valores, esse valores são aprendizados de si próprio, \\ndiante dos seus próprios porquês…Seus questionamentos é a \\nsua evolução e seu aprendizado em querer aprender o novo, \\nsempre a fazer o melhor para o próximo que amanhã irá fazer \\no mesmo.\\nTransborde felicidade, viva a felicidade para sermos mais \\nfortesque as nossas dores do nosso dia a dia!!!\\nSem título-1   117Sem título-1   117 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 147200,
      "chapter": 5,
      "page": 117,
      "segment_type": "page",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 26.83896103896104,
      "complexity_metrics": {
        "word_count": 231,
        "sentence_count": 11,
        "paragraph_count": 1,
        "avg_sentence_length": 21.0,
        "avg_word_length": 4.6147186147186146,
        "unique_word_ratio": 0.6666666666666666,
        "avg_paragraph_length": 231.0,
        "punctuation_density": 0.16017316017316016,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "jesus",
          "melhor",
          "fazer",
          "algo",
          "quem",
          "diante",
          "mais",
          "ponto",
          "vista",
          "passivo",
          "maior",
          "aprendizado",
          "humano",
          "professor",
          "aquele",
          "sempre",
          "entre",
          "valores",
          "seus",
          "felicidade"
        ],
        "entities": [
          [
            "117",
            "CARDINAL"
          ],
          [
            "Jesus",
            "PERSON"
          ],
          [
            "Hitler",
            "PERSON"
          ],
          [
            "Einstein",
            "PERSON"
          ],
          [
            "Tesla",
            "PERSON"
          ],
          [
            "Leonardo da Vinci",
            "PERSON"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "diante de uma forma de ver",
            "PERSON"
          ],
          [
            "Jesus eu",
            "PERSON"
          ],
          [
            "Marcelo",
            "PERSON"
          ]
        ],
        "readability_score": 88.11558441558441,
        "semantic_density": 0,
        "word_count": 231,
        "unique_words": 154,
        "lexical_diversity": 0.6666666666666666
      },
      "preservation_score": 2.553972723077796e-05
    },
    {
      "id": 1,
      "text": "— 118 —Estava conversando com meu filho agora pela manhã, me \\ndeparei com uma situação de autoavaliação…\\nTivemos uma avaliação sobre o que é ter uma vida boa. \\nDentro dessa vida boa que eu e meu filho temos, veio o ques -\\ntionamento de merecimento por viver a vida que temos.\\nEu:\\n– Filho, se nós temos uma vida e não entendemos o moti -\\nvo… dentro desse motivo que eu não reconheço o motivo de \\nter uma boa vida, pessoas me fizeram o bem, me ajudaram a \\nevoluir, me ouviram, estiveram do meu lado… Como uma pes -\\nsoa vive fazendo coisas piores ou sendo pior do que eu e você, \\ncomo uma pessoa dessas consegue viver fazendo pior do que \\nfazemos durante a nossa vida?\\nA geração nascida entre1980 e 1990 não entende o motivo \\nde ser a geração com mais depressão… mais em dúvida sobre \\ncomo viver...mais em dúvida sobre como evoluir...porque isso \\nacontece?\\nSimples, nós somos a transição de uma geração em que as \\npessoas eram reprimidas, preconceituosas, machistas, homo -\\nfóbicas, com baixa tecnologia, internet, videogame, liberda -\\nde… imaginavocê ter que evoluir todo esse processo e cuidar \\nda família? Imagina você ter que competir com uma geração \\nSem título-1   118Sem título-1   118 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 148632,
      "chapter": 5,
      "page": 118,
      "segment_type": "page",
      "themes": {
        "ciencia": 56.52173913043479,
        "tecnologia": 43.47826086956522
      },
      "difficulty": 32.73714454976303,
      "complexity_metrics": {
        "word_count": 211,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 26.375,
        "avg_word_length": 4.748815165876778,
        "unique_word_ratio": 0.6208530805687204,
        "avg_paragraph_length": 211.0,
        "punctuation_density": 0.15165876777251186,
        "line_break_count": 22,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "vida",
          "como",
          "geração",
          "filho",
          "temos",
          "viver",
          "motivo",
          "evoluir",
          "mais",
          "dentro",
          "pessoas",
          "fazendo",
          "pior",
          "você",
          "dúvida",
          "título",
          "estava",
          "conversando",
          "agora",
          "pela"
        ],
        "entities": [
          [
            "118",
            "CARDINAL"
          ],
          [
            "agora pela manhã",
            "PERSON"
          ],
          [
            "Tivemos",
            "PERSON"
          ],
          [
            "Dentro",
            "LOC"
          ],
          [
            "que eu",
            "PERSON"
          ],
          [
            "veio o ques -\\n",
            "PERSON"
          ],
          [
            "Eu",
            "PERSON"
          ],
          [
            "nós temos uma vida",
            "ORG"
          ],
          [
            "moti -\\nvo",
            "PERSON"
          ],
          [
            "que eu não",
            "PERSON"
          ]
        ],
        "readability_score": 85.38785545023697,
        "semantic_density": 0,
        "word_count": 211,
        "unique_words": 131,
        "lexical_diversity": 0.6208530805687204
      },
      "preservation_score": 1.9197361635134767e-05
    },
    {
      "id": 1,
      "text": "— 119 —(1990,2005) que já veio acostumada a ter mais liberdade, a \\nsaber usar a tecnologia, facilidade em estudar, facilidade em \\nir ao mercado e comprar coisas com mais facilidade, ter uma \\nvoz mais ativa na sociedade devido a internet, devido aos pais \\nserem cabeça mais aberta, ter menos coisas a se preocupar, se \\npreocupando apenas em evoluir… Como você leva essa “com -\\npetição” que chega a ser desleal, perante o crescer na vida em \\nprol de melhoria pessoal e familiar?\\nObservação: Queda da Bolsa de 1929 foi a geração da tran -\\nsição da revolução industrial, uma das taxas de maior suicídio \\nque já tivemos!!\\nVocê vive o presente sem pensar quevocê viveu no seu pas -\\nsado, querendo um futuro melhor, sem fazer o melhor no pró -\\nprio presente, que se tornará passado ao você terminar de ler \\nesse texto…\\nQual é a melhor vida que você pode ter?\\nFaça suas avaliações diante de um padrão de acontecimen -\\ntos da normalidade que você acha que não é normal…\\nPerguntas que se deve fazer para si próprio, para se auto \\nentender sobre o que é melhor para você.\\nSem título-1   119Sem título-1   119 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 149980,
      "chapter": 5,
      "page": 119,
      "segment_type": "page",
      "themes": {
        "ciencia": 56.52173913043479,
        "tecnologia": 43.47826086956522
      },
      "difficulty": 36.385999999999996,
      "complexity_metrics": {
        "word_count": 200,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 40.0,
        "avg_word_length": 4.62,
        "unique_word_ratio": 0.67,
        "avg_paragraph_length": 200.0,
        "punctuation_density": 0.12,
        "line_break_count": 20,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "mais",
          "melhor",
          "facilidade",
          "coisas",
          "devido",
          "vida",
          "presente",
          "fazer",
          "título",
          "veio",
          "acostumada",
          "liberdade",
          "saber",
          "usar",
          "tecnologia",
          "estudar",
          "mercado",
          "comprar",
          "ativa"
        ],
        "entities": [
          [
            "119",
            "CARDINAL"
          ],
          [
            "1990,2005",
            "CARDINAL"
          ],
          [
            "já veio acostumada",
            "PERSON"
          ],
          [
            "voz mais",
            "PERSON"
          ],
          [
            "devido aos pais",
            "PERSON"
          ],
          [
            "Como",
            "ORG"
          ],
          [
            "Observação",
            "PERSON"
          ],
          [
            "já tivemos",
            "PERSON"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "sem fazer o melhor",
            "ORG"
          ]
        ],
        "readability_score": 78.614,
        "semantic_density": 0,
        "word_count": 200,
        "unique_words": 134,
        "lexical_diversity": 0.67
      },
      "preservation_score": 1.5749498458979744e-05
    },
    {
      "id": 1,
      "text": "— 120 —Quantos casamentos duraram uma vida inteira?\\nQuantos casamentos ambos foram felizes?\\nQuantos homens ou mulheres solteiras são felizes?\\nComo os solteiros são felizes?\\nComo se vive dentro de um casamento e como se é feliz \\ndentro de um casamento?\\nComo uma pessoa solteira é feliz quando consegue \\nser feliz?\\nQuais são os pontos que se encaixam dentro da minha \\nideologia de viver sendo feliz?\\nNossos planos, nossa forma de ver a felicidade é um padrão \\nde acordo com o que vivemos, será que a minha forma de ver \\na vida é melhor ou estou vendo o que eu fui criado para ver \\ncomo melhor?\\nEm nossos planos, muitas vezes colocamos empecilho para \\nfazermos tais coisas, precisamos atingir tais coisas, as vezes tais \\ncoisas atingimos (casamento) e não seguimos o planejamento \\ndo que queríamos atingir como viver… Como você absorve \\nessa “perda” de um planejamento quevocê achava que era a sua \\nfelicidade?\\nQuanto tempo você leva para se replanejar em um novo \\nestilo de vida, com as suas perdas durante o seu trajeto de um \\nviver melhor?São tantos questionamentos diante de um viver \\nque a maioria esquece de fazer os seus próprios questionamen -\\ntos para se viver melhor…\\n Quantas vezes você se fez um simples questionamento, “eu \\nestou vivendo ou sobrevivendo”?\\nSem título-1   120Sem título-1   120 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 151236,
      "chapter": 6,
      "page": 120,
      "segment_type": "page",
      "themes": {},
      "difficulty": 26.744570135746606,
      "complexity_metrics": {
        "word_count": 221,
        "sentence_count": 12,
        "paragraph_count": 1,
        "avg_sentence_length": 18.416666666666668,
        "avg_word_length": 4.981900452488688,
        "unique_word_ratio": 0.6153846153846154,
        "avg_paragraph_length": 221.0,
        "punctuation_density": 0.09954751131221719,
        "line_break_count": 27,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "como",
          "viver",
          "feliz",
          "melhor",
          "quantos",
          "vida",
          "felizes",
          "dentro",
          "casamento",
          "vezes",
          "tais",
          "coisas",
          "você",
          "casamentos",
          "minha",
          "nossos",
          "planos",
          "forma",
          "felicidade",
          "estou"
        ],
        "entities": [
          [
            "120",
            "CARDINAL"
          ],
          [
            "Quantos",
            "GPE"
          ],
          [
            "feliz quando consegue \\n",
            "PERSON"
          ],
          [
            "Quais",
            "GPE"
          ],
          [
            "nossa forma de ver",
            "PERSON"
          ],
          [
            "eu fui",
            "PERSON"
          ],
          [
            "para ver \\ncomo melhor",
            "PERSON"
          ],
          [
            "coisas atingimos",
            "PERSON"
          ],
          [
            "casamento",
            "ORG"
          ],
          [
            "que queríamos atingir",
            "PERSON"
          ]
        ],
        "readability_score": 89.29709653092006,
        "semantic_density": 0,
        "word_count": 221,
        "unique_words": 136,
        "lexical_diversity": 0.6153846153846154
      },
      "preservation_score": 1.8963247468852635e-05
    },
    {
      "id": 1,
      "text": "— 121 —Nunca podemos imaginar algo sem saber como se vive \\naquele algo, cada vida, cada situação é única, pois cada um age \\nde uma forma diante daquilo que se está vivendo, nem sempre \\na solução de outras pessoas são as suas soluções, nem sempre a \\nsua forma de ver a felicidade ou a tristeza é igual a de outros. \\nNós queremos tanto um viver que esquecemos que só vivemos \\no trajeto para a morte, não sabemos o dia de amanhã, imagina -\\nmos e planejamos de uma forma que o amanhã provavelmen -\\nte será assim…\\n Não se preocupe em como vai ser o amanhã, faça o melhor \\nhojeque o amanhã será melhor ainda!!!!\\nOlha as pessoas à sua volta, pois talvez você esteja agindo \\nerrado diante dos erros de outros… Sua forma de ver a vida \\nprejudica um filho que precisa de liberdade… uma mãe que \\nnão sabe viver, por não conseguir viver melhor, por oferecer o \\nmelhor para você durante uma vida…\\nAmigos, irmãos, pessoas próximas estão mal-acostumados \\npor você fazer coisas demais... Você não enxerga a sua ausência \\ndo que é necessário se ter feito para viver melhor …\\nSão tantos erros que passam despercebidos por você querer \\nfazer o melhor ou está fazendo o pior…\\nPessoas erram, nós erramos, mas o que seriam esses erros? \\nVeja à sua volta, veja você e pense: Como eu vivo? Como quero \\nSem título-1   121Sem título-1   121 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 152697,
      "chapter": 6,
      "page": 121,
      "segment_type": "page",
      "themes": {},
      "difficulty": 36.359336099585065,
      "complexity_metrics": {
        "word_count": 241,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 40.166666666666664,
        "avg_word_length": 4.531120331950207,
        "unique_word_ratio": 0.6224066390041494,
        "avg_paragraph_length": 241.0,
        "punctuation_density": 0.12863070539419086,
        "line_break_count": 23,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "melhor",
          "você",
          "como",
          "forma",
          "pessoas",
          "viver",
          "amanhã",
          "cada",
          "vida",
          "erros",
          "algo",
          "pois",
          "diante",
          "está",
          "sempre",
          "outros",
          "será",
          "volta",
          "fazer",
          "veja"
        ],
        "entities": [
          [
            "121",
            "CARDINAL"
          ],
          [
            "Nunca",
            "ORG"
          ],
          [
            "cada vida",
            "ORG"
          ],
          [
            "cada situação",
            "ORG"
          ],
          [
            "nem sempre",
            "PERSON"
          ],
          [
            "nem sempre",
            "PERSON"
          ],
          [
            "sua forma de ver",
            "PERSON"
          ],
          [
            "não sabemos",
            "ORG"
          ],
          [
            "dia de amanhã",
            "ORG"
          ],
          [
            "imagina -\\nmos",
            "PERSON"
          ]
        ],
        "readability_score": 78.5573305670816,
        "semantic_density": 0,
        "word_count": 241,
        "unique_words": 150,
        "lexical_diversity": 0.6224066390041494
      },
      "preservation_score": 1.8601434666416613e-05
    },
    {
      "id": 1,
      "text": "— 122 —viver? As pessoas à minha volta se encaixam como eu sonho \\nem viver?\\nComo você vai modificara vida de uma pessoa que viveu \\numa vida inteira acreditandoque estava vivendo o melhor \\nda vida?\\nPensa em uma linha de tempo, de cada profissão ou estilo \\nde vida…\\nComo um jogador de futebol viveu a vida toda para ser \\njogador?\\nMédico?\\nAdvogado?\\nLadrão?\\nVagabundo?\\nPlayboy?\\nVocê só sabe o que é viver a felicidade se você viver. Nós \\ntemos padrões de coisas que não são boas e temos padrões de \\ncoisas boas, temos um filtro diante do que é ser feliz, porém \\ncomo você irá modificar a sua vidacheia de “erros” diante da \\nfelicidade de viver a vida?\\nSeguimos as regras, vivemos em uma regra, é necessário ter -\\nmos regras, é necessário fazer o bem, é necessário ser o que te -\\nmos que ser dentro das regras que propomos a seguir…quan -\\ndo você foge das regras necessárias para ser feliz?\\nSem título-1   122Sem título-1   122 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 154170,
      "chapter": 6,
      "page": 122,
      "segment_type": "page",
      "themes": {},
      "difficulty": 22.941835357624832,
      "complexity_metrics": {
        "word_count": 171,
        "sentence_count": 13,
        "paragraph_count": 1,
        "avg_sentence_length": 13.153846153846153,
        "avg_word_length": 4.549707602339181,
        "unique_word_ratio": 0.6198830409356725,
        "avg_paragraph_length": 171.0,
        "punctuation_density": 0.13450292397660818,
        "line_break_count": 23,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "vida",
          "viver",
          "você",
          "como",
          "regras",
          "temos",
          "necessário",
          "viveu",
          "jogador",
          "felicidade",
          "padrões",
          "coisas",
          "boas",
          "diante",
          "feliz",
          "título",
          "pessoas",
          "minha",
          "volta",
          "encaixam"
        ],
        "entities": [
          [
            "122",
            "CARDINAL"
          ],
          [
            "como eu sonho \\n",
            "PERSON"
          ],
          [
            "Médico",
            "ORG"
          ],
          [
            "Advogado",
            "PRODUCT"
          ],
          [
            "Ladrão",
            "PERSON"
          ],
          [
            "Vagabundo",
            "PERSON"
          ],
          [
            "Playboy",
            "WORK_OF_ART"
          ],
          [
            "padrões de coisas que",
            "PERSON"
          ],
          [
            "padrões de \\ncoisas boas",
            "PERSON"
          ],
          [
            "Seguimos",
            "PERSON"
          ]
        ],
        "readability_score": 92.05816464237517,
        "semantic_density": 0,
        "word_count": 171,
        "unique_words": 106,
        "lexical_diversity": 0.6198830409356725
      },
      "preservation_score": 1.5664366034877146e-05
    },
    {
      "id": 1,
      "text": "— 123 —Às vezes temos que sair das regras para encontrarmos a fe -\\nlicidade em viver fora das nossas próprias regras, o “novo” tem \\nque ser experimentado, as antigas felicidades têmque ser revi -\\nvidas para nos mantermos fortes e confiantes em viver o me -\\nlhor de se viver uma vida!!!\\nNão fale isso, as pessoas não vão gostar…\\nEssa palavra não é legal para ser usada… A sua forma de \\nver cada palavra, cada frase, é de acordo com o quevocê viveu, \\na energia emitida pela palavra, a recepção pela mesma varia de \\num para outro!!! \\nExemplo: Coéviado na paz? quanto tempo irmãocomo vai \\no filho da puta do seu irmão?\\nAs palavras podem ser ditas, tudo depende da energia de \\ncomo você fala!!!\\nO mundo está se transformando em uma mentira de hipó -\\ncritas, onde tudoque os outros fazem e falam é errado, regras \\nque as pessoas seguem,que alguém colocou, que eu não sei \\nquem colocou como errado e certo, é o falso moralismo diante \\ndas palavras “certas”!!\\nSem título-1   123Sem título-1   123 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 155251,
      "chapter": 6,
      "page": 123,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 29.309234411996844,
      "complexity_metrics": {
        "word_count": 181,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 25.857142857142858,
        "avg_word_length": 4.602209944751381,
        "unique_word_ratio": 0.7182320441988951,
        "avg_paragraph_length": 181.0,
        "punctuation_density": 0.1712707182320442,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "regras",
          "viver",
          "palavra",
          "pessoas",
          "cada",
          "energia",
          "pela",
          "palavras",
          "como",
          "errado",
          "colocou",
          "título",
          "vezes",
          "temos",
          "sair",
          "encontrarmos",
          "licidade",
          "fora",
          "nossas",
          "próprias"
        ],
        "entities": [
          [
            "123",
            "CARDINAL"
          ],
          [
            "para encontrarmos",
            "PERSON"
          ],
          [
            "para nos mantermos",
            "PERSON"
          ],
          [
            "de se",
            "PERSON"
          ],
          [
            "varia de \\n",
            "PERSON"
          ],
          [
            "para outro",
            "PERSON"
          ],
          [
            "Coéviado",
            "GPE"
          ],
          [
            "quanto tempo",
            "PERSON"
          ],
          [
            "falam",
            "GPE"
          ],
          [
            "que eu não",
            "PERSON"
          ]
        ],
        "readability_score": 85.69076558800316,
        "semantic_density": 0,
        "word_count": 181,
        "unique_words": 130,
        "lexical_diversity": 0.7182320441988951
      },
      "preservation_score": 1.738829762295466e-05
    },
    {
      "id": 1,
      "text": "— 124 —“Excesso de regras está destruindo o viver melhor… ” Esta -\\nmos cada vez mais exigentes, em sermos algo que não temos \\nque ser. Se fazemos alguma coisa “fora da regra” que nos faz \\nfelizes isso afeta o ser correto diante de uma vida quetodos \\nimaginam ser correta…\\nSe somos uma imagem pública, não podemos fazer isso ou \\naquilo… se somos um esportista, não podemos fazer isso ou \\naquilo… se vivemos em algumas classes sociais, não podemos \\nfazer isso ou aquilo… se somos seres humanos querendo viver, \\nnão podemos viver isso ou aquilo…\\nHoje a exigência de “ser exemplo” para outros não é exem -\\nplo, é a destruição de um viver feliz. Sua felicidade não pode \\nser realizada pela discriminação diante do que a sociedade im -\\npôs, o quevocê tem que ser diante daquilo quevocê propôs a \\nser para ter uma vida melhor…\\nEstamos com tantas regras que temos uma sociedade que \\nsó vê como necessário para vida ser a melhor tenista e Osaka \\nem depressão… ser a melhor ginástica Simone Biles em de -\\npressão…\\nSer o melhor comediante Whindersson Nunes em de -\\npressão…\\nSer o melhor jogador de futebol do mundo Messi em de -\\npressão…\\nSerá mesmo que estamos à procura de viver melhor ou es -\\ntamos aprocura de sermos doutrinados para fazer um mundo \\nmelhor?\\nSem título-1   124Sem título-1   124 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 156398,
      "chapter": 6,
      "page": 124,
      "segment_type": "page",
      "themes": {},
      "difficulty": 35.335193133047206,
      "complexity_metrics": {
        "word_count": 233,
        "sentence_count": 4,
        "paragraph_count": 1,
        "avg_sentence_length": 58.25,
        "avg_word_length": 4.622317596566524,
        "unique_word_ratio": 0.5579399141630901,
        "avg_paragraph_length": 233.0,
        "punctuation_density": 0.060085836909871244,
        "line_break_count": 26,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "melhor",
          "viver",
          "isso",
          "podemos",
          "fazer",
          "aquilo",
          "diante",
          "vida",
          "somos",
          "pressão",
          "regras",
          "sermos",
          "temos",
          "sociedade",
          "quevocê",
          "estamos",
          "mundo",
          "título",
          "excesso",
          "está"
        ],
        "entities": [
          [
            "124",
            "CARDINAL"
          ],
          [
            "Excesso de regras",
            "ORG"
          ],
          [
            "mos cada",
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
          ],
          [
            "diante de uma vida",
            "PERSON"
          ],
          [
            "Se",
            "PERSON"
          ],
          [
            "não podemos",
            "ORG"
          ],
          [
            "não podemos",
            "ORG"
          ]
        ],
        "readability_score": 69.48830472103005,
        "semantic_density": 0,
        "word_count": 233,
        "unique_words": 130,
        "lexical_diversity": 0.5579399141630901
      },
      "preservation_score": 1.715418345667253e-05
    },
    {
      "id": 1,
      "text": "— 125 —Vemos um UFC com vários atletas em depressão, vemos \\numUFC que antes eram várias atletas de artes marciais dife -\\nrentes, hoje quem tem só uma especialidade de lutar? O que é \\no ser humano?\\nO que temos que ser como humano?Somos feito só de \\nregras?\\nTemos que ser felizes ou seguirmos uma regra de vida para \\nchegar a algum lugar na sociedade que imaginávamos ser me -\\nlhor do que a vivemos? O que é viver?\\nNós estamos no mundo em uma cobrança pela evolução \\ntão alta que quem não acompanha a evolução (natural) o \\nmundo te exclui…\\nExemplos: UFC – quase todos os lutadores são faixa preta \\nem várias modalidades.\\nFutebol – os jogadores de futebol vêm sendo doutrinados -\\ndesde criança a serem aquele tipo de jogador.\\nSeres humanos – quando eu era criança, para se ter acesso \\na uma educação, nós tínhamos que recorrer ao Aurélio, enci -\\nclopédia e o acesso a essas informações era caro para a maioria \\ndas famílias. Hoje temos um telefone quevocê não tem dúvida \\nsobre as suas próprias dúvidas.\\nRevolução – essa geração X já vive em uma revolução tec -\\nnológica, nós viemos de vestígios de uma revolução industrial, \\nSem título-1   125Sem título-1   125 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 157843,
      "chapter": 6,
      "page": 125,
      "segment_type": "page",
      "themes": {
        "filosofia": 60.0,
        "arte": 40.0
      },
      "difficulty": 25.982337662337663,
      "complexity_metrics": {
        "word_count": 210,
        "sentence_count": 11,
        "paragraph_count": 1,
        "avg_sentence_length": 19.09090909090909,
        "avg_word_length": 4.6380952380952385,
        "unique_word_ratio": 0.6904761904761905,
        "avg_paragraph_length": 210.0,
        "punctuation_density": 0.10476190476190476,
        "line_break_count": 23,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "temos",
          "revolução",
          "vemos",
          "atletas",
          "várias",
          "hoje",
          "quem",
          "humano",
          "mundo",
          "evolução",
          "futebol",
          "criança",
          "acesso",
          "título",
          "vários",
          "depressão",
          "umufc",
          "antes",
          "eram",
          "artes"
        ],
        "entities": [
          [
            "125",
            "CARDINAL"
          ],
          [
            "UFC",
            "ORG"
          ],
          [
            "depressão",
            "GPE"
          ],
          [
            "vemos \\numUFC",
            "PERSON"
          ],
          [
            "de artes marciais",
            "PERSON"
          ],
          [
            "hoje quem",
            "PERSON"
          ],
          [
            "Temos",
            "PERSON"
          ],
          [
            "de vida",
            "PERSON"
          ],
          [
            "evolução \\ntão alta que quem não",
            "ORG"
          ],
          [
            "Futebol",
            "GPE"
          ]
        ],
        "readability_score": 89.06311688311689,
        "semantic_density": 0,
        "word_count": 210,
        "unique_words": 145,
        "lexical_diversity": 0.6904761904761905
      },
      "preservation_score": 1.615387747346706e-05
    },
    {
      "id": 1,
      "text": "— 126 —não temos costume de trabalhar com a tecnologia a nosso fa -\\nvor (somos arcaicos para o mundo moderno).\\nTemos que evoluir, pois para você se manter na sua zona \\nde conforto, você tem que acompanhar a evolução natural \\ndo mundo.\\nEstude, crie, recrie, revise, reconstrua, adapte-se, profissiona -\\nlize-se e faça o melhor para você, pois a sua energia em se dar o \\nmelhor é diferente de você só executar, a sua determinação, seu \\nestímulo é contagiante, sinta a energia à sua volta, sinta as pes -\\nsoas e evolua para que outros possam evoluir junto com você.\\nEm uma viagem bem engraçada!!!\\nO homem toca punheta pensando em várias mulheres, po -\\nrém quando as mulheres resolvem se relacionar com vários ho -\\nmens, realizando o sonho dos homens, os homens não gostam \\nda ação das mulheres… Vai entender esse povo…\\nDeixa todo mundo ser o que quer ser, tanto o homem \\nquanto a mulher que querem ter um relacionamento de mo -\\nnogamia acho lindo, tanto quanto eu vejo os homens ou as \\nmulheres que querem viver do jeito que querem ser. Fique \\ncom quiser com responsabilidade, respeite o espaço de cada \\num, conheça as pessoas antes de se relacionar, viagem… Cada \\num faz o que quiser, não faltando com respeito a ninguém, vá \\nviver!!\\nSem título-1   126Sem título-1   126 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 159161,
      "chapter": 6,
      "page": 126,
      "segment_type": "page",
      "themes": {
        "ciencia": 56.52173913043479,
        "tecnologia": 43.47826086956522
      },
      "difficulty": 32.68703007518797,
      "complexity_metrics": {
        "word_count": 228,
        "sentence_count": 7,
        "paragraph_count": 1,
        "avg_sentence_length": 32.57142857142857,
        "avg_word_length": 4.671052631578948,
        "unique_word_ratio": 0.6885964912280702,
        "avg_paragraph_length": 228.0,
        "punctuation_density": 0.15789473684210525,
        "line_break_count": 23,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "mulheres",
          "mundo",
          "homens",
          "querem",
          "temos",
          "evoluir",
          "pois",
          "melhor",
          "energia",
          "sinta",
          "viagem",
          "homem",
          "relacionar",
          "tanto",
          "quanto",
          "viver",
          "quiser",
          "cada",
          "título"
        ],
        "entities": [
          [
            "126",
            "CARDINAL"
          ],
          [
            "arcaicos",
            "CARDINAL"
          ],
          [
            "para",
            "PRODUCT"
          ],
          [
            "Temos",
            "PERSON"
          ],
          [
            "para você se",
            "PERSON"
          ],
          [
            "manter na sua zona \\nde conforto",
            "ORG"
          ],
          [
            "reconstrua",
            "GPE"
          ],
          [
            "profissiona",
            "GPE"
          ],
          [
            "para você",
            "PERSON"
          ],
          [
            "evolua",
            "NORP"
          ]
        ],
        "readability_score": 82.31296992481202,
        "semantic_density": 0,
        "word_count": 228,
        "unique_words": 157,
        "lexical_diversity": 0.6885964912280702
      },
      "preservation_score": 2.4475571929495542e-05
    },
    {
      "id": 1,
      "text": "— 127 —Maior regra de vida que eu tenho!!!\\nNão faço com os outros o que eu não gosto que façam co -\\nmigo!!! Se alguém fizer alguma coisa não julgue, pois se ele \\nestá fazendo é bem provável que ele gosta que façam com ele \\nmesmo. Se ele tá fazendo algo que ele não gosta que seja feito \\ncom ele, como ele terá uma explicação plausível?\\nNós só sabemos explicar aquilo que vivemos, se vivemos \\nem uma visão de vida errada, temos que ensinar e mostrar o \\nmelhor caminho que passamos para que outros possam ver e \\nmelhorar o que nós mesmos estamosmelhorando!!!\\nEvolução é você evoluir junto e não sozinho.\\nNossos questionamentos são de acordo com o que \\nvivemos…\\nQuais são os maiores questionamentos que temos?\\nQuando observamos alguém, nós perguntamos o porquê?\\nNós nos questionamos de qual forma?\\nQue sorriso lindo…porque essa pessoa sorri tanto?Por -\\nque essa pessoa sorri, parece um idiota?Porque essa pessoa \\nsorri, desnecessário?São tantos porquês errados diante da si -\\ntuação que não percebemos que os nossos porquêsé que são \\nerrados …\\nSem título-1   127Sem título-1   127 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 160588,
      "chapter": 6,
      "page": 127,
      "segment_type": "page",
      "themes": {},
      "difficulty": 23.778815302344714,
      "complexity_metrics": {
        "word_count": 187,
        "sentence_count": 13,
        "paragraph_count": 1,
        "avg_sentence_length": 14.384615384615385,
        "avg_word_length": 4.903743315508021,
        "unique_word_ratio": 0.6524064171122995,
        "avg_paragraph_length": 187.0,
        "punctuation_density": 0.15508021390374332,
        "line_break_count": 21,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "vivemos",
          "essa",
          "pessoa",
          "sorri",
          "vida",
          "outros",
          "façam",
          "alguém",
          "fazendo",
          "gosta",
          "temos",
          "nossos",
          "questionamentos",
          "porque",
          "errados",
          "título",
          "maior",
          "regra",
          "tenho",
          "faço"
        ],
        "entities": [
          [
            "127",
            "CARDINAL"
          ],
          [
            "eu não gosto",
            "PERSON"
          ],
          [
            "Se",
            "PERSON"
          ],
          [
            "Se ele tá",
            "PERSON"
          ],
          [
            "que vivemos",
            "PERSON"
          ],
          [
            "se vivemos \\n",
            "PERSON"
          ],
          [
            "visão de vida errada",
            "ORG"
          ],
          [
            "mostrar o",
            "PERSON"
          ],
          [
            "que outros",
            "PERSON"
          ],
          [
            "mesmos",
            "PERSON"
          ]
        ],
        "readability_score": 91.3365693130399,
        "semantic_density": 0,
        "word_count": 187,
        "unique_words": 122,
        "lexical_diversity": 0.6524064171122995
      },
      "preservation_score": 1.6090028155390115e-05
    },
    {
      "id": 1,
      "text": "— 128 —Porque essa pessoa sorri tanto, como foi o trajeto até essa \\npessoa chegar a esse sorriso?\\nNão percebemos a quantidade de perguntas erradas que \\nfazemos diante das situações a qual vivemos, reveja as suas per -\\nguntas diante de viver melhor, diante de sorrir mais, diante de \\nse divertir mais…\\nToda ação tem um trajeto, nesse trajeto como chegamos até \\nessa “conclusão”?Não pense no ocorrido, não pense no mo -\\nmento, pense no contexto!!!\\nTodos nós temos dores proporcionaisà importância que da -\\nmos para o que achamos que é necessário para nós mesmos.\\nNão pense que a sua vida, seus acertos, seus erros, seu ins -\\ntinto, sua vida sãomelhores ou superiores de alguém. Veja, re -\\nveja, observe, admire e entenda a pessoa que está à sua frente, \\npois o seu trajeto até você chegar aondevocê está talvez tenha \\nsido mais fácil do que os demais ou pior que os demais. Não \\njulgue, não critique e sim ensine, pois estamos vivendo em \\numa vida que não sabemos viver!!!\\nQuando você era criança você era muito feliz!\\nQuando você chega entre 50 e 60 anos (estatística padrão \\nda idade) você vive muito feliz!\\nQual é a semelhança?\\nSem título-1   128Sem título-1   128 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 161824,
      "chapter": 6,
      "page": 128,
      "segment_type": "page",
      "themes": {},
      "difficulty": 25.91923076923077,
      "complexity_metrics": {
        "word_count": 208,
        "sentence_count": 11,
        "paragraph_count": 1,
        "avg_sentence_length": 18.90909090909091,
        "avg_word_length": 4.730769230769231,
        "unique_word_ratio": 0.6634615384615384,
        "avg_paragraph_length": 208.0,
        "punctuation_density": 0.16826923076923078,
        "line_break_count": 22,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "trajeto",
          "diante",
          "pense",
          "essa",
          "pessoa",
          "mais",
          "vida",
          "como",
          "chegar",
          "qual",
          "viver",
          "seus",
          "veja",
          "está",
          "pois",
          "demais",
          "quando",
          "muito",
          "feliz"
        ],
        "entities": [
          [
            "128",
            "CARDINAL"
          ],
          [
            "erradas que \\n",
            "PERSON"
          ],
          [
            "fazemos diante das situações",
            "PERSON"
          ],
          [
            "diante de sorrir mais",
            "PERSON"
          ],
          [
            "diante de \\nse",
            "PERSON"
          ],
          [
            "conclusão”?Não",
            "PERSON"
          ],
          [
            "que achamos",
            "ORG"
          ],
          [
            "que",
            "CARDINAL"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "nós mesmos",
            "PERSON"
          ]
        ],
        "readability_score": 89.12622377622378,
        "semantic_density": 0,
        "word_count": 208,
        "unique_words": 138,
        "lexical_diversity": 0.6634615384615384
      },
      "preservation_score": 2.2474959963084605e-05
    },
    {
      "id": 1,
      "text": "— 129 —Sentir conforto em viver e não se cobrar em viver algo que \\nvocê não sabe o que é viver!\\nQuando você é novo você não tem problema. Quando você \\nfica mais velho, você já passou por tanto problema que deixou \\nde se importar com os mesmos problemas.\\nO viver melhor é evitar ter problemas, se você não con -\\nsegue enxergar o que lhe dá problema diante da sua própria \\nvida, como alguém vai resolver os seus problemas?\\nNão reclame da vida que está vivendo, use como solução de \\nproblemas futuros, previna o pior antes que aconteça o pior…\\nviver é simples, a dificuldade de viver é você querer viver o \\n“melhor” da vida… Queremos ter carros de um milhão sem \\nnem imaginar a dificuldade que é para ter.\\nQueremos viajar o mundo sem saber a dificuldade que é \\npara ter.\\nQueremos morar em casas gigantes sem saber a dificuldade \\nque é para ter.\\nO ter uma vida é o melhor de viver uma vida quevocê ima -\\ngina ser melhor que algo que não é como você pensa que é. \\nViva a sua vida dentro do que é melhor, dentro da sua própria \\nvida. Faça você a história da sua própria felicidade, não viva a \\nfelicidade dos outros, viva a sua felicidade!!!\\nSem título-1   129Sem título-1   129 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 163148,
      "chapter": 6,
      "page": 129,
      "segment_type": "page",
      "themes": {},
      "difficulty": 25.786139421117,
      "complexity_metrics": {
        "word_count": 223,
        "sentence_count": 11,
        "paragraph_count": 1,
        "avg_sentence_length": 20.272727272727273,
        "avg_word_length": 4.36322869955157,
        "unique_word_ratio": 0.5336322869955157,
        "avg_paragraph_length": 223.0,
        "punctuation_density": 0.11210762331838565,
        "line_break_count": 22,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "viver",
          "vida",
          "melhor",
          "problemas",
          "dificuldade",
          "problema",
          "própria",
          "como",
          "queremos",
          "viva",
          "felicidade",
          "algo",
          "quando",
          "pior",
          "saber",
          "dentro",
          "título",
          "sentir",
          "conforto"
        ],
        "entities": [
          [
            "129",
            "CARDINAL"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "novo você não",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "fica mais velho",
            "PERSON"
          ],
          [
            "já passou",
            "PERSON"
          ],
          [
            "tanto",
            "GPE"
          ],
          [
            "mesmos problemas",
            "PERSON"
          ],
          [
            "Queremos",
            "PERSON"
          ],
          [
            "nem imaginar",
            "PERSON"
          ]
        ],
        "readability_score": 88.5546677537709,
        "semantic_density": 0,
        "word_count": 223,
        "unique_words": 119,
        "lexical_diversity": 0.5336322869955157
      },
      "preservation_score": 1.545153497462067e-05
    },
    {
      "id": 1,
      "text": "— 130 —A sua absorção de ver a vida é diferente da minha, o meu \\nolhar, o seu olhar diante dos acontecimentos à sua volta acon -\\ntecede acordo como você enxerga a sua vida…quandovocê vê \\nalgo, você absorve a sua própria“necessidade” , quando conver -\\nsar com alguém pergunte o porquê de ele pensar daquela for -\\nma. Assim como você pensa que a sua forma está certa diante \\nda sua própria vida, o outro também está certo dentro da sua \\nprópria vida.\\nNossos erros e acertos são aprendizados para se planejar e \\nviver melhor o amanhã, não são todos que gostam de comer \\ncarne, não são todos que gostam da cor branca, não são todos \\nque entendem o quevocê fala, pois não são todos que estão \\nte acompanhando no seu dia a dia… Sua forma de agir não \\né igual aquela da sua infância, sua forma de agir não é igual à \\nsua adolescência, sua forma de agir não é igual da faculdade, \\nsua forma de agir não é igual do seu primeiro emprego, sua \\nforma de agir não é igual a cada meio quevocê viveu!!!\\nViva e entenda que a vida é feita de se adaptar e não es -\\nquecendo do que passou, e sim o que passou, foi ensinamento \\npara você ser uma melhor versão de si próprio, para todos que \\npassaram em sua vida!!!\\nSem título-1   130Sem título-1   130 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 164479,
      "chapter": 6,
      "page": 130,
      "segment_type": "page",
      "themes": {},
      "difficulty": 34.61974789915966,
      "complexity_metrics": {
        "word_count": 238,
        "sentence_count": 5,
        "paragraph_count": 1,
        "avg_sentence_length": 47.6,
        "avg_word_length": 4.264705882352941,
        "unique_word_ratio": 0.5336134453781513,
        "avg_paragraph_length": 238.0,
        "punctuation_density": 0.11764705882352941,
        "line_break_count": 21,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "vida",
          "forma",
          "todos",
          "agir",
          "igual",
          "você",
          "própria",
          "olhar",
          "diante",
          "como",
          "está",
          "melhor",
          "gostam",
          "quevocê",
          "passou",
          "título",
          "absorção",
          "diferente",
          "minha",
          "acontecimentos"
        ],
        "entities": [
          [
            "130",
            "CARDINAL"
          ],
          [
            "quandovocê",
            "GPE"
          ],
          [
            "quando conver",
            "PERSON"
          ],
          [
            "porquê de ele",
            "PERSON"
          ],
          [
            "outro também está certo dentro da sua",
            "PERSON"
          ],
          [
            "para se planejar",
            "PERSON"
          ],
          [
            "que gostam de comer",
            "PERSON"
          ],
          [
            "que gostam da cor",
            "PERSON"
          ],
          [
            "entendem",
            "PERSON"
          ],
          [
            "quevocê fala",
            "GPE"
          ]
        ],
        "readability_score": 74.92058823529412,
        "semantic_density": 0,
        "word_count": 238,
        "unique_words": 127,
        "lexical_diversity": 0.5336134453781513
      },
      "preservation_score": 1.6983918608467345e-05
    },
    {
      "id": 1,
      "text": "— 131 —O mundo é aquilo que você tem!!! \\nAnalogia:\\nElon Musk te oferece um terreno que não tem água, tudo -\\nquevocê planta não cresce, cheio de relevo. No meio do nada, \\nte falandoque esse terreno custa R$ 500 mil com uma projeção \\nfutura para daqui a 10 anos valer 1 milhão, você compraria?\\nVem o Joãozinho malarrumado, do interior,que tem um \\nterreno de herança com uma complicação de escritura que \\ncusta 50 mil para resolver, porém esse terreno tem uma nas -\\ncente natural, terra plana com poucas elevações e é um terreno \\nótimo para se plantar e cultivar qualquer tipo de alimento cus -\\ntando R$ 350 mil e ele não sabe quanto esse mesmo terreno \\nvale, porém você não o conhece e a imagem dele não te pas -\\nsou mais confiança do que a do Elon Musk. Você investiria em \\nqual terreno, no do Elon Musk que te deu uma visão futura \\nsem lógica ou no Joãozinho quevocê não confia na imagem \\nnem na história dele por não te passar confiança?\\nObservação: os dois terrenos são do mesmo tamanho!!\\nEm nossas vidas é assim, para você ter acesso a uma me -\\nlhor qualidade de vida, você precisa morar em algum lugar de \\nconfiança, ter um carro que passa confiança, uma roupa que \\npassa confiança, uma imagem que passa confiança, um falar \\nque passa confiança. Nem sempre o ser de confiança te torna \\numa pessoa de confiança… Temos tantos pré-conceitos sobre \\nalgo que não imaginamos a grandeza dos nossos próprios pre -\\nconceitos!!!\\nSem título-1   131Sem título-1   131 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 165869,
      "chapter": 6,
      "page": 131,
      "segment_type": "page",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 35.146950710108605,
      "complexity_metrics": {
        "word_count": 266,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 29.555555555555557,
        "avg_word_length": 4.56390977443609,
        "unique_word_ratio": 0.6015037593984962,
        "avg_paragraph_length": 266.0,
        "punctuation_density": 0.13157894736842105,
        "line_break_count": 26,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "confiança",
          "terreno",
          "você",
          "passa",
          "elon",
          "musk",
          "esse",
          "imagem",
          "quevocê",
          "custa",
          "futura",
          "joãozinho",
          "porém",
          "mesmo",
          "dele",
          "conceitos",
          "título",
          "mundo",
          "aquilo",
          "analogia"
        ],
        "entities": [
          [
            "131",
            "CARDINAL"
          ],
          [
            "Elon Musk",
            "PERSON"
          ],
          [
            "nada",
            "GPE"
          ],
          [
            "500",
            "CARDINAL"
          ],
          [
            "futura para daqui",
            "PERSON"
          ],
          [
            "10 anos valer 1 milhão",
            "QUANTITY"
          ],
          [
            "50",
            "CARDINAL"
          ],
          [
            "350",
            "CARDINAL"
          ],
          [
            "porém você não o conhece e",
            "ORG"
          ],
          [
            "sou mais",
            "PERSON"
          ]
        ],
        "readability_score": 83.8530492898914,
        "semantic_density": 0,
        "word_count": 266,
        "unique_words": 160,
        "lexical_diversity": 0.6015037593984962
      },
      "preservation_score": 2.5454594806675367e-05
    },
    {
      "id": 1,
      "text": "— 132 —Para você fazer melhor para a maioria, a minoria não pode \\nser beneficiada pelos seus próprios erros…\\nQuando ficamos adultos temos obrigações perante outras \\npessoas, quais são as pessoas as quaisvocê tem obrigações?\\nSe ajudarmos muito uma pessoa que “não quer ser ajuda -\\nda” , até que ponto eu tenho que me propor a ajudar essa mes -\\nma pessoa?\\nEu ajudando essa pessoa até que ponto irei ter disponibili -\\ndade?Até que ponto a preocupação não irá me preocupar?Até \\nque ponto ele tem que ser mais beneficiado que meu filho, -\\nminha mãe, meus irmãos, meus amigos que merecem mais do \\nque o outro que não está fazendo por merecer?\\nInimigos não vão te fazer mal, pois você não se preocupa \\ncom ele… Só quem te faz malsão pessoas quevocê ama por \\nvocê se preocupar com ele…\\nSe afastar não é falta de amor, se afastar é sabedoria em dar \\namor para quem realmente precisa!!!\\nSe afastar de uma pessoa que não vê o quanto ela mesma \\nestá se prejudicando é ensiná-la a enxergar a sua ausência dian -\\nte da dificuldade. Por você sempre ajudá-la, ela não entenderá \\no motivo por estar passando pelo o que está passando…\\nA sua necessidade mental de estar bem consigo mesmo \\né necessário para fazer bem para outros, até que ponto o fa -\\nzer bem para outros não está afetando o seu próprio estado \\nmental?\\nSem título-1   132Sem título-1   132 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 167487,
      "chapter": 6,
      "page": 132,
      "segment_type": "page",
      "themes": {},
      "difficulty": 30.08875283446712,
      "complexity_metrics": {
        "word_count": 245,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 27.22222222222222,
        "avg_word_length": 4.555102040816327,
        "unique_word_ratio": 0.6244897959183674,
        "avg_paragraph_length": 245.0,
        "punctuation_density": 0.09795918367346938,
        "line_break_count": 25,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "ponto",
          "você",
          "pessoa",
          "está",
          "fazer",
          "pessoas",
          "afastar",
          "obrigações",
          "essa",
          "preocupar",
          "mais",
          "meus",
          "quem",
          "amor",
          "passando",
          "mental",
          "outros",
          "título",
          "melhor",
          "maioria"
        ],
        "entities": [
          [
            "132",
            "CARDINAL"
          ],
          [
            "ser beneficiada pelos",
            "ORG"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "Se ajudarmos muito",
            "PERSON"
          ],
          [
            "ser ajuda -\\nda",
            "PERSON"
          ],
          [
            "eu",
            "PERSON"
          ],
          [
            "Eu",
            "PERSON"
          ],
          [
            "essa pessoa até",
            "ORG"
          ],
          [
            "merecem mais",
            "PERSON"
          ],
          [
            "Inimigos",
            "ORG"
          ]
        ],
        "readability_score": 85.02235827664398,
        "semantic_density": 0,
        "word_count": 245,
        "unique_words": 153,
        "lexical_diversity": 0.6244897959183674
      },
      "preservation_score": 2.0218950724365884e-05
    },
    {
      "id": 1,
      "text": "— 133 —Não existe sorte…\\nFoi Deus quem enviou…\\nExemplos:\\nEstou caminhando na rua, pisei na merda de vaca… agri -\\ncultor precisando de adubo.\\nEstou caminhando na rua, pisei na merda de vaca…Sorte e \\nazar são as mesmas coisas.\\nSorte ou azar é uma palavra referência proporcional de \\ncada indivíduo… Sorte é usada em um termo bom para cada \\npessoa e azar é o mesmo termo para o lado ruim.Sorte ou azar \\nsão palavras usadas igual você usa qualquer outra palavra.\\nUsar palavras com valor de energia boa é necessário, temos \\ntantas palavras com estereótipos raciais, culturais, regionais, fi -\\nlosóficos, estruturais, espirituais etc.Que “não percebemos” o \\nquanto é necessário a forma que falamos em cada meio em \\nque vivemos.\\nSe você é um agricultor que crê em Deus, quandovocê pisar \\nna merda precisando de adubo, o que irá falar?\\nSe você é uma pessoa que crê em Deus,e pisar na merda,o \\nque irá falar?\\nSe um ateu pisar na merda,o que ele irá falar?\\nSe qualquer um dos três ganhar na Mega Senna, o que \\nvão dizer?\\nO valor da palavra é relativo para cada pessoa, e usar pala -\\nvras com boas energias nos traz boa energia proporcional ao \\nmeio em que vivemos!!!\\nSem título-1   133Sem título-1   133 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 168982,
      "chapter": 6,
      "page": 133,
      "segment_type": "page",
      "themes": {},
      "difficulty": 26.893457943925235,
      "complexity_metrics": {
        "word_count": 214,
        "sentence_count": 12,
        "paragraph_count": 1,
        "avg_sentence_length": 17.833333333333332,
        "avg_word_length": 4.691588785046729,
        "unique_word_ratio": 0.5794392523364486,
        "avg_paragraph_length": 214.0,
        "punctuation_density": 0.1542056074766355,
        "line_break_count": 26,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "sorte",
          "merda",
          "azar",
          "cada",
          "deus",
          "palavra",
          "pessoa",
          "palavras",
          "você",
          "pisar",
          "falar",
          "estou",
          "caminhando",
          "pisei",
          "vaca",
          "precisando",
          "adubo",
          "proporcional",
          "termo",
          "qualquer"
        ],
        "entities": [
          [
            "133",
            "CARDINAL"
          ],
          [
            "Foi Deus",
            "PERSON"
          ],
          [
            "merda de vaca",
            "PERSON"
          ],
          [
            "merda de vaca",
            "PERSON"
          ],
          [
            "Sorte",
            "PRODUCT"
          ],
          [
            "mesmas coisas",
            "PERSON"
          ],
          [
            "referência proporcional de \\ncada",
            "PERSON"
          ],
          [
            "Sorte",
            "PRODUCT"
          ],
          [
            "para cada",
            "PERSON"
          ],
          [
            "mesmo",
            "ORG"
          ]
        ],
        "readability_score": 89.67585669781931,
        "semantic_density": 0,
        "word_count": 214,
        "unique_words": 124,
        "lexical_diversity": 0.5794392523364486
      },
      "preservation_score": 2.324115178000794e-05
    },
    {
      "id": 1,
      "text": "— 134 —Tempo é dinheiro…\\nTempo é dinheiro no tempo que estou dando para o meu \\ntrabalho.\\nPrincipal motivo da vida é ter tempo para viver a vida, e \\ndentro desse tempo que eu tenho para viver a vida, minha \\nmaior meta é ser feliz!!!\\nO que você é: um vendedor ou um realizador?\\nVendedor – aquele que vende.\\nVendedor pensa no lucro acima da necessidade do cliente. \\nEle vende aquilo que tem que vender, sem pensar no que é \\nnecessário para o cliente e sim necessário para a empresa ou \\npara si próprio!!!\\nRealizador –aquele que realiza (algo), revelando capacidade \\npara tal; empreendedor.\\nComo o próprio significado já diz, o realizador é realizado, \\npois como você vai ser algo quevocê, não é?\\nRealizador pergunta ao cliente o que ele precisa… Ele en -\\ntende o que é necessário além do lucro para o cliente, reali -\\nzador não vê qual é o melhor material, ele entende da neces -\\nsidade do cliente sem pensar no seu lucro, não vê se você é \\nrico ou pobre, ele entende o que é necessário para lhe atender \\nmelhor dentro daquilo quevocênecessita… realizador é aquele \\nSem título-1   134Sem título-1   134 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 170334,
      "chapter": 6,
      "page": 134,
      "segment_type": "page",
      "themes": {},
      "difficulty": 27.37211111111111,
      "complexity_metrics": {
        "word_count": 200,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 22.22222222222222,
        "avg_word_length": 4.62,
        "unique_word_ratio": 0.595,
        "avg_paragraph_length": 200.0,
        "punctuation_density": 0.145,
        "line_break_count": 22,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "tempo",
          "realizador",
          "cliente",
          "necessário",
          "vida",
          "você",
          "vendedor",
          "aquele",
          "lucro",
          "dinheiro",
          "viver",
          "dentro",
          "vende",
          "pensar",
          "próprio",
          "algo",
          "como",
          "melhor",
          "entende",
          "título"
        ],
        "entities": [
          [
            "134",
            "CARDINAL"
          ],
          [
            "dando",
            "ORG"
          ],
          [
            "que eu",
            "PERSON"
          ],
          [
            "Vendedor",
            "PERSON"
          ],
          [
            "Vendedor",
            "ORG"
          ],
          [
            "acima da",
            "PERSON"
          ],
          [
            "Ele",
            "PERSON"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "Ele",
            "PERSON"
          ]
        ],
        "readability_score": 87.50288888888889,
        "semantic_density": 0,
        "word_count": 200,
        "unique_words": 119,
        "lexical_diversity": 0.595
      },
      "preservation_score": 1.779267663744198e-05
    },
    {
      "id": 1,
      "text": "— 135 —que realiza sonhos que não são seus, porém quandovocê sente \\na realização do cliente,você se sente realizado como se fosse \\nseu próprio sonho.\\nVocê gostaria de adquirir um serviço, produto, seja lá o que -\\nvocê quiser adquirir e não ficar satisfeito?O quevocê quer para \\no seu empreendimento, compradores ou pessoas realizadas?\\nOlhe para si mesmo, sinta a energia do seu cliente perante a \\nsua necessidade. Você entenderá que a vida não é feita de sorte \\ne sim de realizações!!!\\nTem dias que temos quenos perder para nos acharmos…\\nTem dias que precisamos sair do conforto para lembrar o \\nque é viver…\\nTem dias que não sabemos o motivo de tantos problemas \\nem nossa vida, pois esquecemos de viver…\\nTem dias e dias, tem dias tranquilos, tem dias turbulentos, \\ntem dias quevocêtá cansado e tem dias que nunca mais vão se \\nrepetir…\\nViva o “desnecessário” para conseguir ter vontade de viver o \\nque é necessário.\\nNós sempre estamos nos obrigando a viver uma vida, que \\nnem sabemos a real proporção dessa mesma vida que estamos \\nvivendo, são tantos malefícios que esquecemos que temos o \\nlado do benefício de viver com pessoas quevocê ama.\\nSem título-1   135Sem título-1   135 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 171592,
      "chapter": 6,
      "page": 135,
      "segment_type": "page",
      "themes": {},
      "difficulty": 29.223399014778323,
      "complexity_metrics": {
        "word_count": 203,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 25.375,
        "avg_word_length": 4.911330049261084,
        "unique_word_ratio": 0.6059113300492611,
        "avg_paragraph_length": 203.0,
        "punctuation_density": 0.12315270935960591,
        "line_break_count": 23,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "dias",
          "viver",
          "você",
          "vida",
          "sente",
          "cliente",
          "adquirir",
          "quevocê",
          "pessoas",
          "temos",
          "sabemos",
          "tantos",
          "esquecemos",
          "estamos",
          "título",
          "realiza",
          "sonhos",
          "seus",
          "porém",
          "quandovocê"
        ],
        "entities": [
          [
            "135",
            "CARDINAL"
          ],
          [
            "fosse \\nseu próprio",
            "ORG"
          ],
          [
            "Você gostaria de",
            "ORG"
          ],
          [
            "quevocê quer",
            "ORG"
          ],
          [
            "para \\n",
            "PERSON"
          ],
          [
            "Olhe",
            "ORG"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "Viva",
            "ORG"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "Nós sempre estamos",
            "ORG"
          ]
        ],
        "readability_score": 85.83910098522168,
        "semantic_density": 0,
        "word_count": 203,
        "unique_words": 123,
        "lexical_diversity": 0.6059113300492611
      },
      "preservation_score": 1.5664366034877146e-05
    },
    {
      "id": 1,
      "text": "— 136 —Nos obrigamos tanto a trabalhar, conquistar, cuidar, metas, \\nobrigações que esquecemos que o simples da vida em viver o \\nmelhor da vida é um abraço de quem você ama, conversar com \\nquem você ama, brincar com quem você ama, beijar quem \\nvocê ama.O melhor da vida não está só na sua obrigação, o me -\\nlhor da vida está sempre àsua volta, a felicidade da vida está no \\nsimples do viver, a felicidade da vida está nas pessoas quevocê \\nesqueceu que as ama…\\nViva com pessoas quevocê ama que o resto da vida é o resto.\\nPorquevocê se cobra uma vida quenão está vivendo?\\nDepressão!!\\nO que ocasiona a depressão? Expectativa (gerada por si pró -\\nprio) ou caso do acaso (fatalidades, morte, doenças etc.).\\nComo você sabe que está em depressão?\\nOs seus porquês que dizem o porquê e as suas certezas …\\n Como assim?\\nAs suas perguntas diante da sua própria vid são respostas de \\ncomplexo de inferioridade.\\nE as suas certezas também são de complexo de infe -\\nrioridade.\\n Exemplos: Porque eu vivo?\\nPorque aconteceu isso comigo?\\nEu sou uma merda de pessoa.\\nNão aguento mais viver.\\nSem título-1   136Sem título-1   136 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 172928,
      "chapter": 6,
      "page": 136,
      "segment_type": "page",
      "themes": {},
      "difficulty": 30.7105,
      "complexity_metrics": {
        "word_count": 200,
        "sentence_count": 16,
        "paragraph_count": 1,
        "avg_sentence_length": 12.5,
        "avg_word_length": 4.66,
        "unique_word_ratio": 0.635,
        "avg_paragraph_length": 200.0,
        "punctuation_density": 0.165,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "vida",
          "está",
          "você",
          "quem",
          "viver",
          "depressão",
          "suas",
          "simples",
          "melhor",
          "felicidade",
          "pessoas",
          "quevocê",
          "resto",
          "como",
          "certezas",
          "complexo",
          "porque",
          "título",
          "obrigamos",
          "tanto"
        ],
        "entities": [
          [
            "136",
            "CARDINAL"
          ],
          [
            "cuidar",
            "ORG"
          ],
          [
            "abraço de quem você ama",
            "PERSON"
          ],
          [
            "beijar quem \\nvocê ama",
            "PERSON"
          ],
          [
            "Viva",
            "ORG"
          ],
          [
            "Porquevocê",
            "PERSON"
          ],
          [
            "Depressão",
            "GPE"
          ],
          [
            "ocasiona",
            "GPE"
          ],
          [
            "depressão",
            "GPE"
          ],
          [
            "Expectativa",
            "ORG"
          ]
        ],
        "readability_score": 92.352,
        "semantic_density": 0,
        "word_count": 200,
        "unique_words": 127,
        "lexical_diversity": 0.635
      },
      "preservation_score": 2.2474959963084605e-05
    },
    {
      "id": 1,
      "text": "— 137 —Tem pessoas, por não conseguirem resolver essas questões, \\nque entram em fuga, seja ela nas drogas, em comer, academia…\\nNos excessos de sua própria vida por não conseguir admi -\\nnistrar a sua própria vida.\\nComo posso melhorar?\\nA melhora só parte quandovocê aceita o viver.\\nComo assim?Qual é o sentido da vida se não for o viver? Se \\nvocê não consegue enxergar que o simples da vida é viver, eu \\nfalo quevocê precisa se enxergar para poder ver o que é viver…\\nAnalogia – estamos dentro de um poço, dentro desse poço \\nestamos com água até o pescoço. Nós enxergamos a saída, po -\\nrém as dificuldades não deixam que saiamos, tentamos, tenta -\\nmos e sempre falhamos, ficando cansados de viver… se pensar -\\nmos por uma outra perspectiva, nós começamos a imaginar \\nde onde brota a água? Será que abaixo de nós tem um córrego, \\ntem um rio, tem um caminho com uma maior dificuldade? \\nPorém,eu tenho que ir, pois lá é minha única chance.\\nAssim eu vejo, se você não se aprofundar em si próprio, se \\nvocê não encarar os seus problemas, o poço vai te cansar tan -\\ntoquevocê vai desistir (morte). Não tenha medo de se apro -\\nfundar na sua vida, pois você já viveu tudoque você já passou, \\njá aconteceu, aceite, aprenda e corrija, pois você é único, você \\né exclusivo e nada e nem ninguém fará melhor que você para \\nvocê mesmo.\\nSem título-1   137Sem título-1   137 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 174192,
      "chapter": 6,
      "page": 137,
      "segment_type": "page",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 27.849402390438247,
      "complexity_metrics": {
        "word_count": 251,
        "sentence_count": 12,
        "paragraph_count": 1,
        "avg_sentence_length": 20.916666666666668,
        "avg_word_length": 4.49800796812749,
        "unique_word_ratio": 0.6533864541832669,
        "avg_paragraph_length": 251.0,
        "punctuation_density": 0.1593625498007968,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "vida",
          "viver",
          "poço",
          "pois",
          "própria",
          "como",
          "assim",
          "enxergar",
          "estamos",
          "dentro",
          "água",
          "título",
          "pessoas",
          "conseguirem",
          "resolver",
          "essas",
          "questões",
          "entram",
          "fuga"
        ],
        "entities": [
          [
            "137",
            "CARDINAL"
          ],
          [
            "por não conseguirem",
            "ORG"
          ],
          [
            "ela nas drogas",
            "PERSON"
          ],
          [
            "sua própria",
            "ORG"
          ],
          [
            "melhora",
            "GPE"
          ],
          [
            "quandovocê aceita",
            "PERSON"
          ],
          [
            "sentido da vida se não",
            "PERSON"
          ],
          [
            "eu",
            "PERSON"
          ],
          [
            "precisa se enxergar para",
            "PERSON"
          ],
          [
            "Analogia",
            "GPE"
          ]
        ],
        "readability_score": 88.19226427622841,
        "semantic_density": 0,
        "word_count": 251,
        "unique_words": 164,
        "lexical_diversity": 0.6533864541832669
      },
      "preservation_score": 2.656131632000908e-05
    },
    {
      "id": 1,
      "text": "— 138 —Ao decorrer da vida passamos por erros, falhas e falta de \\nnecessidade de ter aquilo em sua vida. Eu aprendi a direcionar \\nmeu tempo para amanhã, na necessidade de evoluir para um \\nbem necessário da minha felicidade (nunca abri um sorriso \\nsozinho).\\nComo assim?\\nDurante a vida eu desisti de ver sobre …\\nPolítica – Nós somos tão padronizadosque a nossa política \\nvirou um ciclo vicioso eterno, pois tudoque estamos vivendo \\nhoje já vivemos no passado. Todos os conflitos, disputas, inte -\\nresses pessoais maioresque um interesse coletivo, nós vemos \\nos erros e insistimos nos erros, em sempre colocar os mesmos \\npolíticos, o mesmo padrão de pensamento diante do povo (es -\\ntudo Egito Antigo, mongóis, Roma e etc.).\\nPessoas – pessoas que não conseguem reconhecer suas pró -\\nprias falhas, pessoas que sempre estão reclamando, pessoas que \\nnão veem que estão destruindo a sua própria vida…\\nTelevisão aberta – você tem uma empresa, você quer o bem \\ndela, o quevocê faria para melhor atender o seu público? Meu \\nponto de vista de canal aberto é você ser doutrinado para o \\nmeupróprio bem. Não vejo canal aberto, vejo que é necessário \\npara a minha evolução (jogo de futebol).\\nAlgumas redes sociais – semelhante à televisão, temos tanta \\ngente em disputa por algo que esquecemque a sua disputa é \\nconsigo mesmo.\\nSem título-1   138Sem título-1   138 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 175706,
      "chapter": 6,
      "page": 138,
      "segment_type": "page",
      "themes": {},
      "difficulty": 26.985652173913046,
      "complexity_metrics": {
        "word_count": 230,
        "sentence_count": 11,
        "paragraph_count": 1,
        "avg_sentence_length": 20.90909090909091,
        "avg_word_length": 4.952173913043478,
        "unique_word_ratio": 0.7260869565217392,
        "avg_paragraph_length": 230.0,
        "punctuation_density": 0.13043478260869565,
        "line_break_count": 25,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "vida",
          "pessoas",
          "erros",
          "você",
          "falhas",
          "necessidade",
          "necessário",
          "minha",
          "política",
          "sempre",
          "mesmo",
          "estão",
          "televisão",
          "canal",
          "aberto",
          "vejo",
          "disputa",
          "título",
          "decorrer",
          "passamos"
        ],
        "entities": [
          [
            "138",
            "CARDINAL"
          ],
          [
            "Eu",
            "PERSON"
          ],
          [
            "para amanhã",
            "PERSON"
          ],
          [
            "necessário da minha",
            "PERSON"
          ],
          [
            "Durante",
            "PERSON"
          ],
          [
            "vida eu desisti de ver sobre",
            "PERSON"
          ],
          [
            "Política",
            "LOC"
          ],
          [
            "tudoque estamos",
            "PERSON"
          ],
          [
            "hoje já vivemos",
            "PERSON"
          ],
          [
            "mesmos \\npolíticos",
            "PERSON"
          ]
        ],
        "readability_score": 88.05980237154151,
        "semantic_density": 0,
        "word_count": 230,
        "unique_words": 167,
        "lexical_diversity": 0.7260869565217392
      },
      "preservation_score": 2.287933897757192e-05
    },
    {
      "id": 1,
      "text": "— 139 —WhatsApp grupo – os grupos de WhatsApp têm muita \\nfalsidade, você achar um grupo decente é muito difícil, pois \\nos grupos têm aquela pessoa quetodo mundo fala mal, tem \\npessoas que fazem subgrupo do grupo, tem conversas, brigas, \\ntraições, ostentação, inveja…\\nSair para ficar com alguém – é tanto malefício para se ter \\nalguém que o benefício de se viver o momento com os seus \\namigos e família vale muito mais que perder o tempo para fi -\\ncar com alguém quevocênem conhece.\\nNa vida se você não reconhecer o que não te faz bem, a vida \\nsempre estará voltandoao quevocê não sabe o que quer…\\nViva, sinta, trabalhe, conquiste, evolua para você ter aquilo \\nquevocê quer de volta para si próprio!\\nMinha vida, meu tempo é um só, se eu não souber fazer \\npor mim o que é necessário dentro do tempo de vida que eu \\ntenho, eu estou perdendo meu tempo de vida, pois tudo aqui -\\nlo que vivo é perda de tempo no trajeto até a morte. Como \\nvocê quer perder tempo de vida até a sua morte?\\nO que é viver a vida?\\nPara responder essa pergunta, temos que ver quantas per -\\nguntas giram em torno dessa pergunta…\\nO viver a vida, a meu ver, é você viver no meio de pessoas \\nque te façam evoluir sentimentalmente e monetariamente.\\nComo assim?Conforme vamos melhorando de vida, seja \\naonde for, no tráfico, na polícia, no hospital, na fábrica etc.\\nCriamos confiança com pessoas necessárias para melhor vi -\\nvermos a vida, e com isso nós aumentamosnossos valores \\nSem título-1   139Sem título-1   139 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 177213,
      "chapter": 6,
      "page": 139,
      "segment_type": "page",
      "themes": {},
      "difficulty": 31.476055760557607,
      "complexity_metrics": {
        "word_count": 271,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 30.11111111111111,
        "avg_word_length": 4.549815498154982,
        "unique_word_ratio": 0.6051660516605166,
        "avg_paragraph_length": 271.0,
        "punctuation_density": 0.14022140221402213,
        "line_break_count": 27,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "vida",
          "tempo",
          "você",
          "viver",
          "grupo",
          "pessoas",
          "alguém",
          "quer",
          "whatsapp",
          "grupos",
          "muito",
          "pois",
          "perder",
          "quevocê",
          "morte",
          "como",
          "pergunta",
          "título",
          "muita",
          "falsidade"
        ],
        "entities": [
          [
            "139",
            "CARDINAL"
          ],
          [
            "WhatsApp",
            "ORG"
          ],
          [
            "grupos de WhatsApp",
            "ORG"
          ],
          [
            "muito difícil",
            "PERSON"
          ],
          [
            "têm aquela",
            "PERSON"
          ],
          [
            "fala mal",
            "PERSON"
          ],
          [
            "traições",
            "GPE"
          ],
          [
            "Sair",
            "PERSON"
          ],
          [
            "tanto",
            "GPE"
          ],
          [
            "benefício de se",
            "PERSON"
          ]
        ],
        "readability_score": 83.57949979499796,
        "semantic_density": 0,
        "word_count": 271,
        "unique_words": 164,
        "lexical_diversity": 0.6051660516605166
      },
      "preservation_score": 2.643361768385519e-05
    },
    {
      "id": 1,
      "text": "— 140 —monetários, pois precisamos continuar tendo a confiança ne -\\ncessária no meio em que vivemos gradativamente.\\nMarcelo,o que isso tem aver com o viver a vida? \\nSe você não conseguir reconhecer o seu corpo, tempo, valo -\\nres, felicidade, necessidade,você vai ficar estagnado no tempo, \\nte afetando em ter um conforto melhor em viver.\\nComo reconhecemos essa necessidade?\\nSinta o seu corpo, calcule o seu financeiro e não tenha \\nmedo de se arriscar perante querer viver melhor, você é capaz \\nde ser melhor, basta você querer e lutar por isso, pois se você \\nnão fizer por você, quem puder fazer não irá fazer, pois assim \\ncomo você não confia em qualquer amigo para contratar, ima -\\ngina se você não passa confiança necessária para ter as suas \\npróprias oportunidades?\\nOportunidades vêm de oportuno e oportuno vem de si \\npróprio.\\nEstou falando sobre isso por minha própria experiên -\\ncia, pois no momento em que me encontro vejo que o meio \\nem que eu vivotrabalha bem menos,tendo mais tempo para \\nevoluir.\\nQuando deixamos de trabalhar para sobreviver (pagar luz, \\naluguel, comida, necessidade básica, estrutura familiar), come -\\nçamos a ter tempo para pensar em como viver melhor. Não de -\\nsejo que ninguém sofra pelo que eu sofro, eu desejo para todos \\num caminho mais fácil, pois eu trabalho em média 14 horas \\npara ganhar oque é necessário para viver no meio em que vivo. \\nJá a maioria das pessoas com quem eu vivo trabalha entre 7 a \\nSem título-1   140Sem título-1   140 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 178854,
      "chapter": 7,
      "page": 140,
      "segment_type": "page",
      "themes": {},
      "difficulty": 31.296303501945523,
      "complexity_metrics": {
        "word_count": 257,
        "sentence_count": 10,
        "paragraph_count": 1,
        "avg_sentence_length": 25.7,
        "avg_word_length": 4.821011673151751,
        "unique_word_ratio": 0.642023346303502,
        "avg_paragraph_length": 257.0,
        "punctuation_density": 0.14396887159533073,
        "line_break_count": 27,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "pois",
          "viver",
          "tempo",
          "melhor",
          "meio",
          "isso",
          "necessidade",
          "como",
          "tendo",
          "confiança",
          "corpo",
          "querer",
          "quem",
          "fazer",
          "oportunidades",
          "oportuno",
          "mais",
          "vivo",
          "título"
        ],
        "entities": [
          [
            "140",
            "CARDINAL"
          ],
          [
            "Marcelo",
            "PERSON"
          ],
          [
            "Se",
            "PERSON"
          ],
          [
            "seu corpo",
            "GPE"
          ],
          [
            "Como",
            "ORG"
          ],
          [
            "calcule o seu",
            "ORG"
          ],
          [
            "medo de se",
            "PERSON"
          ],
          [
            "basta",
            "NORP"
          ],
          [
            "não irá fazer",
            "PERSON"
          ],
          [
            "qualquer amigo",
            "PERSON"
          ]
        ],
        "readability_score": 85.70369649805447,
        "semantic_density": 0,
        "word_count": 257,
        "unique_words": 165,
        "lexical_diversity": 0.642023346303502
      },
      "preservation_score": 2.8157549271932698e-05
    },
    {
      "id": 1,
      "text": "— 141 —10 horas por dia, tendo férias, folga e outros benefícios que eu \\nnão consigo ter. O viver bem é relativo para cada um. \\nPara mim, o viver bem é não passar dificuldade para ter \\nmais tempo para viver, não me importo muito com os meus \\nbens materiais, eu vejo como necessários para se viver melhor.\\nNós somos fantoches da ganância de quem mais poder \\npossui…\\nO quevocê lembra da sua infância?O quevocê lembra da \\nsua adolescência? O quevocê lembra da sua vida? Você não \\nconsegue se lembrar, mas aparecem lembranças avulsas, va -\\ngas, sem contextos… nossas lembranças são ativadas de acordo \\ncom a nossa necessidade de usá-las.\\nAssim como você não consegue se lembrar das suas lem -\\nbranças, você não consegue se lembrar do sentimento que elas \\nte proporcionam, sentimento de ser criança, sentimento de \\nser adolescente… o sentimento de viver o quevocê viveu de \\nmelhor!\\nSem título-1   141Sem título-1   141 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 180488,
      "chapter": 7,
      "page": 141,
      "segment_type": "page",
      "themes": {},
      "difficulty": 25.314345991561183,
      "complexity_metrics": {
        "word_count": 158,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 17.555555555555557,
        "avg_word_length": 4.936708860759493,
        "unique_word_ratio": 0.6645569620253164,
        "avg_paragraph_length": 158.0,
        "punctuation_density": 0.14556962025316456,
        "line_break_count": 17,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "viver",
          "quevocê",
          "sentimento",
          "lembra",
          "você",
          "consegue",
          "lembrar",
          "mais",
          "como",
          "melhor",
          "lembranças",
          "título",
          "horas",
          "tendo",
          "férias",
          "folga",
          "outros",
          "benefícios",
          "consigo",
          "relativo"
        ],
        "entities": [
          [
            "141",
            "CARDINAL"
          ],
          [
            "10",
            "CARDINAL"
          ],
          [
            "dia",
            "ORG"
          ],
          [
            "que eu \\nnão",
            "PERSON"
          ],
          [
            "Para mim",
            "PERSON"
          ],
          [
            "muito",
            "PERSON"
          ],
          [
            "eu vejo",
            "ORG"
          ],
          [
            "para se viver melhor",
            "PERSON"
          ],
          [
            "da ganância de quem mais poder \\npossui",
            "PERSON"
          ],
          [
            "lembra da \\nsua adolescência",
            "PERSON"
          ]
        ],
        "readability_score": 89.74120956399437,
        "semantic_density": 0,
        "word_count": 158,
        "unique_words": 105,
        "lexical_diversity": 0.6645569620253164
      },
      "preservation_score": 1.0854384073080632e-05
    },
    {
      "id": 1,
      "text": "— 142 —Os líderes religiosos estão cada vez mais ricos.\\nOs líderes do Brasil estão ao lado de quem? Os líderes das \\nfacções, milícia, tráfico, estão ao lado de quem?\\nAté que ponto, deixaremos de enxergar que sempre esta -\\nmos sendo manipulados, de acordo com a necessidade de \\nquem tem mais poder? Até que ponto a sua religião é melhor \\nque a minha forma de viver?Até que ponto a religião é bene -\\nfício?Até que ponto vocême aceita não sendo da sua religião?\\nEstamos sempre nos dividindo, estamos sempre querendo \\nver que o meu grupo tem que viver mais que o seu. Porque \\nnão aceitamos todos e fazemos o melhor para todos, pois to -\\ndos sabemos o ruim, pois na própriaBíblia está escrito: Faça ao \\npróximo o que gostaria que fizesse por você!Mateus,capítulo 7, \\nversículo 12\\nPedro aproximou-se de Jesus e perguntou: “Senhor, quantas \\nvezes devo perdoar, se meu irmão pecar contra mim? Até sete \\nvezes?” \\nJesus respondeu: “Não te digo até sete vezes, mas até setenta \\nvezes sete.\\nNós vivemos sempre o mesmo padrão contextual de vida, \\ntudo em nossa volta segue uma semelhança de como assumir \\nou manipular a sociedade. A religião, historicamente, sempre \\nSem título-1   142Sem título-1   142 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 181560,
      "chapter": 7,
      "page": 142,
      "segment_type": "page",
      "themes": {},
      "difficulty": 23.96504854368932,
      "complexity_metrics": {
        "word_count": 206,
        "sentence_count": 14,
        "paragraph_count": 1,
        "avg_sentence_length": 14.714285714285714,
        "avg_word_length": 4.883495145631068,
        "unique_word_ratio": 0.6893203883495146,
        "avg_paragraph_length": 206.0,
        "punctuation_density": 0.17475728155339806,
        "line_break_count": 22,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "sempre",
          "ponto",
          "religião",
          "vezes",
          "líderes",
          "estão",
          "mais",
          "quem",
          "sete",
          "lado",
          "sendo",
          "melhor",
          "viver",
          "estamos",
          "todos",
          "pois",
          "jesus",
          "título",
          "religiosos",
          "cada"
        ],
        "entities": [
          [
            "142",
            "CARDINAL"
          ],
          [
            "religiosos estão",
            "PERSON"
          ],
          [
            "cada vez mais",
            "ORG"
          ],
          [
            "Brasil",
            "PERSON"
          ],
          [
            "lado de quem",
            "PERSON"
          ],
          [
            "lado de quem",
            "PERSON"
          ],
          [
            "deixaremos de enxergar que sempre",
            "ORG"
          ],
          [
            "vocême aceita não",
            "PERSON"
          ],
          [
            "sendo da sua",
            "ORG"
          ],
          [
            "Estamos",
            "ORG"
          ]
        ],
        "readability_score": 91.17780859916782,
        "semantic_density": 0,
        "word_count": 206,
        "unique_words": 142,
        "lexical_diversity": 0.6893203883495146
      },
      "preservation_score": 2.2006731630520344e-05
    },
    {
      "id": 1,
      "text": "— 143 —foi usada de uma forma de manipulação. Diante da necessida -\\nde de controlar a sociedade, perante a manipulação através do \\ncaos criado pelo meu interesse de ser maior que o seu, criamos \\ngrupos e subgrupos, nos tornando certos, mesmo estando er -\\nrados, por sermos maioria diante da necessidade de “todos” …\\nQuando o cristianismo chegou ao Brasil, como chegou?\\nFaçamos o homem à nossa imagem, conforme a nossa se -\\nmelhança. Chegando com uma imagem do filho de Deus \\nbranco, de cabelos grandes e olhos azuis, uma imagem seme -\\nlhante à do europeu tendo poder sobre os índios e os negros. \\nHoje estamos vivendo de forma semelhante… o tráfico, a milí -\\ncia, a religião estão se juntando, destruindo terreiros, destruin -\\ndo a opção de querer viver, poispor mais que eu fique mais \\nrico e o pobre cada vez mais pobre, sendo manipulado em dar \\ndízimos (quanto vale a esperança ? ) através da sua falta de co -\\nnhecimento, nos tornamos cegos diante da nossa falta de co -\\nnhecimento…\\nO povo brasileiro quer o Brasil para todos… o povo mal \\nsabe do processo evolutivo que passamos para ter ou ser o que \\nsomos, um país de terceiro mundo que mal era conhecido na \\ndécada de 50 em que a música brasileira e o futebol fizeram o \\nBrasil ter visibilidade… Começamos a ter turismo, criando ex -\\npectativas de mercado futuro… porém veio a ditadura militar \\ndestruindo a ascensão que estávamos vivendo… novamente a \\nSem título-1   143Sem título-1   143 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 182909,
      "chapter": 7,
      "page": 143,
      "segment_type": "page",
      "themes": {},
      "difficulty": 38.4027027027027,
      "complexity_metrics": {
        "word_count": 259,
        "sentence_count": 6,
        "paragraph_count": 1,
        "avg_sentence_length": 43.166666666666664,
        "avg_word_length": 4.675675675675675,
        "unique_word_ratio": 0.667953667953668,
        "avg_paragraph_length": 259.0,
        "punctuation_density": 0.10424710424710425,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "diante",
          "brasil",
          "nossa",
          "imagem",
          "mais",
          "forma",
          "manipulação",
          "através",
          "todos",
          "chegou",
          "vivendo",
          "destruindo",
          "pobre",
          "falta",
          "nhecimento",
          "povo",
          "título",
          "usada",
          "necessida",
          "controlar"
        ],
        "entities": [
          [
            "143",
            "CARDINAL"
          ],
          [
            "Diante da necessida -\\nde de",
            "PERSON"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "maioria diante da necessidade de",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "Brasil",
            "PERSON"
          ],
          [
            "Façamos",
            "PERSON"
          ],
          [
            "filho de Deus \\nbranco",
            "PERSON"
          ],
          [
            "Hoje",
            "PERSON"
          ],
          [
            "de forma",
            "PERSON"
          ]
        ],
        "readability_score": 77.01396396396396,
        "semantic_density": 0,
        "word_count": 259,
        "unique_words": 173,
        "lexical_diversity": 0.667953667953668
      },
      "preservation_score": 2.2474959963084605e-05
    },
    {
      "id": 1,
      "text": "— 144 —música nos fez ter voz com os grandes festivais, abrindo cami -\\nnho para o movimento Diretas já… logo após conquistarmos \\no direito de escolher o nosso presidente, fizemos a besteira de \\ncolocar um presidente chamado Fernando Collor de Mello( -\\ndécada de 90)…\\nResumo: temos menos de40 anos de “liberdade” e assim \\nque tivemos não soubemos aproveitar. Nós, brasileiros, cobra -\\nmos tantas coisas e não conseguimos enxergar a nossa história, \\nnossos erros, nossas dores e mesmo assim você quer discutir \\npolítica, quer discutir evolução, quer discutir tanta coisa que -\\nvocê não sabe como chegamos à qualidade de vida que te -\\nmos hoje.\\nA nossa evolução é proporcional às nossas necessidades,ao \\ntempo em que temos de vida. Humanos, tribos, povos, ani -\\nmais, insetos, vírus, bactérias e etc. todos os seres vivos (in -\\nclusive o nosso planeta), somos corpos adaptáveis à nossa ne -\\ncessidade.\\nTodos nós evoluímos de acordo com o tempo, dentro desse \\ntempo temos dificuldades e necessidades, dentro dessas neces -\\nsidades oque é necessário para se permanecer vivo?\\nNesse mesmo raciocínio, criamos um padrão de tempo ne -\\ncessário para adaptação de acordo com a nossa necessidade. O \\nplaneta Terra está caótico ou está se protegendo?\\nSem título-1   144Sem título-1   144 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 184514,
      "chapter": 7,
      "page": 144,
      "segment_type": "page",
      "themes": {},
      "difficulty": 28.414122533748703,
      "complexity_metrics": {
        "word_count": 214,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 23.77777777777778,
        "avg_word_length": 5.08411214953271,
        "unique_word_ratio": 0.6962616822429907,
        "avg_paragraph_length": 214.0,
        "punctuation_density": 0.14953271028037382,
        "line_break_count": 23,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "nossa",
          "tempo",
          "temos",
          "quer",
          "discutir",
          "nosso",
          "presidente",
          "assim",
          "nossas",
          "mesmo",
          "você",
          "evolução",
          "vida",
          "necessidades",
          "todos",
          "planeta",
          "acordo",
          "dentro",
          "está",
          "título"
        ],
        "entities": [
          [
            "144",
            "CARDINAL"
          ],
          [
            "Diretas",
            "ORG"
          ],
          [
            "nosso presidente",
            "GPE"
          ],
          [
            "besteira de \\n",
            "ORG"
          ],
          [
            "Fernando Collor de Mello",
            "PERSON"
          ],
          [
            "de 90",
            "PRODUCT"
          ],
          [
            "de40",
            "PRODUCT"
          ],
          [
            "anos de “liberdade",
            "PERSON"
          ],
          [
            "que tivemos não soubemos aproveitar",
            "PERSON"
          ],
          [
            "nossas dores",
            "ORG"
          ]
        ],
        "readability_score": 86.5858774662513,
        "semantic_density": 0,
        "word_count": 214,
        "unique_words": 149,
        "lexical_diversity": 0.6962616822429907
      },
      "preservation_score": 2.5454594806675363e-05
    },
    {
      "id": 1,
      "text": "— 145 —Nós humanos estamos em guerra? Estamos sofrendo? Esta -\\nmos fazendo o quêpara melhorar a nossa própria espécie? “Nós \\nsó passamos por algo que nós mesmos criamos, pensa você \\napanhar a vida toda e depois de velho você quer que aquele \\nsofrimento de toda a sua vida você esqueça, porque aquela \\nmesma sociedade que te machucou a vida toda tem uma ideo -\\nlogia de vida melhor que a sua…você sofreu a vida toda devi -\\ndo a outra ideologia, você aceitaria depois de ter sofrido a vida \\ntoda? Assim serve para tudo em que passamos desde o mundo, \\nanimais, bactérias, humanos (o maior problema do mundo). ” \\nNossos atos, nossas consequências!\\nSer solteiro é ser autêntico!\\nSer solteiro é saber estar sozinho!\\nSer solteiro é você trabalhar para se sustentar sozinho!\\nSer solteiro é ser pai!\\nSer solteiro é cuidar da sua casa!\\nSer solteiro é ser responsável!\\nSer solteiro é ser feliz!\\nSer solteiro é você ter que cozinhar para você, arrumar a \\nsua casa só você, é cagar e esquecer a merda no vaso, descobrir \\nque o lixo tem que ser retirado, entender a importância das \\nbrigas da sua mãe… ser solteiro é ser humano, ser solteiro é \\nmais difícil de ser do quevocê pensa que é a minha facilidade \\nem viver… ser solteiro é viver eu comigo mesmo, pois se você \\nSem título-1   145Sem título-1   145 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 185947,
      "chapter": 7,
      "page": 145,
      "segment_type": "page",
      "themes": {},
      "difficulty": 23.920516717325228,
      "complexity_metrics": {
        "word_count": 235,
        "sentence_count": 14,
        "paragraph_count": 1,
        "avg_sentence_length": 16.785714285714285,
        "avg_word_length": 4.595744680851064,
        "unique_word_ratio": 0.5659574468085107,
        "avg_paragraph_length": 235.0,
        "punctuation_density": 0.1276595744680851,
        "line_break_count": 24,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "solteiro",
          "você",
          "vida",
          "toda",
          "humanos",
          "estamos",
          "passamos",
          "pensa",
          "depois",
          "mundo",
          "sozinho",
          "casa",
          "viver",
          "título",
          "guerra",
          "sofrendo",
          "esta",
          "fazendo",
          "quêpara",
          "melhorar"
        ],
        "entities": [
          [
            "145",
            "CARDINAL"
          ],
          [
            "quêpara melhorar",
            "PERSON"
          ],
          [
            "mesmos criamos",
            "PERSON"
          ],
          [
            "pensa você",
            "PERSON"
          ],
          [
            "porque aquela",
            "PERSON"
          ],
          [
            "logia de vida melhor que",
            "ORG"
          ],
          [
            "outra",
            "NORP"
          ],
          [
            "você aceitaria depois de ter",
            "PERSON"
          ],
          [
            "ser autêntico",
            "ORG"
          ],
          [
            "cuidar da sua",
            "ORG"
          ]
        ],
        "readability_score": 90.22841945288754,
        "semantic_density": 0,
        "word_count": 235,
        "unique_words": 133,
        "lexical_diversity": 0.5659574468085107
      },
      "preservation_score": 2.0942576329237928e-05
    },
    {
      "id": 1,
      "text": "— 146 —não fizer por você mesmo, você nunca irá conseguir ser soltei -\\nro! E acima de tudo, o solteiro sente fome, amor, sofre, sorri, \\nbrinca, viaja, se cuida e tudo isso sozinho, por saber viver o me -\\nlhor que está por vir, só por ser feliz em estar consigo mesmo!\\nEu leio tantas preocupações de algo que eu não entendo o \\nmotivo de alguém ter aquela preocupação… se alguém falar \\nde você ou pensar algo de você, se não falou para você e nem \\nse importou com você, logo eu penso, não me importo com \\nalguém falar de você ou de mim, pois se não for diretamente \\na pessoa designada ao assunto, por quais motivos essa pessoa \\nfaria isso?\\nDireito de resposta ou resposta diante da situação a qual \\nestá tendo o assunto? Foda-se qualquer coisa vinda de alguém \\nque não falou de você na sua cara, pois esse alguém não irá \\nsomar na sua vida. Quem gosta, mesmo dando esporro, bri -\\ngando, falando besteira… tem um sentido de ter aquele tipo \\nde pensamento, se a pessoa a qual falou de você não veio até \\nvocê, por qual motivo você vai dar atenção? Fofoca, intrigas, \\nfalsidade… nós só sentimos se damos importância, e se damos \\nimportância é um sinal quealgo realmente está nos afetando \\nnaquela situação...\\nSem título-1   146Sem título-1   146 17/03/2022   15:08:3717/03/2022   15:08:37",
      "position": 187398,
      "chapter": 7,
      "page": 146,
      "segment_type": "page",
      "themes": {},
      "difficulty": 30.609210526315792,
      "complexity_metrics": {
        "word_count": 228,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 28.5,
        "avg_word_length": 4.530701754385965,
        "unique_word_ratio": 0.6359649122807017,
        "avg_paragraph_length": 228.0,
        "punctuation_density": 0.16228070175438597,
        "line_break_count": 21,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "alguém",
          "mesmo",
          "está",
          "falou",
          "pessoa",
          "qual",
          "tudo",
          "isso",
          "algo",
          "motivo",
          "falar",
          "pois",
          "assunto",
          "resposta",
          "situação",
          "damos",
          "importância",
          "título",
          "fizer"
        ],
        "entities": [
          [
            "146",
            "CARDINAL"
          ],
          [
            "irá conseguir",
            "PERSON"
          ],
          [
            "Eu leio",
            "PERSON"
          ],
          [
            "eu não entendo",
            "PERSON"
          ],
          [
            "aquela preocupação",
            "PERSON"
          ],
          [
            "logo eu penso",
            "PERSON"
          ],
          [
            "essa pessoa",
            "PERSON"
          ],
          [
            "Direito de resposta",
            "PERSON"
          ],
          [
            "Foda-se",
            "PERSON"
          ],
          [
            "coisa vinda de alguém \\n",
            "PERSON"
          ]
        ],
        "readability_score": 84.39078947368421,
        "semantic_density": 0,
        "word_count": 228,
        "unique_words": 145,
        "lexical_diversity": 0.6359649122807017
      },
      "preservation_score": 2.0112535194237645e-05
    },
    {
      "id": 1,
      "text": "— 147 —Você não irá deixar de ser: preto, branco, gay, viado, lésbi -\\nca, homossexual, homoafetivo, gordo, magro, feio, bonito, rico, \\npobre, trans, feminista, esquerda, direita…você pode apoiar \\nqualquer bandeira…você nasceu da forma que tinha que nas -\\ncer. Você ama, faz sexo, beija, admira, é feliz, é triste, vive e tem \\nvontades igual a todo mundo, porém atéque ponto a sua von -\\ntade é maior que a vontade do outro?\\nAtéqueponto você merece ser mais humano que o outro? \\nAtéque ponto a sua vida foi mais difícil ou pior que a \\ndo outro?\\nIndependente de viver, a falta de respeito perante o nosso \\nsemelhante não tem que ser exaltada, temos que exaltar o me -\\nlhor da vida, para aquela vida ser maior exemplo de vida que \\naquela mais falada!\\nNós humanos não precisamos apoiar uma causa, nós hu -\\nmanos temos que apoiar a humanidade, pois aquele “humano” \\nque não entende que a vida dele é semelhante à sua, ele nunca \\nvai ser exemplo para eu ser um ser humano!\\nQuantidade de perda de pensamentos e tempo perante um \\nquerer viver de uma forma…\\nQual a quantidade de tempo que você perde pensando \\nem quanto tempo alguém vai te achar bonito? Equivale a se \\nSem título-1   147Sem título-1   147 17/03/2022   15:08:3817/03/2022   15:08:38",
      "position": 188797,
      "chapter": 7,
      "page": 147,
      "segment_type": "page",
      "themes": {},
      "difficulty": 29.893055555555556,
      "complexity_metrics": {
        "word_count": 216,
        "sentence_count": 8,
        "paragraph_count": 1,
        "avg_sentence_length": 27.0,
        "avg_word_length": 4.643518518518518,
        "unique_word_ratio": 0.6574074074074074,
        "avg_paragraph_length": 216.0,
        "punctuation_density": 0.18981481481481483,
        "line_break_count": 22,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "vida",
          "apoiar",
          "outro",
          "mais",
          "humano",
          "tempo",
          "bonito",
          "forma",
          "atéque",
          "ponto",
          "maior",
          "viver",
          "perante",
          "semelhante",
          "temos",
          "aquela",
          "exemplo",
          "quantidade",
          "título"
        ],
        "entities": [
          [
            "147",
            "CARDINAL"
          ],
          [
            "irá deixar de ser",
            "PERSON"
          ],
          [
            "bonito",
            "GPE"
          ],
          [
            "rico",
            "LAW"
          ],
          [
            "trans",
            "ORG"
          ],
          [
            "direita",
            "ORG"
          ],
          [
            "você pode apoiar",
            "PERSON"
          ],
          [
            "qualquer bandeira",
            "PERSON"
          ],
          [
            "você nasceu da forma",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ]
        ],
        "readability_score": 85.10694444444445,
        "semantic_density": 0,
        "word_count": 216,
        "unique_words": 142,
        "lexical_diversity": 0.6574074074074074
      },
      "preservation_score": 2.434787329334166e-05
    },
    {
      "id": 1,
      "text": "— 148 —cuidar, arrumar, se sentir bem entre as pessoas e pensando em \\ncomo executar isso tudo!!!\\nQuanto tempo você perde pensando nos seus problemas…\\nSeus problemas são relativos para vocêmesmo. Quanto \\ntempo você perde pensando no problema, preocupado com o \\nproblema e executando a solução para o problema?\\nAté que ponto você vive o seu tempo?\\nAtéque ponto você acha que está vivendo o seu tempo?\\nAté que ponto realmente você está vivendo?\\nA maioria das pessoas não se sente capaz…as pessoas se su -\\nbestimam, tornando-se reféns dos pensamentos hipócritas e \\nconservadores de uma sociedade que mal sabe se cuidar, cheia \\nde ganância, egoísmo, chegando ao ponto do egocêntrico ser \\nmais valorizado que os valores idealizados por uma sociedade \\n“perfeita” …\\nQual é o ser humano mais evoluído?\\nO rico, pois ele cresceu financeiramente…chegamosa um \\nponto que se pode comprar desde pessoas e qualquer bem ma -\\nterial sem saber o próprio limite. \\nSem título-1   148Sem título-1   148 17/03/2022   15:08:3817/03/2022   15:08:38",
      "position": 190151,
      "chapter": 7,
      "page": 148,
      "segment_type": "page",
      "themes": {},
      "difficulty": 25.608929788684392,
      "complexity_metrics": {
        "word_count": 163,
        "sentence_count": 9,
        "paragraph_count": 1,
        "avg_sentence_length": 18.11111111111111,
        "avg_word_length": 5.177914110429448,
        "unique_word_ratio": 0.7116564417177914,
        "avg_paragraph_length": 163.0,
        "punctuation_density": 0.13496932515337423,
        "line_break_count": 19,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "você",
          "ponto",
          "pessoas",
          "tempo",
          "pensando",
          "problema",
          "cuidar",
          "quanto",
          "perde",
          "seus",
          "problemas",
          "está",
          "vivendo",
          "sociedade",
          "mais",
          "título",
          "arrumar",
          "sentir",
          "entre",
          "como"
        ],
        "entities": [
          [
            "148",
            "CARDINAL"
          ],
          [
            "cuidar",
            "ORG"
          ],
          [
            "arrumar",
            "PERSON"
          ],
          [
            "Quanto",
            "PRODUCT"
          ],
          [
            "você perde pensando",
            "ORG"
          ],
          [
            "nos seus problemas",
            "PERSON"
          ],
          [
            "você perde pensando",
            "ORG"
          ],
          [
            "preocupado",
            "GPE"
          ],
          [
            "Atéque",
            "NORP"
          ],
          [
            "cuidar",
            "ORG"
          ]
        ],
        "readability_score": 89.39107021131561,
        "semantic_density": 0,
        "word_count": 163,
        "unique_words": 116,
        "lexical_diversity": 0.7116564417177914
      },
      "preservation_score": 1.2535749449106848e-05
    },
    {
      "id": 1,
      "text": "— 149 —O pobre, pois ele com todos as dificuldades, com todos os \\nproblemas que o cercam, ainda assim consegue passar amor \\ne afeto de uma forma que quem tem dinheiro não consegue \\ndar valor ao sentimento, devido a ter as mulheres (homens), \\nos carros, casas,pelo próprio dinheiro, o tornando uma pessoa \\nque se acha melhor que os demais. Porém, o pobrenão tem es -\\nperança, a visão de vida melhor do pobre é um miliciano rico, \\num traficante rico, assim o tornando uma pessoa cheia de so -\\nnhos,porém com a visão de quem não tem limites para chegar \\nao seu objetivo (tanto rico quanto pobre).\\nQuem está no meio, como se comportar? Como sabemos \\nqual é o limite de quem está na sua frente? \\nAté que pontopodemos passar por cima das nossas crenças, \\nmetodologia de vida? Até que ponto é o necessário para se ter \\numa vida dentro da sociedadesem deixar de ser coerente com \\nas suas próprias ações?\\nAs palavras, as ações das pessoas que vivem em nossa socie -\\ndade não condizem com o que realmente julgam. O certo e o \\nerrado estão em uma briga constante, a falta de questionamen -\\ntos, a falta de se importar com o próximo, a falta de respeito \\nestá nos tornando pessoas doentes, pessoas que quando olham \\numa para a outra não temos confiança, pois a confiança está \\ntão destoada que ninguém consegue acreditar que a confiança \\ndo seu próprio pré-julgamento ao conhecer alguém faz você \\nnão enxergar as qualidades, fazendo você desacreditar que te -\\nmos solução. \\nOque é ser evoluído? \\nSem título-1   149Sem título-1   149 17/03/2022   15:08:3817/03/2022   15:08:38",
      "position": 191290,
      "chapter": 7,
      "page": 149,
      "segment_type": "page",
      "themes": {},
      "difficulty": 29.950369003690035,
      "complexity_metrics": {
        "word_count": 271,
        "sentence_count": 10,
        "paragraph_count": 1,
        "avg_sentence_length": 27.1,
        "avg_word_length": 4.667896678966789,
        "unique_word_ratio": 0.6014760147601476,
        "avg_paragraph_length": 271.0,
        "punctuation_density": 0.12915129151291513,
        "line_break_count": 27,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "quem",
          "está",
          "pobre",
          "consegue",
          "tornando",
          "vida",
          "rico",
          "pessoas",
          "falta",
          "confiança",
          "pois",
          "todos",
          "assim",
          "passar",
          "dinheiro",
          "próprio",
          "pessoa",
          "melhor",
          "porém",
          "visão"
        ],
        "entities": [
          [
            "149",
            "CARDINAL"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "ainda",
            "ORG"
          ],
          [
            "casas",
            "GPE"
          ],
          [
            "pelo próprio dinheiro",
            "PERSON"
          ],
          [
            "que se acha melhor que",
            "PERSON"
          ],
          [
            "visão de vida melhor",
            "ORG"
          ],
          [
            "rico",
            "LAW"
          ],
          [
            "rico",
            "LAW"
          ],
          [
            "cheia de so -\\nnhos",
            "PERSON"
          ]
        ],
        "readability_score": 85.04963099630996,
        "semantic_density": 0,
        "word_count": 271,
        "unique_words": 163,
        "lexical_diversity": 0.6014760147601476
      },
      "preservation_score": 2.8157549271932698e-05
    },
    {
      "id": 1,
      "text": "— 150 —A pessoa que faz a diferença para um em prol de todos ou \\naquele cara que faz a diferença para si próprio?\\nNós vivemos dentro do caos, com a liberdade proporcional \\nao caos de onde vivemos!!!\\nSem título-1   150Sem título-1   150 17/03/2022   15:08:3817/03/2022   15:08:38",
      "position": 192969,
      "chapter": 7,
      "page": 150,
      "segment_type": "page",
      "themes": {},
      "difficulty": 24.121014492753623,
      "complexity_metrics": {
        "word_count": 46,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 15.333333333333334,
        "avg_word_length": 4.8478260869565215,
        "unique_word_ratio": 0.8043478260869565,
        "avg_paragraph_length": 46.0,
        "punctuation_density": 0.1956521739130435,
        "line_break_count": 4,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "diferença",
          "vivemos",
          "caos",
          "título",
          "pessoa",
          "prol",
          "todos",
          "aquele",
          "cara",
          "próprio",
          "dentro",
          "liberdade",
          "proporcional",
          "onde"
        ],
        "entities": [
          [
            "150",
            "CARDINAL"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "150Sem",
            "CARDINAL"
          ],
          [
            "150",
            "CARDINAL"
          ],
          [
            "17/03/2022",
            "DATE"
          ],
          [
            "15:08:3817/03/2022",
            "CARDINAL"
          ],
          [
            "15:08:38",
            "TIME"
          ]
        ],
        "readability_score": 90.87898550724637,
        "semantic_density": 0,
        "word_count": 46,
        "unique_words": 37,
        "lexical_diversity": 0.8043478260869565
      },
      "preservation_score": 1.1067215133337116e-06
    },
    {
      "id": 1,
      "text": "— 151 —\\nSem título-1   151Sem título-1   151 17/03/2022   15:08:3817/03/2022   15:08:38",
      "position": 193364,
      "chapter": 7,
      "page": 151,
      "segment_type": "page",
      "themes": {},
      "difficulty": 22.381818181818183,
      "complexity_metrics": {
        "word_count": 11,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 11.0,
        "avg_word_length": 6.2727272727272725,
        "unique_word_ratio": 0.7272727272727273,
        "avg_paragraph_length": 11.0,
        "punctuation_density": 0.36363636363636365,
        "line_break_count": 1,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "título"
        ],
        "entities": [
          [
            "151",
            "CARDINAL"
          ],
          [
            "151Sem",
            "CARDINAL"
          ],
          [
            "151",
            "CARDINAL"
          ],
          [
            "17/03/2022",
            "DATE"
          ],
          [
            "15:08:3817/03/2022",
            "CARDINAL"
          ],
          [
            "15:08:38",
            "TIME"
          ]
        ],
        "readability_score": 92.61818181818182,
        "semantic_density": 0,
        "word_count": 11,
        "unique_words": 8,
        "lexical_diversity": 0.7272727272727273
      },
      "preservation_score": 1.7026484820518643e-07
    },
    {
      "id": 1,
      "text": "Este livro foi composto em\\nSabon Next LT Pro\\npela Editora Autografia\\ne impresso em polén 80.\\nSem título-1   152Sem título-1   152 17/03/2022   15:08:3817/03/2022   15:08:38",
      "position": 193567,
      "chapter": 7,
      "page": 152,
      "segment_type": "page",
      "themes": {},
      "difficulty": 22.93,
      "complexity_metrics": {
        "word_count": 25,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 12.5,
        "avg_word_length": 5.6,
        "unique_word_ratio": 0.92,
        "avg_paragraph_length": 25.0,
        "punctuation_density": 0.2,
        "line_break_count": 4,
        "formatting_preservation_score": 80.0
      },
      "analysis": {
        "keywords": [
          "título",
          "este",
          "livro",
          "composto",
          "sabon",
          "next",
          "pela",
          "editora",
          "autografia",
          "impresso",
          "polén"
        ],
        "entities": [
          [
            "Editora Autografia",
            "PERSON"
          ],
          [
            "80",
            "CARDINAL"
          ],
          [
            "152Sem",
            "CARDINAL"
          ],
          [
            "152",
            "CARDINAL"
          ],
          [
            "17/03/2022",
            "DATE"
          ],
          [
            "15:08:3817/03/2022",
            "CARDINAL"
          ],
          [
            "15:08:38",
            "TIME"
          ]
        ],
        "readability_score": 92.07,
        "semantic_density": 0,
        "word_count": 25,
        "unique_words": 23,
        "lexical_diversity": 0.92
      },
      "preservation_score": 5.959269687181524e-07
    }
  ],
  "book_name": "miolo_liberdade dentro do caos_17032022.pdf",
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