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
    "total_chapters": 4,
    "total_pages": 115,
    "avg_difficulty": 31.62413536439335,
    "max_difficulty": 40.99817073170732,
    "min_difficulty": 20.24054054054054,
    "theme_distribution": {
      "filosofia": 80.1715983507155,
      "ciencia": 87.08113200251681,
      "arte": 86.21052631578947,
      "tecnologia": 28.31807780320366
    },
    "total_words": 25112,
    "avg_words_per_segment": 165.21052631578948,
    "formatting_preservation": 90.5592105263158,
    "preservation_score": 7.268131228072864e-05,
    "book_name": "paradoxo dos movimentos concluído.docx",
    "analysis_timestamp": "2025-09-15T19:25:52",
    "structure_preserved": false
  },
  "theme_analysis": {
    "filosofia": [
      {
        "segment": 1,
        "score": 100.0,
        "position": 0,
        "chapter": 2
      },
      {
        "segment": 13,
        "score": 53.57142857142857,
        "position": 10998,
        "chapter": 3
      },
      {
        "segment": 27,
        "score": 60.0,
        "position": 24926,
        "chapter": 3
      },
      {
        "segment": 28,
        "score": 60.0,
        "position": 25926,
        "chapter": 3
      },
      {
        "segment": 33,
        "score": 100.0,
        "position": 30961,
        "chapter": 4
      },
      {
        "segment": 41,
        "score": 100.0,
        "position": 39200,
        "chapter": 5
      },
      {
        "segment": 57,
        "score": 16.129032258064516,
        "position": 55031,
        "chapter": 5
      },
      {
        "segment": 88,
        "score": 53.57142857142857,
        "position": 85667,
        "chapter": 5
      },
      {
        "segment": 91,
        "score": 100.0,
        "position": 88660,
        "chapter": 5
      },
      {
        "segment": 92,
        "score": 100.0,
        "position": 89660,
        "chapter": 5
      },
      {
        "segment": 99,
        "score": 100.0,
        "position": 96507,
        "chapter": 5
      },
      {
        "segment": 107,
        "score": 100.0,
        "position": 104147,
        "chapter": 5
      },
      {
        "segment": 111,
        "score": 39.473684210526315,
        "position": 107915,
        "chapter": 5
      },
      {
        "segment": 125,
        "score": 100.0,
        "position": 121727,
        "chapter": 5
      },
      {
        "segment": 126,
        "score": 100.0,
        "position": 122727,
        "chapter": 5
      },
      {
        "segment": 148,
        "score": 100.0,
        "position": 144490,
        "chapter": 5
      }
    ],
    "ciencia": [
      {
        "segment": 4,
        "score": 100.0,
        "position": 2175,
        "chapter": 3
      },
      {
        "segment": 5,
        "score": 100.0,
        "position": 3175,
        "chapter": 3
      },
      {
        "segment": 11,
        "score": 100.0,
        "position": 9045,
        "chapter": 3
      },
      {
        "segment": 13,
        "score": 46.42857142857144,
        "position": 10998,
        "chapter": 3
      },
      {
        "segment": 57,
        "score": 83.87096774193549,
        "position": 55031,
        "chapter": 5
      },
      {
        "segment": 83,
        "score": 56.52173913043479,
        "position": 80676,
        "chapter": 5
      },
      {
        "segment": 88,
        "score": 46.42857142857144,
        "position": 85667,
        "chapter": 5
      },
      {
        "segment": 93,
        "score": 100.0,
        "position": 90562,
        "chapter": 5
      },
      {
        "segment": 105,
        "score": 100.0,
        "position": 102287,
        "chapter": 5
      },
      {
        "segment": 110,
        "score": 100.0,
        "position": 106929,
        "chapter": 5
      },
      {
        "segment": 111,
        "score": 34.21052631578947,
        "position": 107915,
        "chapter": 5
      },
      {
        "segment": 116,
        "score": 100.0,
        "position": 112725,
        "chapter": 5
      },
      {
        "segment": 123,
        "score": 100.0,
        "position": 119737,
        "chapter": 5
      },
      {
        "segment": 135,
        "score": 100.0,
        "position": 131578,
        "chapter": 5
      },
      {
        "segment": 136,
        "score": 100.0,
        "position": 132578,
        "chapter": 5
      },
      {
        "segment": 138,
        "score": 100.0,
        "position": 134494,
        "chapter": 5
      },
      {
        "segment": 143,
        "score": 100.0,
        "position": 139458,
        "chapter": 5
      },
      {
        "segment": 152,
        "score": 100.0,
        "position": 148554,
        "chapter": 5
      }
    ],
    "arte": [
      {
        "segment": 24,
        "score": 100.0,
        "position": 21893,
        "chapter": 3
      },
      {
        "segment": 27,
        "score": 40.0,
        "position": 24926,
        "chapter": 3
      },
      {
        "segment": 28,
        "score": 40.0,
        "position": 25926,
        "chapter": 3
      },
      {
        "segment": 29,
        "score": 100.0,
        "position": 27003,
        "chapter": 4
      },
      {
        "segment": 30,
        "score": 100.0,
        "position": 28003,
        "chapter": 4
      },
      {
        "segment": 37,
        "score": 100.0,
        "position": 35077,
        "chapter": 4
      },
      {
        "segment": 39,
        "score": 100.0,
        "position": 37188,
        "chapter": 5
      },
      {
        "segment": 60,
        "score": 100.0,
        "position": 58154,
        "chapter": 5
      },
      {
        "segment": 78,
        "score": 100.0,
        "position": 75898,
        "chapter": 5
      },
      {
        "segment": 80,
        "score": 100.0,
        "position": 77807,
        "chapter": 5
      },
      {
        "segment": 111,
        "score": 13.157894736842104,
        "position": 107915,
        "chapter": 5
      },
      {
        "segment": 112,
        "score": 100.0,
        "position": 108861,
        "chapter": 5
      },
      {
        "segment": 115,
        "score": 100.0,
        "position": 111803,
        "chapter": 5
      },
      {
        "segment": 140,
        "score": 100.0,
        "position": 136512,
        "chapter": 5
      },
      {
        "segment": 150,
        "score": 100.0,
        "position": 146554,
        "chapter": 5
      }
    ],
    "tecnologia": [
      {
        "segment": 83,
        "score": 43.47826086956522,
        "position": 80676,
        "chapter": 5
      },
      {
        "segment": 111,
        "score": 13.157894736842104,
        "position": 107915,
        "chapter": 5
      }
    ]
  },
  "difficulty_map": [
    {
      "segment": 1,
      "difficulty": 20.24054054054054,
      "position": 0,
      "chapter": 2,
      "main_theme": "filosofia",
      "word_count": 37,
      "preservation_score": 1.684364479079058e-05
    },
    {
      "segment": 2,
      "difficulty": 32.727777777777774,
      "position": 233,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 162,
      "preservation_score": 3.5291446228323116e-05
    },
    {
      "segment": 3,
      "difficulty": 36.549019607843135,
      "position": 1229,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 153,
      "preservation_score": 5.347188822473199e-06
    },
    {
      "segment": 4,
      "difficulty": 40.00571428571429,
      "position": 2175,
      "chapter": 3,
      "main_theme": "ciencia",
      "word_count": 175,
      "preservation_score": 3.07463357292209e-05
    },
    {
      "segment": 5,
      "difficulty": 40.99817073170732,
      "position": 3175,
      "chapter": 3,
      "main_theme": "ciencia",
      "word_count": 164,
      "preservation_score": 1.5239488144048618e-05
    },
    {
      "segment": 6,
      "difficulty": 31.044755244755244,
      "position": 4161,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 143,
      "preservation_score": 3.2083132934839193e-05
    },
    {
      "segment": 7,
      "difficulty": 33.969166666666666,
      "position": 5097,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 160,
      "preservation_score": 4.010391616854898e-05
    },
    {
      "segment": 8,
      "difficulty": 36.45801886792453,
      "position": 6097,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 159,
      "preservation_score": 2.94095385236026e-06
    },
    {
      "segment": 9,
      "difficulty": 36.62467532467532,
      "position": 7097,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 154,
      "preservation_score": 6.416626586967839e-06
    },
    {
      "segment": 10,
      "difficulty": 36.52322580645161,
      "position": 8097,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 155,
      "preservation_score": 1.2031174850564695e-05
    },
    {
      "segment": 11,
      "difficulty": 36.56666666666666,
      "position": 9045,
      "chapter": 3,
      "main_theme": "ciencia",
      "word_count": 153,
      "preservation_score": 2.0051958084274496e-06
    },
    {
      "segment": 12,
      "difficulty": 36.113461538461536,
      "position": 9998,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 156,
      "preservation_score": 7.218704910338818e-06
    },
    {
      "segment": 13,
      "difficulty": 36.59941860465116,
      "position": 10998,
      "chapter": 3,
      "main_theme": "filosofia",
      "word_count": 172,
      "preservation_score": 5.614548263596859e-06
    },
    {
      "segment": 14,
      "difficulty": 36.52884615384615,
      "position": 12090,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 156,
      "preservation_score": 1.3367972056182997e-06
    },
    {
      "segment": 15,
      "difficulty": 36.57450980392157,
      "position": 13042,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 153,
      "preservation_score": 2.94095385236026e-06
    },
    {
      "segment": 16,
      "difficulty": 31.679189686924495,
      "position": 14000,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 181,
      "preservation_score": 4.611950359383134e-05
    },
    {
      "segment": 17,
      "difficulty": 36.52926829268293,
      "position": 15000,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 164,
      "preservation_score": 0.0
    },
    {
      "segment": 18,
      "difficulty": 36.51472392638037,
      "position": 16000,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 163,
      "preservation_score": 4.344590918259474e-05
    },
    {
      "segment": 19,
      "difficulty": 21.63589232303091,
      "position": 16991,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 177,
      "preservation_score": 0.0004764345240823619
    },
    {
      "segment": 20,
      "difficulty": 36.40113636363637,
      "position": 17991,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 176,
      "preservation_score": 1.0427018203822739e-05
    },
    {
      "segment": 21,
      "difficulty": 35.13035714285714,
      "position": 18991,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 168,
      "preservation_score": 3.5090926647480365e-05
    },
    {
      "segment": 22,
      "difficulty": 28.596974789915965,
      "position": 19910,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 170,
      "preservation_score": 7.018185329496074e-05
    },
    {
      "segment": 23,
      "difficulty": 36.42280701754386,
      "position": 20910,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 171,
      "preservation_score": 1.1362776247755548e-06
    },
    {
      "segment": 24,
      "difficulty": 31.48491620111732,
      "position": 21893,
      "chapter": 3,
      "main_theme": "arte",
      "word_count": 179,
      "preservation_score": 7.940575401372699e-05
    },
    {
      "segment": 25,
      "difficulty": 25.620604781997187,
      "position": 22966,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 158,
      "preservation_score": 8.515398199788572e-05
    },
    {
      "segment": 26,
      "difficulty": 35.57142857142857,
      "position": 23926,
      "chapter": 3,
      "main_theme": "none",
      "word_count": 168,
      "preservation_score": 2.6735944112365995e-05
    },
    {
      "segment": 27,
      "difficulty": 36.40113636363637,
      "position": 24926,
      "chapter": 3,
      "main_theme": "filosofia",
      "word_count": 176,
      "preservation_score": 2.6735944112365995e-06
    },
    {
      "segment": 28,
      "difficulty": 28.196195652173913,
      "position": 25926,
      "chapter": 3,
      "main_theme": "filosofia",
      "word_count": 184,
      "preservation_score": 4.177491267557186e-05
    },
    {
      "segment": 29,
      "difficulty": 36.42369942196532,
      "position": 27003,
      "chapter": 4,
      "main_theme": "arte",
      "word_count": 173,
      "preservation_score": 1.924987976090352e-05
    },
    {
      "segment": 30,
      "difficulty": 36.553642384105956,
      "position": 28003,
      "chapter": 4,
      "main_theme": "arte",
      "word_count": 151,
      "preservation_score": 1.2699573453373847e-06
    },
    {
      "segment": 31,
      "difficulty": 36.331868131868134,
      "position": 28937,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 182,
      "preservation_score": 1.6843644790790576e-05
    },
    {
      "segment": 32,
      "difficulty": 33.59112426035503,
      "position": 29937,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 169,
      "preservation_score": 7.205336938282638e-05
    },
    {
      "segment": 33,
      "difficulty": 28.72606516290727,
      "position": 30961,
      "chapter": 4,
      "main_theme": "filosofia",
      "word_count": 171,
      "preservation_score": 9.3575804393281e-05
    },
    {
      "segment": 34,
      "difficulty": 39.534131736526945,
      "position": 31961,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 167,
      "preservation_score": 1.804676227584704e-05
    },
    {
      "segment": 35,
      "difficulty": 33.67,
      "position": 32987,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 180,
      "preservation_score": 2.5666506347871358e-05
    },
    {
      "segment": 36,
      "difficulty": 33.55235294117647,
      "position": 34077,
      "chapter": 4,
      "main_theme": "none",
      "word_count": 170,
      "preservation_score": 8.822861557080777e-06
    },
    {
      "segment": 37,
      "difficulty": 32.02204301075269,
      "position": 35077,
      "chapter": 4,
      "main_theme": "arte",
      "word_count": 186,
      "preservation_score": 1.0828057365508227e-05
    },
    {
      "segment": 38,
      "difficulty": 22.185798816568045,
      "position": 36162,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 169,
      "preservation_score": 0.00030499028246181516
    },
    {
      "segment": 39,
      "difficulty": 28.80656146179402,
      "position": 37188,
      "chapter": 5,
      "main_theme": "arte",
      "word_count": 172,
      "preservation_score": 6.877821622906154e-05
    },
    {
      "segment": 40,
      "difficulty": 28.59873949579832,
      "position": 38200,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 170,
      "preservation_score": 3.6093524551694095e-05
    },
    {
      "segment": 41,
      "difficulty": 36.46228571428571,
      "position": 39200,
      "chapter": 5,
      "main_theme": "filosofia",
      "word_count": 175,
      "preservation_score": 2.245819305438744e-05
    },
    {
      "segment": 42,
      "difficulty": 36.37900552486188,
      "position": 40233,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 181,
      "preservation_score": 1.1229096527193718e-05
    },
    {
      "segment": 43,
      "difficulty": 31.154,
      "position": 41248,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 175,
      "preservation_score": 2.5399146906747697e-05
    },
    {
      "segment": 44,
      "difficulty": 32.48544303797468,
      "position": 42248,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 158,
      "preservation_score": 4.411430778540389e-05
    },
    {
      "segment": 45,
      "difficulty": 36.51168831168831,
      "position": 43248,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 154,
      "preservation_score": 1.06943776449464e-06
    },
    {
      "segment": 46,
      "difficulty": 32.25396825396825,
      "position": 44179,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 189,
      "preservation_score": 4.344590918259474e-05
    },
    {
      "segment": 47,
      "difficulty": 36.74450867052023,
      "position": 45270,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 173,
      "preservation_score": 1.2031174850564695e-05
    },
    {
      "segment": 48,
      "difficulty": 31.588461538461537,
      "position": 46279,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 182,
      "preservation_score": 1.6041566467419597e-05
    },
    {
      "segment": 49,
      "difficulty": 27.337406015037594,
      "position": 47279,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 152,
      "preservation_score": 6.95134546921516e-06
    },
    {
      "segment": 50,
      "difficulty": 28.54642857142857,
      "position": 48183,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 168,
      "preservation_score": 4.4114307785403885e-05
    },
    {
      "segment": 51,
      "difficulty": 35.192814371257484,
      "position": 49183,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 167,
      "preservation_score": 1.5239488144048618e-05
    },
    {
      "segment": 52,
      "difficulty": 36.49281437125748,
      "position": 50183,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 167,
      "preservation_score": 8.020783233709797e-06
    },
    {
      "segment": 53,
      "difficulty": 36.40571428571428,
      "position": 51183,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 175,
      "preservation_score": 1.5239488144048618e-05
    },
    {
      "segment": 54,
      "difficulty": 35.36758241758242,
      "position": 52183,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 182,
      "preservation_score": 0.0
    },
    {
      "segment": 55,
      "difficulty": 35.73235294117647,
      "position": 53187,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 153,
      "preservation_score": 4.812469940225879e-06
    },
    {
      "segment": 56,
      "difficulty": 25.48672086720867,
      "position": 54102,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 164,
      "preservation_score": 0.00021836582353774924
    },
    {
      "segment": 57,
      "difficulty": 24.11299498047964,
      "position": 55031,
      "chapter": 5,
      "main_theme": "ciencia",
      "word_count": 163,
      "preservation_score": 0.00024262869281972137
    },
    {
      "segment": 58,
      "difficulty": 36.439361702127655,
      "position": 56031,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 188,
      "preservation_score": 7.75342379258614e-06
    },
    {
      "segment": 59,
      "difficulty": 26.829255319148935,
      "position": 57124,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 188,
      "preservation_score": 9.731883656901226e-05
    },
    {
      "segment": 60,
      "difficulty": 33.08735632183908,
      "position": 58154,
      "chapter": 5,
      "main_theme": "arte",
      "word_count": 174,
      "preservation_score": 5.681388123877773e-05
    },
    {
      "segment": 61,
      "difficulty": 27.90232142857143,
      "position": 59159,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 160,
      "preservation_score": 6.877821622906154e-05
    },
    {
      "segment": 62,
      "difficulty": 35.18983050847458,
      "position": 60113,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 177,
      "preservation_score": 2.085403640764548e-05
    },
    {
      "segment": 63,
      "difficulty": 28.402323580034423,
      "position": 61113,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 166,
      "preservation_score": 0.00017378363673037895
    },
    {
      "segment": 64,
      "difficulty": 24.960233918128655,
      "position": 62144,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 152,
      "preservation_score": 9.203848760681994e-05
    },
    {
      "segment": 65,
      "difficulty": 28.844991789819378,
      "position": 63075,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 174,
      "preservation_score": 4.010391616854899e-05
    },
    {
      "segment": 66,
      "difficulty": 33.19759036144578,
      "position": 64026,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 166,
      "preservation_score": 2.352763081888208e-05
    },
    {
      "segment": 67,
      "difficulty": 26.872045454545454,
      "position": 65080,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 165,
      "preservation_score": 4.010391616854899e-05
    },
    {
      "segment": 68,
      "difficulty": 23.83382269904009,
      "position": 66040,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 161,
      "preservation_score": 0.0002406234970112939
    },
    {
      "segment": 69,
      "difficulty": 22.85347091932458,
      "position": 67006,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 164,
      "preservation_score": 0.00020586676966521817
    },
    {
      "segment": 70,
      "difficulty": 33.900571428571425,
      "position": 68006,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 175,
      "preservation_score": 3.341993014045749e-05
    },
    {
      "segment": 71,
      "difficulty": 33.95294117647059,
      "position": 69005,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 153,
      "preservation_score": 3.47567273460758e-05
    },
    {
      "segment": 72,
      "difficulty": 26.475963020030818,
      "position": 70005,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 177,
      "preservation_score": 0.000145443535971271
    },
    {
      "segment": 73,
      "difficulty": 26.807727272727274,
      "position": 71036,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 165,
      "preservation_score": 8.187882884412088e-05
    },
    {
      "segment": 74,
      "difficulty": 33.14438095238095,
      "position": 71999,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 175,
      "preservation_score": 5.5343404312597604e-05
    },
    {
      "segment": 75,
      "difficulty": 26.211290322580645,
      "position": 73044,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 155,
      "preservation_score": 9.203848760681994e-05
    },
    {
      "segment": 76,
      "difficulty": 27.836980108499098,
      "position": 73966,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 158,
      "preservation_score": 8.842913515165055e-05
    },
    {
      "segment": 77,
      "difficulty": 29.443763440860216,
      "position": 74948,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 155,
      "preservation_score": 4.571846443214584e-05
    },
    {
      "segment": 78,
      "difficulty": 29.577426160337552,
      "position": 75898,
      "chapter": 5,
      "main_theme": "arte",
      "word_count": 158,
      "preservation_score": 6.015587425282348e-05
    },
    {
      "segment": 79,
      "difficulty": 38.4406976744186,
      "position": 76807,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 172,
      "preservation_score": 1.5239488144048618e-05
    },
    {
      "segment": 80,
      "difficulty": 38.70155172413793,
      "position": 77807,
      "chapter": 5,
      "main_theme": "arte",
      "word_count": 145,
      "preservation_score": 1.4972128702924959e-05
    },
    {
      "segment": 81,
      "difficulty": 22.52518059855521,
      "position": 78720,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 153,
      "preservation_score": 5.561076375372128e-05
    },
    {
      "segment": 82,
      "difficulty": 40.18017543859649,
      "position": 79628,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 190,
      "preservation_score": 3.676192315450324e-05
    },
    {
      "segment": 83,
      "difficulty": 26.606451612903225,
      "position": 80676,
      "chapter": 5,
      "main_theme": "ciencia",
      "word_count": 155,
      "preservation_score": 0.0002406234970112939
    },
    {
      "segment": 84,
      "difficulty": 38.3984126984127,
      "position": 81675,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 189,
      "preservation_score": 1.263273359309293e-05
    },
    {
      "segment": 85,
      "difficulty": 23.901520036849377,
      "position": 82748,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 167,
      "preservation_score": 0.0001122909652719372
    },
    {
      "segment": 86,
      "difficulty": 25.59375,
      "position": 83748,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 144,
      "preservation_score": 0.00017324891784813165
    },
    {
      "segment": 87,
      "difficulty": 24.90562130177515,
      "position": 84667,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 169,
      "preservation_score": 0.00017645723114161557
    },
    {
      "segment": 88,
      "difficulty": 29.802555248618784,
      "position": 85667,
      "chapter": 5,
      "main_theme": "filosofia",
      "word_count": 181,
      "preservation_score": 0.00011135520722800439
    },
    {
      "segment": 89,
      "difficulty": 25.157562724014337,
      "position": 86755,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 155,
      "preservation_score": 0.00010266602539148543
    },
    {
      "segment": 90,
      "difficulty": 26.00526315789474,
      "position": 87717,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 171,
      "preservation_score": 0.00011122152750744256
    },
    {
      "segment": 91,
      "difficulty": 27.455113636363635,
      "position": 88660,
      "chapter": 5,
      "main_theme": "filosofia",
      "word_count": 176,
      "preservation_score": 8.983277221754977e-05
    },
    {
      "segment": 92,
      "difficulty": 27.22239382239382,
      "position": 89660,
      "chapter": 5,
      "main_theme": "filosofia",
      "word_count": 148,
      "preservation_score": 7.532852253659121e-05
    },
    {
      "segment": 93,
      "difficulty": 24.21720195971693,
      "position": 90562,
      "chapter": 5,
      "main_theme": "ciencia",
      "word_count": 167,
      "preservation_score": 0.00014704769261801297
    },
    {
      "segment": 94,
      "difficulty": 22.529152376286135,
      "position": 91620,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 157,
      "preservation_score": 0.0003275153153764835
    },
    {
      "segment": 95,
      "difficulty": 24.053551912568306,
      "position": 92553,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 183,
      "preservation_score": 0.0002502484368917457
    },
    {
      "segment": 96,
      "difficulty": 40.43333333333334,
      "position": 93594,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 171,
      "preservation_score": 2.8874819641355277e-05
    },
    {
      "segment": 97,
      "difficulty": 22.84403500690926,
      "position": 94587,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 167,
      "preservation_score": 0.00021174867736993867
    },
    {
      "segment": 98,
      "difficulty": 25.16045321637427,
      "position": 95559,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 152,
      "preservation_score": 0.0001515928031171152
    },
    {
      "segment": 99,
      "difficulty": 32.21612903225807,
      "position": 96507,
      "chapter": 5,
      "main_theme": "filosofia",
      "word_count": 155,
      "preservation_score": 3.843291966152611e-05
    },
    {
      "segment": 100,
      "difficulty": 23.56149732620321,
      "position": 97502,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 153,
      "preservation_score": 0.00014704769261801297
    },
    {
      "segment": 101,
      "difficulty": 25.867332002661342,
      "position": 98415,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 167,
      "preservation_score": 0.00010854793309620596
    },
    {
      "segment": 102,
      "difficulty": 22.892447552447553,
      "position": 99415,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 165,
      "preservation_score": 0.00033687289581581145
    },
    {
      "segment": 103,
      "difficulty": 31.701999999999998,
      "position": 100381,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 150,
      "preservation_score": 2.2458193054387435e-05
    },
    {
      "segment": 104,
      "difficulty": 30.33152610441767,
      "position": 101287,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 166,
      "preservation_score": 4.010391616854898e-05
    },
    {
      "segment": 105,
      "difficulty": 34.05477832512315,
      "position": 102287,
      "chapter": 5,
      "main_theme": "ciencia",
      "word_count": 145,
      "preservation_score": 4.5985823873269514e-05
    },
    {
      "segment": 106,
      "difficulty": 27.307568590350048,
      "position": 103222,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 151,
      "preservation_score": 5.293716934248467e-05
    },
    {
      "segment": 107,
      "difficulty": 23.39909090909091,
      "position": 104147,
      "chapter": 5,
      "main_theme": "filosofia",
      "word_count": 150,
      "preservation_score": 0.0002259187277494927
    },
    {
      "segment": 108,
      "difficulty": 24.892982456140352,
      "position": 105058,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 171,
      "preservation_score": 0.00014036370658992146
    },
    {
      "segment": 109,
      "difficulty": 24.685034013605442,
      "position": 106026,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 147,
      "preservation_score": 0.00013535071706885285
    },
    {
      "segment": 110,
      "difficulty": 27.104444444444447,
      "position": 106929,
      "chapter": 5,
      "main_theme": "ciencia",
      "word_count": 150,
      "preservation_score": 5.293716934248467e-05
    },
    {
      "segment": 111,
      "difficulty": 30.3,
      "position": 107915,
      "chapter": 5,
      "main_theme": "filosofia",
      "word_count": 134,
      "preservation_score": 0.00017358311714953624
    },
    {
      "segment": 112,
      "difficulty": 32.1658064516129,
      "position": 108861,
      "chapter": 5,
      "main_theme": "arte",
      "word_count": 155,
      "preservation_score": 2.352763081888208e-05
    },
    {
      "segment": 113,
      "difficulty": 24.002348993288592,
      "position": 109832,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 149,
      "preservation_score": 0.00017324891784813162
    },
    {
      "segment": 114,
      "difficulty": 21.582088565763385,
      "position": 110767,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 178,
      "preservation_score": 0.0008879007039716746
    },
    {
      "segment": 115,
      "difficulty": 25.909183673469386,
      "position": 111803,
      "chapter": 5,
      "main_theme": "arte",
      "word_count": 147,
      "preservation_score": 0.0001582767891452067
    },
    {
      "segment": 116,
      "difficulty": 29.01616766467066,
      "position": 112725,
      "chapter": 5,
      "main_theme": "ciencia",
      "word_count": 167,
      "preservation_score": 0.00024730748303938545
    },
    {
      "segment": 117,
      "difficulty": 27.558441558441558,
      "position": 113751,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 154,
      "preservation_score": 2.6067545509556844e-05
    },
    {
      "segment": 118,
      "difficulty": 23.851923076923075,
      "position": 114711,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 156,
      "preservation_score": 0.00014076474575160696
    },
    {
      "segment": 119,
      "difficulty": 35.07258064516129,
      "position": 115692,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 186,
      "preservation_score": 4.6787902196640486e-05
    },
    {
      "segment": 120,
      "difficulty": 22.47905150753769,
      "position": 116735,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 199,
      "preservation_score": 0.00033687289581581145
    },
    {
      "segment": 121,
      "difficulty": 27.271026011560693,
      "position": 117787,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 173,
      "preservation_score": 6.73745791631623e-05
    },
    {
      "segment": 122,
      "difficulty": 38.519999999999996,
      "position": 118737,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 165,
      "preservation_score": 0.0
    },
    {
      "segment": 123,
      "difficulty": 28.159070990359332,
      "position": 119737,
      "chapter": 5,
      "main_theme": "ciencia",
      "word_count": 163,
      "preservation_score": 0.00010480490092047472
    },
    {
      "segment": 124,
      "difficulty": 34.68524590163935,
      "position": 120693,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 183,
      "preservation_score": 4.845889870366336e-05
    },
    {
      "segment": 125,
      "difficulty": 36.26910994764398,
      "position": 121727,
      "chapter": 5,
      "main_theme": "filosofia",
      "word_count": 191,
      "preservation_score": 9.624939880451758e-06
    },
    {
      "segment": 126,
      "difficulty": 33.540000000000006,
      "position": 122727,
      "chapter": 5,
      "main_theme": "filosofia",
      "word_count": 170,
      "preservation_score": 2.459706858337672e-05
    },
    {
      "segment": 127,
      "difficulty": 32.41121212121212,
      "position": 123718,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 165,
      "preservation_score": 6.456730503136388e-05
    },
    {
      "segment": 128,
      "difficulty": 36.47222222222222,
      "position": 124718,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 162,
      "preservation_score": 1.4437409820677639e-05
    },
    {
      "segment": 129,
      "difficulty": 36.38219895287958,
      "position": 125677,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 191,
      "preservation_score": 2.780538187686064e-05
    },
    {
      "segment": 130,
      "difficulty": 35.11476510067114,
      "position": 126753,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 149,
      "preservation_score": 1.47047692618013e-06
    },
    {
      "segment": 131,
      "difficulty": 32.85776397515528,
      "position": 127661,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 161,
      "preservation_score": 3.7430321757312396e-05
    },
    {
      "segment": 132,
      "difficulty": 36.5158940397351,
      "position": 128661,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 151,
      "preservation_score": 4.27775105797856e-06
    },
    {
      "segment": 133,
      "difficulty": 33.82890173410404,
      "position": 129578,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 173,
      "preservation_score": 1.6041566467419597e-05
    },
    {
      "segment": 134,
      "difficulty": 36.505421686746985,
      "position": 130578,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 166,
      "preservation_score": 9.223900718766269e-06
    },
    {
      "segment": 135,
      "difficulty": 36.425862068965515,
      "position": 131578,
      "chapter": 5,
      "main_theme": "ciencia",
      "word_count": 174,
      "preservation_score": 0.0
    },
    {
      "segment": 136,
      "difficulty": 37.400999999999996,
      "position": 132578,
      "chapter": 5,
      "main_theme": "ciencia",
      "word_count": 150,
      "preservation_score": 1.3234292335621167e-05
    },
    {
      "segment": 137,
      "difficulty": 36.54259259259259,
      "position": 133494,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 162,
      "preservation_score": 2.2725552495511095e-06
    },
    {
      "segment": 138,
      "difficulty": 36.5462962962963,
      "position": 134494,
      "chapter": 5,
      "main_theme": "ciencia",
      "word_count": 162,
      "preservation_score": 1.1229096527193718e-05
    },
    {
      "segment": 139,
      "difficulty": 36.407303370786515,
      "position": 135494,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 178,
      "preservation_score": 2.085403640764548e-05
    },
    {
      "segment": 140,
      "difficulty": 36.404216867469884,
      "position": 136512,
      "chapter": 5,
      "main_theme": "arte",
      "word_count": 166,
      "preservation_score": 4.545110499102219e-06
    },
    {
      "segment": 141,
      "difficulty": 32.069736842105264,
      "position": 137458,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 152,
      "preservation_score": 2.00519580842745e-05
    },
    {
      "segment": 142,
      "difficulty": 36.425862068965515,
      "position": 138458,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 174,
      "preservation_score": 0.0
    },
    {
      "segment": 143,
      "difficulty": 34.00571428571429,
      "position": 139458,
      "chapter": 5,
      "main_theme": "ciencia",
      "word_count": 175,
      "preservation_score": 1.2833253173935679e-05
    },
    {
      "segment": 144,
      "difficulty": 36.45438596491228,
      "position": 140458,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 171,
      "preservation_score": 0.0
    },
    {
      "segment": 145,
      "difficulty": 40.50727272727273,
      "position": 141458,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 165,
      "preservation_score": 5.614548263596859e-06
    },
    {
      "segment": 146,
      "difficulty": 38.54311377245509,
      "position": 142458,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 167,
      "preservation_score": 9.624939880451756e-06
    },
    {
      "segment": 147,
      "difficulty": 32.567499999999995,
      "position": 143490,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 160,
      "preservation_score": 5.0129895210686234e-05
    },
    {
      "segment": 148,
      "difficulty": 27.94065934065934,
      "position": 144490,
      "chapter": 5,
      "main_theme": "filosofia",
      "word_count": 182,
      "preservation_score": 0.00011549927856542111
    },
    {
      "segment": 149,
      "difficulty": 32.93333333333333,
      "position": 145557,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 162,
      "preservation_score": 8.421822395395286e-05
    },
    {
      "segment": 150,
      "difficulty": 36.45438596491228,
      "position": 146554,
      "chapter": 5,
      "main_theme": "arte",
      "word_count": 171,
      "preservation_score": 2.2725552495511095e-06
    },
    {
      "segment": 151,
      "difficulty": 38.449122807017545,
      "position": 147554,
      "chapter": 5,
      "main_theme": "none",
      "word_count": 171,
      "preservation_score": 4.411430778540389e-06
    },
    {
      "segment": 152,
      "difficulty": 36.44852071005917,
      "position": 148554,
      "chapter": 5,
      "main_theme": "ciencia",
      "word_count": 169,
      "preservation_score": 7.218704910338818e-06
    }
  ],
  "segments": [
    {
      "id": 1,
      "text": "Paradoxo dos movimentos\\n\\nPrefácio \\n\\nExistência de tudo!!\\n\\nTudo em nosso universo partiu de um movimento e qual foi esse movimento?\\n\\nPara que teve esse movimento?\\n\\nQual é a força desse movimento?\\n\\nPara qual direção foi esse movimento?",
      "position": 0,
      "chapter": 2,
      "page": 1,
      "segment_type": "preserved_segment",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 20.24054054054054,
      "complexity_metrics": {
        "word_count": 37,
        "sentence_count": 5,
        "paragraph_count": 7,
        "avg_sentence_length": 7.4,
        "avg_word_length": 5.135135135135135,
        "unique_word_ratio": 0.7567567567567568,
        "avg_paragraph_length": 5.285714285714286,
        "punctuation_density": 0.16216216216216217,
        "line_break_count": 12,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "movimento",
          "qual",
          "esse",
          "tudo",
          "paradoxo",
          "movimentos",
          "prefácio",
          "existência",
          "nosso",
          "universo",
          "partiu",
          "teve",
          "força",
          "desse",
          "direção"
        ],
        "entities": [
          [
            "Prefácio \\n\\nExistência de tudo",
            "ORG"
          ],
          [
            "Tudo",
            "PERSON"
          ]
        ],
        "readability_score": 94.75945945945946,
        "semantic_density": 0,
        "word_count": 37,
        "unique_words": 28,
        "lexical_diversity": 0.7567567567567568
      },
      "preservation_score": 1.684364479079058e-05
    },
    {
      "id": 2,
      "text": "\\n\\n\\n\\nQual é a diferença da matemática quântica e a matemática de exatas?\\n\\nQual é a diferença do cálculo dos movimentos quântico (propagação) e o cálculo dos movimentos físico(ciclo)?\\n\\nTudo que existe no universo é semelhante a tudo que existe no universo, porém somos um próprio universo imaginário de movimentos necessários a serem feitos proporcionais ao nosso próprio imaginar e executar no nosso espaço tempo.\\n\\nIrei imaginar um vácuo, um vazio, “Deus estava enjoado da sua rotina”, um nada que é alguma coisa e essa coisa se sentiu esmagado, pressionado, preso e queria sair desse incômodo, queria tanto, que gerou um grande movimento inicial e esse movimento têm uma direção que ninguém consegue parar a trajetória de tanta força feita para sair desse casulo. Ao gerar esse movimento reto para algum lado em 360° vezes 360° , ele não esperava criar uma reação oposta e reta para a direção oposta e voltando a se encontrar no trajeto(triângulo) sempre proporcional ao seu próprio movimento. \\n\\n",
      "position": 233,
      "chapter": 3,
      "page": 1,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 32.727777777777774,
      "complexity_metrics": {
        "word_count": 162,
        "sentence_count": 5,
        "paragraph_count": 4,
        "avg_sentence_length": 32.4,
        "avg_word_length": 5.092592592592593,
        "unique_word_ratio": 0.6358024691358025,
        "avg_paragraph_length": 40.5,
        "punctuation_density": 0.08641975308641975,
        "line_break_count": 12,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "movimento",
          "movimentos",
          "universo",
          "próprio",
          "qual",
          "diferença",
          "matemática",
          "cálculo",
          "tudo",
          "existe",
          "nosso",
          "imaginar",
          "coisa",
          "queria",
          "sair",
          "desse",
          "esse",
          "direção",
          "oposta",
          "quântica"
        ],
        "entities": [
          [
            "Tudo",
            "PERSON"
          ],
          [
            "universo imaginário de movimentos",
            "ORG"
          ],
          [
            "Deus",
            "PERSON"
          ],
          [
            "nada",
            "ORG"
          ],
          [
            "tanto",
            "GPE"
          ],
          [
            "têm uma direção",
            "ORG"
          ],
          [
            "para algum lado em 360",
            "PERSON"
          ]
        ],
        "readability_score": 82.27222222222223,
        "semantic_density": 0,
        "word_count": 162,
        "unique_words": 103,
        "lexical_diversity": 0.6358024691358025
      },
      "preservation_score": 3.5291446228323116e-05
    },
    {
      "id": 3,
      "text": "Aí irmão, fudeu!\\n\\n Surgiram vários problemas sinistros, tão sinistro que têm quase 14 bilhões de anos aproximadamente e ainda têm muito tempo pela frente e espaço, dentro desse espaço, criaram outros movimentos e cada um com o seu movimento triangular dentro dos próprios ciclos para conseguir sobreviver e resolver ali no seu espaço tempo, porém com todas as dificuldades de conseguir se movimentar entre várias linhas que se esbarravam toda hora sem querer, até que, eles perceberam que por mais que fossem para um lado, alguém vinha e esbarravam pelo o outro lado, por mais que eu tente sair daqui, eu não consigo sair dessa direção e tudo que eu faço, cria uma interferência quântica (tempo que demora a adaptação de uma ação e reação) entre o entrelaçamento quântico (semelhante a várias linhas entrelaçadas em uma proporção incalculável), um interferindo na linha do outro até criar um sincronismo com o movimento inicial (singularidade).\\n\\n",
      "position": 1229,
      "chapter": 3,
      "page": 2,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.549019607843135,
      "complexity_metrics": {
        "word_count": 153,
        "sentence_count": 2,
        "paragraph_count": 2,
        "avg_sentence_length": 76.5,
        "avg_word_length": 5.163398692810458,
        "unique_word_ratio": 0.7058823529411765,
        "avg_paragraph_length": 76.5,
        "punctuation_density": 0.0915032679738562,
        "line_break_count": 4,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "tempo",
          "espaço",
          "dentro",
          "movimento",
          "conseguir",
          "entre",
          "várias",
          "linhas",
          "esbarravam",
          "mais",
          "lado",
          "outro",
          "sair",
          "irmão",
          "fudeu",
          "surgiram",
          "vários",
          "problemas",
          "sinistros",
          "sinistro"
        ],
        "entities": [
          [
            "Surgiram",
            "ORG"
          ],
          [
            "problemas sinistros",
            "ORG"
          ],
          [
            "tão",
            "ORG"
          ],
          [
            "14",
            "CARDINAL"
          ],
          [
            "ainda",
            "ORG"
          ],
          [
            "têm muito",
            "ORG"
          ],
          [
            "pela frente e",
            "PERSON"
          ],
          [
            "criaram outros movimentos",
            "PERSON"
          ],
          [
            "sobreviver",
            "GPE"
          ],
          [
            "várias linhas que",
            "PERSON"
          ]
        ],
        "readability_score": 60.200980392156865,
        "semantic_density": 0,
        "word_count": 153,
        "unique_words": 108,
        "lexical_diversity": 0.7058823529411765
      },
      "preservation_score": 5.347188822473199e-06
    },
    {
      "id": 4,
      "text": "“Estudei tudo aquilo que eu pensava como caos quando estava em depressão quando só se teve amor.”\\n\\nPercebi o quão necessário é ensinarmos a outros humanos movimentar-se em concordância um para com o outro. \\n\\n“De nada adianta fazer o melhor para a humanidade se a humanidade não está me fazendo bem, querer ter fama, dinheiro, ser reconhecido, sexo, amigos e querer ter o que não é para ter ou ser. “\\n\\nEsses são alguns dos caminhos propícios a perder o próprio viver, esse questionamento que me faz entender e perceber o quão é necessário me permanecer com as conquistas que eu já conquistei, assim, agrego os valores necessários de acordo com a necessidade do meu próprio entorno para um viver melhor em sociedade e devido a essa forma de ver a vida, criei 2 teorias. \\n\\nExatas - Teoria de 1 átomo em movimento de singularidade onde temos o relógio (tempo é a marcação da propagação da energia), símbolos dos zodíacos, estrela de Davi e outras teorias do movimento de si próprio e esse movimento quand",
      "position": 2175,
      "chapter": 3,
      "page": 3,
      "segment_type": "preserved_segment",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 40.00571428571429,
      "complexity_metrics": {
        "word_count": 175,
        "sentence_count": 5,
        "paragraph_count": 5,
        "avg_sentence_length": 35.0,
        "avg_word_length": 4.685714285714286,
        "unique_word_ratio": 0.6685714285714286,
        "avg_paragraph_length": 35.0,
        "punctuation_density": 0.08571428571428572,
        "line_break_count": 8,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "próprio",
          "movimento",
          "quando",
          "quão",
          "necessário",
          "melhor",
          "humanidade",
          "querer",
          "viver",
          "esse",
          "teorias",
          "estudei",
          "tudo",
          "aquilo",
          "pensava",
          "como",
          "caos",
          "estava",
          "depressão",
          "teve"
        ],
        "entities": [
          [
            "que eu pensava",
            "PERSON"
          ],
          [
            "quando estava",
            "PERSON"
          ],
          [
            "depressão",
            "GPE"
          ],
          [
            "quando só se teve amor",
            "PERSON"
          ],
          [
            "Percebi",
            "ORG"
          ],
          [
            "necessário é",
            "PERSON"
          ],
          [
            "fazer o melhor",
            "ORG"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "que eu já conquistei",
            "PERSON"
          ]
        ],
        "readability_score": 81.09428571428572,
        "semantic_density": 0,
        "word_count": 175,
        "unique_words": 117,
        "lexical_diversity": 0.6685714285714286
      },
      "preservation_score": 3.07463357292209e-05
    },
    {
      "id": 5,
      "text": "o se têm uma falha, geram outras falhas e outros cálculos em termos um novo padrão, até chegar ao padrão da falha inicial e são essas falhas que me fizeram criar uma outra teoria. \\n\\nPropagação – Varias energias em movimentos perfeitos onde as mesmas podem ser de qualquer tamanho e escala no espaço tempo e em singularidade. Podemos encaixar outros movimentos fora do padrão em um padrão, sabendo que: essa situação só pode ser corrigida sabendo todos os inícios ou motivos para conseguir criar a perfeição, até porque, algo que já existe é mais difícil de controlar, assim é melhor deixarmos esses problemas serem resolvidas por “aqueles que as criou.”\\n\\nExplico as duas teorias no meu livro Caos do passado sendo vívido no futuro (explicação em captação quântica) e os demais livros, são os nossos movimentos executados de uma forma relativa e interpretativa de cada um.\\n\\nDentro dessas duas teorias, todas as teorias servem para agregar, auxiliar e interpretar o destino a ser seguido.",
      "position": 3175,
      "chapter": 3,
      "page": 4,
      "segment_type": "preserved_segment",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 40.99817073170732,
      "complexity_metrics": {
        "word_count": 164,
        "sentence_count": 5,
        "paragraph_count": 4,
        "avg_sentence_length": 32.8,
        "avg_word_length": 4.9939024390243905,
        "unique_word_ratio": 0.7317073170731707,
        "avg_paragraph_length": 41.0,
        "punctuation_density": 0.09146341463414634,
        "line_break_count": 6,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "padrão",
          "movimentos",
          "teorias",
          "falha",
          "falhas",
          "outros",
          "criar",
          "sabendo",
          "duas",
          "geram",
          "outras",
          "cálculos",
          "termos",
          "novo",
          "chegar",
          "inicial",
          "essas",
          "fizeram",
          "outra",
          "teoria"
        ],
        "entities": [
          [
            "novo padrão",
            "PERSON"
          ],
          [
            "mesmas podem",
            "PERSON"
          ],
          [
            "ser de qualquer",
            "ORG"
          ],
          [
            "Podemos",
            "ORG"
          ],
          [
            "outros movimentos",
            "PERSON"
          ],
          [
            "essa situação",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "mais difícil de controlar",
            "PERSON"
          ],
          [
            "melhor deixarmos",
            "PERSON"
          ],
          [
            "problemas serem",
            "PERSON"
          ]
        ],
        "readability_score": 82.10182926829268,
        "semantic_density": 0,
        "word_count": 164,
        "unique_words": 120,
        "lexical_diversity": 0.7317073170731707
      },
      "preservation_score": 1.5239488144048618e-05
    },
    {
      "id": 6,
      "text": " Podemos implementar arquétipos platônicos, Fibonacci, cristal do tempo (átomos sendo comprimidos até ficar em singularidade), darwinismo quântico, Tesla, Einstein, Sócrates, todas as formas de captação religiosa e tudo que contém movimento.\\n\\n“Aqui eu digo: tudo que contém matéria, física e tudo que existe, contém vida.”\\n\\n Logo eu percebo que a diferença entre nós humanos e qualquer coisa existente é conseguir interpretar o fim. Tudo que existe precisa da morte para a vida consumir e todos os nossos movimentos são necessários passa por caos e adaptar-se, dentro dessa adaptação caótica contém “registros” de DNA, gravidade, forças, física, física quântica e todas as energias existente no universo.\\n\\n  Quando ocorreu o início do universo, sua origem teve uma grande liberação de energia e essa energia veio derivada de um grande movimento inicial, qual é o valor desse movimento inicial e quanto tempo leva para ele adaptar-se? \\n\\n",
      "position": 4161,
      "chapter": 3,
      "page": 5,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 31.044755244755244,
      "complexity_metrics": {
        "word_count": 143,
        "sentence_count": 5,
        "paragraph_count": 4,
        "avg_sentence_length": 28.6,
        "avg_word_length": 5.4825174825174825,
        "unique_word_ratio": 0.7622377622377622,
        "avg_paragraph_length": 35.75,
        "punctuation_density": 0.15384615384615385,
        "line_break_count": 8,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "tudo",
          "contém",
          "movimento",
          "física",
          "tempo",
          "todas",
          "existe",
          "vida",
          "existente",
          "adaptar",
          "universo",
          "grande",
          "energia",
          "inicial",
          "podemos",
          "implementar",
          "arquétipos",
          "platônicos",
          "fibonacci",
          "cristal"
        ],
        "entities": [
          [
            "Podemos",
            "ORG"
          ],
          [
            "platônicos",
            "GPE"
          ],
          [
            "Fibonacci",
            "GPE"
          ],
          [
            "darwinismo quântico",
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
            "Sócrates",
            "GPE"
          ],
          [
            "todas",
            "PERSON"
          ],
          [
            "formas de captação religiosa e tudo que",
            "ORG"
          ],
          [
            "Aqui eu",
            "PERSON"
          ]
        ],
        "readability_score": 84.05524475524476,
        "semantic_density": 0,
        "word_count": 143,
        "unique_words": 109,
        "lexical_diversity": 0.7622377622377622
      },
      "preservation_score": 3.2083132934839193e-05
    },
    {
      "id": 7,
      "text": "Assim percebo que o movimento inicial é o movimento que controla todo universo em adaptar-se e ir rumo ao apocalipse bíblico (fim do amor) que é a singularidade.\\n\\n Qual é a quantidade de caos no universo? \\n\\nDentro desses movimentos de adaptação qual é a energia de maior força: Universo, galáxia, sistema solar, Terra ou humanos?\\n\\nQuem precisa se adaptar para viver: nós humanos ou o universo adaptar a nós humanos?\\n\\n   “Todos nós seguimos o nosso próprio livre arbítrio dentro de um sistema construído pela necessidade de sobrevivência da espécie.”\\n\\n   Antes mesmo de sermos sentimentais, nós provemos de vários tipos de espécies humanas e cada uma continha um tipo de empatia e instinto de sobrevivência proporcional as suas necessidades territoriais, suas peculiaridades e a sua forma de agir perante as dificuldades e é devido a essa forma de viver em adaptar-se aos territórios hostis, proporcional ao nosso próprio corpo e junto a necessidade de procriar, logo a necessidade de locomoção estilo",
      "position": 5097,
      "chapter": 3,
      "page": 6,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 33.969166666666666,
      "complexity_metrics": {
        "word_count": 160,
        "sentence_count": 6,
        "paragraph_count": 6,
        "avg_sentence_length": 26.666666666666668,
        "avg_word_length": 5.175,
        "unique_word_ratio": 0.65,
        "avg_paragraph_length": 26.666666666666668,
        "punctuation_density": 0.0875,
        "line_break_count": 10,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "universo",
          "adaptar",
          "humanos",
          "necessidade",
          "movimento",
          "qual",
          "dentro",
          "sistema",
          "viver",
          "nosso",
          "próprio",
          "sobrevivência",
          "proporcional",
          "suas",
          "forma",
          "assim",
          "percebo",
          "inicial",
          "controla",
          "todo"
        ],
        "entities": [
          [
            "Universo",
            "GPE"
          ],
          [
            "galáxia",
            "ORG"
          ],
          [
            "universo adaptar",
            "ORG"
          ],
          [
            "Todos nós seguimos o",
            "WORK_OF_ART"
          ],
          [
            "livre arbítrio dentro",
            "PERSON"
          ],
          [
            "construído pela",
            "PERSON"
          ],
          [
            "Antes mesmo de sermos sentimentais",
            "WORK_OF_ART"
          ],
          [
            "nós provemos de vários",
            "ORG"
          ],
          [
            "forma de agir",
            "ORG"
          ],
          [
            "essa forma de viver",
            "PERSON"
          ]
        ],
        "readability_score": 85.11416666666666,
        "semantic_density": 0,
        "word_count": 160,
        "unique_words": 104,
        "lexical_diversity": 0.65
      },
      "preservation_score": 4.010391616854898e-05
    },
    {
      "id": 8,
      "text": " cigana e em pequenos grupos (família) ou ate mesmo grandes grupos ( povoado, aldeia, tribo, cidade, estado e pais) no intuito de melhorar a sobrevivência da própria raça humana. Nossa percepção com os novos achados sobre a adaptação humana em ter empatia e o mesmo desejo de sobreviver entre as espécies, nesse achado continham um homem, uma mulher e uma criança e ao examinar o DNA percebeu que um integrante provinha da espécie Homo Sapiens, e essa espécime, eram humanos mais agressivos e menos emotivos, o outro integrante provinha da espécime Homo Naledi, esses eram baixos e menos resistentes, porém continham afetos com empatia e entendia o valor da morte. Percebemos que ambas as espécies contém padrões e forma de sobreviver diferente e ao juntarmos, entendemos quem era o terceiro membro da família, assim comprovamos que existiram humanos híbridos. \\n\\nO período vivido entre várias espécies humanas ocorreram muitas mudanças climáticas, muitas mudanças em adaptar-se e durante um período m",
      "position": 6097,
      "chapter": 3,
      "page": 7,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.45801886792453,
      "complexity_metrics": {
        "word_count": 159,
        "sentence_count": 4,
        "paragraph_count": 2,
        "avg_sentence_length": 39.75,
        "avg_word_length": 5.276729559748428,
        "unique_word_ratio": 0.6981132075471698,
        "avg_paragraph_length": 79.5,
        "punctuation_density": 0.1069182389937107,
        "line_break_count": 2,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "espécies",
          "grupos",
          "família",
          "mesmo",
          "humana",
          "empatia",
          "sobreviver",
          "entre",
          "continham",
          "integrante",
          "provinha",
          "homo",
          "espécime",
          "eram",
          "humanos",
          "menos",
          "período",
          "muitas",
          "mudanças",
          "cigana"
        ],
        "entities": [
          [
            "raça humana",
            "PERSON"
          ],
          [
            "Nossa",
            "PERSON"
          ],
          [
            "mesmo desejo de sobreviver",
            "ORG"
          ],
          [
            "Homo Sapiens",
            "PERSON"
          ],
          [
            "Homo Naledi",
            "PERSON"
          ],
          [
            "Percebemos",
            "PERSON"
          ],
          [
            "forma de sobreviver",
            "PERSON"
          ],
          [
            "entendemos quem era o terceiro membro da família",
            "PERSON"
          ],
          [
            "climáticas",
            "GPE"
          ]
        ],
        "readability_score": 78.54198113207548,
        "semantic_density": 0,
        "word_count": 159,
        "unique_words": 111,
        "lexical_diversity": 0.6981132075471698
      },
      "preservation_score": 2.94095385236026e-06
    },
    {
      "id": 9,
      "text": "uito longo para estudar e termos informações, assim percebo que o entender e interpretar a nossa evolução, contém muitas lacunas e fragmentos a serem desvendados assim vejo que a nossa percepção sobre as espécies são especulativas, imaginativas, intuitivas e interpretativas perante a um padrão dos costumes e dos acontecimentos da própria espécie humana.          \\n\\nIrei me imaginar usando o meu instinto de sobrevivência humana junto ao instinto de sobrevivência animal, vejamos os cachorros de raça e os famosos vira latas, o primeiro provém de uma linhagem de DNA e o outro dê um entrelaçamento quântico entre as raças, assim eu correlaciono nós humanos sem entender e compreender o nosso próprio sentir o desejo, carinho, necessidade, afeto, sexo e tudo aquilo que esquecemos de sentir em sermos o melhor amigo do humano.\\n\\nPercebo que as espécies humanas continham impulsos perante a própria necessidade corpórea como um cachorro da raça pitbull não sabendo doutrinar, criar, educar, direcionar ",
      "position": 7097,
      "chapter": 3,
      "page": 8,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.62467532467532,
      "complexity_metrics": {
        "word_count": 154,
        "sentence_count": 3,
        "paragraph_count": 3,
        "avg_sentence_length": 51.333333333333336,
        "avg_word_length": 5.415584415584416,
        "unique_word_ratio": 0.7142857142857143,
        "avg_paragraph_length": 51.333333333333336,
        "punctuation_density": 0.1038961038961039,
        "line_break_count": 4,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "assim",
          "percebo",
          "entender",
          "nossa",
          "espécies",
          "perante",
          "própria",
          "humana",
          "instinto",
          "sobrevivência",
          "raça",
          "sentir",
          "necessidade",
          "uito",
          "longo",
          "estudar",
          "termos",
          "informações",
          "interpretar",
          "evolução"
        ],
        "entities": [
          [
            "uito longo para estudar",
            "PERSON"
          ],
          [
            "lacunas e fragmentos",
            "PERSON"
          ],
          [
            "vejo",
            "ORG"
          ],
          [
            "da própria",
            "PERSON"
          ],
          [
            "espécie humana",
            "PERSON"
          ],
          [
            "cachorros de raça e os",
            "ORG"
          ],
          [
            "famosos vira latas",
            "PERSON"
          ],
          [
            "primeiro provém de uma linhagem de DNA e o",
            "ORG"
          ],
          [
            "assim eu correlaciono",
            "PERSON"
          ],
          [
            "desejo",
            "ORG"
          ]
        ],
        "readability_score": 72.708658008658,
        "semantic_density": 0,
        "word_count": 154,
        "unique_words": 110,
        "lexical_diversity": 0.7142857142857143
      },
      "preservation_score": 6.416626586967839e-06
    },
    {
      "id": 10,
      "text": "torna-se agressiva e o instinto animal exaltado, assim percebo que na natureza tudo evolui de acordo com a própria necessidade de adaptação perante ao próprio viver com afeto ou sem afeto.\\n\\n   Os animais que vivem em lugar que o tocar, fazer carinho, passar confiança, alimentar-se, procriar e necessário viver em harmonia com o ambiente e todos os seres que ali estão sobrevivendo e respeitando.\\n\\nVoltamos aos humanos, até porque, percebemos que o próprio afeto e a fraqueza humana é a adaptação evolutiva da própria espécie, já as palavras as quais usamos, não continham valores como peso entre as espécies, esse tipo de estrondo não era de dar medo assim os valores só serviam para aqueles que eram da família em ter uma boa sobrevivência, já aqueles humanos que não conseguiam arrumar uma fêmea por serem fracos ou menos astutos, eram esses que estupravam as fêmeas pela necessidade corpórea ou mental, assim ocasionando “vira latas humanos”.\\n\\n",
      "position": 8097,
      "chapter": 3,
      "page": 9,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.52322580645161,
      "complexity_metrics": {
        "word_count": 155,
        "sentence_count": 3,
        "paragraph_count": 3,
        "avg_sentence_length": 51.666666666666664,
        "avg_word_length": 5.077419354838709,
        "unique_word_ratio": 0.7096774193548387,
        "avg_paragraph_length": 51.666666666666664,
        "punctuation_density": 0.1032258064516129,
        "line_break_count": 6,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "assim",
          "afeto",
          "humanos",
          "própria",
          "necessidade",
          "adaptação",
          "próprio",
          "viver",
          "valores",
          "aqueles",
          "eram",
          "torna",
          "agressiva",
          "instinto",
          "animal",
          "exaltado",
          "percebo",
          "natureza",
          "tudo",
          "evolui"
        ],
        "entities": [
          [
            "agressiva e o instinto animal exaltado",
            "ORG"
          ],
          [
            "alimentar-se",
            "PERSON"
          ],
          [
            "Voltamos",
            "PRODUCT"
          ],
          [
            "da própria espécie",
            "PERSON"
          ],
          [
            "só serviam para aqueles",
            "PERSON"
          ],
          [
            "já aqueles humanos",
            "PERSON"
          ],
          [
            "serem fracos",
            "PERSON"
          ],
          [
            "vira latas",
            "PERSON"
          ]
        ],
        "readability_score": 72.64344086021505,
        "semantic_density": 0,
        "word_count": 155,
        "unique_words": 110,
        "lexical_diversity": 0.7096774193548387
      },
      "preservation_score": 1.2031174850564695e-05
    },
    {
      "id": 11,
      "text": "Temos aqueles que conseguiram encontrar uma fêmea e construir uma melhor estabilidade em sobreviver, e essa sensação nos dias de hoje “está mais fácil ganhar na mega sena que manter um casamento para a vida toda”, porém, essa preocupação e a necessidade de manter uma boa sobrevivência, foi gerando necessidades de se viver em coletivo, bando, tribo, aldeia, povoado e tudo que é necessário em termos cuidados com o nosso próprio sobreviver melhor. \\n\\nO registro de DNA mais antigo que contemos de nossa origem com uma maior semelhança é da espécime Australopitecos afarensis, esse fóssil foi batizado com o nome de Lucy e foi encontrado e datado que viveu aproximadamente 3,2 milhões e viveu no território da Etiópia e a partir dessa descoberta, começamos a investigar as pegadas humanas em suas fugas desesperadas por um planeta desconhecido e querendo viver na sobrevivência por ter uma grande quantidade dos mesmos ou pelas dificuldades territoriais.",
      "position": 9045,
      "chapter": 3,
      "page": 10,
      "segment_type": "preserved_segment",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 36.56666666666666,
      "complexity_metrics": {
        "word_count": 153,
        "sentence_count": 2,
        "paragraph_count": 2,
        "avg_sentence_length": 76.5,
        "avg_word_length": 5.222222222222222,
        "unique_word_ratio": 0.7254901960784313,
        "avg_paragraph_length": 76.5,
        "punctuation_density": 0.08496732026143791,
        "line_break_count": 2,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "melhor",
          "sobreviver",
          "essa",
          "mais",
          "manter",
          "sobrevivência",
          "viver",
          "viveu",
          "temos",
          "aqueles",
          "conseguiram",
          "encontrar",
          "fêmea",
          "construir",
          "estabilidade",
          "sensação",
          "dias",
          "hoje",
          "está",
          "fácil"
        ],
        "entities": [
          [
            "sobreviver",
            "GPE"
          ],
          [
            "bando",
            "GPE"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "Australopitecos",
            "PERSON"
          ],
          [
            "nome de Lucy",
            "PERSON"
          ],
          [
            "datado",
            "NORP"
          ],
          [
            "3,2",
            "CARDINAL"
          ],
          [
            "desconhecido e querendo",
            "PERSON"
          ]
        ],
        "readability_score": 60.18333333333333,
        "semantic_density": 0,
        "word_count": 153,
        "unique_words": 111,
        "lexical_diversity": 0.7254901960784313
      },
      "preservation_score": 2.0051958084274496e-06
    },
    {
      "id": 12,
      "text": " Com o aumento da própria espécie a migração foi se espalhando e ocorrendo mais conflitos nos territórios onde se encontravam muitos das mesmas espécies junto ao adaptar-se em territórios, a necessidade de adaptar-se era caótica e com muito amor, assim, aqueles que continham muito amor e muito caos migravam para novos países e novos continentes, através da “data início” percebemos que a migração (África) foi para Asia, Europa e onde conseguíamos sobreviver.\\n\\nApós milhares de anos aprendendo a sobreviver e aumentando a quantidade de seres humanos, provavelmente as espécies se acasalavam, protegiam e migravam em busca de segurança e alimentos. A última espécie que temos registros de vida sem ser humano moderno é do homem Neandertal, esses conviveram com a espécie moderna a qual o instinto de sobrevivência tornou-se instinto pela eternidade.\\n\\n   Assim percebemos que o próprio Planeta Terra tem a sua própria seleção natural daqueles que conseguem sobreviver melhor a própria histeria e ao p",
      "position": 9998,
      "chapter": 3,
      "page": 11,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.113461538461536,
      "complexity_metrics": {
        "word_count": 156,
        "sentence_count": 4,
        "paragraph_count": 3,
        "avg_sentence_length": 39.0,
        "avg_word_length": 5.378205128205129,
        "unique_word_ratio": 0.6794871794871795,
        "avg_paragraph_length": 52.0,
        "punctuation_density": 0.07051282051282051,
        "line_break_count": 4,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "própria",
          "espécie",
          "muito",
          "sobreviver",
          "migração",
          "territórios",
          "onde",
          "espécies",
          "adaptar",
          "amor",
          "assim",
          "migravam",
          "novos",
          "percebemos",
          "instinto",
          "aumento",
          "espalhando",
          "ocorrendo",
          "mais",
          "conflitos"
        ],
        "entities": [
          [
            "da própria",
            "PERSON"
          ],
          [
            "das mesmas",
            "PERSON"
          ],
          [
            "muito amor",
            "PERSON"
          ],
          [
            "muito amor",
            "PERSON"
          ],
          [
            "muito caos",
            "ORG"
          ],
          [
            "para novos",
            "PRODUCT"
          ],
          [
            "percebemos",
            "PERSON"
          ],
          [
            "África",
            "ORG"
          ],
          [
            "Asia",
            "LOC"
          ],
          [
            "Europa",
            "LOC"
          ]
        ],
        "readability_score": 78.88653846153846,
        "semantic_density": 0,
        "word_count": 156,
        "unique_words": 106,
        "lexical_diversity": 0.6794871794871795
      },
      "preservation_score": 7.218704910338818e-06
    },
    {
      "id": 13,
      "text": "aradoxo provinda do Universo, até porque, essa percepção só foi possível conseguir, por sermos um único ser em livre arbítrio com capacidade de inventar escrita, ferramenta, matemática, religião, filosofia, ciências e tudo aquilo que tornou-se necessário movimentar em concordância com o viver paralelo ao destino do Nosso Planeta Terra (singularidade)!!! \\n\\nEm um certo ponto da história temos um caso do acaso no Planeta Terra no Estreito de Bering onde exatamente o continente Europeu e as Américas ficam mais próximos um do outro, aproximadamente a 50 mil anos atrás formou-se um caminho de gelo que unia os dois continentes e como os humanos do velho continente estavam em crescimento desordenado a todo vapor, assim para onde o nariz apontava eles iam sem olhar para trás, dessa forma os humanos atravessaram entre os Oceanos pacífico e Ártico. Percebo que os continentes mais adaptados e em concordância dê um pensar semelhante a um sobreviver mais confortável com uma maior quantidade de humanos ali vivendo, com menos recursos proporcional ao próprio crescimento em um viver melhor.\\n\\n",
      "position": 10998,
      "chapter": 3,
      "page": 12,
      "segment_type": "preserved_segment",
      "themes": {
        "filosofia": 53.57142857142857,
        "ciencia": 46.42857142857144
      },
      "difficulty": 36.59941860465116,
      "complexity_metrics": {
        "word_count": 172,
        "sentence_count": 3,
        "paragraph_count": 2,
        "avg_sentence_length": 57.333333333333336,
        "avg_word_length": 5.3313953488372094,
        "unique_word_ratio": 0.7093023255813954,
        "avg_paragraph_length": 86.0,
        "punctuation_density": 0.09883720930232558,
        "line_break_count": 4,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "humanos",
          "concordância",
          "viver",
          "planeta",
          "terra",
          "onde",
          "continente",
          "continentes",
          "crescimento",
          "aradoxo",
          "provinda",
          "universo",
          "porque",
          "essa",
          "percepção",
          "possível",
          "conseguir",
          "sermos",
          "único"
        ],
        "entities": [
          [
            "aradoxo provinda",
            "PERSON"
          ],
          [
            "Universo",
            "GPE"
          ],
          [
            "único",
            "GPE"
          ],
          [
            "ferramenta, matemática, religião",
            "ORG"
          ],
          [
            "Nosso Planeta Terra",
            "ORG"
          ],
          [
            "da história",
            "PERSON"
          ],
          [
            "Américas",
            "GPE"
          ],
          [
            "50",
            "CARDINAL"
          ],
          [
            "iam sem",
            "PERSON"
          ],
          [
            "dessa forma",
            "PERSON"
          ]
        ],
        "readability_score": 69.73391472868217,
        "semantic_density": 0,
        "word_count": 172,
        "unique_words": 122,
        "lexical_diversity": 0.7093023255813954
      },
      "preservation_score": 5.614548263596859e-06
    },
    {
      "id": 14,
      "text": "Aqueles que atravessaram para a Asia se isolaram pela dificuldade de atravessar Os Montes Urais e aqueles que atravessaram se multiplicaram e povoaram com vontade, ate porque, “naquela época não existia televisão” e para suprir essa ausência era necessário uma grande adaptação em larga escala, assim surgiu o Budismo em guiar a achar o conforto no desconforto necessário entre a fome, assim o aprender a respirar para se concentrar no próprio corpo e esquecer da própria fome pela escassez em grande escala, tornava-se fanatismo em viver em um prol da fome que por muitas vezes o extremismo da religião, era se unir a uma arvore e ficar sem se mexer, para isso ocorrer, tomava pequenas quantidade dê um chá que os deixava “mumificado” junto a própria arvore, não podemos esquecer das posições que fazemos no yoga para melhorar o olhar, falar, equilibrar, acalmar, encontrar, aceitar o tédio e tudo que provém do autoconhecimento da própria histeria.\\n\\n",
      "position": 12090,
      "chapter": 3,
      "page": 13,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.52884615384615,
      "complexity_metrics": {
        "word_count": 156,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 156.0,
        "avg_word_length": 5.096153846153846,
        "unique_word_ratio": 0.6730769230769231,
        "avg_paragraph_length": 156.0,
        "punctuation_density": 0.09615384615384616,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "fome",
          "própria",
          "aqueles",
          "atravessaram",
          "pela",
          "necessário",
          "grande",
          "escala",
          "assim",
          "esquecer",
          "arvore",
          "asia",
          "isolaram",
          "dificuldade",
          "atravessar",
          "montes",
          "urais",
          "multiplicaram",
          "povoaram",
          "vontade"
        ],
        "entities": [
          [
            "Asia",
            "LOC"
          ],
          [
            "Montes Urais",
            "PERSON"
          ],
          [
            "naquela época não existia televisão",
            "ORG"
          ],
          [
            "suprir essa",
            "PERSON"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "assim surgiu",
            "PERSON"
          ],
          [
            "Budismo",
            "ORG"
          ],
          [
            "da própria",
            "PERSON"
          ],
          [
            "pela",
            "PERSON"
          ],
          [
            "tornava",
            "PERSON"
          ]
        ],
        "readability_score": 20.47115384615384,
        "semantic_density": 0,
        "word_count": 156,
        "unique_words": 105,
        "lexical_diversity": 0.6730769230769231
      },
      "preservation_score": 1.3367972056182997e-06
    },
    {
      "id": 15,
      "text": "O mar mediterrâneo junto ao deserto do Saara dificultava a Europa e África trocarem informações culturais em como sobreviver melhor entre nós, vós e eles, mesmo assim, após a maior necessidade de adaptação territorial acontecer no velho continente a limitação do território não foi o suficiente para combater a escravidão daqueles que vivam com menos intensidade com os próprios problemas.\\n\\nAqueles que se isolaram pelo próprio destino ser o que deveria ser formaram a América do Norte, Central e Sul, toda a cultura dos povos desses continentes que habitavam como grandes civilizações ou eram os mais evoluídos e adaptados ao território, foram pequenos quando aqueles mais antigos e mais adaptados a viver entre si, sabia como fazer uma boa estratégia com o próprio mal vivido e com essa sagacidade e experiência dizimaram os Maias, Incas, Astecas e todos aqueles que entravam no caminho da sobrevivência daqueles que provieram da experiência dê um viver.\\n\\n",
      "position": 13042,
      "chapter": 3,
      "page": 14,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.57450980392157,
      "complexity_metrics": {
        "word_count": 153,
        "sentence_count": 2,
        "paragraph_count": 2,
        "avg_sentence_length": 76.5,
        "avg_word_length": 5.248366013071895,
        "unique_word_ratio": 0.7320261437908496,
        "avg_paragraph_length": 76.5,
        "punctuation_density": 0.0718954248366013,
        "line_break_count": 4,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "como",
          "aqueles",
          "mais",
          "entre",
          "território",
          "daqueles",
          "próprio",
          "adaptados",
          "viver",
          "experiência",
          "mediterrâneo",
          "junto",
          "deserto",
          "saara",
          "dificultava",
          "europa",
          "áfrica",
          "trocarem",
          "informações",
          "culturais"
        ],
        "entities": [
          [
            "Saara dificultava",
            "PERSON"
          ],
          [
            "nós, vós e eles",
            "ORG"
          ],
          [
            "mesmo",
            "ORG"
          ],
          [
            "América",
            "PRODUCT"
          ],
          [
            "Norte",
            "PERSON"
          ],
          [
            "quando aqueles mais",
            "PERSON"
          ],
          [
            "Maias",
            "PERSON"
          ],
          [
            "Incas",
            "GPE"
          ],
          [
            "Astecas",
            "ORG"
          ]
        ],
        "readability_score": 60.17549019607843,
        "semantic_density": 0,
        "word_count": 153,
        "unique_words": 112,
        "lexical_diversity": 0.7320261437908496
      },
      "preservation_score": 2.94095385236026e-06
    },
    {
      "id": 16,
      "text": "“A vida humana se resume em termos empatia pelo semelhante como impulso em ser ou ter um sobreviver melhor que o meu.”   \\n\\nCapítulo 1\\n\\nA amizade, nem mesmo a força do tempo poderá destruir.\\n\\n“Meus ciclos de amizades é uma forma de cortar o caminho para uma nova amizade.”\\n\\n“Meu ciclo de amigos não têm futilidades em um aceitar o viver do outro, até porque, se tiver a futilidade de pensar algo ruim sem perguntar ao próprio, não é digno de ser meu amigo.”\\n\\nPalavras fortes e intensas, porém necessárias serem ditas, por mais que queira escrever lindas palavras em forma de poesia com pássaros cantando e a chuva caindo, acho chato e arcaico. Todos falamos de uma forma com os nossos amigos e família, no trabalho temos que ser mais educados e não modificados ao ponto de termos duas caras ou duas vidas, tudo é relativo de quanto esquecemos dos amigos e daqueles que amamos e no caminho de fazer, dar o melhor para os mesmos, mesmo assim brigamos uns com os outros sem saber o melhor para os outros,",
      "position": 14000,
      "chapter": 3,
      "page": 15,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 31.679189686924495,
      "complexity_metrics": {
        "word_count": 181,
        "sentence_count": 6,
        "paragraph_count": 6,
        "avg_sentence_length": 30.166666666666668,
        "avg_word_length": 4.486187845303867,
        "unique_word_ratio": 0.6685082872928176,
        "avg_paragraph_length": 30.166666666666668,
        "punctuation_density": 0.09392265193370165,
        "line_break_count": 10,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "melhor",
          "forma",
          "amigos",
          "termos",
          "amizade",
          "mesmo",
          "caminho",
          "palavras",
          "mais",
          "duas",
          "outros",
          "vida",
          "humana",
          "resume",
          "empatia",
          "pelo",
          "semelhante",
          "como",
          "impulso",
          "sobreviver"
        ],
        "entities": [
          [
            "pelo",
            "PERSON"
          ],
          [
            "sobreviver melhor que",
            "ORG"
          ],
          [
            "nem mesmo",
            "PERSON"
          ],
          [
            "Meus ciclos de amizades é uma forma de cortar o caminho",
            "WORK_OF_ART"
          ],
          [
            "nova",
            "LOC"
          ],
          [
            "Palavras",
            "PERSON"
          ],
          [
            "necessárias serem ditas",
            "PERSON"
          ],
          [
            "lindas palavras",
            "PERSON"
          ],
          [
            "forma de poesia",
            "ORG"
          ],
          [
            "acho chato e arcaico",
            "FAC"
          ]
        ],
        "readability_score": 83.5708103130755,
        "semantic_density": 0,
        "word_count": 181,
        "unique_words": 121,
        "lexical_diversity": 0.6685082872928176
      },
      "preservation_score": 4.611950359383134e-05
    },
    {
      "id": 17,
      "text": " direcionando, discutindo, debatendo e conversando tudo aquilo que pensamos que é melhor para o outro, sem saber o quanto o outro entendeu e interpretou aquela mensagem dita e como era para ser entendida. O mundo não será dominado por inteligentes ou sábios e sim por todos nós sermos ignorantes diante do meu próprio pensar, sem saber a capacidade mental dos outros pensarem e acompanharem a evolução daqueles que pensam que estão evoluindo, mas na verdade, estão acabando com o próprio tédio em pensar que está solucionando os problemas do planeta Terra, e esses ocorridos, provém com muitas discrepâncias de um pensar no futuro não vívido, com várias soluções desnecessárias para aqueles que pensam e tem as dificuldades semelhantes, e são esses pensamentos, preguiçosos e “evoluídos” que não deixam perceber o excesso de consumo junto ao tédio nós transformando em pessoas cheias de vícios e ganância dê um viver confortável, achando que a solução é em criar e não em adaptar-se, até porque, em n",
      "position": 15000,
      "chapter": 3,
      "page": 16,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.52926829268293,
      "complexity_metrics": {
        "word_count": 164,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 82.0,
        "avg_word_length": 5.097560975609756,
        "unique_word_ratio": 0.7012195121951219,
        "avg_paragraph_length": 164.0,
        "punctuation_density": 0.09146341463414634,
        "line_break_count": 0,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "pensar",
          "outro",
          "saber",
          "próprio",
          "pensam",
          "estão",
          "tédio",
          "esses",
          "direcionando",
          "discutindo",
          "debatendo",
          "conversando",
          "tudo",
          "aquilo",
          "pensamos",
          "melhor",
          "quanto",
          "entendeu",
          "interpretou",
          "aquela"
        ],
        "entities": [
          [
            "que pensamos",
            "PERSON"
          ],
          [
            "outro",
            "ORG"
          ],
          [
            "sem saber",
            "ORG"
          ],
          [
            "quanto o outro entendeu",
            "PERSON"
          ],
          [
            "aquela mensagem dita",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "nós sermos",
            "ORG"
          ],
          [
            "outros pensarem",
            "GPE"
          ],
          [
            "mas",
            "PERSON"
          ],
          [
            "estão acabando",
            "PERSON"
          ]
        ],
        "readability_score": 57.47073170731707,
        "semantic_density": 0,
        "word_count": 164,
        "unique_words": 115,
        "lexical_diversity": 0.7012195121951219
      },
      "preservation_score": 0.0
    },
    {
      "id": 18,
      "text": "ossas casas e em nossas empresas na maioria das vezes a solução é a diminuição dos gastos, e quando não conseguimos reduzir, os poucos que conseguem acompanhar ficam egoístas, solitários e invejados, também temos aqueles que não conseguem acompanhar e usam isso de uma forma para o próprio benefício ou benefício para uma pequena quantidade proporcional a quantidade de malefícios gerado.\\n\\n“Quando se têm Amigos, não precisamos pensar nesse texto acima, até porque, amigo que é amigo, cuida.”\\n\\nAs dificuldades de se manter uma amizade:\\n\\nInfância – são os amigos ninja e quando menos espera eles aparecem com um filho, esposa, separação, careca, implante, morto e outras coisas que a velhice vão nós trazendo.\\n\\nSolteiros – amigos para fazer “merda” e sempre dão um jeito de estar junto no momento da zoação e quando se é para bater uma laje faz um mocotó, feijoada, churrasco, futebol com crianças correndo, caindo de cara e todas aquelas coisas que os humanos são desastrados e engraçados.\\n\\n",
      "position": 16000,
      "chapter": 3,
      "page": 17,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.51472392638037,
      "complexity_metrics": {
        "word_count": 163,
        "sentence_count": 4,
        "paragraph_count": 5,
        "avg_sentence_length": 40.75,
        "avg_word_length": 5.049079754601227,
        "unique_word_ratio": 0.7116564417177914,
        "avg_paragraph_length": 32.6,
        "punctuation_density": 0.13496932515337423,
        "line_break_count": 10,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "quando",
          "amigos",
          "conseguem",
          "acompanhar",
          "benefício",
          "quantidade",
          "amigo",
          "coisas",
          "ossas",
          "casas",
          "nossas",
          "empresas",
          "maioria",
          "vezes",
          "solução",
          "diminuição",
          "gastos",
          "conseguimos",
          "reduzir",
          "poucos"
        ],
        "entities": [
          [
            "casas",
            "GPE"
          ],
          [
            "nossas empresas na maioria das",
            "ORG"
          ],
          [
            "quando não",
            "PERSON"
          ],
          [
            "também temos aqueles",
            "PERSON"
          ],
          [
            "usam isso de uma forma",
            "PERSON"
          ],
          [
            "benefício ou benefício",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "Amigos",
            "LOC"
          ],
          [
            "esposa",
            "PERSON"
          ],
          [
            "separação",
            "GPE"
          ]
        ],
        "readability_score": 78.11027607361963,
        "semantic_density": 0,
        "word_count": 163,
        "unique_words": 116,
        "lexical_diversity": 0.7116564417177914
      },
      "preservation_score": 4.344590918259474e-05
    },
    {
      "id": 19,
      "text": "Casados – esses são semelhantes ao de infância, porém mora ao seu lado e quando se esbarram: \\n\\nQuanto tempo!\\n\\nTemos que marcar alguma coisa... \\n\\nVamos fazer um churrasco, qual dia?...\\n\\nComo vai a família? Está bem e a sua? Também.\\n\\nEstou com dor nos joelhos, coluna e ainda estou com problemas na lombar, hérnia de disco, estou mais parecido com o Zé meningite...\\n\\nTrabalho — quando menos se espera surge uma fofoca: \\n\\nAí, tá sabendo: Zezinho e Joãozinho foram pego roubando... \\n\\nAí tá sabendo: Zezinho e o Joãozinho foram pego de novo... Fazendo o quê? Pegando no meu pau e no meu ovo...\\n\\nAí tá sabendo: Zezinho e o Joãozinho foram pego novamente... Fazendo o quê? “Brincando com os dentes...” e isso, é um vocabulário que me fez e faz sorrir e essas coisas do tipo obrigações, nós já vivemos para isso.\\n\\n“Amigos são amigos, só precisamos ser.”\\n\\nO difícil de se manter uma amizade é manter os seus amigos pertos e quando não se tem guerra o amar se torna menos confiável, até porque, quando deixamos",
      "position": 16991,
      "chapter": 3,
      "page": 18,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 21.63589232303091,
      "complexity_metrics": {
        "word_count": 177,
        "sentence_count": 17,
        "paragraph_count": 12,
        "avg_sentence_length": 10.411764705882353,
        "avg_word_length": 4.570621468926554,
        "unique_word_ratio": 0.6836158192090396,
        "avg_paragraph_length": 14.75,
        "punctuation_density": 0.2768361581920904,
        "line_break_count": 22,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "quando",
          "estou",
          "sabendo",
          "zezinho",
          "joãozinho",
          "pego",
          "amigos",
          "menos",
          "fazendo",
          "isso",
          "manter",
          "casados",
          "esses",
          "semelhantes",
          "infância",
          "porém",
          "mora",
          "lado",
          "esbarram",
          "quanto"
        ],
        "entities": [
          [
            "quando se",
            "PERSON"
          ],
          [
            "Temos",
            "PERSON"
          ],
          [
            "Vamos",
            "PERSON"
          ],
          [
            "dia",
            "ORG"
          ],
          [
            "Como",
            "ORG"
          ],
          [
            "joelhos",
            "GPE"
          ],
          [
            "coluna",
            "GPE"
          ],
          [
            "ainda",
            "ORG"
          ],
          [
            "hérnia de disco",
            "ORG"
          ],
          [
            "Trabalho",
            "GPE"
          ]
        ],
        "readability_score": 93.42293120638085,
        "semantic_density": 0,
        "word_count": 177,
        "unique_words": 121,
        "lexical_diversity": 0.6836158192090396
      },
      "preservation_score": 0.0004764345240823619
    },
    {
      "id": 20,
      "text": " de amar desistimos de brigar pois são tantas dificuldades e preguiça que ambos concordam em ficar na própria casa de boa, até porque, segunda feira temos que trabalhar de novo e não posso ficar cansado para trabalhar.\\n\\nSou o amigo que é desapegado de tudo, solteiro, casa com churrasqueira, moro com o filho em uma casa construída bem acima da mamãe e organizado, sempre estou com tempo livre, não por trabalhar menos ou ter dinheiro, essas duas coisas, não faço e não tenho. O ter menos dificuldades em organizar a minha vida é um pesar bem menor, assim, poucos conseguem ter o estilo de vida com a minha idade e obter a qualidade de vida que tenho, só tenho como agradecer por isso, até porque, sou abençoado por ter uma mãe e amigos (família) que souberam me direcionar com amor, quando eu estava procurando as respostas em meio ao ódio.\\n\\nResumo: sempre to ligando para todos, sempre estou com “todos”, mas para estar com todos é uma dificuldade terrível fazer o amigo de infância aparecer, solte",
      "position": 17991,
      "chapter": 3,
      "page": 19,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.40113636363637,
      "complexity_metrics": {
        "word_count": 176,
        "sentence_count": 4,
        "paragraph_count": 3,
        "avg_sentence_length": 44.0,
        "avg_word_length": 4.670454545454546,
        "unique_word_ratio": 0.6590909090909091,
        "avg_paragraph_length": 58.666666666666664,
        "punctuation_density": 0.125,
        "line_break_count": 4,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "casa",
          "trabalhar",
          "sempre",
          "tenho",
          "vida",
          "todos",
          "dificuldades",
          "ficar",
          "porque",
          "amigo",
          "estou",
          "menos",
          "minha",
          "amar",
          "desistimos",
          "brigar",
          "pois",
          "tantas",
          "preguiça",
          "ambos"
        ],
        "entities": [
          [
            "casa de boa",
            "ORG"
          ],
          [
            "que trabalhar de novo",
            "ORG"
          ],
          [
            "posso ficar",
            "ORG"
          ],
          [
            "para trabalhar",
            "PERSON"
          ],
          [
            "Sou",
            "PERSON"
          ],
          [
            "casa",
            "ORG"
          ],
          [
            "moro",
            "ORG"
          ],
          [
            "acima da mamãe",
            "PERSON"
          ],
          [
            "quando eu estava procurando",
            "PERSON"
          ],
          [
            "para todos",
            "PERSON"
          ]
        ],
        "readability_score": 76.59886363636363,
        "semantic_density": 0,
        "word_count": 176,
        "unique_words": 116,
        "lexical_diversity": 0.6590909090909091
      },
      "preservation_score": 1.0427018203822739e-05
    },
    {
      "id": 21,
      "text": "iro curtir alguma coisa que não seja putaria, casado para sair de casa pois a mulher ou o marido “não vivem” só, e sim, um para o outro, trabalho sempre têm um compromisso “mais importante”, passear com a família é quase impossível, até porque, têm muitas pendências sentimentais e quando todos se encontram, basta uma pequena faísca para se ter um incêndio.\\n\\nAgora eu pergunto: como queremos ser felizes se só vivemos pelas obrigações do sistema e não pela obrigação de viver a nossa própria vida?\\n\\nAté que ponto as minhas obrigações precisam ser o que limita meu próprio viver?\\n\\nAmigo é aquele que dividi um miojo quando só têm àquele para almoçar.\\n\\n Amigo é aquele que mesmo quando cai em um bueiro e arranha da ponta do dedo do pé e o arranhão foi até onde a perna não passava e, ao se apoiar com as mãos para conseguir evitar e a perna não entrar, apoiou a mão na merda e todos ficaram zoando, rindo e brincando.\\n\\n",
      "position": 18991,
      "chapter": 3,
      "page": 20,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 35.13035714285714,
      "complexity_metrics": {
        "word_count": 168,
        "sentence_count": 5,
        "paragraph_count": 5,
        "avg_sentence_length": 33.6,
        "avg_word_length": 4.434523809523809,
        "unique_word_ratio": 0.6904761904761905,
        "avg_paragraph_length": 33.6,
        "punctuation_density": 0.10119047619047619,
        "line_break_count": 10,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "quando",
          "todos",
          "obrigações",
          "viver",
          "amigo",
          "aquele",
          "perna",
          "curtir",
          "alguma",
          "coisa",
          "seja",
          "putaria",
          "casado",
          "sair",
          "casa",
          "pois",
          "mulher",
          "marido",
          "vivem",
          "outro"
        ],
        "entities": [
          [
            "iro curtir alguma coisa",
            "ORG"
          ],
          [
            "para sair de casa",
            "PERSON"
          ],
          [
            "têm muitas",
            "ORG"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "se encontram",
            "GPE"
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
            "Agora eu",
            "PERSON"
          ],
          [
            "como queremos",
            "PERSON"
          ],
          [
            "para almoçar.",
            "PERSON"
          ]
        ],
        "readability_score": 81.86964285714285,
        "semantic_density": 0,
        "word_count": 168,
        "unique_words": 116,
        "lexical_diversity": 0.6904761904761905
      },
      "preservation_score": 3.5090926647480365e-05
    },
    {
      "id": 22,
      "text": "Amigo é aquele que te acompanha na homem ou homem feia(o) ou bonita(o), não importa, só precisa fazer o “sacrifício”. \\n\\nAmigo é aquele que chama para dançar e disputar para ver quem dança melhor e ambos são horrorosos.\\n\\nAmigo é aquele que corre atrás quando estamos chorando por um amor não retribuído e cheios de expectativas, são tantas expectativas que esperamos conseguir subir uma ladeira correndo e no meio do caminho, chorando, paramos e pedimos pausa e tempo, até porque, correr cansa ainda mais em uma subida fugindo da dor que amor nós causa.\\n\\nAmigos são aqueles que voltamos a ser crianças quando olhamos em nossa volta e percebemos que estamos cheios de insights para situações de termos doces ou travessuras.\\n\\nAmigo não escolhemos e sim vivemos.\\n\\nAmigo não pede permissão para ser amigo, e sim, aconteceu.\\n\\nAmigo é amigo não importa a situação, sendo lendária e digna de ser uma lembrança, será bem vista, não importa em qual caminho foi levado o respeito e a história vivida, só precisa",
      "position": 19910,
      "chapter": 3,
      "page": 21,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 28.596974789915965,
      "complexity_metrics": {
        "word_count": 170,
        "sentence_count": 7,
        "paragraph_count": 7,
        "avg_sentence_length": 24.285714285714285,
        "avg_word_length": 4.847058823529411,
        "unique_word_ratio": 0.6588235294117647,
        "avg_paragraph_length": 24.285714285714285,
        "punctuation_density": 0.11176470588235295,
        "line_break_count": 12,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "amigo",
          "aquele",
          "importa",
          "homem",
          "precisa",
          "quando",
          "estamos",
          "chorando",
          "amor",
          "cheios",
          "expectativas",
          "caminho",
          "acompanha",
          "feia",
          "bonita",
          "fazer",
          "sacrifício",
          "chama",
          "dançar",
          "disputar"
        ],
        "entities": [
          [
            "precisa fazer",
            "PERSON"
          ],
          [
            "para dançar",
            "PERSON"
          ],
          [
            "quem dança melhor",
            "ORG"
          ],
          [
            "quando estamos",
            "PERSON"
          ],
          [
            "uma ladeira correndo",
            "ORG"
          ],
          [
            "paramos e pedimos pausa",
            "ORG"
          ],
          [
            "ainda mais",
            "PERSON"
          ],
          [
            "fugindo da dor",
            "PERSON"
          ],
          [
            "quando olhamos",
            "PERSON"
          ],
          [
            "estamos cheios de insights",
            "PERSON"
          ]
        ],
        "readability_score": 86.40302521008404,
        "semantic_density": 0,
        "word_count": 170,
        "unique_words": 112,
        "lexical_diversity": 0.6588235294117647
      },
      "preservation_score": 7.018185329496074e-05
    },
    {
      "id": 23,
      "text": "mos sermos gratos e sabermos agregar os valores que foram adquiridos, seja ele para o lado da felicidade e da alegria quando as vivemos ou quando se teve a tristeza e ódio, são esses, os maiores aprendizados em vivermos uma vida melhor com aqueles que precisamos viver e sobreviver a vida que iremos levar e deixaremos como legado para aqueles que deixaremos em um viver mais viciado pelo conforto, não basta termos uma vida que o esforço de arrumar uma cama, arrumar uma casa, lavar uma louça, uma roupa é muito mais cansativo que outras situações que servem para nos deixarmos mais belos e atraentes e o fazer esse tipo de serviço, não é bem visto por aqueles que pensam ter e ser melhores que outros, porém, em uma academia com 500kg nas pernas, 150kg no supino e muitos outros esforços para emagrecer, aparecer ou “ficar mais saudável”, até porque, fazer aquele serviço que auxilia em um bem estar em uma aproximação daqueles que amamos é muito cansativo e pouco compensatório.\\n\\n",
      "position": 20910,
      "chapter": 3,
      "page": 22,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.42280701754386,
      "complexity_metrics": {
        "word_count": 171,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 171.0,
        "avg_word_length": 4.742690058479532,
        "unique_word_ratio": 0.6491228070175439,
        "avg_paragraph_length": 171.0,
        "punctuation_density": 0.08771929824561403,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "vida",
          "aqueles",
          "quando",
          "viver",
          "deixaremos",
          "arrumar",
          "muito",
          "cansativo",
          "fazer",
          "serviço",
          "outros",
          "sermos",
          "gratos",
          "sabermos",
          "agregar",
          "valores",
          "adquiridos",
          "seja",
          "lado"
        ],
        "entities": [
          [
            "mos sermos",
            "PERSON"
          ],
          [
            "lado da felicidade",
            "PERSON"
          ],
          [
            "vivemos ou quando",
            "PERSON"
          ],
          [
            "legado",
            "GPE"
          ],
          [
            "pelo",
            "PERSON"
          ],
          [
            "basta",
            "NORP"
          ],
          [
            "esforço de arrumar uma cama",
            "ORG"
          ],
          [
            "muito mais",
            "PERSON"
          ],
          [
            "deixarmos mais belos",
            "PERSON"
          ],
          [
            "fazer",
            "ORG"
          ]
        ],
        "readability_score": 13.07719298245614,
        "semantic_density": 0,
        "word_count": 171,
        "unique_words": 111,
        "lexical_diversity": 0.6491228070175439
      },
      "preservation_score": 1.1362776247755548e-06
    },
    {
      "id": 24,
      "text": "Não precisamos ser extremistas e super vaidosos ao ponto de não conseguirmos enxergar as rugas que conquistamos ao decorrer da vida, e as vezes, vejo uns rostos tão esticado, que se cortarmos um “tendão” daquele que fica esticado no pescoço, a cabeça irá cair de lado.\\n\\nNós somos extremistas ao ponto que as danças estão virando robóticas e sem sentimento, quando têm sentimento são jogadas bananas nos estádios de futebol e quando se têm arte, as coreografias são “perfeitas” e não uma expressão corpórea, já os atletas, estão virando super humanos pela cobrança de sermos melhores que a “perfeição”.\\n\\nNós temos tantos amigos que não podemos fazer muitas coisas com um dom para nada, que um dia, quem sabe, venha ser bom em alguma coisa que fico pensando: quantas pessoas são capazes de acompanhar a evolução, “involução” ou “desvolução” humana?\\n\\nCapítulo 2\\n\\nMetáforas ou analogias?\\n\\n  “Toda brincadeira têm um fundo de verdade e se falamos é por quê pensamos, se pensamos, esse pensamento vem de nós mesmos e se provém de nós mesmos, merdas cagadas não voltam ao rabo.”\\n\\n",
      "position": 21893,
      "chapter": 3,
      "page": 23,
      "segment_type": "preserved_segment",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 31.48491620111732,
      "complexity_metrics": {
        "word_count": 179,
        "sentence_count": 6,
        "paragraph_count": 6,
        "avg_sentence_length": 29.833333333333332,
        "avg_word_length": 4.949720670391062,
        "unique_word_ratio": 0.7039106145251397,
        "avg_paragraph_length": 29.833333333333332,
        "punctuation_density": 0.11731843575418995,
        "line_break_count": 12,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "extremistas",
          "super",
          "ponto",
          "esticado",
          "estão",
          "virando",
          "sentimento",
          "quando",
          "pensamos",
          "mesmos",
          "precisamos",
          "vaidosos",
          "conseguirmos",
          "enxergar",
          "rugas",
          "conquistamos",
          "decorrer",
          "vida",
          "vezes",
          "vejo"
        ],
        "entities": [
          [
            "ponto de não conseguirmos enxergar",
            "ORG"
          ],
          [
            "vejo uns rostos",
            "GPE"
          ],
          [
            "tão",
            "ORG"
          ],
          [
            "fica",
            "GPE"
          ],
          [
            "quando têm",
            "PERSON"
          ],
          [
            "são jogadas bananas",
            "ORG"
          ],
          [
            "têm arte",
            "ORG"
          ],
          [
            "corpórea",
            "GPE"
          ],
          [
            "humanos",
            "NORP"
          ],
          [
            "pela cobrança de sermos",
            "PERSON"
          ]
        ],
        "readability_score": 83.59841713221601,
        "semantic_density": 0,
        "word_count": 179,
        "unique_words": 126,
        "lexical_diversity": 0.7039106145251397
      },
      "preservation_score": 7.940575401372699e-05
    },
    {
      "id": 25,
      "text": "“Temos que nós responsabilizar pelos nossos atos e se falamos ou fizemos, temos que dar a nossa cara tapa em estarmos dispostos a resolvermos.”\\n\\n“Para quem têm fé a vida sempre terá cura e aqueles que acreditam na religião a morte é a maior conquista.”\\n\\n“Se erramos e pedimos perdão para aquele que não foi prejudicado, do que adianta reconhecermos os nossos erros? “\\n\\n“Afinal, existe errado e certo ou tudo precisa coexistir?”\\n\\n“Não conseguimos nem interpretar a diferença entre analogia e metáforas nas religiões, o que esperamos de entender e compreender o que é certo ou errado se tudo está errado dentro de uma seleção natural?”\\n\\n“Queremos cordeiros na política e só temos lobos que sabem usar as metáforas para fazerem promessas e usam analogias para ganharem simpatia pela semelhança de um viver. Não vejo a política como solução e sim um trajeto que precisa muito ser melhorado.”\\n\\n“Nenhuma pessoa inteligente é inteligente estudando para si próprio.”\\n\\n",
      "position": 22966,
      "chapter": 3,
      "page": 24,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 25.620604781997187,
      "complexity_metrics": {
        "word_count": 158,
        "sentence_count": 9,
        "paragraph_count": 7,
        "avg_sentence_length": 17.555555555555557,
        "avg_word_length": 5.031645569620253,
        "unique_word_ratio": 0.7151898734177216,
        "avg_paragraph_length": 22.571428571428573,
        "punctuation_density": 0.0759493670886076,
        "line_break_count": 14,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "temos",
          "errado",
          "nossos",
          "certo",
          "tudo",
          "precisa",
          "metáforas",
          "política",
          "inteligente",
          "responsabilizar",
          "pelos",
          "atos",
          "falamos",
          "fizemos",
          "nossa",
          "cara",
          "tapa",
          "estarmos",
          "dispostos",
          "resolvermos"
        ],
        "entities": [
          [
            "Para",
            "PRODUCT"
          ],
          [
            "cura e aqueles que",
            "ORG"
          ],
          [
            "precisa coexistir",
            "PERSON"
          ],
          [
            "analogia",
            "GPE"
          ],
          [
            "nas religiões",
            "PERSON"
          ],
          [
            "dentro de uma seleção",
            "ORG"
          ],
          [
            "Queremos",
            "PERSON"
          ],
          [
            "metáforas",
            "ORG"
          ],
          [
            "para fazerem promessas",
            "PERSON"
          ],
          [
            "pela semelhança de",
            "PERSON"
          ]
        ],
        "readability_score": 89.71272855133614,
        "semantic_density": 0,
        "word_count": 158,
        "unique_words": 113,
        "lexical_diversity": 0.7151898734177216
      },
      "preservation_score": 8.515398199788572e-05
    },
    {
      "id": 26,
      "text": "  Como iremos saber os nossos erros se nós mesmos estamos nós dando as nossas respostas?\\n\\n“Temos tantas convicções sobre os nossos estudos que outros estudos viram metáforas, já os nossos, dão analogias feitas com o nosso próprio viver, logo a nossa forma de pensar não têm metáforas a serem interpretadas e sim analogias a serem seguidas como destino.”\\n\\n“Como posso fazer uma analogia perante a vida de outros que eu não vivi, não vivo, não quero saber e não sei ter empatia pela forma de ver, analisar, interpretar e compreender outros que não conseguem processar nem o que viveu e muito menos olhou para aqueles do próprio entorno.”\\n\\n“Muitas das vezes estamos com tantos problemas que não conseguimos nem lembrar de colocar um sal na comida.” \\n\\n  Quando temos fome, falta de estrutura familiar, críticas de um erro que não vemos como erro e sim enxergamos como necessários serem feitos, abandonos por negligência de não saber lhe dar com os nossos próprios traumas e fugas involuntárias devido a n",
      "position": 23926,
      "chapter": 3,
      "page": 25,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 35.57142857142857,
      "complexity_metrics": {
        "word_count": 168,
        "sentence_count": 5,
        "paragraph_count": 5,
        "avg_sentence_length": 33.6,
        "avg_word_length": 4.904761904761905,
        "unique_word_ratio": 0.6785714285714286,
        "avg_paragraph_length": 33.6,
        "punctuation_density": 0.08333333333333333,
        "line_break_count": 8,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "como",
          "nossos",
          "saber",
          "outros",
          "serem",
          "estamos",
          "temos",
          "estudos",
          "metáforas",
          "analogias",
          "próprio",
          "forma",
          "erro",
          "iremos",
          "erros",
          "mesmos",
          "dando",
          "nossas",
          "respostas",
          "tantas"
        ],
        "entities": [
          [
            "nós mesmos estamos",
            "ORG"
          ],
          [
            "nós dando",
            "GPE"
          ],
          [
            "viram metáforas",
            "PERSON"
          ],
          [
            "já os nossos",
            "PERSON"
          ],
          [
            "uma analogia",
            "ORG"
          ],
          [
            "eu não vivi",
            "PERSON"
          ],
          [
            "forma de ver",
            "PERSON"
          ],
          [
            "outros que",
            "PERSON"
          ],
          [
            "muito menos",
            "PERSON"
          ],
          [
            "olhou",
            "GPE"
          ]
        ],
        "readability_score": 81.72857142857143,
        "semantic_density": 0,
        "word_count": 168,
        "unique_words": 114,
        "lexical_diversity": 0.6785714285714286
      },
      "preservation_score": 2.6735944112365995e-05
    },
    {
      "id": 27,
      "text": "ecessidade de sermos felizes ou alegres e tudo que possa vir ser usado como respostas quando vivemos em uma vida digna de ser usado metáforas como direcionamentos, até porque, se usarmos analogias nesses casos, os mesmos não são vistos como exemplos para uma vida a não ser que estejam na bíblia, alcorão, filosofia, livros motivacionais e tudo aquilo que nós humanos não fazemos, e sim, só falamos e escrevemos como a melhor forma de se viver e não fazer.\\n\\n  Sou do tempo do alto da compadecida, American Pie, De Volta Para o Futuro, será que ele é, Se Beber não Case e várias outras formas de expressões engraçadas e na maioria das vezes felizes, alegres e cômico, até porque, estão acabando com a nossa forma pesada de pensar sobre um todo e quando entendemos a graça da piada junto a arte de sorrir com a lembrança de sermos crianças puras por conseguir entender a brincadeira, não a forma destoada de enxergar a comédia. Sarcasmo, irônico e o duplo sentido é preconceituoso, feri as pessoas e sã",
      "position": 24926,
      "chapter": 3,
      "page": 26,
      "segment_type": "preserved_segment",
      "themes": {
        "filosofia": 60.0,
        "arte": 40.0
      },
      "difficulty": 36.40113636363637,
      "complexity_metrics": {
        "word_count": 176,
        "sentence_count": 3,
        "paragraph_count": 2,
        "avg_sentence_length": 58.666666666666664,
        "avg_word_length": 4.670454545454546,
        "unique_word_ratio": 0.6875,
        "avg_paragraph_length": 88.0,
        "punctuation_density": 0.11363636363636363,
        "line_break_count": 2,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "como",
          "forma",
          "sermos",
          "felizes",
          "alegres",
          "tudo",
          "usado",
          "quando",
          "vida",
          "porque",
          "ecessidade",
          "possa",
          "respostas",
          "vivemos",
          "digna",
          "metáforas",
          "direcionamentos",
          "usarmos",
          "analogias",
          "nesses"
        ],
        "entities": [
          [
            "ser usado como",
            "ORG"
          ],
          [
            "quando vivemos",
            "PERSON"
          ],
          [
            "vida digna de ser",
            "PERSON"
          ],
          [
            "mesmos não",
            "PERSON"
          ],
          [
            "que",
            "CARDINAL"
          ],
          [
            "não fazemos",
            "PERSON"
          ],
          [
            "forma de se",
            "PERSON"
          ],
          [
            "Sou",
            "PERSON"
          ],
          [
            "alto da compadecida",
            "PERSON"
          ],
          [
            "American Pie",
            "ORG"
          ]
        ],
        "readability_score": 69.2655303030303,
        "semantic_density": 0,
        "word_count": 176,
        "unique_words": 121,
        "lexical_diversity": 0.6875
      },
      "preservation_score": 2.6735944112365995e-06
    },
    {
      "id": 28,
      "text": "o esses feridos, que não conseguem entender um sentimento de dor que possa vir ser engraçado em um momento caótico e cômico que é necessário sermos leves e calmos diante do peso em sobreviver dentro do nosso viver feliz.\\n\\n“Nós queremos uma vida sem graça e sem brincadeiras onde a arte de paquerar uma pessoa com mal hálito e talvez fazer a felicidade de alguém que era um “aí namoral, duvido...” essa frase motivacional pode ser a motivação para conseguir realizar o sonho de ter uma esposa e filhos.”\\n\\n“Acordar no dia seguinte com vergonha de perguntar o nome daquele(a) e vice versa, e mesmo assim, transformar esse constrangimento em uma árvore de fazer novos Amigos.”\\n\\n Essas ausências já estão sendo vistas no Japão e os danos estão quase irreversíveis.\\n\\n“Nos dias atuais somos semelhantes a um cardápio de restaurante, onde escolhemos as melhores comidas através de uma imagem com um acompanhamento e se pagar um outro pedaço de carne, pagando bem que mal têm. Já os valores das calorias são avaliados por uma escrita feita pela nossa própria forma de ver e imaginar.”\\n\\n",
      "position": 25926,
      "chapter": 3,
      "page": 27,
      "segment_type": "preserved_segment",
      "themes": {
        "filosofia": 60.0,
        "arte": 40.0
      },
      "difficulty": 28.196195652173913,
      "complexity_metrics": {
        "word_count": 184,
        "sentence_count": 8,
        "paragraph_count": 5,
        "avg_sentence_length": 23.0,
        "avg_word_length": 4.820652173913044,
        "unique_word_ratio": 0.7282608695652174,
        "avg_paragraph_length": 36.8,
        "punctuation_density": 0.08152173913043478,
        "line_break_count": 10,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "onde",
          "fazer",
          "estão",
          "esses",
          "feridos",
          "conseguem",
          "entender",
          "sentimento",
          "possa",
          "engraçado",
          "momento",
          "caótico",
          "cômico",
          "necessário",
          "sermos",
          "leves",
          "calmos",
          "diante",
          "peso",
          "sobreviver"
        ],
        "entities": [
          [
            "caótico e cômico",
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
            "talvez fazer",
            "PERSON"
          ],
          [
            "duvido",
            "PERSON"
          ],
          [
            "Acordar",
            "PRODUCT"
          ],
          [
            "dia",
            "ORG"
          ],
          [
            "transformar",
            "PERSON"
          ],
          [
            "Amigos",
            "LOC"
          ],
          [
            "Essas",
            "GPE"
          ]
        ],
        "readability_score": 87.05380434782609,
        "semantic_density": 0,
        "word_count": 184,
        "unique_words": 134,
        "lexical_diversity": 0.7282608695652174
      },
      "preservation_score": 4.177491267557186e-05
    },
    {
      "id": 29,
      "text": "Capítulo 3\\n\\nA vida é uma troca \\n\\n“O universo não joga dados com o destino, até porque, o mesmo é usado na sorte ou no azar e ambos estão certos, basta enxergarmos, compreender e entender como podemos usar as palavras corretamente.”\\n\\n   O universo é tão focado em equilibrar os nossos ciclos, que cada ciclo têm o seu próprio espaço e tempo em adaptar-se, e isso, é tão foda, que dependendo do quanto a nossa ancestralidade sofreu de caos, nós somos humanos mais adaptáveis quando se têm muita arte e sentimento, logo, esses humanos se destacam não por querer ser melhor, e sim, pelo destino ser o que deve ser. Nós temos a ancestralidade dos judeus que são os maiores profetas, messias, matemáticos, cientistas e tudo aquilo que necessita escutar o nosso próprio sentir o destino, e hoje, temos os negros que vieram de um tempo longevo de escravidão e nessa escravidão tivemos um número incalculável de quantidades de holocaustos que os negros sofreram, devido a essa quantidade de caos sofrido e a n",
      "position": 27003,
      "chapter": 4,
      "page": 1,
      "segment_type": "preserved_segment",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 36.42369942196532,
      "complexity_metrics": {
        "word_count": 173,
        "sentence_count": 3,
        "paragraph_count": 4,
        "avg_sentence_length": 57.666666666666664,
        "avg_word_length": 4.745664739884393,
        "unique_word_ratio": 0.7109826589595376,
        "avg_paragraph_length": 43.25,
        "punctuation_density": 0.12138728323699421,
        "line_break_count": 6,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "destino",
          "universo",
          "próprio",
          "tempo",
          "ancestralidade",
          "caos",
          "humanos",
          "temos",
          "negros",
          "escravidão",
          "capítulo",
          "vida",
          "troca",
          "joga",
          "dados",
          "porque",
          "mesmo",
          "usado",
          "sorte",
          "azar"
        ],
        "entities": [
          [
            "3",
            "CARDINAL"
          ],
          [
            "basta enxergarmos",
            "PERSON"
          ],
          [
            "como podemos usar",
            "ORG"
          ],
          [
            "têm o seu próprio",
            "ORG"
          ],
          [
            "tão",
            "ORG"
          ],
          [
            "quando se",
            "PERSON"
          ],
          [
            "têm muita arte",
            "ORG"
          ],
          [
            "pelo destino",
            "PERSON"
          ],
          [
            "judeus que",
            "PERSON"
          ],
          [
            "matemáticos",
            "PERSON"
          ]
        ],
        "readability_score": 69.74296724470135,
        "semantic_density": 0,
        "word_count": 173,
        "unique_words": 123,
        "lexical_diversity": 0.7109826589595376
      },
      "preservation_score": 1.924987976090352e-05
    },
    {
      "id": 30,
      "text": "ecessidade de adaptar-se em navios negreiros, chicotadas, criatividade em fazer comida com o que continha, ser feliz e alegre no meio da dor e da miséria e mesmo assim criamos o blues, jazz, rap, a arte negra em gera, conseguiu expressar o sentir e interpretar o próprio sentimento e através desses movimentos caóticos, que estão sendo gerado uma ascensão maior que a economia da China. Recentemente tivemos um negro no maior poder político do mundo e foi o último a destacar-se, assim está acontecendo na maioria dos esportes e tudo que precisa de adaptação em meio as dificuldades, até porque, onde alguns enxergam lixo outros enxergam flores e oportunidades de comprar terrenos para esperar a guerra acabar e vender quando estiver valorizado para ganhar dinheiro no futuro, outros fazem invenções antes vistas como impossíveis, sendo possíveis, e essa possibilidade, provém da dor com muito amor em um sobreviver feliz e caótico.\\n\\n",
      "position": 28003,
      "chapter": 4,
      "page": 2,
      "segment_type": "preserved_segment",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 36.553642384105956,
      "complexity_metrics": {
        "word_count": 151,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 75.5,
        "avg_word_length": 5.178807947019868,
        "unique_word_ratio": 0.7218543046357616,
        "avg_paragraph_length": 151.0,
        "punctuation_density": 0.11258278145695365,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "feliz",
          "meio",
          "assim",
          "sendo",
          "maior",
          "enxergam",
          "outros",
          "ecessidade",
          "adaptar",
          "navios",
          "negreiros",
          "chicotadas",
          "criatividade",
          "fazer",
          "comida",
          "continha",
          "alegre",
          "miséria",
          "mesmo",
          "criamos"
        ],
        "entities": [
          [
            "chicotadas",
            "GPE"
          ],
          [
            "caóticos",
            "GPE"
          ],
          [
            "gerado uma ascensão",
            "PERSON"
          ],
          [
            "China",
            "GPE"
          ],
          [
            "Recentemente tivemos",
            "PERSON"
          ],
          [
            "lixo outros",
            "ORG"
          ],
          [
            "vender quando",
            "PERSON"
          ],
          [
            "valorizado",
            "GPE"
          ],
          [
            "muito amor",
            "PERSON"
          ]
        ],
        "readability_score": 60.69635761589404,
        "semantic_density": 0,
        "word_count": 151,
        "unique_words": 109,
        "lexical_diversity": 0.7218543046357616
      },
      "preservation_score": 1.2699573453373847e-06
    },
    {
      "id": 31,
      "text": "   A Terra está tão fudida que: as estações do ano são coisas do passado o outono parece inverno, já o inverno parece a primavera, e a primavera é um verão em forma de mormaço e quando o Rio chegar a 40° como é a sua fama, a sensação térmica será de 55° e não semelhante a música que está virando uma lembrança do que era a beleza e o caos em meios ao outono.\\n\\n  “Somos marionetes do destino com livre arbítrio.”\\n\\n  “Estamos à procura da perfeição, contra vontade de ir e querendo ir sem perceber que estamos indo.”\\n\\n Como assim: Brigamos por tudo e por todos dentro da nossa maneira de ver o nosso universo, imaginando aquela estrada sendo a melhor para todos, e isso, sem saber fazer o melhor para si próprio e sem perceber que cada um criou o seu próprio universo imaginário dentro do seu próprio entrelaçamento quântico de ódio ou amor, caos e adaptação, sorte ou azar e tudo que um precisa existir para o outro coexistir, assim, tudo que imaginamos ser impossível torna-se possível quando se têm",
      "position": 28937,
      "chapter": 4,
      "page": 3,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.331868131868134,
      "complexity_metrics": {
        "word_count": 182,
        "sentence_count": 4,
        "paragraph_count": 4,
        "avg_sentence_length": 45.5,
        "avg_word_length": 4.43956043956044,
        "unique_word_ratio": 0.6703296703296703,
        "avg_paragraph_length": 45.5,
        "punctuation_density": 0.08791208791208792,
        "line_break_count": 6,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "tudo",
          "próprio",
          "está",
          "outono",
          "parece",
          "inverno",
          "primavera",
          "quando",
          "como",
          "caos",
          "estamos",
          "perceber",
          "assim",
          "todos",
          "dentro",
          "universo",
          "melhor",
          "terra",
          "fudida",
          "estações"
        ],
        "entities": [
          [
            "passado",
            "GPE"
          ],
          [
            "outono parece inverno",
            "PERSON"
          ],
          [
            "já o",
            "PERSON"
          ],
          [
            "forma de mormaço e quando",
            "ORG"
          ],
          [
            "Rio",
            "ORG"
          ],
          [
            "40",
            "CARDINAL"
          ],
          [
            "55",
            "CARDINAL"
          ],
          [
            "Somos",
            "PERSON"
          ],
          [
            "livre arbítrio",
            "PERSON"
          ],
          [
            "Estamos",
            "PERSON"
          ]
        ],
        "readability_score": 75.91813186813187,
        "semantic_density": 0,
        "word_count": 182,
        "unique_words": 122,
        "lexical_diversity": 0.6703296703296703
      },
      "preservation_score": 1.6843644790790576e-05
    },
    {
      "id": 32,
      "text": " amor e ódio ao sentir o destino que o universo nós direcionou como livre arbítrio em uma falsa democracia, socialismo, capitalismo, narcisismo e todas as formas de pensar que uma direção é mais correta ou melhor que outras.\\n\\n   “O nosso crescimento interno é semelhante a uma raiz de árvore, assim como o seu florescer para cima e para os lados e a sua necessidade de ter nutrientes e espaço para conseguir respirar, alimentar, crescer e viver para baixo semelhante ao ser parecido para cima, assim somos nós para alma(raiz) espírito(nutrientes) e corpo(florescer).”\\n\\nCapítulo 4\\n\\nMente vazia é oficina do diabo \\n\\n“O tédio junto ao excesso de conforto são os maiores causadores do benefício de se ter procrastinação.” \\n\\n  Irei expor alguns dos meus pensamentos sobre temas bem contraditórios e com muita força em direcionar as pessoas.\\n\\nDeus – Vejo que Deus é uma palavra usada para descrever uma percepção humana sobre seu próprio ver o destino de vida proporcional ao momento e o tempo a qual estava vivendo ou sentindo.\\n\\n",
      "position": 29937,
      "chapter": 4,
      "page": 4,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 33.59112426035503,
      "complexity_metrics": {
        "word_count": 169,
        "sentence_count": 5,
        "paragraph_count": 7,
        "avg_sentence_length": 33.8,
        "avg_word_length": 4.970414201183432,
        "unique_word_ratio": 0.6863905325443787,
        "avg_paragraph_length": 24.142857142857142,
        "punctuation_density": 0.07100591715976332,
        "line_break_count": 14,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "destino",
          "como",
          "semelhante",
          "raiz",
          "assim",
          "florescer",
          "cima",
          "nutrientes",
          "deus",
          "amor",
          "ódio",
          "sentir",
          "universo",
          "direcionou",
          "livre",
          "arbítrio",
          "falsa",
          "democracia",
          "socialismo",
          "capitalismo"
        ],
        "entities": [
          [
            "destino que",
            "LAW"
          ],
          [
            "universo nós",
            "ORG"
          ],
          [
            "formas de pensar",
            "PERSON"
          ],
          [
            "seu",
            "ORG"
          ],
          [
            "para cima e para",
            "PERSON"
          ],
          [
            "alimentar",
            "ORG"
          ],
          [
            "para cima",
            "PERSON"
          ],
          [
            "assim somos",
            "PERSON"
          ],
          [
            "alma(raiz",
            "CARDINAL"
          ],
          [
            "excesso de conforto são",
            "PERSON"
          ]
        ],
        "readability_score": 81.60887573964497,
        "semantic_density": 0,
        "word_count": 169,
        "unique_words": 116,
        "lexical_diversity": 0.6863905325443787
      },
      "preservation_score": 7.205336938282638e-05
    },
    {
      "id": 33,
      "text": "Exemplos: \\n\\nFica com o Destino (Deus)!\\n\\nQue o destino (Deus) te acompanhe!\\n\\nO destino (Deus) escreve certo com linhas tortas!\\n\\nSe não escutamos o destino (Deus) não estamos indo na direção que devemos ir.\\n\\n Cada pessoa provém de ter um destino com muita intensidade, contraditória e com a sua própria certeza da sua direção ser melhor e mais correta de um viver mais próximo do divino que os demais.\\n\\n“Deus é o filho mimado do universo, e isso, provém através de enxergar o lado bom da esperança para aqueles que não querem ser e muito menos parecem ter.”\\n\\nMalefícios – Vejo que a mente humana é relativa ao nosso DNA junto a uma coexistência territorial, costumes, quantidade de adaptação que precisar ser vívido para viver uma vida melhor e outras necessidades de adaptação de si próprio, assim, aqueles que não conseguiram desenvolver uma forma melhor ou pior sendo relativo ao ser feliz, não conseguem entender quando são metáforas ou analogias e sendo confundindo o meu viver ser melhor que o se",
      "position": 30961,
      "chapter": 4,
      "page": 5,
      "segment_type": "preserved_segment",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 28.72606516290727,
      "complexity_metrics": {
        "word_count": 171,
        "sentence_count": 7,
        "paragraph_count": 8,
        "avg_sentence_length": 24.428571428571427,
        "avg_word_length": 4.8011695906432745,
        "unique_word_ratio": 0.6432748538011696,
        "avg_paragraph_length": 21.375,
        "punctuation_density": 0.08771929824561403,
        "line_break_count": 14,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "destino",
          "deus",
          "melhor",
          "viver",
          "direção",
          "provém",
          "mais",
          "aqueles",
          "adaptação",
          "sendo",
          "exemplos",
          "fica",
          "acompanhe",
          "escreve",
          "certo",
          "linhas",
          "tortas",
          "escutamos",
          "estamos",
          "indo"
        ],
        "entities": [
          [
            "Fica",
            "GPE"
          ],
          [
            "Destino",
            "PERSON"
          ],
          [
            "Que",
            "PERSON"
          ],
          [
            "Deus",
            "PERSON"
          ],
          [
            "Se",
            "PERSON"
          ],
          [
            "destino",
            "PERSON"
          ],
          [
            "Deus",
            "PERSON"
          ],
          [
            "não estamos",
            "PERSON"
          ],
          [
            "Cada",
            "GPE"
          ],
          [
            "da sua",
            "ORG"
          ]
        ],
        "readability_score": 86.34536340852131,
        "semantic_density": 0,
        "word_count": 171,
        "unique_words": 110,
        "lexical_diversity": 0.6432748538011696
      },
      "preservation_score": 9.3575804393281e-05
    },
    {
      "id": 34,
      "text": "u viver, gerando conflitos de comportamentos devido ao meu pensar certo ser mais correto que um aceitar o pensar do outro como ser certo também.\\n\\nUniverso – Não tenho a menor ideia sobre a origem, mas, temos noção sobre os movimentos iniciais, assim, percebo que para descobri um padrão para o movimento do universo é necessário saber a origem, e talvez, essa origem já tenha sido extinta por um outro início de uma maior força, assim como, cada galáxia têm um buraco negro de grande massa central criando novos movimentos padrões que observamos e denominamos como galáxias, esses mesmos movimentos são padronizados de acordo com um início (relatividade geral de Einstein), esse início interferiu em outro início que já existia (galáxia), assim foram gerando novos inícios (filho), novos movimentos(sobreviver) e novas necessidades de adaptação(vida).\\n\\n  “O trajeto do nosso próprio universo é tão interessante, que o fácil de hoje é o difícil de amanhã e o que possa vir ser fácil amanhã, está sendo a dificuldade de hoje.”\\n\\n",
      "position": 31961,
      "chapter": 4,
      "page": 6,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 39.534131736526945,
      "complexity_metrics": {
        "word_count": 167,
        "sentence_count": 4,
        "paragraph_count": 3,
        "avg_sentence_length": 41.75,
        "avg_word_length": 5.11377245508982,
        "unique_word_ratio": 0.6826347305389222,
        "avg_paragraph_length": 55.666666666666664,
        "punctuation_density": 0.10778443113772455,
        "line_break_count": 6,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "movimentos",
          "início",
          "outro",
          "como",
          "universo",
          "origem",
          "assim",
          "novos",
          "gerando",
          "pensar",
          "certo",
          "galáxia",
          "fácil",
          "hoje",
          "amanhã",
          "viver",
          "conflitos",
          "comportamentos",
          "devido",
          "mais"
        ],
        "entities": [
          [
            "Universo",
            "PERSON"
          ],
          [
            "descobri",
            "GPE"
          ],
          [
            "padrão",
            "ORG"
          ],
          [
            "para",
            "PRODUCT"
          ],
          [
            "universo é necessário",
            "ORG"
          ],
          [
            "essa origem já",
            "ORG"
          ],
          [
            "cada galáxia",
            "ORG"
          ],
          [
            "buraco negro de grande massa central criando",
            "ORG"
          ],
          [
            "padrões",
            "GPE"
          ],
          [
            "mesmos",
            "PERSON"
          ]
        ],
        "readability_score": 77.59086826347306,
        "semantic_density": 0,
        "word_count": 167,
        "unique_words": 114,
        "lexical_diversity": 0.6826347305389222
      },
      "preservation_score": 1.804676227584704e-05
    },
    {
      "id": 35,
      "text": "  Não precisamos viver em uma seleção natural e sim em um sistema de aceitação, até porque, se fossemos semelhantes a uma planta que não conseguem se mexer nem para mijar, imagina diante da morte sem poder se mexer diante dos seus semelhantes morrendo pela própria ganância ou pela fome? Suas filhas(o) ou clones precisam morrer para outros conseguirem sobreviver, não temos tantos nutrientes e espaço para todos, assim, com pouco espaço até à água mal jogada ocupada mais espaço que a vida. Achamos que temos livres arbítrios, e esse pensamento, nós mostra um falso coletivo na democracia.\\n\\n“O tédio não é o mal do século, e sim, evolução humana.”\\n\\n  “Todos nós somos habituados a usarmos palavras como sorte e azar direcionado para um próprio benefício.”\\n\\nTemos palavras que usamos na matemática que o movimento descrito vira probabilidade, assim percebemos que as palavras as quais usamos têm um significado de peso para o movimento dela no próprio universo de cada um, por mais que tenha um significado e uma etimologia as mesmas são relativas ao interpretar o sentir em nossas almas.\\n\\n",
      "position": 32987,
      "chapter": 4,
      "page": 7,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 33.67,
      "complexity_metrics": {
        "word_count": 180,
        "sentence_count": 6,
        "paragraph_count": 4,
        "avg_sentence_length": 30.0,
        "avg_word_length": 5.011111111111111,
        "unique_word_ratio": 0.6944444444444444,
        "avg_paragraph_length": 45.0,
        "punctuation_density": 0.1,
        "line_break_count": 8,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "temos",
          "espaço",
          "palavras",
          "semelhantes",
          "mexer",
          "diante",
          "pela",
          "todos",
          "assim",
          "mais",
          "próprio",
          "usamos",
          "movimento",
          "significado",
          "precisamos",
          "viver",
          "seleção",
          "natural",
          "sistema",
          "aceitação"
        ],
        "entities": [
          [
            "nem para mijar",
            "PERSON"
          ],
          [
            "imagina diante da morte",
            "PERSON"
          ],
          [
            "diante",
            "PERSON"
          ],
          [
            "própria ganância",
            "PERSON"
          ],
          [
            "para outros conseguirem",
            "PERSON"
          ],
          [
            "sobreviver",
            "GPE"
          ],
          [
            "para todos",
            "PERSON"
          ],
          [
            "pouco espaço até à água",
            "PERSON"
          ],
          [
            "jogada ocupada mais",
            "ORG"
          ],
          [
            "Achamos",
            "PERSON"
          ]
        ],
        "readability_score": 83.49666666666667,
        "semantic_density": 0,
        "word_count": 180,
        "unique_words": 125,
        "lexical_diversity": 0.6944444444444444
      },
      "preservation_score": 2.5666506347871358e-05
    },
    {
      "id": 36,
      "text": "  Nós Humanos sempre estamos entediados, até quando estava sendo caçado, porém em um tédio com muito pânico e sem histeria, só instintos. Ao decorrer da nossa própria evolução e a necessidade de sobrevivência da própria espécie, começamos a fuder e ter filhos pacaralho para tirar o próprio tédio de ficar com tempo obsoleto e a mente vazia, quando essa se encontra nesse estado, vira oficina do diabo. Assim, em toda nossa evolução baseada no tédio em não apreciar o próprio instinto natural e sim querendo mais e mais prazeres, as vezes pela adrenalina, outros pelo vício, outros disfarçados de lobos em pele de cordeiro e vice versa e muitas outras oportunidades que parecem ser doce e se transformam em travessuras.\\n\\n  “Alguém sempre se fode para outros serem felizes, e isso, é uma ordem natural da vida, não por querer, e sim, pela necessidade de um existir para o outro coexistir.”\\n\\n  Não vejo as situações as quais eu vivo como ruins ou boas e sim necessárias serem vividas, ainda mais quando",
      "position": 34077,
      "chapter": 4,
      "page": 8,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 33.55235294117647,
      "complexity_metrics": {
        "word_count": 170,
        "sentence_count": 5,
        "paragraph_count": 3,
        "avg_sentence_length": 34.0,
        "avg_word_length": 4.841176470588235,
        "unique_word_ratio": 0.6941176470588235,
        "avg_paragraph_length": 56.666666666666664,
        "punctuation_density": 0.11764705882352941,
        "line_break_count": 4,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "quando",
          "tédio",
          "mais",
          "outros",
          "sempre",
          "nossa",
          "própria",
          "evolução",
          "necessidade",
          "próprio",
          "natural",
          "pela",
          "serem",
          "humanos",
          "estamos",
          "entediados",
          "estava",
          "sendo",
          "caçado",
          "porém"
        ],
        "entities": [
          [
            "Nós Humanos",
            "NORP"
          ],
          [
            "até quando estava",
            "PERSON"
          ],
          [
            "muito pânico e sem histeria",
            "PERSON"
          ],
          [
            "quando essa se encontra nesse",
            "PERSON"
          ],
          [
            "vira oficina",
            "PERSON"
          ],
          [
            "vezes pela adrenalina",
            "PERSON"
          ],
          [
            "outros pelo vício",
            "PERSON"
          ],
          [
            "outros disfarçados de lobos",
            "PERSON"
          ],
          [
            "para outros serem",
            "PERSON"
          ],
          [
            "outro coexistir",
            "PERSON"
          ]
        ],
        "readability_score": 81.54764705882353,
        "semantic_density": 0,
        "word_count": 170,
        "unique_words": 118,
        "lexical_diversity": 0.6941176470588235
      },
      "preservation_score": 8.822861557080777e-06
    },
    {
      "id": 37,
      "text": " eu sobrevivi e ninguém foi prejudicado ao ponto de ser morto ou ao ponto de não conseguir se erguer e dependendo apenas de si. Se por acaso eu causei algum dano mental, não foi por querer, foi sem querer, sem saber e sim por impulso do próprio sentir o momento e a situação. \\n\\n “Percebi o bem em meio ao mal e o mal em meio ao bem e nessa mesma ordem de fatores presenciei muito mais honestidade e maldade onde imaginava ter pessoas semelhantes ao sentir.”\\n\\nVivendo essa vida cheios de extremos desequilibrados com muito equilíbrio, aprendi e estou aprendendo que a prática, junto aos estudos, são bem mais fáceis em absorver e correlacionar os movimentos as quais eu preciso interpretar, adaptar e executar o meu próprio movimentar mais fácil no amanhã. Sinto e percebo que cada parte da dor ou felicidade estão virando estudos e não vivências. Essa ausência provém do excesso de conhecimento, assim, percebo que os meus movimentos mentais e corpóreos é o meu próprio universo imaginário do próprio sentir, como quero ver e viver o meu universo devido as minhas próprias escolhas. \\n\\n",
      "position": 35077,
      "chapter": 4,
      "page": 9,
      "segment_type": "preserved_segment",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 32.02204301075269,
      "complexity_metrics": {
        "word_count": 186,
        "sentence_count": 6,
        "paragraph_count": 3,
        "avg_sentence_length": 31.0,
        "avg_word_length": 4.795698924731183,
        "unique_word_ratio": 0.6612903225806451,
        "avg_paragraph_length": 62.0,
        "punctuation_density": 0.08602150537634409,
        "line_break_count": 6,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "próprio",
          "sentir",
          "mais",
          "ponto",
          "querer",
          "meio",
          "muito",
          "essa",
          "estudos",
          "movimentos",
          "percebo",
          "universo",
          "sobrevivi",
          "ninguém",
          "prejudicado",
          "morto",
          "conseguir",
          "erguer",
          "dependendo",
          "apenas"
        ],
        "entities": [
          [
            "ponto de ser",
            "ORG"
          ],
          [
            "acaso eu causei algum",
            "PERSON"
          ],
          [
            "Percebi",
            "ORG"
          ],
          [
            "muito mais honestidade e",
            "PERSON"
          ],
          [
            "Vivendo",
            "PRODUCT"
          ],
          [
            "muito equilíbrio",
            "PERSON"
          ],
          [
            "prática",
            "GPE"
          ],
          [
            "junto aos",
            "PRODUCT"
          ],
          [
            "Essa",
            "ORG"
          ],
          [
            "excesso de conhecimento",
            "PERSON"
          ]
        ],
        "readability_score": 83.06129032258065,
        "semantic_density": 0,
        "word_count": 186,
        "unique_words": 123,
        "lexical_diversity": 0.6612903225806451
      },
      "preservation_score": 1.0828057365508227e-05
    },
    {
      "id": 38,
      "text": "Capítulo 5\\n\\nLar doce lar\\n\\n  “Família! Família! Papai, mamãe, titia e todos aqueles que cuidamos e tratamos como amigos.”\\n\\n São os momentos mais engraçados e mais doloridos.\\n\\n São os momentos mais felizes e os mais problemáticos.\\n\\n São os que mais nos dão expectativas e os que mais causam depressão.\\n\\nFamília veio da palavra famulus. Era utilizada para denominar a casa onde morava os senhores com os membros originários do seu próprio sangue junto aos seus escravos.\\n\\nQuem é o senhor e quem é o escravo?\\n\\nAmigo veio da palavra amicus. Era utilizada para descrever a percepção humana do amor. \\n\\nQuais são os seus amigos dentro de nossas famílias?\\n\\nObservação: amigos é aquele que precisa ser amigo, quando necessita ser (sentimento ou matéria ambos proporcionais ao que possa ser oferecido).\\n\\n“Aqueles amigos feitos na guerra, são esses que sentem as dores ou alegrias em meio ao caos.”\\n\\nEm nossas vidas aqueles que desconhecem o tamanho das conquistas, serão os mesmos que vão exigir cada vez mais sobre a mesma conquista. \\n\\n",
      "position": 36162,
      "chapter": 5,
      "page": 1,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 22.185798816568045,
      "complexity_metrics": {
        "word_count": 169,
        "sentence_count": 15,
        "paragraph_count": 13,
        "avg_sentence_length": 11.266666666666667,
        "avg_word_length": 4.952662721893491,
        "unique_word_ratio": 0.6923076923076923,
        "avg_paragraph_length": 13.0,
        "punctuation_density": 0.1242603550295858,
        "line_break_count": 26,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "amigos",
          "família",
          "aqueles",
          "momentos",
          "veio",
          "palavra",
          "utilizada",
          "seus",
          "quem",
          "amigo",
          "nossas",
          "capítulo",
          "doce",
          "papai",
          "mamãe",
          "titia",
          "todos",
          "cuidamos",
          "tratamos"
        ],
        "entities": [
          [
            "Família",
            "NORP"
          ],
          [
            "Família",
            "NORP"
          ],
          [
            "titia",
            "GPE"
          ],
          [
            "depressão",
            "GPE"
          ],
          [
            "Família",
            "NORP"
          ],
          [
            "utilizada",
            "NORP"
          ],
          [
            "para denominar",
            "PERSON"
          ],
          [
            "casa",
            "ORG"
          ],
          [
            "Quem",
            "PERSON"
          ],
          [
            "quem é o escravo",
            "ORG"
          ]
        ],
        "readability_score": 92.88086785009862,
        "semantic_density": 0,
        "word_count": 169,
        "unique_words": 117,
        "lexical_diversity": 0.6923076923076923
      },
      "preservation_score": 0.00030499028246181516
    },
    {
      "id": 39,
      "text": "Até que ponto precisamos ser:\\n\\nMelhor filho?\\n\\nMelhor criador?\\n\\nMelhor amigo?\\n\\nGratos por aqueles que acham que a própria gratidão é maior que tudo e todos?\\n\\n“Só deixamos de amar, quando desistimos de brigar.”\\n\\n  Assim que começamos a leitura percebemos que nossos desejos é o que mais nós causam problemas, e essa situação, provém de tanta saúde mental que sentimos ao viver tantas situações confortáveis e prazerosas nós fazendo esquecer outros objetivos e outros contextos que possam ser uma arma contra o tédio. Quando vivemos uma vida mediana sem perceber confortável em um universo de padrões repetitivos e sem novas emoções, semelhante ao filme click, onde o ator com um controle remoto passa a parte de viver na murrinha, não fede e não cheira, monótono, sem sal, nada para fazer com tantas opções para se fazer, assim, o tempo passa e perdemos todo o tempo que tivemos para viver e não percebemos que poderíamos aproveitar onde a idade e o estilo de vida do tempo era mais interessante que o ser feliz.\\n\\n",
      "position": 37188,
      "chapter": 5,
      "page": 2,
      "segment_type": "preserved_segment",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 28.80656146179402,
      "complexity_metrics": {
        "word_count": 172,
        "sentence_count": 7,
        "paragraph_count": 7,
        "avg_sentence_length": 24.571428571428573,
        "avg_word_length": 4.8313953488372094,
        "unique_word_ratio": 0.6569767441860465,
        "avg_paragraph_length": 24.571428571428573,
        "punctuation_density": 0.11046511627906977,
        "line_break_count": 14,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "melhor",
          "viver",
          "tempo",
          "quando",
          "assim",
          "percebemos",
          "mais",
          "tantas",
          "outros",
          "vida",
          "onde",
          "passa",
          "fazer",
          "ponto",
          "precisamos",
          "filho",
          "criador",
          "amigo",
          "gratos",
          "aqueles"
        ],
        "entities": [
          [
            "Melhor",
            "GPE"
          ],
          [
            "Melhor",
            "GPE"
          ],
          [
            "acham",
            "ORG"
          ],
          [
            "quando desistimos de brigar",
            "PERSON"
          ],
          [
            "leitura percebemos que",
            "PERSON"
          ],
          [
            "desejos é o",
            "ORG"
          ],
          [
            "que mais",
            "PERSON"
          ],
          [
            "causam problemas",
            "PERSON"
          ],
          [
            "essa situação",
            "ORG"
          ],
          [
            "outros objetivos",
            "PERSON"
          ]
        ],
        "readability_score": 86.26486710963455,
        "semantic_density": 0,
        "word_count": 172,
        "unique_words": 113,
        "lexical_diversity": 0.6569767441860465
      },
      "preservation_score": 6.877821622906154e-05
    },
    {
      "id": 40,
      "text": "Como imaginamos a família “perfeita”? \\n\\nPrecisa existir um padrão familiar?\\n\\nO termo família é atual e necessário ser usado ou virou mais um incômodo evolutivo?\\n\\n “Vejo família como alicerce, base de tudo, construção e tudo que provém de outros e não só de si”\\n\\nTemos diferentes lares felizes e com muitas tristezas e independente de como seja ou onde seja, se dá para cair morto e ligar o foda-se para o resto do mundo, isso dá um alívio mental de conquista fora do comum. Esse alívio só é possível ser completo com aqueles que sonhamos viver ao lado e construir uma família, não precisando ser um homem com uma mulher como manda a “tradição”, basta ter amor e confiança que tudo dará certo. Queria que não tivéssemos outras opções de famílias... percebemos que as perguntas feitas, foram incriminadoras e bem compreensível coexistir, até porque, onde têm amor se têm ódio na mesma proporção e por muitas vezes esses momentos odiosos estão disfarçados na criação pelas limitações, medo, não pode, nã",
      "position": 38200,
      "chapter": 5,
      "page": 3,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 28.59873949579832,
      "complexity_metrics": {
        "word_count": 170,
        "sentence_count": 7,
        "paragraph_count": 5,
        "avg_sentence_length": 24.285714285714285,
        "avg_word_length": 4.852941176470588,
        "unique_word_ratio": 0.711764705882353,
        "avg_paragraph_length": 34.0,
        "punctuation_density": 0.11764705882352941,
        "line_break_count": 8,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "como",
          "família",
          "tudo",
          "muitas",
          "seja",
          "onde",
          "alívio",
          "amor",
          "imaginamos",
          "perfeita",
          "precisa",
          "existir",
          "padrão",
          "familiar",
          "termo",
          "atual",
          "necessário",
          "usado",
          "virou",
          "mais"
        ],
        "entities": [
          [
            "Precisa",
            "PERSON"
          ],
          [
            "necessário ser usado",
            "ORG"
          ],
          [
            "virou mais",
            "PERSON"
          ],
          [
            "Vejo",
            "LOC"
          ],
          [
            "Temos",
            "PERSON"
          ],
          [
            "para cair morto e ligar",
            "ORG"
          ],
          [
            "basta",
            "NORP"
          ],
          [
            "amor",
            "GPE"
          ],
          [
            "Queria",
            "PERSON"
          ],
          [
            "perguntas",
            "ORG"
          ]
        ],
        "readability_score": 86.40126050420169,
        "semantic_density": 0,
        "word_count": 170,
        "unique_words": 121,
        "lexical_diversity": 0.711764705882353
      },
      "preservation_score": 3.6093524551694095e-05
    },
    {
      "id": 41,
      "text": "o consegue, é perigoso, precisa estudar, não sai de casa, joga vídeo game, não conversar, não direcionar, não falar a verdade, omissão, culpa e a nossa gratidão vem disfarçada na depressão provida da dedicação, empenho, amor e ser o que precisa ser quando necessita ser. \\n\\n“O destino escreve uma família errada para alguém dar certo...”\\n\\n Todos aqueles que são fora da curva tiveram sérios problemas com as famílias e superaram os conflitos mentais em uma forma de direcionamento para o povão, vejamos alguns exemplos:\\n\\n Jesus nasceu de uma virgem em meio ao Sodoma e Gomorra, já Hitler era um garoto bom e inteligente até perder um irmão, aí viado namoral, provavelmente essa situação abriu a mente do inferno, também tivemos outras que foram mais que orientadores e foram a salvação quando ninguém acreditava, pensa: se a mãe do Tesla não tivesse dado todo dinheiro da família para ele jogar, será que ele teria aprendido o valor de se superar perante a uma necessidade de ser, o que precisa fazer para ter em meio as dificuldades?",
      "position": 39200,
      "chapter": 5,
      "page": 4,
      "segment_type": "preserved_segment",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 36.46228571428571,
      "complexity_metrics": {
        "word_count": 175,
        "sentence_count": 3,
        "paragraph_count": 4,
        "avg_sentence_length": 58.333333333333336,
        "avg_word_length": 4.8742857142857146,
        "unique_word_ratio": 0.72,
        "avg_paragraph_length": 43.75,
        "punctuation_density": 0.14857142857142858,
        "line_break_count": 6,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "precisa",
          "quando",
          "família",
          "meio",
          "consegue",
          "perigoso",
          "estudar",
          "casa",
          "joga",
          "vídeo",
          "game",
          "conversar",
          "direcionar",
          "falar",
          "verdade",
          "omissão",
          "culpa",
          "nossa",
          "gratidão",
          "disfarçada"
        ],
        "entities": [
          [
            "precisa estudar",
            "PERSON"
          ],
          [
            "não sai de casa",
            "ORG"
          ],
          [
            "depressão",
            "GPE"
          ],
          [
            "quando necessita",
            "PERSON"
          ],
          [
            "errada para",
            "PERSON"
          ],
          [
            "Todos",
            "ORG"
          ],
          [
            "fora da curva",
            "PERSON"
          ],
          [
            "uma forma de direcionamento",
            "PERSON"
          ],
          [
            "Jesus",
            "PERSON"
          ],
          [
            "Gomorra",
            "GPE"
          ]
        ],
        "readability_score": 69.37104761904762,
        "semantic_density": 0,
        "word_count": 175,
        "unique_words": 126,
        "lexical_diversity": 0.72
      },
      "preservation_score": 2.245819305438744e-05
    },
    {
      "id": 42,
      "text": " Família pode ser boa ou ruim, eu prefiro a minha do jeito que foi e do jeito que é. Tenho 36 anos de idade, sou chato, cheio de manias e me aturar, nem eu me aguento, porém, tenho uma família que posso brigar, posso conversar, qual assunto posso conversar, sei o quanto posso ser com cada um, sei os limites impostos pelas brigas vividas, sei viver os momentos felizes quando conseguimos viver, sei as brincadeiras que posso fazer com cada um e isso tudo provém de uma vida familiar bem conturbada (padrão) muito louca que vem se tornando bem interessante diante da sincronicidade dos acontecimentos vividos e a forma vivida.\\n\\n“A mesma cobrança familiar que nós criam estímulos são os mesmos que nós causam cansaço, fadiga, excesso de gratidão, pendências e tudo que possa vir ser um desconforto mental e corpóreo por amar e querer o melhor para todos.”\\n\\n“Lado negro da família” - Em um pagode com samba e dê algumas coisas que irei escrever em meu último livro que irá se chamar “Fuder ou não Fuder, és a questão?",
      "position": 40233,
      "chapter": 5,
      "page": 5,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.37900552486188,
      "complexity_metrics": {
        "word_count": 181,
        "sentence_count": 4,
        "paragraph_count": 3,
        "avg_sentence_length": 45.25,
        "avg_word_length": 4.596685082872928,
        "unique_word_ratio": 0.7182320441988951,
        "avg_paragraph_length": 60.333333333333336,
        "punctuation_density": 0.11049723756906077,
        "line_break_count": 4,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "posso",
          "família",
          "jeito",
          "tenho",
          "conversar",
          "cada",
          "viver",
          "tudo",
          "familiar",
          "fuder",
          "pode",
          "ruim",
          "prefiro",
          "minha",
          "anos",
          "idade",
          "chato",
          "cheio",
          "manias",
          "aturar"
        ],
        "entities": [
          [
            "Família",
            "GPE"
          ],
          [
            "eu prefiro",
            "PERSON"
          ],
          [
            "jeito",
            "PERSON"
          ],
          [
            "Tenho",
            "ORG"
          ],
          [
            "36",
            "CARDINAL"
          ],
          [
            "sou chato",
            "PERSON"
          ],
          [
            "nem eu",
            "PERSON"
          ],
          [
            "posso conversar",
            "PERSON"
          ],
          [
            "sei o quanto",
            "ORG"
          ],
          [
            "posso",
            "PERSON"
          ]
        ],
        "readability_score": 75.99599447513812,
        "semantic_density": 0,
        "word_count": 181,
        "unique_words": 130,
        "lexical_diversity": 0.7182320441988951
      },
      "preservation_score": 1.1229096527193718e-05
    },
    {
      "id": 43,
      "text": "”. Observação: o engajamento vem de oportunidade e qual é a hora de criar uma nova oportunidade? \\n\\nEsse assunto é outra linha de raciocínio, vamos para o momento que eu estava lá dançando, cheio de bebidas e mulheres para todos os lados em um camarote semelhante a um curral, e do nada, parava e começava a estudar aqueles movimentos que estava vivendo de todos os tipos, desde suruba no camarote ao lado a pessoa morrendo com marca passo provida do som alto em meu colo.  \\n\\n“O estudar e querer interpretar veio originário da minha ganância de um sonho em ter uma família sem pensar na fome e sem fazer os mesmos erros cometidos.”\\n\\n“Escrever é a minha forma de evitar outro sofrimento ou acrescentar em outra felicidade que possa vir se semelhante ao meu universo observável.”\\n\\nFase depressiva e prazerosa - O estar em um poço quase me afogando e me apoiando em qualquer coisa que pudesse me impulsionar em direção a saída, me fazia viver loucuras prazerosas e extremas, onde se encontram situações l",
      "position": 41248,
      "chapter": 5,
      "page": 6,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 31.154,
      "complexity_metrics": {
        "word_count": 175,
        "sentence_count": 6,
        "paragraph_count": 5,
        "avg_sentence_length": 29.166666666666668,
        "avg_word_length": 4.68,
        "unique_word_ratio": 0.6971428571428572,
        "avg_paragraph_length": 35.0,
        "punctuation_density": 0.07428571428571429,
        "line_break_count": 8,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "oportunidade",
          "outra",
          "estava",
          "todos",
          "camarote",
          "semelhante",
          "estudar",
          "minha",
          "observação",
          "engajamento",
          "qual",
          "hora",
          "criar",
          "nova",
          "esse",
          "assunto",
          "linha",
          "raciocínio",
          "vamos",
          "momento"
        ],
        "entities": [
          [
            "Observação",
            "PERSON"
          ],
          [
            "engajamento vem de oportunidade e",
            "ORG"
          ],
          [
            "nova",
            "LOC"
          ],
          [
            "vamos para",
            "PERSON"
          ],
          [
            "que eu estava",
            "PERSON"
          ],
          [
            "cheio de bebidas",
            "ORG"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "nada",
            "GPE"
          ],
          [
            "que estava vivendo de todos",
            "PERSON"
          ],
          [
            "desde suruba",
            "ORG"
          ]
        ],
        "readability_score": 84.01266666666666,
        "semantic_density": 0,
        "word_count": 175,
        "unique_words": 122,
        "lexical_diversity": 0.6971428571428572
      },
      "preservation_score": 2.5399146906747697e-05
    },
    {
      "id": 44,
      "text": "endárias e engraçadas nas casas de shows, pagodes, festivais, barzinhos, puteiros, raves, churrasco com amigos, futebol com amigos, cachorro quente com os amigos, bebida alcoólica, maconha, bala, ecstasy e tudo que vejo como uma fuga a ser vivida e controlada, pois temos outras drogas que quase todos aqueles que usam ou usaram, criaram danos irreversíveis e distanciamentos daqueles que nascemos para viver ao lado. Mesmo vivendo com distanciamento necessário ou involuntário, essa situação sendo confortável para ambos e não ocasionar danos colaterais, mesmo assim, esse fator é prejudicial para aqueles de seu entorno, não por fazer mal, e sim, pelo mal estar do legado familiar em outros imaginar que “todos” são semelhantes e por muitas vezes passam por “iguais”.\\n\\nCapítulo 6\\n\\nDroga, Fuga, vício, dependência e usuário\\n\\n  “O passado e o futuro se misturam em qualquer momento no presente.”\\n\\n  Drogas são interessantes. Em um passado distante para uma vida humana e curta quando se está em uma o",
      "position": 42248,
      "chapter": 5,
      "page": 7,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 32.48544303797468,
      "complexity_metrics": {
        "word_count": 158,
        "sentence_count": 5,
        "paragraph_count": 5,
        "avg_sentence_length": 31.6,
        "avg_word_length": 5.284810126582278,
        "unique_word_ratio": 0.7721518987341772,
        "avg_paragraph_length": 31.6,
        "punctuation_density": 0.17088607594936708,
        "line_break_count": 8,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "amigos",
          "fuga",
          "drogas",
          "todos",
          "aqueles",
          "danos",
          "mesmo",
          "passado",
          "endárias",
          "engraçadas",
          "casas",
          "shows",
          "pagodes",
          "festivais",
          "barzinhos",
          "puteiros",
          "raves",
          "churrasco",
          "futebol",
          "cachorro"
        ],
        "entities": [
          [
            "nas casas de shows",
            "PERSON"
          ],
          [
            "futebol",
            "GPE"
          ],
          [
            "bala",
            "PERSON"
          ],
          [
            "vejo",
            "NORP"
          ],
          [
            "temos outras drogas",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "nascemos para",
            "PERSON"
          ],
          [
            "Mesmo",
            "PERSON"
          ],
          [
            "distanciamento necessário",
            "PERSON"
          ],
          [
            "essa situação",
            "ORG"
          ]
        ],
        "readability_score": 82.61455696202532,
        "semantic_density": 0,
        "word_count": 158,
        "unique_words": 122,
        "lexical_diversity": 0.7721518987341772
      },
      "preservation_score": 4.411430778540389e-05
    },
    {
      "id": 45,
      "text": "nda, muitos sábios, profetas, matemáticos, filósofos, pajés, e tudo que precisa acessar o seu eu interior, e o despertar provém de alguma droga que foi parar em uma fuga pela dor de perder um trabalho, talvez pelo vício que a fome causa em não ver felicidade na vida, podendo vir através da dependência de tanto querer ser ou ter e o corpo deixar de fazer ou produzir, criamos abstinência com alimentos que não são considerados como drogas serem vendidas e circulando livremente sem ninguém olhar de cara feia, até porque, antes não eram consideradas drogas não existia a obesidade como problema no planeta Terra e com a culpa de industrializarmos tudo que era saudável pela necessidade de sobrevivência da espécie em produzir uma maior quantidade junto a necessidade de ser armazenado, desse jeito, morrer tornou-se mais agradável que comer coisas podres e ruins que revolucionaram a nossa forma de cozinhar e admirar o paladar.\\n\\n",
      "position": 43248,
      "chapter": 5,
      "page": 8,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.51168831168831,
      "complexity_metrics": {
        "word_count": 154,
        "sentence_count": 1,
        "paragraph_count": 1,
        "avg_sentence_length": 154.0,
        "avg_word_length": 5.038961038961039,
        "unique_word_ratio": 0.7272727272727273,
        "avg_paragraph_length": 154.0,
        "punctuation_density": 0.09740259740259741,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "tudo",
          "pela",
          "produzir",
          "como",
          "drogas",
          "necessidade",
          "muitos",
          "sábios",
          "profetas",
          "matemáticos",
          "filósofos",
          "pajés",
          "precisa",
          "acessar",
          "interior",
          "despertar",
          "provém",
          "alguma",
          "droga",
          "parar"
        ],
        "entities": [
          [
            "nda",
            "ORG"
          ],
          [
            "profetas",
            "GPE"
          ],
          [
            "matemáticos",
            "PERSON"
          ],
          [
            "seu eu",
            "ORG"
          ],
          [
            "talvez pelo vício que",
            "PERSON"
          ],
          [
            "através da dependência de tanto",
            "PERSON"
          ],
          [
            "circulando",
            "ORG"
          ],
          [
            "morrer tornou-se",
            "PERSON"
          ],
          [
            "nossa forma de cozinhar",
            "PERSON"
          ]
        ],
        "readability_score": 21.488311688311683,
        "semantic_density": 0,
        "word_count": 154,
        "unique_words": 112,
        "lexical_diversity": 0.7272727272727273
      },
      "preservation_score": 1.06943776449464e-06
    },
    {
      "id": 46,
      "text": " “Tudo que vira chique ou sofisticado deixa de ser droga e vira remédio para a mente e o corpo.”\\n\\n Nunca deixe de experimentar e viver com segurança a dosagem ingerida e sempre controlada, estude antes sobre os malefícios e os benefícios de cada fuga que pretende ingerir, assim, sinta a vibe, divirta-se, pule, cante, grite, abrace, fode e se por acaso bater uma bad trip, aprenda a entender e sentir a própria vida para não usar em momentos importunos.\\n\\nQuantidade e macetes de como dosar:\\n\\nAçúcar – O açúcar sempre existiu. As pessoas não eram gordas os problemas e o culpado não pode provir apenas de um, até porque, a industrialização junto ao aumento de calorias durante todo o dia ingerido mais uma vida semelhante a de um parasita, são fatores determinantes para culpar alguém e esse alguém parece ser o açúcar e não a gula.\\n\\nSódio – Semelhante ao açúcar só que pela linha de raciocínio de conservar e temperar. Mesmo usando em excesso nas carnes nos navios e estoques cheios de baratas, moscas, larvas, fungos e mesmo assim ninguém ficava com pressão alta e muito menos engordava.\\n\\n",
      "position": 44179,
      "chapter": 5,
      "page": 9,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 32.25396825396825,
      "complexity_metrics": {
        "word_count": 189,
        "sentence_count": 6,
        "paragraph_count": 5,
        "avg_sentence_length": 31.5,
        "avg_word_length": 4.735449735449736,
        "unique_word_ratio": 0.7142857142857143,
        "avg_paragraph_length": 37.8,
        "punctuation_density": 0.12169312169312169,
        "line_break_count": 10,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "açúcar",
          "vira",
          "sempre",
          "assim",
          "vida",
          "semelhante",
          "alguém",
          "mesmo",
          "tudo",
          "chique",
          "sofisticado",
          "deixa",
          "droga",
          "remédio",
          "mente",
          "corpo",
          "nunca",
          "deixe",
          "experimentar",
          "viver"
        ],
        "entities": [
          [
            "deixa de ser",
            "PERSON"
          ],
          [
            "Nunca",
            "ORG"
          ],
          [
            "de cada",
            "PERSON"
          ],
          [
            "divirta-se",
            "PERSON"
          ],
          [
            "vida",
            "PRODUCT"
          ],
          [
            "Quantidade",
            "PERSON"
          ],
          [
            "gordas os problemas e o",
            "PERSON"
          ],
          [
            "culpado",
            "GPE"
          ],
          [
            "dia ingerido mais",
            "ORG"
          ],
          [
            "para culpar",
            "PERSON"
          ]
        ],
        "readability_score": 82.82936507936508,
        "semantic_density": 0,
        "word_count": 189,
        "unique_words": 135,
        "lexical_diversity": 0.7142857142857143
      },
      "preservation_score": 4.344590918259474e-05
    },
    {
      "id": 47,
      "text": "Observação: não generaliza os alimentos com as mortes pela falta de higiene, falta de estrutura e conhecimento sobre saneamento básico.\\n\\nÁlcool – Cada hora vem um estudo diferente e com uma nova dúvida se nós faz bem ou mal, tá semelhante as informações sobre os ovos... Não sei se só bebo vinho, cerveja, whisky, tequila, gim, Vodka ou todas as opções, na dúvida eu bebo de acordo com o meu ser feliz e com a dosagem que o meu corpo permiti me manter sóbrio diante da loucura e não ficar com caganeira no dia seguinte.\\n\\nMaconha – Dependendo do ramo a qual se trabalha não vejo com bons olhos pessoas que trabalham bêbado e muito menos chapado. Vejo como fraqueza e vício em busca de procurar conforto onde não consegue se sentir confortável, pois precisa desacelerar e esvaziar a mente como fuga dos próprios problemas incontroláveis de uma vida que já foi vivida, não aconselho adolescentes e pessoas que precisam de motivação, ambição, adrenalina e aquelas coisas que precisamos viver e não procrastinar.\\n\\n",
      "position": 45270,
      "chapter": 5,
      "page": 10,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.74450867052023,
      "complexity_metrics": {
        "word_count": 173,
        "sentence_count": 5,
        "paragraph_count": 3,
        "avg_sentence_length": 34.6,
        "avg_word_length": 4.815028901734104,
        "unique_word_ratio": 0.7283236994219653,
        "avg_paragraph_length": 57.666666666666664,
        "punctuation_density": 0.11560693641618497,
        "line_break_count": 6,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "falta",
          "dúvida",
          "bebo",
          "vejo",
          "pessoas",
          "como",
          "observação",
          "generaliza",
          "alimentos",
          "mortes",
          "pela",
          "higiene",
          "estrutura",
          "conhecimento",
          "saneamento",
          "básico",
          "álcool",
          "cada",
          "hora",
          "estudo"
        ],
        "entities": [
          [
            "falta de higiene",
            "ORG"
          ],
          [
            "falta de estrutura",
            "ORG"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "Vodka",
            "FAC"
          ],
          [
            "bebo de acordo",
            "ORG"
          ],
          [
            "sóbrio diante da loucura",
            "PERSON"
          ],
          [
            "dia",
            "ORG"
          ],
          [
            "vejo",
            "ORG"
          ],
          [
            "trabalham bêbado",
            "PERSON"
          ],
          [
            "muito menos",
            "PERSON"
          ]
        ],
        "readability_score": 81.25549132947977,
        "semantic_density": 0,
        "word_count": 173,
        "unique_words": 126,
        "lexical_diversity": 0.7283236994219653
      },
      "preservation_score": 1.2031174850564695e-05
    },
    {
      "id": 48,
      "text": "Bala – Essa onda é uma onda, até porque, têm horas que estamos na onda e temos hora que não estamos na onda ainda na onda. Não sabendo o momento certo e a quantidade da dose, torna-se perigosa e traiçoeira. O sentir fica muito mais aflorado e sensível, tudo fica feliz ou triste e ambas as situações em ecstasy. Uma bala triturada e distribuída na forma de gelo é possível controlar e dosar a histeria causada.\\n\\n “Tudo que é droga cura ou mata ou tanto faz, drogas são drogas e não se deve usar...”\\n\\n   O excesso ou escassez de alimentos ao nosso corpo é o que irá controlar a importância que o próprio corpo irá sentir saudades do excesso ou da escassez, como assim:\\n\\nSe crescemos em meio a uma alimentação totalmente incoerente e cheios de ausência de tempo e fora de padrão somos tendenciosos a sermos obesos, e isso, é semelhante ao fazer uma dieta sem carboidratos, após um tempo os nossos corpos entram em fadiga e apagões provindas da ausência de energia devido à o corpo estar na reserva daqu",
      "position": 46279,
      "chapter": 5,
      "page": 11,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 31.588461538461537,
      "complexity_metrics": {
        "word_count": 182,
        "sentence_count": 6,
        "paragraph_count": 4,
        "avg_sentence_length": 30.333333333333332,
        "avg_word_length": 4.461538461538462,
        "unique_word_ratio": 0.6648351648351648,
        "avg_paragraph_length": 45.5,
        "punctuation_density": 0.09340659340659341,
        "line_break_count": 6,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "onda",
          "corpo",
          "bala",
          "estamos",
          "sentir",
          "fica",
          "tudo",
          "controlar",
          "drogas",
          "excesso",
          "escassez",
          "ausência",
          "tempo",
          "essa",
          "porque",
          "horas",
          "temos",
          "hora",
          "ainda",
          "sabendo"
        ],
        "entities": [
          [
            "Bala",
            "PERSON"
          ],
          [
            "Essa",
            "PERSON"
          ],
          [
            "têm horas",
            "ORG"
          ],
          [
            "que",
            "CARDINAL"
          ],
          [
            "hora",
            "NORP"
          ],
          [
            "não estamos",
            "PERSON"
          ],
          [
            "onda ainda",
            "PERSON"
          ],
          [
            "fica muito mais",
            "PERSON"
          ],
          [
            "fica",
            "GPE"
          ],
          [
            "Uma bala triturada e",
            "PERSON"
          ]
        ],
        "readability_score": 83.4948717948718,
        "semantic_density": 0,
        "word_count": 182,
        "unique_words": 121,
        "lexical_diversity": 0.6648351648351648
      },
      "preservation_score": 1.6041566467419597e-05
    },
    {
      "id": 49,
      "text": "eles nutrientes e vitaminas, quando esses mesmos corpos começam a ingerir os alimentos escassos com uma maior frequência e sem padrão, nossos corpos absorvem e mantém uma maior reserva pelo medo de viver a mesma escassez, semelhante à quando bebemos e não lembramos... Lembrei!\\n\\nBebemos para comemorar qualquer coisa que seja motivacional para beber. Em meio as comemorações e a empolgação de estar se divertindo semelhante a pular de Bungee jumping, rico, bonito, atraente, dançarino, cansado, sono e quando chegamos ao final do elástico, voltamos a sentir a adrenalina e queremos voltar a sentir mais e mais... Essa é a ilusão problemática do álcool. Estamos indo em direção a ficar em coma e a bebida que está sendo ingerida, só irá ser distribuída e fazer o efeito dentro de 30 a 90 minutos após o consumo, e dentro desse tempo, qual é a quantidade que podemos ingerir? Antes ou depois do vômito...\\n\\n",
      "position": 47279,
      "chapter": 5,
      "page": 12,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 27.337406015037594,
      "complexity_metrics": {
        "word_count": 152,
        "sentence_count": 7,
        "paragraph_count": 2,
        "avg_sentence_length": 21.714285714285715,
        "avg_word_length": 4.934210526315789,
        "unique_word_ratio": 0.7368421052631579,
        "avg_paragraph_length": 76.0,
        "punctuation_density": 0.17105263157894737,
        "line_break_count": 4,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "quando",
          "corpos",
          "ingerir",
          "maior",
          "semelhante",
          "bebemos",
          "sentir",
          "mais",
          "dentro",
          "eles",
          "nutrientes",
          "vitaminas",
          "esses",
          "mesmos",
          "começam",
          "alimentos",
          "escassos",
          "frequência",
          "padrão",
          "nossos"
        ],
        "entities": [
          [
            "vitaminas",
            "GPE"
          ],
          [
            "quando",
            "PERSON"
          ],
          [
            "mesmos corpos",
            "PERSON"
          ],
          [
            "sem padrão",
            "PERSON"
          ],
          [
            "mantém",
            "GPE"
          ],
          [
            "pelo medo de viver",
            "PERSON"
          ],
          [
            "quando bebemos",
            "PERSON"
          ],
          [
            "não lembramos",
            "FAC"
          ],
          [
            "Bebemos",
            "GPE"
          ],
          [
            "para comemorar qualquer coisa",
            "ORG"
          ]
        ],
        "readability_score": 87.6625939849624,
        "semantic_density": 0,
        "word_count": 152,
        "unique_words": 112,
        "lexical_diversity": 0.7368421052631579
      },
      "preservation_score": 6.95134546921516e-06
    },
    {
      "id": 50,
      "text": "Quando acordamos e falamos: nunca mais irei beber... Esse é o sinal que ficaremos com uma puta ressaca e com pensamentos depressivos ou pensativos na crise existencial de nunca mais fazer isso sem rumo e sem vontade de fazer nada, e isso, provém dos nossos corpos sentindo o álcool nós levar em direção ao submundo da mente e ao perceber que estamos vivos, nossos corpos são bem sentimentais e sensível, qualquer “coisinha” fica magoado. \\n\\nCapítulo 7\\n\\nExcesso de saúde ou pouca saúde, o que é saudável?\\n\\nPor que é necessário termos padrões de acordar, ingerir uma quantidade de calorias padrão todos os dias nos nossos horários padrões e padronizar o horário de dormir?\\n\\n“O homem mais rico é aquele cujos prazeres são mais baratos. Se um homem marcha com um passo diferente do dos seus companheiros, é porque ouve outro tambor.” Henry Ford\\n\\nSe não conseguimos achar padrões em nossas vidas, não conseguimos achar os movimentos necessários para se ter uma vida saudável e feliz, não precisamos seguir ",
      "position": 48183,
      "chapter": 5,
      "page": 13,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 28.54642857142857,
      "complexity_metrics": {
        "word_count": 168,
        "sentence_count": 7,
        "paragraph_count": 6,
        "avg_sentence_length": 24.0,
        "avg_word_length": 4.916666666666667,
        "unique_word_ratio": 0.7023809523809523,
        "avg_paragraph_length": 28.0,
        "punctuation_density": 0.10714285714285714,
        "line_break_count": 10,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "nossos",
          "padrões",
          "nunca",
          "fazer",
          "isso",
          "corpos",
          "saúde",
          "saudável",
          "homem",
          "conseguimos",
          "achar",
          "quando",
          "acordamos",
          "falamos",
          "irei",
          "beber",
          "esse",
          "sinal",
          "ficaremos"
        ],
        "entities": [
          [
            "Quando",
            "PERSON"
          ],
          [
            "nunca mais",
            "ORG"
          ],
          [
            "mais fazer",
            "PERSON"
          ],
          [
            "de fazer",
            "PERSON"
          ],
          [
            "nada",
            "GPE"
          ],
          [
            "álcool nós levar",
            "ORG"
          ],
          [
            "estamos vivos",
            "PERSON"
          ],
          [
            "pouca saúde",
            "PERSON"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "todos",
            "CARDINAL"
          ]
        ],
        "readability_score": 86.525,
        "semantic_density": 0,
        "word_count": 168,
        "unique_words": 118,
        "lexical_diversity": 0.7023809523809523
      },
      "preservation_score": 4.4114307785403885e-05
    },
    {
      "id": 51,
      "text": "uma regra de horário, até porque, em toda nossa evolução cada povo têm um costume de horário, costume de quantidade de alimentos ingeridos e estrutura familiar. Nós brasileiros somos mistura do mundo todo, logo não temos um costume enraizado e sim o costume que criamos como raiz.\\n\\nNa história da humanidade nunca tivemos tanta abundância de comida e variedades para se comer, penso que os nossos corpos não necessitam de todos os nutrientes e sim aqueles nutrientes padrões que o nosso povo têm costume, pois quanto mais fazemos, mais aprendemos, e os nossos corpos, não são diferentes.\\n\\nA nossa evolução é composta por duas funções naturais: evolutiva e adaptativa, são essas duas funções que são as regentes em nossas vidas antes mesmo de nascer e após morrer, e isso, provém de um entrelaçamento quântico de todos aqueles que vieram antes de nós.\\n\\nCrie padrões alimentares proporcionais ao corpo e forma que viveu a vida toda, não faça agressividades intensas com os corpos e se for para crescer,",
      "position": 49183,
      "chapter": 5,
      "page": 14,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 35.192814371257484,
      "complexity_metrics": {
        "word_count": 167,
        "sentence_count": 5,
        "paragraph_count": 4,
        "avg_sentence_length": 33.4,
        "avg_word_length": 4.976047904191617,
        "unique_word_ratio": 0.6646706586826348,
        "avg_paragraph_length": 41.75,
        "punctuation_density": 0.11377245508982035,
        "line_break_count": 6,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "costume",
          "corpos",
          "horário",
          "toda",
          "nossa",
          "evolução",
          "povo",
          "nossos",
          "todos",
          "nutrientes",
          "aqueles",
          "padrões",
          "mais",
          "duas",
          "funções",
          "antes",
          "regra",
          "porque",
          "cada",
          "quantidade"
        ],
        "entities": [
          [
            "uma regra de horário",
            "ORG"
          ],
          [
            "raiz",
            "GPE"
          ],
          [
            "nunca tivemos",
            "PERSON"
          ],
          [
            "abundância de comida e",
            "PERSON"
          ],
          [
            "para se comer",
            "PERSON"
          ],
          [
            "quanto mais fazemos",
            "PERSON"
          ],
          [
            "mais aprendemos",
            "PERSON"
          ],
          [
            "são essas duas",
            "ORG"
          ],
          [
            "mesmo de nascer e após morrer",
            "ORG"
          ],
          [
            "corpo e forma",
            "ORG"
          ]
        ],
        "readability_score": 81.80718562874252,
        "semantic_density": 0,
        "word_count": 167,
        "unique_words": 111,
        "lexical_diversity": 0.6646706586826348
      },
      "preservation_score": 1.5239488144048618e-05
    },
    {
      "id": 52,
      "text": " vá com calma e se for para reduzir, faça com calma, pois toda ação, têm uma reação proporcional para ambos os lados.\\n\\n“Cada corpo contém uma regra e em todas as regras precisam estar de bem estar.”\\n\\nO procurar e viver cheio de restrições alimentares totalmente fora do padrão dos nossos costumes junto a alimentos que nossos corpos não são acostumados é sinônimo de caganeira ou cocô de passarinho, quem consegue se adaptar a essa situação em viver com excesso ou escassez extrema, para chegar nessa aceitação um nível acima ou abaixo de um padrão corpóreo evolutivo e para se manter em ambos os níveis a fuga nos esteroides, bombas, grandes quantidades de alimentos de rápida absorção, exercícios constantes, drogas auxiliadoras, suplementos alimentares, suplementos vitamínicos e muitas outras coisas que nós dão saúde, muita dedicação, consumo de tempo e perda de tempo só de pensar durante o dia todo em cada vidro de carro que passa, para, e fica se admirando, já os espelhos de shoppings conse",
      "position": 50183,
      "chapter": 5,
      "page": 15,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.49281437125748,
      "complexity_metrics": {
        "word_count": 167,
        "sentence_count": 3,
        "paragraph_count": 3,
        "avg_sentence_length": 55.666666666666664,
        "avg_word_length": 4.976047904191617,
        "unique_word_ratio": 0.7305389221556886,
        "avg_paragraph_length": 55.666666666666664,
        "punctuation_density": 0.10778443113772455,
        "line_break_count": 4,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "calma",
          "ambos",
          "cada",
          "viver",
          "alimentares",
          "padrão",
          "nossos",
          "alimentos",
          "suplementos",
          "tempo",
          "reduzir",
          "faça",
          "pois",
          "toda",
          "ação",
          "reação",
          "proporcional",
          "lados",
          "corpo",
          "contém"
        ],
        "entities": [
          [
            "toda ação",
            "PERSON"
          ],
          [
            "têm uma",
            "ORG"
          ],
          [
            "para ambos",
            "PERSON"
          ],
          [
            "Cada",
            "PRODUCT"
          ],
          [
            "estar de bem estar",
            "PERSON"
          ],
          [
            "de rápida absorção",
            "ORG"
          ],
          [
            "drogas auxiliadoras",
            "GPE"
          ],
          [
            "vitamínicos e muitas",
            "ORG"
          ],
          [
            "dão saúde",
            "PERSON"
          ],
          [
            "só de pensar durante",
            "PERSON"
          ]
        ],
        "readability_score": 70.67385229540918,
        "semantic_density": 0,
        "word_count": 167,
        "unique_words": 122,
        "lexical_diversity": 0.7305389221556886
      },
      "preservation_score": 8.020783233709797e-06
    },
    {
      "id": 53,
      "text": "guimos ver até aquela veia que ganhamos em um dia de academia nós fazendo perder outros momentos que poderiam ser mais lembrados e engraçados que poderiam ainda vir ser mais saudáveis, não pelo cuidado do corpo, e sim, pelo cuidado mental de ficarmos menos estressados e agitados, assim nossas células nervosas ficam calmas e passivas sem movimentos incoerentes e agitados por todo o corpo, e quando estão dessa forma, trabalham em coletivo com um resfriado podendo se transforma em uma pneumonia, também temos o estar em pânico em uma pandemia que causa medo e nervosismo, e é esse sentimento, que aumentam o risco de pegar a própria doença.\\n\\nAté que ponto o medo de ficar doente é de maior benefício que o não ter medo?\\n\\n“Medo, histeria e problema são a nossa falha na Matrix.”\\n\\n   Toda a nossa vida não entendemos a falta de sono, dormir mal, ter sonhos estranhos e sem sentido que as vezes e por costumes não percebemos a quantidade de comida ingerida antes de dormir, até porque, para ter uma bo",
      "position": 51183,
      "chapter": 5,
      "page": 16,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.40571428571428,
      "complexity_metrics": {
        "word_count": 175,
        "sentence_count": 4,
        "paragraph_count": 4,
        "avg_sentence_length": 43.75,
        "avg_word_length": 4.685714285714286,
        "unique_word_ratio": 0.68,
        "avg_paragraph_length": 43.75,
        "punctuation_density": 0.09714285714285714,
        "line_break_count": 6,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "medo",
          "poderiam",
          "mais",
          "pelo",
          "cuidado",
          "corpo",
          "agitados",
          "nossa",
          "dormir",
          "guimos",
          "aquela",
          "veia",
          "ganhamos",
          "academia",
          "fazendo",
          "perder",
          "outros",
          "momentos",
          "lembrados",
          "engraçados"
        ],
        "entities": [
          [
            "guimos ver até aquela",
            "PERSON"
          ],
          [
            "dia de academia nós fazendo",
            "ORG"
          ],
          [
            "perder outros momentos que poderiam ser mais",
            "ORG"
          ],
          [
            "poderiam ainda",
            "PERSON"
          ],
          [
            "ser mais saudáveis",
            "ORG"
          ],
          [
            "não pelo",
            "PERSON"
          ],
          [
            "pelo cuidado",
            "PERSON"
          ],
          [
            "de ficarmos",
            "PERSON"
          ],
          [
            "nervosas ficam",
            "ORG"
          ],
          [
            "quando",
            "GPE"
          ]
        ],
        "readability_score": 76.71928571428572,
        "semantic_density": 0,
        "word_count": 175,
        "unique_words": 119,
        "lexical_diversity": 0.68
      },
      "preservation_score": 1.5239488144048618e-05
    },
    {
      "id": 54,
      "text": "a noite de sono e não ter o excesso de sono temos que padronizar o nosso dormir e para conseguirmos essa façanha, temos que estar confortáveis com os nossos pensamentos e os níveis hormonais principalmente o cortisona precisa estar em um nível “10 ao acordar e ao dormir no nível 3 aproximadamente”, não deixando de atentar para não comer em excesso antes de dormir, pois ao acordar o corpo vai assimilar o padrão a qual se encontra, e quando isso acontecer, irá perceber que para se manter no nível que despertou “precisa” repor a energia consumida durante o sono e equilibrar semelhante a última memória do dia anterior. Além dessa situação, temos o excesso de dormir e essa condição me lembra que o excesso de dormir não é necessário, e sim, precisamos dê 5, 6 até 7 horas por dia no máximo. Quando deitamos para dormir e se realmente apagamos ao dormir, são necessários 3 horas de sono profundo, 2 horas para sair do sono profundo e 1 a 2 horas para o corpo se acostumar e acordar para um novo viver.",
      "position": 52183,
      "chapter": 5,
      "page": 17,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 35.36758241758242,
      "complexity_metrics": {
        "word_count": 182,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 60.666666666666664,
        "avg_word_length": 4.521978021978022,
        "unique_word_ratio": 0.5604395604395604,
        "avg_paragraph_length": 182.0,
        "punctuation_density": 0.07692307692307693,
        "line_break_count": 0,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "dormir",
          "sono",
          "excesso",
          "horas",
          "temos",
          "nível",
          "acordar",
          "essa",
          "precisa",
          "corpo",
          "quando",
          "profundo",
          "noite",
          "padronizar",
          "nosso",
          "conseguirmos",
          "façanha",
          "confortáveis",
          "nossos",
          "pensamentos"
        ],
        "entities": [
          [
            "noite de",
            "ORG"
          ],
          [
            "excesso de sono",
            "ORG"
          ],
          [
            "para conseguirmos",
            "PERSON"
          ],
          [
            "precisa estar",
            "PERSON"
          ],
          [
            "10 ao acordar",
            "QUANTITY"
          ],
          [
            "3",
            "CARDINAL"
          ],
          [
            "não deixando de atentar",
            "ORG"
          ],
          [
            "corpo vai assimilar o",
            "ORG"
          ],
          [
            "irá perceber",
            "PERSON"
          ],
          [
            "dia",
            "ORG"
          ]
        ],
        "readability_score": 68.31007326007327,
        "semantic_density": 0,
        "word_count": 182,
        "unique_words": 102,
        "lexical_diversity": 0.5604395604395604
      },
      "preservation_score": 0.0
    },
    {
      "id": 55,
      "text": " Quando temos mais vontades em querer ficar dormindo, não por estarmos cansados do trabalho do dia a dia, e sim, pela procrastinação e o tédio em não ter nada para fazer, até porque, essas condições de dormir a hora que quiser e quando quer, nunca foram de luxo para todos da espécie humana e aqueles que foram criados nessa condição, não percebem a criação desregulada em ter uma boa noite de sono. Nós humanos precisamos dos excessos para sermos felizes ou tristes, amor e ódio e tudo que precisamos ter nos momentos extravagantes necessários serem vividos e apreciados, sem se perder nós excessos quando vivenciar e quando estiver satisfeito pela noite ou pelo dia engraçado e divertido, lembre-se: os nossos corpos vão querer mais e mais desse viver gostoso e sensacional.\\n\\n  “Restringir uma vida toda só para um propósito é deixar de viver os momentos que tanto sonhamos, trabalhamos e talvez iremos viver.” \\n\\n",
      "position": 53187,
      "chapter": 5,
      "page": 18,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 35.73235294117647,
      "complexity_metrics": {
        "word_count": 153,
        "sentence_count": 4,
        "paragraph_count": 2,
        "avg_sentence_length": 38.25,
        "avg_word_length": 4.9411764705882355,
        "unique_word_ratio": 0.7058823529411765,
        "avg_paragraph_length": 76.5,
        "punctuation_density": 0.09803921568627451,
        "line_break_count": 4,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "quando",
          "mais",
          "viver",
          "querer",
          "pela",
          "noite",
          "precisamos",
          "excessos",
          "momentos",
          "temos",
          "vontades",
          "ficar",
          "dormindo",
          "estarmos",
          "cansados",
          "trabalho",
          "procrastinação",
          "tédio",
          "nada",
          "fazer"
        ],
        "entities": [
          [
            "Quando",
            "PERSON"
          ],
          [
            "querer ficar dormindo",
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
            "nada",
            "ORG"
          ],
          [
            "para fazer",
            "PRODUCT"
          ],
          [
            "hora",
            "NORP"
          ],
          [
            "quando quer",
            "PERSON"
          ],
          [
            "nessa condição",
            "PERSON"
          ],
          [
            "noite de sono",
            "ORG"
          ]
        ],
        "readability_score": 79.39264705882353,
        "semantic_density": 0,
        "word_count": 153,
        "unique_words": 108,
        "lexical_diversity": 0.7058823529411765
      },
      "preservation_score": 4.812469940225879e-06
    },
    {
      "id": 56,
      "text": "Não participar de uma brincadeira com um filho, não beijar uma mãe, não abraçar um amigo, não ter um tempo consigo mesmo, não ter momentos de confiança que trabalhamos para conquistar e não vivemos, e essa situação, vem junto com a ansiedade, cobrança, exigências e tudo que queremos dar de melhor, sem conseguir viver o melhor.\\n\\nCapítulo 8\\n\\nFrases e textos, reflexão ou loucura?\\n\\nFormas de se perder na vida devido ao próprio pensar ser melhor:\\n\\n Imaginar que uma vida a qual está olhando ser melhor que a nossa.\\n\\nTer inveja de algo, sem saber que aquele algo possa ser ruim, quando se tem.\\n\\nNão pensar, que pensar algo ruim, seja ruim de pensar.\\n\\nDeixar o nosso sentimento ser contra o viver do outro.\\n\\nO nosso viver não pode ser melhor, que, daqueles que temos respeito e confiança.\\n\\nNosso viver não têm e nem precisa ser melhor ou pior que o de alguém, apenas diferente.\\n\\nTer medo do próprio sentimento e do próprio viver. \\n\\n",
      "position": 54102,
      "chapter": 5,
      "page": 19,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 25.48672086720867,
      "complexity_metrics": {
        "word_count": 164,
        "sentence_count": 9,
        "paragraph_count": 11,
        "avg_sentence_length": 18.22222222222222,
        "avg_word_length": 4.585365853658536,
        "unique_word_ratio": 0.6280487804878049,
        "avg_paragraph_length": 14.909090909090908,
        "punctuation_density": 0.16463414634146342,
        "line_break_count": 22,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "melhor",
          "viver",
          "pensar",
          "próprio",
          "algo",
          "ruim",
          "nosso",
          "confiança",
          "vida",
          "sentimento",
          "participar",
          "brincadeira",
          "filho",
          "beijar",
          "abraçar",
          "amigo",
          "tempo",
          "consigo",
          "mesmo",
          "momentos"
        ],
        "entities": [
          [
            "beijar uma mãe",
            "ORG"
          ],
          [
            "essa situação",
            "ORG"
          ],
          [
            "cobrança",
            "ORG"
          ],
          [
            "sem conseguir viver o melhor",
            "ORG"
          ],
          [
            "8",
            "CARDINAL"
          ],
          [
            "reflexão ou loucura",
            "ORG"
          ],
          [
            "Formas de se",
            "PERSON"
          ],
          [
            "Imaginar",
            "LOC"
          ],
          [
            "quando se",
            "PERSON"
          ],
          [
            "Deixar",
            "PERSON"
          ]
        ],
        "readability_score": 89.51327913279133,
        "semantic_density": 0,
        "word_count": 164,
        "unique_words": 103,
        "lexical_diversity": 0.6280487804878049
      },
      "preservation_score": 0.00021836582353774924
    },
    {
      "id": 57,
      "text": "Pensar que o meu estudo é melhor e definitivo.\\n\\nNão analisar, interpretar e compreender a si.\\n\\nPensar que sempre a melhor resposta é se omitir.\\n\\nPensar que não somos capazes de fazer algo.\\n\\nTer vergonha de si.\\n\\n“Uma imagem mostra muito mais verdade que uma verdade.”\\n\\n“Nossas vidas é um eterno que eu não sei quais são.”\\n\\n“O maior mal que um humano possa ter é não ter paciência consigo mesmo.”\\n\\nNão tendo paciência consigo mesmo, não conseguimos ser racionais em ter paciência para enxergar as próprias falhas, não conseguindo ter consciência em observar nossas falhas, não temos paciência com os nossos impulsos, falta de paciência em ficar em casa, observar o seu entorno, ouvir o próximo, interpretar próximo e entender o sentimento do próximo.\\n\\n“Nascemos sem pedir e por muitas vezes a ingratidão originária desse ocorrido, toma conta!” \\n\\nCrescemos com pessoas que admiramos, confiamos, amamos, brigamos, apoiamos e tudo que é necessário viver para sermos o que somos, nascemos sem “motivação de",
      "position": 55031,
      "chapter": 5,
      "page": 20,
      "segment_type": "preserved_segment",
      "themes": {
        "filosofia": 16.129032258064516,
        "ciencia": 83.87096774193549
      },
      "difficulty": 24.11299498047964,
      "complexity_metrics": {
        "word_count": 163,
        "sentence_count": 11,
        "paragraph_count": 11,
        "avg_sentence_length": 14.818181818181818,
        "avg_word_length": 5.07361963190184,
        "unique_word_ratio": 0.6748466257668712,
        "avg_paragraph_length": 14.818181818181818,
        "punctuation_density": 0.147239263803681,
        "line_break_count": 20,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "paciência",
          "pensar",
          "próximo",
          "melhor",
          "interpretar",
          "somos",
          "verdade",
          "nossas",
          "consigo",
          "mesmo",
          "falhas",
          "observar",
          "nascemos",
          "estudo",
          "definitivo",
          "analisar",
          "compreender",
          "sempre",
          "resposta",
          "omitir"
        ],
        "entities": [
          [
            "Pensar que",
            "GPE"
          ],
          [
            "muito mais verdade",
            "PERSON"
          ],
          [
            "Nossas",
            "ORG"
          ],
          [
            "que eu não sei quais",
            "PERSON"
          ],
          [
            "humano possa",
            "PERSON"
          ],
          [
            "não conseguimos ser racionais em",
            "ORG"
          ],
          [
            "falta de paciência",
            "ORG"
          ],
          [
            "casa",
            "GPE"
          ],
          [
            "interpretar próximo",
            "PERSON"
          ],
          [
            "Nascemos",
            "PERSON"
          ]
        ],
        "readability_score": 91.06882320133855,
        "semantic_density": 0,
        "word_count": 163,
        "unique_words": 110,
        "lexical_diversity": 0.6748466257668712
      },
      "preservation_score": 0.00024262869281972137
    },
    {
      "id": 58,
      "text": " viver” e ao decorrer da vida fui adquirindo felicidades, tristezas, amor, dores, problemas, caos, angústia e todas aquelas coisas que me fizeram querer viver novamente e outras que me ensinaram a não viver novamente, em meu viver curti carnavais, fui ao Maracanã várias vezes, fui nos pagodes tradicionais, curti escolas de samba, vou em raves, sertanejo, festas juninas, réveillon em copa, corri na praia, almocei de frente a praia com pouco dinheiro, fui em vários puteiros e nunca na vida deixei de viver e sempre procurei a diversão onde meu bolso cabe, minha vida não é exemplo para aqueles que não amam a sua própria casa, até porque, a minha casa se chama Brasil.\\n\\nAqueles que falam que o Brasil é uma merda, não sabe o valor de viver com gratidão, pois todos aqueles que percebem a gratidão de ser brasileiro vão entender que 90 por cento dos Negro moram nas favelas, vão entender que todos aqueles países que os brasileiros idolatram são os mesmos que destruíram sua casa e destroem casas alheias, toda essa gana de viver, fazem outros viverem na miséria, sabe por que isso ocorre?\\n\\n",
      "position": 56031,
      "chapter": 5,
      "page": 21,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.439361702127655,
      "complexity_metrics": {
        "word_count": 188,
        "sentence_count": 2,
        "paragraph_count": 2,
        "avg_sentence_length": 94.0,
        "avg_word_length": 4.797872340425532,
        "unique_word_ratio": 0.6808510638297872,
        "avg_paragraph_length": 94.0,
        "punctuation_density": 0.14893617021276595,
        "line_break_count": 4,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "viver",
          "aqueles",
          "vida",
          "casa",
          "novamente",
          "curti",
          "praia",
          "minha",
          "brasil",
          "sabe",
          "gratidão",
          "todos",
          "entender",
          "decorrer",
          "adquirindo",
          "felicidades",
          "tristezas",
          "amor",
          "dores",
          "problemas"
        ],
        "entities": [
          [
            "Maracanã",
            "ORG"
          ],
          [
            "vou",
            "ORG"
          ],
          [
            "sertanejo",
            "ORG"
          ],
          [
            "festas juninas",
            "PERSON"
          ],
          [
            "pouco dinheiro",
            "PERSON"
          ],
          [
            "fui em vários puteiros",
            "ORG"
          ],
          [
            "para aqueles",
            "PERSON"
          ],
          [
            "casa",
            "ORG"
          ],
          [
            "Brasil",
            "PERSON"
          ],
          [
            "falam",
            "GPE"
          ]
        ],
        "readability_score": 51.56063829787234,
        "semantic_density": 0,
        "word_count": 188,
        "unique_words": 128,
        "lexical_diversity": 0.6808510638297872
      },
      "preservation_score": 7.75342379258614e-06
    },
    {
      "id": 59,
      "text": " O Brasileiro não sabe o valor de ser brasileiro!!!\\n\\n“Quem sabe a dor de sentir fome, sabe o quão difícil é controlar os nossos impulsos.”\\n\\nAo sair de casa coloco uma música, passo meu perfume e no trajeto do trabalho observo o local onde moro, esse mesmo lugar é uma favela chamada Tirol, essa favela me ensina a entender a dor que vivi e ter empatia pela lembrança da mesma. \\n\\nQuem sabe a dor de sentir fome sem ter como resolver, consegue compreender qual é a expressão da fome.\\n\\nVejo pessoas que vi crescendo passando fome e traficando, pois ninguém olha com confiança para aqueles, logo essa mesma o faz ser caos efeito.\\n\\nEu vejo políticos prejudicando 208 milhões de pessoas e terem privilégios ao ser preso, lembrando que: ele faz isso sem passar fome. \\n\\nNão estou querendo ser a favor do erro, estou sendo a favor da penitência digna.\\n\\n“Nem todos tiveram a sorte que eu tive ao passar fome. Essa mesma que me fez entender é a mesma que me faz ser o que eu sou, não por minha competência, sim pela competência de minha mãe.",
      "position": 57124,
      "chapter": 5,
      "page": 22,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 26.829255319148935,
      "complexity_metrics": {
        "word_count": 188,
        "sentence_count": 9,
        "paragraph_count": 8,
        "avg_sentence_length": 20.88888888888889,
        "avg_word_length": 4.430851063829787,
        "unique_word_ratio": 0.6542553191489362,
        "avg_paragraph_length": 23.5,
        "punctuation_density": 0.12234042553191489,
        "line_break_count": 14,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "fome",
          "sabe",
          "mesma",
          "essa",
          "brasileiro",
          "quem",
          "sentir",
          "favela",
          "entender",
          "pela",
          "vejo",
          "pessoas",
          "passar",
          "estou",
          "favor",
          "minha",
          "competência",
          "valor",
          "quão",
          "difícil"
        ],
        "entities": [
          [
            "valor de ser",
            "ORG"
          ],
          [
            "moro",
            "ORG"
          ],
          [
            "favela chamada Tirol",
            "PERSON"
          ],
          [
            "Vejo",
            "GPE"
          ],
          [
            "essa mesma",
            "ORG"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "208",
            "CARDINAL"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "penitência digna",
            "PERSON"
          ],
          [
            "que eu",
            "PERSON"
          ]
        ],
        "readability_score": 88.22630023640662,
        "semantic_density": 0,
        "word_count": 188,
        "unique_words": 123,
        "lexical_diversity": 0.6542553191489362
      },
      "preservation_score": 9.731883656901226e-05
    },
    {
      "id": 60,
      "text": " Por ter uma mãe digna em saber me guiar na fome, não serei o que posso ser, até porque, não teria forças para suportar a vergonha que era passar fome.”\\n\\nNós evoluímos na vida sabendo limitar as situações que vão nos puxar para o lado oposto, até que ponto o limitar “o lado oposto” realmente vai nós beneficiar?\\n\\n“Rico se mata por não saber lhe dar com perda (material ou sentimental) e pobre se mata cavando a própria cova (drogas).”\\n\\nAssim percebo que grande parte dos endinheirados que querem ter mais, qualquer pequena perda se torna grande. O miserável que vive em fuga, mais drogas irá usar, até porque, tem grande chance de ser a única felicidade a qual pode ter com fome na miséria.\\n\\nQuando terminei o livro chamado “O Presidente”, inspirado no livro “O Príncipe” de Maquiavel, percebi que somos paradigmas de nós mesmos e qualquer conclusão que chegava era impossível ser concluída, não por causa de comida, fome, religião, cor, sexo ou qualquer coisa que provém em aceitar o próprio destino. \\n\\n",
      "position": 58154,
      "chapter": 5,
      "page": 23,
      "segment_type": "preserved_segment",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 33.08735632183908,
      "complexity_metrics": {
        "word_count": 174,
        "sentence_count": 6,
        "paragraph_count": 5,
        "avg_sentence_length": 29.0,
        "avg_word_length": 4.735632183908046,
        "unique_word_ratio": 0.7011494252873564,
        "avg_paragraph_length": 34.8,
        "punctuation_density": 0.1206896551724138,
        "line_break_count": 10,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "fome",
          "grande",
          "qualquer",
          "saber",
          "porque",
          "limitar",
          "lado",
          "oposto",
          "mata",
          "perda",
          "drogas",
          "mais",
          "livro",
          "digna",
          "guiar",
          "serei",
          "posso",
          "teria",
          "forças",
          "suportar"
        ],
        "entities": [
          [
            "digna",
            "PERSON"
          ],
          [
            "posso ser",
            "FAC"
          ],
          [
            "não teria forças para suportar",
            "ORG"
          ],
          [
            "lado oposto",
            "PERSON"
          ],
          [
            "Rico",
            "LAW"
          ],
          [
            "perda",
            "PERSON"
          ],
          [
            "Assim",
            "NORP"
          ],
          [
            "que querem",
            "PERSON"
          ],
          [
            "qualquer pequena perda se torna",
            "PERSON"
          ],
          [
            "mais drogas irá usar",
            "PERSON"
          ]
        ],
        "readability_score": 84.07931034482759,
        "semantic_density": 0,
        "word_count": 174,
        "unique_words": 122,
        "lexical_diversity": 0.7011494252873564
      },
      "preservation_score": 5.681388123877773e-05
    },
    {
      "id": 61,
      "text": "Todos nós estamos presos a um passado tão distante que não percebemos o quanto evoluímos o conforto e não o pensar, até porque, são as mesmas semelhanças nos erros cometidos, os mesmos ciclos religiosos, e a luxúria, nunca saiu de moda junto ao pensar que a nossa felicidade é maior e melhor por merecer em ter mais direito de satisfazer o próprio ego.\\n\\nTenho amigos empresários reclamando que trabalham muito, para quem não quer trabalhar.\\n\\nTenho amigos na área da saúde falando que a profissão é mais digna comparado a outras profissões.\\n\\nVejo pessoas que trabalham na área da segurança reclamando da insegurança. \\n\\nTodo mundo é aquilo que necessita ser, para merecer ter.\\n\\nO meu, o seu, o nosso não é melhor, nem pior, apenas somos diferentes em cada profissão necessária coexistir.\\n\\nSe não sabemos como queremos e quais são as nossas prioridades e felicidades, sempre estaremos reclamando da fuga de alguém feliz ao invés de viver a própria vida!!!\\n\\n",
      "position": 59159,
      "chapter": 5,
      "page": 24,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 27.90232142857143,
      "complexity_metrics": {
        "word_count": 160,
        "sentence_count": 7,
        "paragraph_count": 7,
        "avg_sentence_length": 22.857142857142858,
        "avg_word_length": 4.9125,
        "unique_word_ratio": 0.70625,
        "avg_paragraph_length": 22.857142857142858,
        "punctuation_density": 0.13125,
        "line_break_count": 14,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "reclamando",
          "pensar",
          "melhor",
          "merecer",
          "mais",
          "tenho",
          "amigos",
          "trabalham",
          "área",
          "profissão",
          "todos",
          "estamos",
          "presos",
          "passado",
          "distante",
          "percebemos",
          "quanto",
          "evoluímos",
          "conforto",
          "porque"
        ],
        "entities": [
          [
            "nós estamos",
            "ORG"
          ],
          [
            "presos",
            "PERSON"
          ],
          [
            "quanto evoluímos",
            "PERSON"
          ],
          [
            "mesmas semelhanças",
            "PERSON"
          ],
          [
            "mesmos ciclos religiosos",
            "PERSON"
          ],
          [
            "próprio ego",
            "PERSON"
          ],
          [
            "Tenho",
            "ORG"
          ],
          [
            "trabalham muito",
            "PERSON"
          ],
          [
            "para quem não quer",
            "PERSON"
          ],
          [
            "Tenho",
            "ORG"
          ]
        ],
        "readability_score": 87.09767857142857,
        "semantic_density": 0,
        "word_count": 160,
        "unique_words": 113,
        "lexical_diversity": 0.70625
      },
      "preservation_score": 6.877821622906154e-05
    },
    {
      "id": 62,
      "text": "“O não conhecer a si próprio é a certeza de viver uma vida de merda.”\\n\\nSe temos medos de aceitar a vida que já foi vivida como iremos enxergar a felicidade, amor, ódio, carinho, afeto, empatia, alegria, fugas, valores, confiança e tudo que é necessário viver, para saber se sabemos viver?\\n\\nSe temos medo de nós conhecer como podemos cobrar e exigir algo que não somos capazes de perceber dentro do próprio viver?  O viver provém da nossa própria inteligência ou sabedoria em prever os próprios movimentos e não saber o “básico”, nós deixa cegos diante de uma certeza que imaginamos ser como melhor.\\n\\nO que adianta almejar uma vida a qual não me sinto confortável em estar onde precisa estar, sendo “forçado” a viver com pessoas e lugares que o nosso destino provém de se sentir desconfortável, seja uma casa que moramos, por uma empolgação de ser muito feliz e perder os compromissos que vão nós fazer melhores e mais feliz ou um membro da família, esse, pode ser um parasita sem perceber perante a s",
      "position": 60113,
      "chapter": 5,
      "page": 25,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 35.18983050847458,
      "complexity_metrics": {
        "word_count": 177,
        "sentence_count": 5,
        "paragraph_count": 4,
        "avg_sentence_length": 35.4,
        "avg_word_length": 4.632768361581921,
        "unique_word_ratio": 0.655367231638418,
        "avg_paragraph_length": 44.25,
        "punctuation_density": 0.11299435028248588,
        "line_break_count": 6,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "viver",
          "vida",
          "como",
          "conhecer",
          "próprio",
          "certeza",
          "temos",
          "saber",
          "perceber",
          "provém",
          "feliz",
          "merda",
          "medos",
          "aceitar",
          "vivida",
          "iremos",
          "enxergar",
          "felicidade",
          "amor",
          "ódio"
        ],
        "entities": [
          [
            "necessário",
            "GPE"
          ],
          [
            "Se",
            "PERSON"
          ],
          [
            "medo de nós",
            "ORG"
          ],
          [
            "como podemos cobrar e exigir",
            "ORG"
          ],
          [
            "nós deixa",
            "ORG"
          ],
          [
            "diante de uma certeza",
            "PERSON"
          ],
          [
            "precisa estar",
            "PERSON"
          ],
          [
            "nosso destino",
            "PERSON"
          ],
          [
            "de se",
            "PERSON"
          ],
          [
            "perceber perante a s",
            "ORG"
          ]
        ],
        "readability_score": 80.91016949152542,
        "semantic_density": 0,
        "word_count": 177,
        "unique_words": 116,
        "lexical_diversity": 0.655367231638418
      },
      "preservation_score": 2.085403640764548e-05
    },
    {
      "id": 63,
      "text": "i, não pelo lado ruim, e sim, por não ter empatia, esse é o mesmo que nós empurra para o abismo de um viver melhor, alegre, amoroso, carinhoso e todas aquelas coisas que nós humanos geralmente somos felizes.\\n\\nNão adianta querer ser um bombeiro, policial, atleta e qualquer coisa que necessita do corpo não gostando de exercitar-se e de seguir uma doutrina.\\n\\nNão adianta querer ganhar dinheiro, se não sei usar o dinheiro a meu favor.\\n\\nNão adianta querer ter poder, status sociais, influencia e qualquer coisa que chama atenção para si próprio se não sei lhe dar com o tamanho da visibilidade adquirida.\\n\\nDe nada adianta, qualquer coisa, se não sei qual é o tamanho dos malefícios diante dos meus benefícios.\\n\\nO intuito de qualquer rede social é socialização direcionada.\\n\\nTinder – relacionamento\\n\\nInstagram –socializar e trabalho Facebook-socializar e trabalho\\n\\nLinkedIn – trabalho\\n\\nTwitter – trabalho, socializar e informações dinâmicas quando vejo qualquer uma dessas redes sociais, enxergo o mesmo padrão em todas, como assim:\\n\\n",
      "position": 61113,
      "chapter": 5,
      "page": 26,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 28.402323580034423,
      "complexity_metrics": {
        "word_count": 166,
        "sentence_count": 7,
        "paragraph_count": 10,
        "avg_sentence_length": 23.714285714285715,
        "avg_word_length": 5.150602409638554,
        "unique_word_ratio": 0.6807228915662651,
        "avg_paragraph_length": 16.6,
        "punctuation_density": 0.14457831325301204,
        "line_break_count": 20,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "qualquer",
          "adianta",
          "trabalho",
          "querer",
          "coisa",
          "socializar",
          "mesmo",
          "todas",
          "dinheiro",
          "sociais",
          "tamanho",
          "pelo",
          "lado",
          "ruim",
          "empatia",
          "esse",
          "empurra",
          "abismo",
          "viver",
          "melhor"
        ],
        "entities": [
          [
            "não pelo lado ruim",
            "PERSON"
          ],
          [
            "mesmo",
            "ORG"
          ],
          [
            "que",
            "CARDINAL"
          ],
          [
            "nós empurra",
            "ORG"
          ],
          [
            "humanos geralmente somos",
            "NORP"
          ],
          [
            "atleta e qualquer",
            "PERSON"
          ],
          [
            "não sei usar o dinheiro",
            "ORG"
          ],
          [
            "influencia e qualquer coisa",
            "PERSON"
          ],
          [
            "chama atenção para si próprio se não sei",
            "PERSON"
          ],
          [
            "qualquer coisa",
            "PERSON"
          ]
        ],
        "readability_score": 86.59767641996558,
        "semantic_density": 0,
        "word_count": 166,
        "unique_words": 113,
        "lexical_diversity": 0.6807228915662651
      },
      "preservation_score": 0.00017378363673037895
    },
    {
      "id": 64,
      "text": "Todas as redes sociais quando postamos algumas coisas são no intuito de passar algumas informações, seja ela feliz, caótica, trabalho, amor e quaisquer outras coisas que passam em nossas mentes como necessário ser informado.\\n\\nSe todos os dias postamos as mesmas coisas o que queremos dizer?\\n\\nEstamos vivendo o mesmo ciclo de vida e não enxergamos que deixamos de viver?\\n\\nPostamos as mesmas coisas para ensinarmos outros? \\n\\nAquilo que postamos é o que mais nos interessamos? \\n\\nPara postarmos sobre algum assunto é devido a pensarmos bastante durante o dia?\\n\\nNossas vidas são tão ruins que precisamos de uma curtida, elogio, conversar, ser visível ou qualquer outra coisa que não sei fazer quando estou perto de outro humano ou em tédio?\\n\\nNão conseguimos enxergar a propagação da energia e acabamos postando as mesmas coisas por não perceber o próprio tempo?\\n\\nQualquer coisa que me ocupa tempo, pois mente vazia é oficina do diabo.\\n\\n",
      "position": 62144,
      "chapter": 5,
      "page": 27,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 24.960233918128655,
      "complexity_metrics": {
        "word_count": 152,
        "sentence_count": 9,
        "paragraph_count": 9,
        "avg_sentence_length": 16.88888888888889,
        "avg_word_length": 5.052631578947368,
        "unique_word_ratio": 0.7368421052631579,
        "avg_paragraph_length": 16.88888888888889,
        "punctuation_density": 0.1118421052631579,
        "line_break_count": 18,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "coisas",
          "postamos",
          "mesmas",
          "quando",
          "algumas",
          "nossas",
          "qualquer",
          "coisa",
          "tempo",
          "todas",
          "redes",
          "sociais",
          "intuito",
          "passar",
          "informações",
          "seja",
          "feliz",
          "caótica",
          "trabalho",
          "amor"
        ],
        "entities": [
          [
            "Todas",
            "PERSON"
          ],
          [
            "quando postamos",
            "PERSON"
          ],
          [
            "algumas coisas são",
            "PERSON"
          ],
          [
            "ela feliz",
            "PERSON"
          ],
          [
            "outras coisas",
            "PERSON"
          ],
          [
            "necessário ser informado",
            "ORG"
          ],
          [
            "Se",
            "PERSON"
          ],
          [
            "mesmas coisas",
            "PERSON"
          ],
          [
            "Estamos",
            "PERSON"
          ],
          [
            "mesmo ciclo de vida",
            "ORG"
          ]
        ],
        "readability_score": 90.03976608187135,
        "semantic_density": 0,
        "word_count": 152,
        "unique_words": 112,
        "lexical_diversity": 0.7368421052631579
      },
      "preservation_score": 9.203848760681994e-05
    },
    {
      "id": 65,
      "text": "“Cada um necessita agir para com o outro igual para si próprio.”\\n\\nÉ “tradição” o homem pagar a conta para as mulheres e as mulheres querem acabar com a tradição de ser dona de casa, mãe, não ser azarada por ser incômodo, o corpo é meu eu faço o que eu quiser e muitas outras coisas que o movimento humano denominado feminismo apoiam, me parece não ser de bom agrado para as mulheres.\\n\\nComo o homem pagar a conta é benefício para as mulheres e os homens trabalham muito mais, assim contêm mais dinheiro, têm mais benefícios, não sangra, não fica grávido e todas aquelas coisas que nascemos por sermos o que somos: “acho muito justo o homem pagar tudo para todas as mulheres.”\\n\\nPara mim o pagar a conta é relativo ao financeiro de cada um. Se por acaso o homem têm um poder aquisitivo melhor, ele paga. se por acaso a mulher tiver um poder aquisitivo melhor, ela paga.\\n\\nErros de julgamentos em testes que todos acham que são medidores de inteligência:\\n\\n",
      "position": 63075,
      "chapter": 5,
      "page": 28,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 28.844991789819378,
      "complexity_metrics": {
        "word_count": 174,
        "sentence_count": 7,
        "paragraph_count": 5,
        "avg_sentence_length": 24.857142857142858,
        "avg_word_length": 4.436781609195402,
        "unique_word_ratio": 0.5977011494252874,
        "avg_paragraph_length": 34.8,
        "punctuation_density": 0.10344827586206896,
        "line_break_count": 10,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "mulheres",
          "homem",
          "pagar",
          "conta",
          "mais",
          "cada",
          "tradição",
          "coisas",
          "muito",
          "todas",
          "acaso",
          "poder",
          "aquisitivo",
          "melhor",
          "paga",
          "necessita",
          "agir",
          "outro",
          "igual",
          "próprio"
        ],
        "entities": [
          [
            "mulheres querem",
            "PERSON"
          ],
          [
            "dona de casa",
            "ORG"
          ],
          [
            "meu eu faço o que eu quiser",
            "PERSON"
          ],
          [
            "feminismo apoiam",
            "PERSON"
          ],
          [
            "Como",
            "ORG"
          ],
          [
            "benefício para",
            "PERSON"
          ],
          [
            "homens trabalham muito mais",
            "PERSON"
          ],
          [
            "assim contêm mais dinheiro",
            "PERSON"
          ],
          [
            "têm mais benefícios",
            "ORG"
          ],
          [
            "não sangra",
            "ORG"
          ]
        ],
        "readability_score": 86.24039408866994,
        "semantic_density": 0,
        "word_count": 174,
        "unique_words": 104,
        "lexical_diversity": 0.5977011494252874
      },
      "preservation_score": 4.010391616854899e-05
    },
    {
      "id": 66,
      "text": "Teste de QI – quando medimos uma inteligência quando somos crianças, medimos a quantidade de raciocínio lógico que uma pessoa possa desenvolver a base de correlacionar imagens e padrões.\\n\\nErro – pessoas com dislexia são burros.\\n\\nJunção – pessoas com dislexia precisam viver para correlacionar suas próprias linhas de raciocínio. Percebi que conseguimos correlacionar o movimento do sentir junto ao raciocínio lógico do bem estar ou mal estar, logo, quando não vivencio o sentimento semelhante ao movimento não consigo correlacionar o sentir da imagem, alma, cheiro, som, paladar, tocar e tudo que provém de um próprio interpretar o raciocínio lógico de uma pessoa com dislexia.\\n\\nO conseguir concentrar-se e viver o próprio Universo (forma de raciocínio lógico), essa forma de pensar, nós faz esquecer do Universo externo e concentrar no meu próprio Universo imaginário, se por acaso obtiver a necessidade de usar alguma droga como fuga para relaxar, fume um baseado, coloca uma música, esqueça de tudo e foque em resolver o problema antes de acontecer.\\n\\n",
      "position": 64026,
      "chapter": 5,
      "page": 29,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 33.19759036144578,
      "complexity_metrics": {
        "word_count": 166,
        "sentence_count": 5,
        "paragraph_count": 4,
        "avg_sentence_length": 33.2,
        "avg_word_length": 5.325301204819277,
        "unique_word_ratio": 0.6506024096385542,
        "avg_paragraph_length": 41.5,
        "punctuation_density": 0.1144578313253012,
        "line_break_count": 8,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "raciocínio",
          "lógico",
          "correlacionar",
          "quando",
          "dislexia",
          "próprio",
          "universo",
          "medimos",
          "pessoa",
          "pessoas",
          "viver",
          "movimento",
          "sentir",
          "tudo",
          "concentrar",
          "forma",
          "teste",
          "inteligência",
          "somos",
          "crianças"
        ],
        "entities": [
          [
            "Teste de QI",
            "ORG"
          ],
          [
            "quando medimos uma inteligência quando somos crianças",
            "PERSON"
          ],
          [
            "Percebi",
            "ORG"
          ],
          [
            "raciocínio lógico",
            "PERSON"
          ],
          [
            "estar",
            "PRODUCT"
          ],
          [
            "mal estar",
            "PRODUCT"
          ],
          [
            "quando não",
            "PERSON"
          ],
          [
            "da imagem",
            "PERSON"
          ],
          [
            "alma",
            "GPE"
          ],
          [
            "cheiro",
            "GPE"
          ]
        ],
        "readability_score": 81.80240963855422,
        "semantic_density": 0,
        "word_count": 166,
        "unique_words": 108,
        "lexical_diversity": 0.6506024096385542
      },
      "preservation_score": 2.352763081888208e-05
    },
    {
      "id": 67,
      "text": "Como eu me concentro em qualquer lugar?\\n\\nSe for morrer, não saberei. Não sabendo, não me importo. Dessa forma o que eu esteja pensando de valor para um bem com um todo, nada me importa pensar na morte, essa situação, provém junto a uma calmaria dê não entrar em pânico pela própria histeria.\\n\\nNosso pensar são tão focados no passado já vivido, junto a  um futuro que eu quero e espero poder viver, provida pela falta de viver no presente assim não consegue se ter o futuro imaginado e um passado digno de ser lembrado, e isso, ocorre por não reconhecermos a confusão mental do próprio passado, até porque, se tivéssemos reconhecimento nós conseguiríamos reconhecer a nossa melhor forma de movimentar-se no presente.\\n\\n“Todos os humanos que foram obrigados a fazer aquilo que não estavam afim de fazer e fizeram, esse fazer nunca será tão bem feito quanto aquele que fez por vontade própria.”\\n\\n“Minha maior ganância é poder acordar sem a obrigação de acordar.”\\n\\n",
      "position": 65080,
      "chapter": 5,
      "page": 30,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 26.872045454545454,
      "complexity_metrics": {
        "word_count": 165,
        "sentence_count": 8,
        "paragraph_count": 5,
        "avg_sentence_length": 20.625,
        "avg_word_length": 4.781818181818182,
        "unique_word_ratio": 0.7212121212121212,
        "avg_paragraph_length": 33.0,
        "punctuation_density": 0.11515151515151516,
        "line_break_count": 10,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "passado",
          "fazer",
          "forma",
          "pensar",
          "junto",
          "pela",
          "própria",
          "futuro",
          "poder",
          "viver",
          "presente",
          "acordar",
          "como",
          "concentro",
          "qualquer",
          "lugar",
          "morrer",
          "saberei",
          "sabendo",
          "importo"
        ],
        "entities": [
          [
            "Como eu",
            "PERSON"
          ],
          [
            "qualquer lugar",
            "PERSON"
          ],
          [
            "Se",
            "PERSON"
          ],
          [
            "Dessa forma o que eu",
            "PERSON"
          ],
          [
            "pensando de valor",
            "ORG"
          ],
          [
            "nada me",
            "ORG"
          ],
          [
            "importa pensar",
            "PERSON"
          ],
          [
            "essa situação",
            "ORG"
          ],
          [
            "pânico pela",
            "PERSON"
          ],
          [
            "própria histeria",
            "PERSON"
          ]
        ],
        "readability_score": 88.25295454545454,
        "semantic_density": 0,
        "word_count": 165,
        "unique_words": 119,
        "lexical_diversity": 0.7212121212121212
      },
      "preservation_score": 4.010391616854899e-05
    },
    {
      "id": 68,
      "text": "Percebo que em nossas vidas devemos fazer esforços, sacrifícios, superações, determinação e tudo que provém de ter necessidade em ser feito para conseguir o necessário em um viver confortável com todos aqueles que precisamos ter gratidão por nós fazer felizes.\\n\\nAté que ponto:\\n\\nSer e ter gratidão?\\n\\nNecessário se sacrificar?\\n\\nNecessidade de deixar o próprio viver e melhorar a própria autoestima? \\n\\nDeixar de viver a própria vida irá me dar um ganho maior que o meu tempo perdido? \\n\\nQual é o valor do sacrifício feito para conquistar a gratidão?\\n\\nQuanto vale o meu tempo?\\n\\nComo irei ensinar o meu filho a viver, se não sei viver? \\n\\nO meu viver é incômodo para aqueles que não contém empatia por um estilo de vida a qual me faz feliz? \\n\\n“Nossas vidas só é exemplo para aqueles com pensamentos semelhantes ao nosso.”\\n\\nReligiões, políticas, crenças, importâncias, lutas, sonhos, vestimentas, forma de falar e tudo que é feliz para um grupo é infelicidade para outros.\\n\\n",
      "position": 66040,
      "chapter": 5,
      "page": 31,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 23.83382269904009,
      "complexity_metrics": {
        "word_count": 161,
        "sentence_count": 11,
        "paragraph_count": 12,
        "avg_sentence_length": 14.636363636363637,
        "avg_word_length": 4.900621118012422,
        "unique_word_ratio": 0.639751552795031,
        "avg_paragraph_length": 13.416666666666666,
        "punctuation_density": 0.14285714285714285,
        "line_break_count": 24,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "viver",
          "aqueles",
          "gratidão",
          "nossas",
          "vidas",
          "fazer",
          "tudo",
          "necessidade",
          "feito",
          "necessário",
          "deixar",
          "própria",
          "vida",
          "tempo",
          "qual",
          "feliz",
          "percebo",
          "devemos",
          "esforços",
          "sacrifícios"
        ],
        "entities": [
          [
            "nossas vidas",
            "PERSON"
          ],
          [
            "devemos fazer",
            "PERSON"
          ],
          [
            "esforços",
            "PERSON"
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
            "Necessário",
            "GPE"
          ],
          [
            "Deixar",
            "PERSON"
          ],
          [
            "sacrifício feito",
            "PERSON"
          ],
          [
            "Quanto",
            "PRODUCT"
          ],
          [
            "Como",
            "ORG"
          ]
        ],
        "readability_score": 91.21163184641446,
        "semantic_density": 0,
        "word_count": 161,
        "unique_words": 103,
        "lexical_diversity": 0.639751552795031
      },
      "preservation_score": 0.0002406234970112939
    },
    {
      "id": 69,
      "text": "Nossas vidas são ciclos, em quais ciclos queremos viver?\\n\\nPratiquemos os ciclos em agregar os melhores momentos, até porque, os ciclos em meio ao caos nós temos PhD, mestrado, doutorado, faculdade, MIT, supletivo, primário, creche e todos as formas de aprender sobre.\\n\\n“Sem dedicação e comprometimento não tem como haver confiança. Temos empenho e compromissos que não são dignos de serem confiáveis.”\\n\\nNós podemos fazer o que quisermos.\\n\\nNós podemos ser o que quisermos. \\n\\nNós podemos amar quando sentimos. \\n\\nPodemos ser amor se quisermos.\\n\\nPodemos ser o que queremos ser. \\n\\nBasta entendermos que seremos aquilo que escolhemos.\\n\\nToda pequena felicidade torna-se grande e tudo depende do momento em que escolhemos o pensar nela como grande.\\n\\nNão somos uma rotina de desastres caóticos e por mais que o universo observável tenha mais matéria escura, massa escuro ou energia escura... não seio o que é só sei que está lá e o nome provém da aparência que imaginamos através de olhar e achar mais fácil e",
      "position": 67006,
      "chapter": 5,
      "page": 32,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 22.85347091932458,
      "complexity_metrics": {
        "word_count": 164,
        "sentence_count": 13,
        "paragraph_count": 11,
        "avg_sentence_length": 12.615384615384615,
        "avg_word_length": 5.024390243902439,
        "unique_word_ratio": 0.7012195121951219,
        "avg_paragraph_length": 14.909090909090908,
        "punctuation_density": 0.1524390243902439,
        "line_break_count": 20,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "podemos",
          "ciclos",
          "quisermos",
          "mais",
          "queremos",
          "temos",
          "como",
          "escolhemos",
          "grande",
          "escura",
          "nossas",
          "vidas",
          "quais",
          "viver",
          "pratiquemos",
          "agregar",
          "melhores",
          "momentos",
          "porque",
          "meio"
        ],
        "entities": [
          [
            "Nossas",
            "GPE"
          ],
          [
            "são ciclos",
            "PERSON"
          ],
          [
            "ciclos queremos",
            "PERSON"
          ],
          [
            "Pratiquemos",
            "PERSON"
          ],
          [
            "PhD",
            "WORK_OF_ART"
          ],
          [
            "MIT",
            "ORG"
          ],
          [
            "formas de aprender sobre",
            "ORG"
          ],
          [
            "Temos",
            "PERSON"
          ],
          [
            "ser o que quisermos",
            "ORG"
          ],
          [
            "amar quando sentimos",
            "PERSON"
          ]
        ],
        "readability_score": 92.18499061913695,
        "semantic_density": 0,
        "word_count": 164,
        "unique_words": 115,
        "lexical_diversity": 0.7012195121951219
      },
      "preservation_score": 0.00020586676966521817
    },
    {
      "id": 70,
      "text": "nxergar a luz e imaginar a rotina dos ciclos da energia, são esses movimentos que nós ensinam a viver e estudar entre o caos e a energia.\\n\\nSe não percebemos a raridade de sentir os momentos de energia dentro dessa massa escura que vivemos, nunca iremos perceber o quão raro nós somos. \\n\\nO viver não é fácil e muito menos difícil, até porque, podemos ser odiosos ou bondosos se quisermos e quem coloca esse tipo de qualificação, estereótipo, peso, forma de pensar e agir, somos nós mesmos que não vemos o quanto a vida é bela e feliz. \\n\\nOs momentos mais tristes que podemos viver, são nesses momentos que enxergamos os nossos pequenos valores como grande, não pelo valor da lembrança ou da memória, e sim, por arrependimento ou pelo o orgulho de não apreciar o que era para ter sido exaltado e amado.\\n\\nNossos corpos são tão adaptáveis que ao nascer nossas mães começam a produzir colostro pela necessidade de criarmos imunidade, e isso, provém devido a necessidade de adaptar-se a um novo ambiente.\\n\\n",
      "position": 68006,
      "chapter": 5,
      "page": 33,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 33.900571428571425,
      "complexity_metrics": {
        "word_count": 175,
        "sentence_count": 5,
        "paragraph_count": 5,
        "avg_sentence_length": 35.0,
        "avg_word_length": 4.668571428571428,
        "unique_word_ratio": 0.6971428571428572,
        "avg_paragraph_length": 35.0,
        "punctuation_density": 0.10857142857142857,
        "line_break_count": 10,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "energia",
          "viver",
          "momentos",
          "somos",
          "podemos",
          "nossos",
          "pelo",
          "necessidade",
          "nxergar",
          "imaginar",
          "rotina",
          "ciclos",
          "esses",
          "movimentos",
          "ensinam",
          "estudar",
          "entre",
          "caos",
          "percebemos",
          "raridade"
        ],
        "entities": [
          [
            "nxergar",
            "PERSON"
          ],
          [
            "Se",
            "PERSON"
          ],
          [
            "massa escura que vivemos",
            "ORG"
          ],
          [
            "nunca iremos perceber o quão",
            "ORG"
          ],
          [
            "muito menos difícil",
            "PERSON"
          ],
          [
            "quem coloca esse tipo de qualificação",
            "ORG"
          ],
          [
            "forma de pensar",
            "PERSON"
          ],
          [
            "somos nós mesmos que",
            "ORG"
          ],
          [
            "não vemos",
            "PERSON"
          ],
          [
            "não pelo valor da lembrança",
            "PERSON"
          ]
        ],
        "readability_score": 81.09942857142858,
        "semantic_density": 0,
        "word_count": 175,
        "unique_words": 122,
        "lexical_diversity": 0.6971428571428572
      },
      "preservation_score": 3.341993014045749e-05
    },
    {
      "id": 71,
      "text": "Consumimos leite materno e após um período, pouco a pouco, implementamos novos alimentos pela necessidade de adaptar-se, e dentro dessa adaptação, temos padrões pela própria forma de vivermos as nossas vidas que já continham uma forma de aprendizado e legado, seja ela corpórea ou mental.\\n\\nQuando começamos a consumir pequenos pedaços de legumes, até porque, bater no liquidificador não estimula a criança mastigar, e o não mastigar, é a falta de estímulo para o crescimento saudável dê seus dentes e também para o sistema digestivo.\\n\\nCriamos sentimentos por: necessidade, hábitos, costumes, felicidade, tristezas, sonhos, objetivos, metas e dentro de todas essas necessidades de vivência nós consumimos algumas coisas que os nossos corpos sentem prazer ao ser ingerido, as vezes por uma necessidade corpórea e outras por uma necessidade mental.\\n\\nAmbas as necessidades são relativas. \\n\\nO entender que uns são felizes estudando, outros correndo, alguns lutando e em sua maioria se matando, é important",
      "position": 69005,
      "chapter": 5,
      "page": 34,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 33.95294117647059,
      "complexity_metrics": {
        "word_count": 153,
        "sentence_count": 5,
        "paragraph_count": 5,
        "avg_sentence_length": 30.6,
        "avg_word_length": 5.509803921568627,
        "unique_word_ratio": 0.7516339869281046,
        "avg_paragraph_length": 30.6,
        "punctuation_density": 0.16339869281045752,
        "line_break_count": 8,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "necessidade",
          "consumimos",
          "pouco",
          "pela",
          "dentro",
          "forma",
          "corpórea",
          "mental",
          "mastigar",
          "necessidades",
          "leite",
          "materno",
          "após",
          "período",
          "implementamos",
          "novos",
          "alimentos",
          "adaptar",
          "dessa",
          "adaptação"
        ],
        "entities": [
          [
            "implementamos novos",
            "PERSON"
          ],
          [
            "padrões pela",
            "PERSON"
          ],
          [
            "própria forma de vivermos",
            "PERSON"
          ],
          [
            "nossas vidas",
            "PERSON"
          ],
          [
            "que já continham uma forma de aprendizado",
            "PERSON"
          ],
          [
            "legado",
            "GPE"
          ],
          [
            "ela corpórea",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "objetivos",
            "DATE"
          ],
          [
            "metas e dentro de todas",
            "ORG"
          ]
        ],
        "readability_score": 83.04705882352941,
        "semantic_density": 0,
        "word_count": 153,
        "unique_words": 115,
        "lexical_diversity": 0.7516339869281046
      },
      "preservation_score": 3.47567273460758e-05
    },
    {
      "id": 72,
      "text": "e entender que aquilo que nós achamos como gostoso, legal, divertido, dolorido, caótico, ruim, bom é tudo relativo para aquele que não soube movimentar-se. Não sabemos se aquela pessoa a qual nós olhamos, imaginamos e por muitas vezes falamos que é um erro fazer, por qual motivo estamos olhando e pensando dessa forma, até porque, nem tudo que é louco, diferente, sujo, barulhento e incômoda é ruim ou bom, e sim, ao gosto de quem está vivendo e sentindo.\\n\\nQuais são os erros que cometemos? \\n\\nEu errei e erro em beber, fumar, crer, viver?\\n\\nAté que ponto tenho que medir o ser feliz, estar sozinho ou triste?\\n\\nViver não tem uma regra e sim uma coerência, assim, temos que interpretar e compreender um contexto de vida.\\n\\nSomos controlados pela nossa forma de pensar ou somos controlados pelo sistema que nos direciona? \\n\\nQual é a diferença entre religião e ditadura?\\n\\nDurante toda a nossa história sempre foi falado que Deus é perfeito. Quem erra somos nós. Olhamos para os dias atuais, nós conseguiríamos viver como a bíblia diz?\\n\\n",
      "position": 70005,
      "chapter": 5,
      "page": 35,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 26.475963020030818,
      "complexity_metrics": {
        "word_count": 177,
        "sentence_count": 11,
        "paragraph_count": 8,
        "avg_sentence_length": 16.09090909090909,
        "avg_word_length": 4.768361581920904,
        "unique_word_ratio": 0.7401129943502824,
        "avg_paragraph_length": 22.125,
        "punctuation_density": 0.1864406779661017,
        "line_break_count": 16,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "qual",
          "viver",
          "somos",
          "como",
          "ruim",
          "tudo",
          "olhamos",
          "erro",
          "forma",
          "quem",
          "controlados",
          "nossa",
          "entender",
          "aquilo",
          "achamos",
          "gostoso",
          "legal",
          "divertido",
          "dolorido",
          "caótico"
        ],
        "entities": [
          [
            "que",
            "CARDINAL"
          ],
          [
            "nós achamos",
            "ORG"
          ],
          [
            "divertido",
            "GPE"
          ],
          [
            "aquela pessoa",
            "ORG"
          ],
          [
            "nós olhamos",
            "ORG"
          ],
          [
            "imaginamos e",
            "PERSON"
          ],
          [
            "olhando e pensando dessa forma",
            "ORG"
          ],
          [
            "nem tudo",
            "PERSON"
          ],
          [
            "Quais",
            "GPE"
          ],
          [
            "erros que cometemos",
            "ORG"
          ]
        ],
        "readability_score": 90.52403697996918,
        "semantic_density": 0,
        "word_count": 177,
        "unique_words": 131,
        "lexical_diversity": 0.7401129943502824
      },
      "preservation_score": 0.000145443535971271
    },
    {
      "id": 73,
      "text": "Conseguiríamos viver como alcorão diz? \\n\\nConseguiríamos viver em um regime extremista? \\n\\nTodas as religiões causaram uma quantidade de morte perante a própria crença, qual foi a que mais causou morte?\\n\\nLogo a religião que mais causou caos e morte é a que têm mais poder.\\n\\nDeus está sempre certo, lembrando que: esse mesmo certo é relativo para aqueles que são beneficiados, até porque, somos o que pensamos e se pensamos é o certo ou foi Deus que nós direcionou a matar judeus, apoiar Roma, criar as cruzadas, criar o racismo, transformar a Inglaterra, Espanha, frança, Portugal e todos os países em uma maior potência ou é a forma certa de viver sendo branco de cabelos longos e olhos azuis?\\n\\nA Marcelo eu não creio em imagens, porém a sua religião veio derivada da religião citada acima, logo não sabemos o que realmente Deus, está querendo falar. \\n\\n“Aquele que não aceita Deus, está contra todos aqueles que sofrem e sofreram por colocar Deus acima de tudo.”\\n\\n",
      "position": 71036,
      "chapter": 5,
      "page": 36,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 26.807727272727274,
      "complexity_metrics": {
        "word_count": 165,
        "sentence_count": 8,
        "paragraph_count": 7,
        "avg_sentence_length": 20.625,
        "avg_word_length": 4.775757575757575,
        "unique_word_ratio": 0.6666666666666666,
        "avg_paragraph_length": 23.571428571428573,
        "punctuation_density": 0.1393939393939394,
        "line_break_count": 14,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "deus",
          "viver",
          "morte",
          "mais",
          "religião",
          "está",
          "certo",
          "conseguiríamos",
          "causou",
          "logo",
          "aqueles",
          "pensamos",
          "criar",
          "todos",
          "acima",
          "como",
          "alcorão",
          "regime",
          "extremista",
          "todas"
        ],
        "entities": [
          [
            "Conseguiríamos",
            "PERSON"
          ],
          [
            "Conseguiríamos",
            "PERSON"
          ],
          [
            "Todas",
            "PERSON"
          ],
          [
            "se pensamos",
            "PERSON"
          ],
          [
            "matar judeus",
            "PERSON"
          ],
          [
            "apoiar Roma",
            "PERSON"
          ],
          [
            "transformar a Inglaterra,",
            "ORG"
          ],
          [
            "Espanha",
            "GPE"
          ],
          [
            "frança",
            "GPE"
          ],
          [
            "Portugal",
            "GPE"
          ]
        ],
        "readability_score": 88.25477272727272,
        "semantic_density": 0,
        "word_count": 165,
        "unique_words": 110,
        "lexical_diversity": 0.6666666666666666
      },
      "preservation_score": 8.187882884412088e-05
    },
    {
      "id": 74,
      "text": "Eu me sinto em um regime nazista com todos em minha volta apoiando e idolatrando um Deus que se perdeu na história, não por culpa dele, e sim, por culpa daqueles que interpretam apenas a sua própria pátria.\\n\\n“Só sabemos que estamos vivos, provinda de entendermos que os nossos movimentos podem nos ocasionar a nossa própria morte.”\\n\\nSó aprendemos quando sabemos ensinar. \\n\\nAnalogia – todos nós sabemos para qual motivo precisamos de nossas mãos, sabemos usá-la para apanhar as coisas, para termos prazeres, para sentir, para nós auxiliar e qualquer função que precisamos usar para aquilo que necessitamos fazer ou não como benefícios ou malefícios. \\n\\nNós sabemos usar a mão, mas sabemos qual é o processo em nossos corpos para usarmos?\\n\\nNós sabemos tudo e não sabemos nada, até porque, aquele que precisa ser um médico para cuidar de nossas mãos, irá se aprofundar como ela funciona e por muitas vezes ocasiona falta de tempo em saber usar melhor as próprias, onde outros que nunca estudaram sobre como as mãos funciona, sabem usar bem melhor.\\n\\n",
      "position": 71999,
      "chapter": 5,
      "page": 37,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 33.14438095238095,
      "complexity_metrics": {
        "word_count": 175,
        "sentence_count": 6,
        "paragraph_count": 6,
        "avg_sentence_length": 29.166666666666668,
        "avg_word_length": 4.925714285714286,
        "unique_word_ratio": 0.6685714285714286,
        "avg_paragraph_length": 29.166666666666668,
        "punctuation_density": 0.11428571428571428,
        "line_break_count": 12,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "sabemos",
          "usar",
          "mãos",
          "como",
          "todos",
          "culpa",
          "própria",
          "nossos",
          "qual",
          "precisamos",
          "nossas",
          "funciona",
          "melhor",
          "sinto",
          "regime",
          "nazista",
          "minha",
          "volta",
          "apoiando",
          "idolatrando"
        ],
        "entities": [
          [
            "nazista",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "Deus que",
            "DATE"
          ],
          [
            "interpretam",
            "ORG"
          ],
          [
            "provinda de entendermos",
            "ORG"
          ],
          [
            "aprendemos quando sabemos",
            "PERSON"
          ],
          [
            "ensinar",
            "GPE"
          ],
          [
            "Analogia",
            "GPE"
          ],
          [
            "nós sabemos",
            "ORG"
          ],
          [
            "motivo precisamos de nossas mãos",
            "PERSON"
          ]
        ],
        "readability_score": 83.93895238095237,
        "semantic_density": 0,
        "word_count": 175,
        "unique_words": 117,
        "lexical_diversity": 0.6685714285714286
      },
      "preservation_score": 5.5343404312597604e-05
    },
    {
      "id": 75,
      "text": "Nossas vidas são semelhantes as nossas mãos e se não percebemos o sentir os nossos corpos e a nossa mente, como iremos entender a vida?\\n\\nPara entender os movimentos diante da minha própria vida preciso entender como usar a minha vida, e o estudar a mesma, será necessário eu sentir e saber os benefícios e os malefícios dos meus próprios movimentos.\\n\\nNão precisamos saber a função da vida, precisamos sentir, interpretar e nos movimentar da forma que merecemos de acordo com os nossos próprios movimentos (semeadura).\\n\\nO que é democracia?\\n\\nGoverno em que o povo exerce a soberania. Sistema político em que os cidadãos elegem os seus dirigentes por meio de eleições periódicas.\\n\\nAo meu ver a democracia nunca existiu. \\n\\nComo iremos fazer manifestação a favor da democracia se a minha forma de ver democracia é diferente da sua?\\n\\nO que sabemos sobre o termo maquiavélico? \\n\\nPor que esse termo foi criado através do livro? \\n\\n",
      "position": 73044,
      "chapter": 5,
      "page": 38,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 26.211290322580645,
      "complexity_metrics": {
        "word_count": 155,
        "sentence_count": 10,
        "paragraph_count": 9,
        "avg_sentence_length": 15.5,
        "avg_word_length": 4.870967741935484,
        "unique_word_ratio": 0.6451612903225806,
        "avg_paragraph_length": 17.22222222222222,
        "punctuation_density": 0.0967741935483871,
        "line_break_count": 18,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "vida",
          "democracia",
          "sentir",
          "como",
          "entender",
          "movimentos",
          "minha",
          "nossas",
          "nossos",
          "iremos",
          "saber",
          "próprios",
          "precisamos",
          "forma",
          "termo",
          "vidas",
          "semelhantes",
          "mãos",
          "percebemos",
          "corpos"
        ],
        "entities": [
          [
            "Nossas",
            "GPE"
          ],
          [
            "nossas mãos",
            "PERSON"
          ],
          [
            "não percebemos o",
            "ORG"
          ],
          [
            "necessário eu",
            "PERSON"
          ],
          [
            "Governo",
            "PERSON"
          ],
          [
            "diferente da sua",
            "PERSON"
          ]
        ],
        "readability_score": 90.78870967741935,
        "semantic_density": 0,
        "word_count": 155,
        "unique_words": 100,
        "lexical_diversity": 0.6451612903225806
      },
      "preservation_score": 9.203848760681994e-05
    },
    {
      "id": 76,
      "text": "Maquiavel (político) foi expulso de Florença e a maior motivação que serviu de inspiração para escrever um livro (O Presidente), foi na fome em que ele se encontrava a 15 anos e foi através dessa fome o despertar das epifanias pelo sentimento, e isso, o fez enxergar o quanto ele queria voltar para a vida anterior, conseguindo interpretar o quanto nós humanos somos miseráveis perante ao nosso próprio viver e foi através desse livro que o termo “democracia” começou a virar realidade.\\n\\nComo foi visto a democracia através do Maquiavel?\\n\\nComo um príncipe (monarquia) deveria doutrinar, direcionar, restringir, manipular e todas aquelas coisas que a “democracia luta pela igualdade de todos”.\\n\\nQuando sentimos fome qual é a quantidade que comemos?\\n\\nPor qual motivo comemos, pela fome ou pela necessidade?\\n\\nPor quais motivos fazemos sexo, será por prazer ou devido ao nosso corpo sentir vontade?\\n\\nDurante anos de minha vida, não percebia o quanto era manipulado pelo desejo sexual.\\n\\n",
      "position": 73966,
      "chapter": 5,
      "page": 39,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 27.836980108499098,
      "complexity_metrics": {
        "word_count": 158,
        "sentence_count": 7,
        "paragraph_count": 7,
        "avg_sentence_length": 22.571428571428573,
        "avg_word_length": 5.170886075949367,
        "unique_word_ratio": 0.7025316455696202,
        "avg_paragraph_length": 22.571428571428573,
        "punctuation_density": 0.10759493670886076,
        "line_break_count": 14,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "fome",
          "através",
          "quanto",
          "democracia",
          "pela",
          "maquiavel",
          "livro",
          "anos",
          "pelo",
          "vida",
          "nosso",
          "como",
          "qual",
          "comemos",
          "político",
          "expulso",
          "florença",
          "maior",
          "motivação",
          "serviu"
        ],
        "entities": [
          [
            "de Florença",
            "PERSON"
          ],
          [
            "15",
            "CARDINAL"
          ],
          [
            "das epifanias pelo sentimento",
            "PRODUCT"
          ],
          [
            "fez enxergar o",
            "ORG"
          ],
          [
            "quanto ele queria voltar",
            "PERSON"
          ],
          [
            "conseguindo interpretar o quanto",
            "ORG"
          ],
          [
            "humanos somos",
            "PERSON"
          ],
          [
            "miseráveis",
            "DATE"
          ],
          [
            "igualdade de todos",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ]
        ],
        "readability_score": 87.16301989150091,
        "semantic_density": 0,
        "word_count": 158,
        "unique_words": 111,
        "lexical_diversity": 0.7025316455696202
      },
      "preservation_score": 8.842913515165055e-05
    },
    {
      "id": 77,
      "text": "Fiquei em depressão por não controlar os meus impulsos corpóreo e mental, e isso, provém do meu corpo mandar e a minha mente não saber controlar os desejos sexuais e alimentares.\\n\\nVejo que todos nós sabemos pouco sobre os nossos sentimentos (sexo, alimentos e adrenalina = prazer corpóreo junto ao mental), esses sentimentos são os mesmos que nos trazem benefícios e malefícios diante da nossa própria interpretação e inspirações.\\n\\nAté que ponto temos que nos permanecer em um relacionamento onde o sexo, a convivência, estímulo e todas aquelas coisas que imaginamos ter como necessário em um relacionamento?\\n\\nTemos como consertar as guerras, brigas, discussões e as cicatrizes que ficaram de um relacionamento?\\n\\nDentro desse relacionamento, qual é a quantidade de momentos prazerosos, familiares que obtivemos de amor ou ódio e qual é o peso desse mesmo diante do meu ser feliz?\\n\\nSe eu não posso ter e ser bagunçado na minha casa, onde eu poderia?\\n\\n",
      "position": 74948,
      "chapter": 5,
      "page": 40,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 29.443763440860216,
      "complexity_metrics": {
        "word_count": 155,
        "sentence_count": 6,
        "paragraph_count": 6,
        "avg_sentence_length": 25.833333333333332,
        "avg_word_length": 5.090322580645161,
        "unique_word_ratio": 0.6903225806451613,
        "avg_paragraph_length": 25.833333333333332,
        "punctuation_density": 0.10967741935483871,
        "line_break_count": 12,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "relacionamento",
          "controlar",
          "corpóreo",
          "mental",
          "minha",
          "sentimentos",
          "sexo",
          "diante",
          "temos",
          "onde",
          "como",
          "desse",
          "qual",
          "fiquei",
          "depressão",
          "meus",
          "impulsos",
          "isso",
          "provém",
          "corpo"
        ],
        "entities": [
          [
            "Fiquei em depressão",
            "ORG"
          ],
          [
            "desejos sexuais",
            "ORG"
          ],
          [
            "Vejo",
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
            "pouco sobre",
            "PERSON"
          ],
          [
            "adrenalina",
            "GPE"
          ],
          [
            "mesmos",
            "PERSON"
          ],
          [
            "diante da nossa própria",
            "PERSON"
          ],
          [
            "Temos",
            "PERSON"
          ]
        ],
        "readability_score": 85.55623655913979,
        "semantic_density": 0,
        "word_count": 155,
        "unique_words": 107,
        "lexical_diversity": 0.6903225806451613
      },
      "preservation_score": 4.571846443214584e-05
    },
    {
      "id": 78,
      "text": "Eu amo a minha bagunça organizada!!\\n\\n Sabe aquela sujeira que está ali parada no cantinho dela, ela têm história e marcas de guerra... Kkkkkk\\n\\nÀs vezes é muito bom arrumar a casa e tentar deixar ela com cheiro de shopping (Eu tenho muita inveja), com tanto brilho que parece aqueles carecas cabeludos mas a parte que importa é o brilho da careca, brilha tanto que não consigo parar de olhar... Kkkkkk\\n\\nE o ventilador, puta que pariu, para conseguir limpar temos que rezar 10 pai nossos e contar o terço 3 vezes...\\n\\nTemos aquelas coisas que nunca usamos e quando queremos usar nunca sabemos, até porque, geralmente essa coisa é algo que não fica combinando e muito menos tem uma boa aparência para ficar ali a amostra, pensa comigo: se sempre perco por guardar em lugar diferente, por que não deixamos onde sempre pensamos que perdemos? \\n\\nPor quais motivos existe a necessidade de existir a bolsa de valores?\\n\\n",
      "position": 75898,
      "chapter": 5,
      "page": 41,
      "segment_type": "preserved_segment",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 29.577426160337552,
      "complexity_metrics": {
        "word_count": 158,
        "sentence_count": 6,
        "paragraph_count": 6,
        "avg_sentence_length": 26.333333333333332,
        "avg_word_length": 4.7025316455696204,
        "unique_word_ratio": 0.7531645569620253,
        "avg_paragraph_length": 26.333333333333332,
        "punctuation_density": 0.14556962025316456,
        "line_break_count": 12,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "kkkkkk",
          "vezes",
          "muito",
          "tanto",
          "brilho",
          "temos",
          "nunca",
          "sempre",
          "minha",
          "bagunça",
          "organizada",
          "sabe",
          "aquela",
          "sujeira",
          "está",
          "parada",
          "cantinho",
          "dela",
          "história",
          "marcas"
        ],
        "entities": [
          [
            "Eu",
            "ORG"
          ],
          [
            "aquela sujeira",
            "PERSON"
          ],
          [
            "ela têm história",
            "PERSON"
          ],
          [
            "marcas de guerra",
            "FAC"
          ],
          [
            "deixar ela",
            "PERSON"
          ],
          [
            "cheiro de shopping",
            "PERSON"
          ],
          [
            "Eu",
            "PERSON"
          ],
          [
            "tanto brilho",
            "ORG"
          ],
          [
            "brilho da careca",
            "ORG"
          ],
          [
            "tanto",
            "GPE"
          ]
        ],
        "readability_score": 85.42257383966245,
        "semantic_density": 0,
        "word_count": 158,
        "unique_words": 119,
        "lexical_diversity": 0.7531645569620253
      },
      "preservation_score": 6.015587425282348e-05
    },
    {
      "id": 79,
      "text": "Exemplo: nós plantamos batata e essa batata aqui no Brasil onde eu plantei e colhi, custa R$ 1 real hoje, essa mesma batata, quanto custa para eu vender para outros países e qual é o custo operacional?\\n\\nVendi todas as batatas e comecei a plantar as minhas batatas novamente, qual é o custo dessa vez para eu conseguir plantar as batatas e qual é o custo operacional?\\n\\nBolsa de valores tem a função de manter o equilíbrio entre os mercados Financeiros do mundo em não haver discrepância entre as safras, produções, valores das moedas, risco país, investimentos e tudo que possa vir ser negociado entre nações e em grande escala no próprio país.\\n\\nDevido a Eurásia não conseguir ter estrutura territorial para produzir aquilo que consomem, e isso, provém do próprio excesso de consumo ao decorrer dos anos deixando o solo todo infértil, além disso, a mão de obra para produtos primários nos países da Eurásia, não era uma profissão a qual desejamos aos nossos filhos, até porque, os melhores trabalhos s",
      "position": 76807,
      "chapter": 5,
      "page": 42,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 38.4406976744186,
      "complexity_metrics": {
        "word_count": 172,
        "sentence_count": 4,
        "paragraph_count": 4,
        "avg_sentence_length": 43.0,
        "avg_word_length": 4.8023255813953485,
        "unique_word_ratio": 0.686046511627907,
        "avg_paragraph_length": 43.0,
        "punctuation_density": 0.11046511627906977,
        "line_break_count": 6,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "qual",
          "batata",
          "custo",
          "batatas",
          "entre",
          "essa",
          "custa",
          "países",
          "operacional",
          "plantar",
          "conseguir",
          "valores",
          "país",
          "próprio",
          "eurásia",
          "exemplo",
          "plantamos",
          "aqui",
          "brasil",
          "onde"
        ],
        "entities": [
          [
            "nós plantamos batata",
            "ORG"
          ],
          [
            "essa batata",
            "FAC"
          ],
          [
            "Brasil",
            "PERSON"
          ],
          [
            "custa",
            "GPE"
          ],
          [
            "1",
            "CARDINAL"
          ],
          [
            "essa mesma batata",
            "ORG"
          ],
          [
            "quanto custa",
            "PERSON"
          ],
          [
            "para eu vender",
            "PERSON"
          ],
          [
            "para outros",
            "PERSON"
          ],
          [
            "Vendi",
            "PRODUCT"
          ]
        ],
        "readability_score": 77.0593023255814,
        "semantic_density": 0,
        "word_count": 172,
        "unique_words": 118,
        "lexical_diversity": 0.686046511627907
      },
      "preservation_score": 1.5239488144048618e-05
    },
    {
      "id": 80,
      "text": "ão aqueles que não precisamos ter muito esforço e sim um emprego confortável, através desse processo de adaptação em um viver confortável, quantos anos atrás a Eurásia e outros países desenvolvidos deixaram de produzir e só começaram a viver através de empregos? \\n\\nEm qual parte do trajeto o Brasil está?\\n\\nNós vemos os países de primeiro mundo imprimindo dinheiro para conseguir ter poder de compra e viver nos costumes, esses, são acostumados a viver com uma qualidade de vida e alta consumação, comparando com países de terceiro mundo, sabendo que: a maioria dos produtos que necessitamos para sobrevivermos, esses são aqueles produzido por quem têm uma infraestrutura territorial e mão de obra proporcional a oferta e demanda.\\n\\nTemos americanos e europeus que não querem trabalhar por viverem melhor recebendo subsídio do governo, e isso ocorre, pela preguiça de não serem acostumado a ter esforço corpóreo. \\n\\n",
      "position": 77807,
      "chapter": 5,
      "page": 43,
      "segment_type": "preserved_segment",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 38.70155172413793,
      "complexity_metrics": {
        "word_count": 145,
        "sentence_count": 4,
        "paragraph_count": 4,
        "avg_sentence_length": 36.25,
        "avg_word_length": 5.255172413793104,
        "unique_word_ratio": 0.7034482758620689,
        "avg_paragraph_length": 36.25,
        "punctuation_density": 0.09655172413793103,
        "line_break_count": 8,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "viver",
          "países",
          "aqueles",
          "esforço",
          "confortável",
          "através",
          "mundo",
          "esses",
          "precisamos",
          "muito",
          "emprego",
          "desse",
          "processo",
          "adaptação",
          "quantos",
          "anos",
          "atrás",
          "eurásia",
          "outros",
          "desenvolvidos"
        ],
        "entities": [
          [
            "muito esforço",
            "PERSON"
          ],
          [
            "Eurásia",
            "GPE"
          ],
          [
            "países de primeiro mundo imprimindo dinheiro",
            "ORG"
          ],
          [
            "para conseguir",
            "PERSON"
          ],
          [
            "necessitamos",
            "ORG"
          ],
          [
            "para sobrevivermos",
            "PERSON"
          ],
          [
            "Temos",
            "PERSON"
          ],
          [
            "viverem melhor recebendo",
            "FAC"
          ],
          [
            "pela preguiça de não serem",
            "PERSON"
          ]
        ],
        "readability_score": 80.29844827586207,
        "semantic_density": 0,
        "word_count": 145,
        "unique_words": 102,
        "lexical_diversity": 0.7034482758620689
      },
      "preservation_score": 1.4972128702924959e-05
    },
    {
      "id": 81,
      "text": "Temos EUA e a Europa com muitas oportunidades para trabalhar sem ter pessoas querendo trabalhar.\\n\\nTemos cidades nos EUA autorizando a ter roubos de até 900 dólares por serem visto como miseráveis e o policiamento nesses lugares onde a miséria está começando a aparecer, logo não consegue conter o avanço devido à falta de estrutura, e a solução para os moradores desses lugares? ter a própria arma.\\n\\nAté que ponto nós aguentaremos viver e sobreviver com o que a Terra poderá dar sem repor?\\n\\nNão podemos mais chamar uma mulher de gostosa... eu pego... você é linda... eu como aquela mulher... Não podemos mais chamar um negro de negro... crioulo...macaco... Gorila.... mais preto... Não podemos mais chamar o homossexual de viado... gay... Viadinho... Traveco... Ele têm o pênis maior que o meu e dá a Bunda.... Não podemos falar nada nem para amigos e se continuarmos assim, iremos perder a origem do amor.\\n\\n",
      "position": 78720,
      "chapter": 5,
      "page": 44,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 22.52518059855521,
      "complexity_metrics": {
        "word_count": 153,
        "sentence_count": 19,
        "paragraph_count": 4,
        "avg_sentence_length": 8.052631578947368,
        "avg_word_length": 4.908496732026144,
        "unique_word_ratio": 0.7058823529411765,
        "avg_paragraph_length": 38.25,
        "punctuation_density": 0.33986928104575165,
        "line_break_count": 8,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "podemos",
          "mais",
          "chamar",
          "temos",
          "trabalhar",
          "como",
          "lugares",
          "mulher",
          "negro",
          "europa",
          "muitas",
          "oportunidades",
          "pessoas",
          "querendo",
          "cidades",
          "autorizando",
          "roubos",
          "dólares",
          "serem",
          "visto"
        ],
        "entities": [
          [
            "Temos EUA",
            "ORG"
          ],
          [
            "Europa",
            "LOC"
          ],
          [
            "para trabalhar sem",
            "PERSON"
          ],
          [
            "Temos",
            "PERSON"
          ],
          [
            "EUA",
            "ORG"
          ],
          [
            "falta de estrutura",
            "ORG"
          ],
          [
            "Terra",
            "ORG"
          ],
          [
            "mais chamar uma mulher de gostosa",
            "PERSON"
          ],
          [
            "eu pego",
            "PERSON"
          ],
          [
            "linda",
            "PERSON"
          ]
        ],
        "readability_score": 94.50113519091848,
        "semantic_density": 0,
        "word_count": 153,
        "unique_words": 108,
        "lexical_diversity": 0.7058823529411765
      },
      "preservation_score": 5.561076375372128e-05
    },
    {
      "id": 82,
      "text": "Não podemos ter forma de pensar com vício de linguagem e falarmos de uma forma a qual somos habituados?\\n\\nUma coisa é falar de uma forma avulsa e outra coisa é falarmos de uma forma de brincadeira, piada, tesão e até podendo ser uma conquista para uma vida.\\n\\nSe falamos é ofensivo para quem escuta, até que ponto?\\n\\nQual é o preconceito que mais sofre com o preconceito?\\n\\nNão pense que a sua dor ou a minha dor perante a um sofrimento, o preconceito se torna mais brando, todos os dias da minha vida eu entro em lugares que sou analisado da unha do pé até o fio de cabelo, e quando, reparo o meu entorno percebo que poucos são semelhantes a mim e a maior quantidade estão trabalhando no estoque, faxina, pedindo dinheiro, cortando carne. Não pense que o nosso sofrer preconceito é maior do que àqueles que também sofrem (todos sofremos), tudo na vida é relativo, interpretativo e não pense que somos feitos de telhado de vidro, até porque, esses que sentem traumas com tudo no mundo realmente não sabem quanto o mundo pode ser dolorido e engraçado.\\n\\n",
      "position": 79628,
      "chapter": 5,
      "page": 45,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 40.18017543859649,
      "complexity_metrics": {
        "word_count": 190,
        "sentence_count": 6,
        "paragraph_count": 5,
        "avg_sentence_length": 31.666666666666668,
        "avg_word_length": 4.489473684210527,
        "unique_word_ratio": 0.6157894736842106,
        "avg_paragraph_length": 38.0,
        "punctuation_density": 0.10526315789473684,
        "line_break_count": 10,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "forma",
          "preconceito",
          "vida",
          "pense",
          "falarmos",
          "qual",
          "somos",
          "coisa",
          "mais",
          "minha",
          "todos",
          "maior",
          "tudo",
          "mundo",
          "podemos",
          "pensar",
          "vício",
          "linguagem",
          "habituados",
          "falar"
        ],
        "entities": [
          [
            "vício de linguagem",
            "PERSON"
          ],
          [
            "outra",
            "NORP"
          ],
          [
            "falarmos de uma forma de brincadeira",
            "ORG"
          ],
          [
            "piada",
            "GPE"
          ],
          [
            "tesão e até podendo",
            "ORG"
          ],
          [
            "Se",
            "PERSON"
          ],
          [
            "para quem escuta",
            "PERSON"
          ],
          [
            "preconceito",
            "PERSON"
          ],
          [
            "se torna mais brando",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ]
        ],
        "readability_score": 82.81982456140351,
        "semantic_density": 0,
        "word_count": 190,
        "unique_words": 117,
        "lexical_diversity": 0.6157894736842106
      },
      "preservation_score": 3.676192315450324e-05
    },
    {
      "id": 83,
      "text": "“Luto contra todos os preconceitos, porém luto também contra todos aqueles que exageram no seu próprio preconceito.”\\n\\nEternidade é a grande busca dos humanos!!!\\n\\nPor qual motivo precisamos de Deuses?\\n\\nPor qual motivo buscamos respostas?\\n\\nPor qual motivo criamos tecnologias?\\n\\nÚnica certeza que temos sobre o universo, gerado através de uma grande liberação de energia (valor quântico).\\n\\nAtravés desse questionamento sem resposta e com muitas respostas extremistas, queremos saber quem originou?\\n\\nJá se perguntou se essa origem possa ter sido um de nós?\\n\\nEsse mesmo que é semelhante a nós é eterno? \\n\\nNós somos eternos? \\n\\nQual é a procura que nós humanos queremos achar? Todos nós temos compromissos para com o planeta Terra, pois dela nós viemos e para ela nós voltaremos.\\n\\nTemos que ter compromissos e responsabilidade de sermos responsáveis pelas nossas falhas gananciosas e miseráveis, todos viemos de falhas passadas e se viemos de falhas passadas, por quais motivos mantemos as mesmas falhas?\\n\\n",
      "position": 80676,
      "chapter": 5,
      "page": 46,
      "segment_type": "preserved_segment",
      "themes": {
        "ciencia": 56.52173913043479,
        "tecnologia": 43.47826086956522
      },
      "difficulty": 26.606451612903225,
      "complexity_metrics": {
        "word_count": 155,
        "sentence_count": 13,
        "paragraph_count": 12,
        "avg_sentence_length": 11.923076923076923,
        "avg_word_length": 5.354838709677419,
        "unique_word_ratio": 0.7032258064516129,
        "avg_paragraph_length": 12.916666666666666,
        "punctuation_density": 0.13548387096774195,
        "line_break_count": 24,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "todos",
          "qual",
          "falhas",
          "motivo",
          "temos",
          "viemos",
          "luto",
          "contra",
          "grande",
          "humanos",
          "respostas",
          "através",
          "queremos",
          "compromissos",
          "passadas",
          "preconceitos",
          "porém",
          "também",
          "aqueles",
          "exageram"
        ],
        "entities": [
          [
            "contra",
            "NORP"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "Única",
            "PERSON"
          ],
          [
            "universo",
            "ORG"
          ],
          [
            "gerado através de uma",
            "PERSON"
          ],
          [
            "queremos",
            "PERSON"
          ],
          [
            "Já se",
            "PERSON"
          ],
          [
            "essa origem possa",
            "ORG"
          ],
          [
            "nós temos compromissos",
            "ORG"
          ]
        ],
        "readability_score": 92.43200992555832,
        "semantic_density": 0,
        "word_count": 155,
        "unique_words": 109,
        "lexical_diversity": 0.7032258064516129
      },
      "preservation_score": 0.0002406234970112939
    },
    {
      "id": 84,
      "text": "Todos nós temos uma origem e dentro dessa origem, qual é a estrutura familiar?\\n\\nUma pessoa viciada em crack têm um filho, vamos dizer que o destino de vida inicial desse filho começa em 1, paralelo a esse nascimento, temos um outro filho que o seu nascimento seja correlacionado a alguém com muito dinheiro ao ponto de nunca pensar na fome como 5, sendo que, durante o trajeto da vida, nós podemos atingir o nível 10 como felicidade suprema a qual não se tem remorsos pelo que viveu e uma plenitude em satisfação com a própria vida sendo a maior escala, lembrando, para termos essa magnitude de vida precisamos ser e ter um trajeto perfeito, logo essa vida não existe, até porque, única perfeição que eu escuto falar é Deus.\\n\\nQuando somos crianças nós só temos o compromisso de sermos crianças, assim, percebemos que a pureza está em não ter Compromisso com a obrigação e sim com a vida. Quando começamos a ter obrigação em ter Compromisso, sejamos comprometidos para sermos de confiança, até porque: essa confiança é aquela que nos motiva a vivermos em um prol da Terra.\\n\\n",
      "position": 81675,
      "chapter": 5,
      "page": 47,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 38.3984126984127,
      "complexity_metrics": {
        "word_count": 189,
        "sentence_count": 4,
        "paragraph_count": 3,
        "avg_sentence_length": 47.25,
        "avg_word_length": 4.661375661375661,
        "unique_word_ratio": 0.656084656084656,
        "avg_paragraph_length": 63.0,
        "punctuation_density": 0.1111111111111111,
        "line_break_count": 6,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "vida",
          "temos",
          "filho",
          "essa",
          "compromisso",
          "origem",
          "qual",
          "nascimento",
          "como",
          "sendo",
          "trajeto",
          "porque",
          "quando",
          "crianças",
          "sermos",
          "obrigação",
          "confiança",
          "todos",
          "dentro",
          "dessa"
        ],
        "entities": [
          [
            "vamos dizer",
            "PERSON"
          ],
          [
            "destino de vida",
            "ORG"
          ],
          [
            "1",
            "CARDINAL"
          ],
          [
            "seja",
            "NORP"
          ],
          [
            "muito dinheiro",
            "PERSON"
          ],
          [
            "ponto de nunca",
            "ORG"
          ],
          [
            "5",
            "CARDINAL"
          ],
          [
            "nós podemos atingir o",
            "ORG"
          ],
          [
            "10",
            "CARDINAL"
          ],
          [
            "remorsos pelo",
            "PERSON"
          ]
        ],
        "readability_score": 74.9765873015873,
        "semantic_density": 0,
        "word_count": 189,
        "unique_words": 124,
        "lexical_diversity": 0.656084656084656
      },
      "preservation_score": 1.263273359309293e-05
    },
    {
      "id": 85,
      "text": "Como gostaria de ter reconhecimento? \\n\\nComo quero ter reconhecimento monetário, trabalho e pessoal? \\n\\nAté qual nível o ter reconhecimento é saudável? \\n\\nEu quero ter reconhecimento ou ser reconhecido?\\n\\nTer reconhecimento é uma conquista o ser reconhecido é visual.\\n\\nA minha forma de ser e ter reconhecimento é aquela necessária para viver o melhor com aqueles que eu amo.\\n\\nTodos os dias temos que agradecer por termos a oportunidade de ter ressaca... por ficarmos com vontade de cagar a noite toda de tanto que comemos no dia anterior... temos que agradecer por termos aquela pessoa que ronca e perturbar nossa mente todos os dias... temos que sermos gratos por brochar as vezes... temos que agradecer aquele dia em que acordamos sem saber como dormimos... Todos os dias temos que agradecer por estarmos vivos e seja qual for a nossa vida, até porque, ela é única e exclusiva. \\n\\nNão deixe abster-se de tudo e de todos e simplesmente viva e seja grato por poder sentir, apreciar, gargalhar, brincar, di",
      "position": 82748,
      "chapter": 5,
      "page": 48,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 23.901520036849377,
      "complexity_metrics": {
        "word_count": 167,
        "sentence_count": 13,
        "paragraph_count": 8,
        "avg_sentence_length": 12.846153846153847,
        "avg_word_length": 4.92814371257485,
        "unique_word_ratio": 0.6047904191616766,
        "avg_paragraph_length": 20.875,
        "punctuation_density": 0.17365269461077845,
        "line_break_count": 14,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "reconhecimento",
          "temos",
          "todos",
          "agradecer",
          "como",
          "dias",
          "quero",
          "qual",
          "reconhecido",
          "aquela",
          "termos",
          "nossa",
          "seja",
          "gostaria",
          "monetário",
          "trabalho",
          "pessoal",
          "nível",
          "saudável",
          "conquista"
        ],
        "entities": [
          [
            "monetário",
            "PERSON"
          ],
          [
            "Eu",
            "PERSON"
          ],
          [
            "aquela necessária",
            "PERSON"
          ],
          [
            "que eu",
            "PERSON"
          ],
          [
            "Todos",
            "GPE"
          ],
          [
            "noite",
            "GPE"
          ],
          [
            "dia",
            "ORG"
          ],
          [
            "por termos aquela pessoa",
            "ORG"
          ],
          [
            "dia",
            "ORG"
          ],
          [
            "ela é única",
            "PERSON"
          ]
        ],
        "readability_score": 92.09847996315062,
        "semantic_density": 0,
        "word_count": 167,
        "unique_words": 101,
        "lexical_diversity": 0.6047904191616766
      },
      "preservation_score": 0.0001122909652719372
    },
    {
      "id": 86,
      "text": "vertir, beber, comer, cair, levantar, amar, beijar, abraçar, experimentar e aprender que a vida e o mundo são tantas opções que temos, que o desistir de viver por enfrentar dificuldades e martirizar-se, nunca entenderemos a graça de termos as nossas vidas e descobrir que estamos vivos ao acordar.\\n\\nO ser feliz simplesmente por estar vivendo qualquer coisa que os meus movimentos me levam a viver: é ser grato por aquilo que os meus pais se sacrificaram a vida toda para eu ter em uma vida, a qual, eles não conseguiram ou não puderam ter!!!\\n\\nTempos difíceis fazem humanos fortes (necessidade de adaptação).\\n\\nTempos fáceis fazem humanos fracos (proporcional a necessidade de adaptação).\\n\\nComo medimos o que é tempo difícil? \\n\\nEstamos vivendo tempos difíceis?\\n\\nAinda existem agressores (senhores) feudais?\\n\\nEm toda nossa história, já obtivemos dificuldades com a obesidade?\\n\\nAinda temos experiências com humanos vivos?\\n\\n",
      "position": 83748,
      "chapter": 5,
      "page": 49,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 25.59375,
      "complexity_metrics": {
        "word_count": 144,
        "sentence_count": 9,
        "paragraph_count": 9,
        "avg_sentence_length": 16.0,
        "avg_word_length": 5.3125,
        "unique_word_ratio": 0.7361111111111112,
        "avg_paragraph_length": 16.0,
        "punctuation_density": 0.1736111111111111,
        "line_break_count": 18,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "vida",
          "tempos",
          "humanos",
          "temos",
          "viver",
          "dificuldades",
          "estamos",
          "vivos",
          "vivendo",
          "meus",
          "toda",
          "difíceis",
          "fazem",
          "necessidade",
          "adaptação",
          "ainda",
          "vertir",
          "beber",
          "comer",
          "cair"
        ],
        "entities": [
          [
            "amar",
            "PERSON"
          ],
          [
            "beijar",
            "ORG"
          ],
          [
            "abraçar",
            "ORG"
          ],
          [
            "desistir de viver",
            "PERSON"
          ],
          [
            "nossas vidas",
            "PERSON"
          ],
          [
            "feliz simplesmente por",
            "PERSON"
          ],
          [
            "estar vivendo qualquer coisa",
            "PERSON"
          ],
          [
            "para eu",
            "PERSON"
          ],
          [
            "Estamos",
            "PERSON"
          ],
          [
            "Ainda",
            "ORG"
          ]
        ],
        "readability_score": 90.40625,
        "semantic_density": 0,
        "word_count": 144,
        "unique_words": 106,
        "lexical_diversity": 0.7361111111111112
      },
      "preservation_score": 0.00017324891784813165
    },
    {
      "id": 87,
      "text": "Ainda temos navios negreiros?\\n\\nQual é a quantidade de guerras que ainda temos para conquistar territórios através do foda-se (tratado de Tordesilhas)?\\n\\nQuantas guerras de extrema religiosidade ainda temos e que contenham um maior apoio?\\n\\nQuais são os maiores filósofos e a quanto tempo atrás surgiram e viveram?\\n\\nQuais são os maiores profetas? \\n\\nQuando os maiores artistas surgiram, em tempos fáceis ou em tempos difíceis? \\n\\nTudo em nossa história é exaltado em meio ao caos e o valor proporcional ao sentimento sofrido pelo caos, seja esse mesmo: sendo sentindo e expressado no espaço e tempo relativo a própria forma de ver e sentir a própria vida.\\n\\nO que é espaço tempo?\\n\\nExemplos:\\n\\nTemos um dia com 24 horas, dormimos 10 horas por dia e durante o dia nossa mente têm “apagões”, delay, tempo para raciocinar e outras dificuldades mentais, qual é a quantidade de aprendizado em 24 horas?\\n\\nTemos um dia com 24 horas, dormimos 6 horas por dia e acordamos dispostos e criativos, sempre com o dia anter",
      "position": 84667,
      "chapter": 5,
      "page": 50,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 24.90562130177515,
      "complexity_metrics": {
        "word_count": 169,
        "sentence_count": 10,
        "paragraph_count": 11,
        "avg_sentence_length": 16.9,
        "avg_word_length": 4.85207100591716,
        "unique_word_ratio": 0.621301775147929,
        "avg_paragraph_length": 15.363636363636363,
        "punctuation_density": 0.11242603550295859,
        "line_break_count": 20,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "temos",
          "horas",
          "tempo",
          "ainda",
          "maiores",
          "qual",
          "quantidade",
          "guerras",
          "quais",
          "surgiram",
          "tempos",
          "nossa",
          "caos",
          "espaço",
          "própria",
          "dormimos",
          "navios",
          "negreiros",
          "conquistar",
          "territórios"
        ],
        "entities": [
          [
            "Ainda",
            "PERSON"
          ],
          [
            "negreiros",
            "PERSON"
          ],
          [
            "ainda temos",
            "PERSON"
          ],
          [
            "para conquistar",
            "PERSON"
          ],
          [
            "de Tordesilhas",
            "PERSON"
          ],
          [
            "Quantas",
            "GPE"
          ],
          [
            "ainda temos e",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "Tudo",
            "PERSON"
          ],
          [
            "nossa história",
            "PERSON"
          ]
        ],
        "readability_score": 90.09437869822486,
        "semantic_density": 0,
        "word_count": 169,
        "unique_words": 105,
        "lexical_diversity": 0.621301775147929
      },
      "preservation_score": 0.00017645723114161557
    },
    {
      "id": 88,
      "text": "ior completo e não com aquela sensação de ausência, com pensamentos agregadores do dia anterior e dê um passado já vivido, qual é o nosso aprendizado diário? \\n\\nAssim é a nossa percepção de sentir o espaço proporcional ao nosso pensar e aproveitar o nosso tempo que temos de vida.\\n\\nTudo na vida é relativo para aquele que já está vivo.\\n\\nSeja feliz!!!\\n\\nAté porque nosso subconsciente é semelhante a nuvem dê um telefone com fotos, músicas, aqueles programas (igual a andar de bicicleta, nunca esquecemos) e todas aquelas coisas que temos como importante.\\n\\nE a nossa consciência é semelhante ao sistema de um telefone (proporcional a um processador), são aqueles programas que usamos com constância, jogos, conversas e todas aquelas coisas que vivemos no nosso espaço tempo.\\n\\nLogo percebemos, que: para aqueles que querem viver de uma forma mentalmente saudável é necessário estar com o nosso entorno em um bem estar financeiro, viajar, namorar, transar, beber, fumar, sair, sei lá... Qualquer coisa que faça feliz e se for para um bem maior de benfeitoria, siga os intuitos e viva a vida!\\n\\n",
      "position": 85667,
      "chapter": 5,
      "page": 51,
      "segment_type": "preserved_segment",
      "themes": {
        "filosofia": 53.57142857142857,
        "ciencia": 46.42857142857144
      },
      "difficulty": 29.802555248618784,
      "complexity_metrics": {
        "word_count": 181,
        "sentence_count": 8,
        "paragraph_count": 7,
        "avg_sentence_length": 22.625,
        "avg_word_length": 4.966850828729282,
        "unique_word_ratio": 0.6519337016574586,
        "avg_paragraph_length": 25.857142857142858,
        "punctuation_density": 0.16574585635359115,
        "line_break_count": 14,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "nosso",
          "vida",
          "aqueles",
          "nossa",
          "espaço",
          "proporcional",
          "tempo",
          "temos",
          "feliz",
          "semelhante",
          "telefone",
          "programas",
          "todas",
          "aquelas",
          "coisas",
          "completo",
          "aquela",
          "sensação",
          "ausência",
          "pensamentos"
        ],
        "entities": [
          [
            "aquela sensação de ausência",
            "ORG"
          ],
          [
            "dia",
            "ORG"
          ],
          [
            "já vivido",
            "PERSON"
          ],
          [
            "que temos de vida",
            "PERSON"
          ],
          [
            "Tudo",
            "PERSON"
          ],
          [
            "nunca esquecemos",
            "ORG"
          ],
          [
            "jogos",
            "GPE"
          ],
          [
            "Logo percebemos",
            "PERSON"
          ],
          [
            "para aqueles",
            "PERSON"
          ],
          [
            "de uma forma mentalmente",
            "PERSON"
          ]
        ],
        "readability_score": 87.19744475138121,
        "semantic_density": 0,
        "word_count": 181,
        "unique_words": 118,
        "lexical_diversity": 0.6519337016574586
      },
      "preservation_score": 0.00011135520722800439
    },
    {
      "id": 89,
      "text": "Como conseguir respeitar o limite dos nossos corpos e quantidade de raciocínio, se o mundo nos exige mais do que eles deveriam aguentar?\\n\\nExemplos:\\n\\nQuando bebemos muito, como os nossos corpos ficam? Quando usamos muitos anabolizantes o que ocorre com os nossos corpos?\\n\\nAmbos os casos são semelhantes ao excesso, sendo que: Um para de produzir e o outro não consegue se recuperar e antes de tentar se recuperar com o tempo, injetamos e ingerimos mais pela ausência. Já em outros casos é necessário ter reposição, até porque, o nosso corpo para de produzir devido ao excesso que foi ingerido, assim, o mesmo interpreta não sentir necessidade de fazer essas funções.\\n\\nQuanto mais a gente dorme, mais vontade de continuar dá.\\n\\nQuanto mais a gente procrastina, mais cansado ficamos.\\n\\nQuanto mais exercícios fazemos, mais o nosso corpo necessita.\\n\\nSabe aquela ferida cicatrizada que deixou cicatriz, onde ficou aquela cicatriz, fica mais resistente ou mais Frágil?\\n\\n",
      "position": 86755,
      "chapter": 5,
      "page": 52,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 25.157562724014337,
      "complexity_metrics": {
        "word_count": 155,
        "sentence_count": 9,
        "paragraph_count": 8,
        "avg_sentence_length": 17.22222222222222,
        "avg_word_length": 5.15483870967742,
        "unique_word_ratio": 0.6774193548387096,
        "avg_paragraph_length": 19.375,
        "punctuation_density": 0.15483870967741936,
        "line_break_count": 16,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "nossos",
          "corpos",
          "quanto",
          "como",
          "quando",
          "casos",
          "excesso",
          "produzir",
          "recuperar",
          "nosso",
          "corpo",
          "gente",
          "aquela",
          "cicatriz",
          "conseguir",
          "respeitar",
          "limite",
          "quantidade",
          "raciocínio"
        ],
        "entities": [
          [
            "deveriam aguentar",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "muito",
            "ORG"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "Ambos",
            "PERSON"
          ],
          [
            "outro",
            "ORG"
          ],
          [
            "ingerimos mais",
            "PERSON"
          ],
          [
            "pela ausência",
            "PERSON"
          ],
          [
            "Já em outros casos",
            "PERSON"
          ],
          [
            "necessário",
            "GPE"
          ]
        ],
        "readability_score": 89.84243727598566,
        "semantic_density": 0,
        "word_count": 155,
        "unique_words": 105,
        "lexical_diversity": 0.6774193548387096
      },
      "preservation_score": 0.00010266602539148543
    },
    {
      "id": 90,
      "text": "Nossa vida é a mesma coisa, seja corpóreo ou mental. Todas os nossos movimentos nos causam feridas e algumas não deixam marcas e outras deixam cicatrizes, qual é a fragilidade que temos na vida?\\n\\n“Quando a verdade é pesada e séria: quando enxergamos como pesado um viver sem peso com a verdade.”\\n\\n“Só pagamos por aquilo que temos dívida e se não precisamos pagar por nada, isso é um bom sinal para a vida.”\\n\\n“Nós vivemos ansiosos para chegar em algum lugar ou pensando em algo que perdeu imaginando que possa vir ter chance de viver novamente.” \\n\\nTemos ansiedade mental e ansiedade corpórea, e essa, provém em ter percepção e entender a diferença e a causa uma da outra, para depois tratar.\\n\\nJá percebeu que comemoramos o perder a nossa idade (tempo de vida)?\\n\\nSe o tempo é contínuo e sem volta, por qual motivos ficamos ansiosos?\\n\\nÚnica certeza da vida é que um dia iremos morrer e esse trajeto têm um tempo, qual é o tempo que cada um têm?\\n\\n",
      "position": 87717,
      "chapter": 5,
      "page": 53,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 26.00526315789474,
      "complexity_metrics": {
        "word_count": 171,
        "sentence_count": 9,
        "paragraph_count": 8,
        "avg_sentence_length": 19.0,
        "avg_word_length": 4.461988304093567,
        "unique_word_ratio": 0.6842105263157895,
        "avg_paragraph_length": 21.375,
        "punctuation_density": 0.10526315789473684,
        "line_break_count": 16,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "vida",
          "tempo",
          "qual",
          "temos",
          "nossa",
          "mental",
          "deixam",
          "quando",
          "verdade",
          "viver",
          "ansiosos",
          "ansiedade",
          "mesma",
          "coisa",
          "seja",
          "corpóreo",
          "todas",
          "nossos",
          "movimentos",
          "causam"
        ],
        "entities": [
          [
            "Nossa",
            "PERSON"
          ],
          [
            "Todas",
            "PERSON"
          ],
          [
            "nos causam feridas",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "quando enxergamos",
            "PERSON"
          ],
          [
            "que temos",
            "ORG"
          ],
          [
            "não precisamos pagar por nada",
            "ORG"
          ],
          [
            "algum lugar",
            "PERSON"
          ],
          [
            "pensando",
            "GPE"
          ],
          [
            "Temos",
            "PERSON"
          ]
        ],
        "readability_score": 89.16140350877193,
        "semantic_density": 0,
        "word_count": 171,
        "unique_words": 117,
        "lexical_diversity": 0.6842105263157895
      },
      "preservation_score": 0.00011122152750744256
    },
    {
      "id": 91,
      "text": "Cada segundo que vivemos é um segundo a menos para a morte, independente se iremos morrer com 100 anos ou 1 dia e a ansiedade por muitas vezes provém dê um sentimento passado implementado dentro do meu futuro imaginário. \\n\\nA ansiedade vem derivada em chegar a uma felicidade ou tristeza nunca vivida.\\n\\nA ansiedade é causada devido a não pensar na fome ou pensar na fome.\\n\\nAnsiedade é normal termos, difícil é controlar os nossos sentimentos.\\n\\nPensa: se fico ansioso para um futuro, esse mesmo, independente do que for, será o que for para ser, por quais motivos perdemos tempo no presente que estamos vivendo?\\n\\nO futuro é amanhã, e ele, só vai deixar de ser ansioso quando chegar e para ele chegar conforme a nossa ansiedade, faça o que tenha que fazer no presente para não ter tempo ocioso e procrastinador, até porque, o tempo vai passar.\\n\\n“Deus não joga dados com o universo!” Albert Einstein\\n\\nNo final dê sua vida, Einstein sendo judeu estava em dúvida sobre a existência de Deus, e talvez, prové",
      "position": 88660,
      "chapter": 5,
      "page": 54,
      "segment_type": "preserved_segment",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 27.455113636363635,
      "complexity_metrics": {
        "word_count": 176,
        "sentence_count": 8,
        "paragraph_count": 8,
        "avg_sentence_length": 22.0,
        "avg_word_length": 4.642045454545454,
        "unique_word_ratio": 0.6818181818181818,
        "avg_paragraph_length": 22.0,
        "punctuation_density": 0.125,
        "line_break_count": 14,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "ansiedade",
          "futuro",
          "chegar",
          "tempo",
          "segundo",
          "independente",
          "pensar",
          "fome",
          "ansioso",
          "presente",
          "deus",
          "einstein",
          "cada",
          "vivemos",
          "menos",
          "morte",
          "iremos",
          "morrer",
          "anos",
          "muitas"
        ],
        "entities": [
          [
            "Cada",
            "ORG"
          ],
          [
            "100 anos",
            "QUANTITY"
          ],
          [
            "1",
            "CARDINAL"
          ],
          [
            "causada",
            "NORP"
          ],
          [
            "Ansiedade",
            "PERSON"
          ],
          [
            "Pensa",
            "PERSON"
          ],
          [
            "fico ansioso",
            "ORG"
          ],
          [
            "motivos",
            "PERSON"
          ],
          [
            "que estamos vivendo",
            "PERSON"
          ],
          [
            "faça o que",
            "ORG"
          ]
        ],
        "readability_score": 87.60738636363637,
        "semantic_density": 0,
        "word_count": 176,
        "unique_words": 120,
        "lexical_diversity": 0.6818181818181818
      },
      "preservation_score": 8.983277221754977e-05
    },
    {
      "id": 92,
      "text": "m de entender que o universo e Deus é a mesma coisa com forma de percepção, ângulos e destinos diferentes. Através desse pensamento, ele percebeu o quanto somos miseráveis em querer saber uma resposta que já sabemos, porém:\\n\\n “Precisamos descobrir qual é a origem e por qual motivo precisamos dessa resposta?”\\n\\n“Deus não enviou nenhum profeta, a menos que ele fosse um pastor de ovelhas.” \\n\\n“percebeu que havia diferenças irreconciliáveis entre as religiões judaica e cristã e a sua, especialmente quando a crença em sua missão profética se tornou o critério de um verdadeiro muçulmano”. Profeta Maomé \\n\\nEsse foi um político, militar e um líder religioso.\\n\\nEsse mesmo falou que todos nós somos humanos captadores e denominamos como Deus, Alá, God e muitas outras formas de descrever o destino.\\n\\nDeus é universo e universo é Deus, por quais motivos precisamos entender a origem se ambos são os mesmos?\\n\\n",
      "position": 89660,
      "chapter": 5,
      "page": 55,
      "segment_type": "preserved_segment",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 27.22239382239382,
      "complexity_metrics": {
        "word_count": 148,
        "sentence_count": 7,
        "paragraph_count": 7,
        "avg_sentence_length": 21.142857142857142,
        "avg_word_length": 5.027027027027027,
        "unique_word_ratio": 0.7027027027027027,
        "avg_paragraph_length": 21.142857142857142,
        "punctuation_density": 0.11486486486486487,
        "line_break_count": 14,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "deus",
          "universo",
          "precisamos",
          "entender",
          "percebeu",
          "somos",
          "resposta",
          "qual",
          "origem",
          "profeta",
          "esse",
          "mesma",
          "coisa",
          "forma",
          "percepção",
          "ângulos",
          "destinos",
          "diferentes",
          "através",
          "desse"
        ],
        "entities": [
          [
            "universo e Deus",
            "PERSON"
          ],
          [
            "forma de percepção",
            "ORG"
          ],
          [
            "quanto somos miseráveis",
            "PERSON"
          ],
          [
            "querer",
            "ORG"
          ],
          [
            "que",
            "CARDINAL"
          ],
          [
            "já sabemos",
            "PERSON"
          ],
          [
            "Precisamos",
            "PERSON"
          ],
          [
            "religiões judaica",
            "PERSON"
          ],
          [
            "sua missão",
            "FAC"
          ],
          [
            "Profeta Maomé \\n\\nEsse",
            "PERSON"
          ]
        ],
        "readability_score": 87.92046332046333,
        "semantic_density": 0,
        "word_count": 148,
        "unique_words": 104,
        "lexical_diversity": 0.7027027027027027
      },
      "preservation_score": 7.532852253659121e-05
    },
    {
      "id": 93,
      "text": "Todos nós temos o nosso espaço relativo ao nosso tempo. Como queremos aproveitar o nosso espaço com o tempo que temos?\\n\\nOnde temos segurança, temos desconfiança.\\n\\nOnde temos insegurança, temos Confiança. \\n\\nSão as dificuldades que nós fazem entendermos o valor do amor.\\n\\nOnde temos pessoas que passam maiores dificuldades a confiança é maior, e isso, provém do viver na miséria ser semelhante ou quando percebemos que amor acabou o brigar também, até porque, os nossos momentos mais difíceis servem de aprendizado para entender o valor da gratidão do amor.\\n\\n“Onde temos pessoas achando que vivem melhor o viver semelhante é de causar inveja.”\\n\\nO querer estudar é diferente de ser obrigado a estudar.\\n\\nNinguém gosta de sair para trabalhar naqueles dias sem vontade nenhuma.\\n\\nAmbos os casos causam falta de paciência e procrastinação.\\n\\nNossas vidas depende de como nos movimentamos e interpretamos, até porque, tudo que está sendo agora, foram muitos agora passado para ter cada átomo no universo em sincronicidade para estarmos vivendo esse presente momento.\\n\\n",
      "position": 90562,
      "chapter": 5,
      "page": 56,
      "segment_type": "preserved_segment",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 24.21720195971693,
      "complexity_metrics": {
        "word_count": 167,
        "sentence_count": 11,
        "paragraph_count": 10,
        "avg_sentence_length": 15.181818181818182,
        "avg_word_length": 5.269461077844311,
        "unique_word_ratio": 0.7125748502994012,
        "avg_paragraph_length": 16.7,
        "punctuation_density": 0.11976047904191617,
        "line_break_count": 20,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "temos",
          "onde",
          "nosso",
          "amor",
          "espaço",
          "tempo",
          "como",
          "confiança",
          "dificuldades",
          "valor",
          "pessoas",
          "viver",
          "semelhante",
          "porque",
          "estudar",
          "agora",
          "todos",
          "relativo",
          "queremos",
          "aproveitar"
        ],
        "entities": [
          [
            "nós temos o",
            "ORG"
          ],
          [
            "Como",
            "ORG"
          ],
          [
            "aproveitar o",
            "ORG"
          ],
          [
            "Confiança",
            "GPE"
          ],
          [
            "quando percebemos",
            "PERSON"
          ],
          [
            "amor acabou o brigar também",
            "ORG"
          ],
          [
            "nossos momentos mais difíceis",
            "ORG"
          ],
          [
            "achando que vivem melhor o",
            "ORG"
          ],
          [
            "diferente de ser",
            "PERSON"
          ],
          [
            "Ninguém",
            "ORG"
          ]
        ],
        "readability_score": 90.82825258573762,
        "semantic_density": 0,
        "word_count": 167,
        "unique_words": 119,
        "lexical_diversity": 0.7125748502994012
      },
      "preservation_score": 0.00014704769261801297
    },
    {
      "id": 94,
      "text": "“Nós somos os únicos capazes de entender e tentar adaptar-se ao movimento já vivido.”\\n\\nTodo mundo quer ser feliz e contente.\\n\\nQuais são os cargos que podemos ser felizes e contentes?\\n\\nQuando estamos felizes o que comentam sobre o estar feliz?\\n\\nEm uma empresa que temos um ótimo profissional que vive rindo e fazendo piadas, como essa pessoa é vista? \\n\\nO que achamos de um palhaço ser deputado ou presidente?\\n\\nQuais são os cargos que temos felicidades e alegrias? \\n\\nNós almejamos o que não confiamos.\\n\\nPor qual motivo o ser feliz, engraçado, alegre, riso solto, brincalhão e tudo aquilo que nos dá alívio na vida é de ser ou ter uma vida sem merecimento, credibilidade, incapaz, desconfiança por não ser de confiança apenas por ser feliz?\\n\\nO que irá mudar em nossas vidas:\\n\\nDescobrindo o início de tudo?\\n\\nDeus existiu ou existe?\\n\\nBudismo possa vir ser a religião que melhor possa direcionar?\\n\\nMenosprezar ou diminuir outras pessoas?\\n\\n",
      "position": 91620,
      "chapter": 5,
      "page": 57,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 22.529152376286135,
      "complexity_metrics": {
        "word_count": 157,
        "sentence_count": 13,
        "paragraph_count": 14,
        "avg_sentence_length": 12.076923076923077,
        "avg_word_length": 4.840764331210191,
        "unique_word_ratio": 0.6942675159235668,
        "avg_paragraph_length": 11.214285714285714,
        "punctuation_density": 0.14012738853503184,
        "line_break_count": 28,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "feliz",
          "quais",
          "cargos",
          "felizes",
          "temos",
          "tudo",
          "vida",
          "possa",
          "somos",
          "únicos",
          "capazes",
          "entender",
          "tentar",
          "adaptar",
          "movimento",
          "vivido",
          "todo",
          "mundo",
          "quer",
          "contente"
        ],
        "entities": [
          [
            "únicos capazes de",
            "ORG"
          ],
          [
            "tentar adaptar",
            "PERSON"
          ],
          [
            "já vivido",
            "PERSON"
          ],
          [
            "cargos que podemos ser felizes e contentes",
            "ORG"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "que",
            "CARDINAL"
          ],
          [
            "comentam sobre",
            "ORG"
          ],
          [
            "estar",
            "PRODUCT"
          ],
          [
            "vista",
            "ORG"
          ],
          [
            "ser de confiança",
            "ORG"
          ]
        ],
        "readability_score": 92.5093091621754,
        "semantic_density": 0,
        "word_count": 157,
        "unique_words": 109,
        "lexical_diversity": 0.6942675159235668
      },
      "preservation_score": 0.0003275153153764835
    },
    {
      "id": 95,
      "text": "Ser melhor ou inferior a outras pessoas?\\n\\nDescobrir toda a verdade do universo?\\n\\nDo que adianta descobrir sobre tudo e não descobrir o que possa nós fazer felizes ou tristes?\\n\\nTodos vivendo o melhor que cada um possa almejar como melhor?\\n\\nTemos dinheiro e não temos humanos que me faça uma pessoa melhor?\\n\\nO que nós queremos é o melhor em um viver para todos?\\n\\nO que queremos?\\n\\nAs crianças que brigam constantemente, são exemplos?\\n\\nEm uma conversa, por quais motivos erramos?\\n\\nPor quais motivos devemos entrar em uma zona de desconforto?\\n\\n“Os que brigam em vão, não são bem visto, porém os que brigam por amor, são bem vistos.”\\n\\nAo entrarmos em uma zona caótica e problemática devido a necessidade de não ser menosprezado ou qualquer coisa que nunca faríamos com outros, lembre-se: O valor da recompensa necessita ser maior para um maior contexto e se por acaso o nosso lutar for a favor de uma minoria, essa luta precisa ser contra a fome, até porque, mesmo sendo pela fome se a luta for extremista, essa mesma luta se perderá no trajeto.\\n\\n",
      "position": 92553,
      "chapter": 5,
      "page": 58,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 24.053551912568306,
      "complexity_metrics": {
        "word_count": 183,
        "sentence_count": 12,
        "paragraph_count": 12,
        "avg_sentence_length": 15.25,
        "avg_word_length": 4.622950819672131,
        "unique_word_ratio": 0.6502732240437158,
        "avg_paragraph_length": 15.25,
        "punctuation_density": 0.12568306010928962,
        "line_break_count": 24,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "melhor",
          "descobrir",
          "brigam",
          "luta",
          "possa",
          "todos",
          "temos",
          "queremos",
          "quais",
          "motivos",
          "zona",
          "maior",
          "essa",
          "fome",
          "inferior",
          "outras",
          "pessoas",
          "toda",
          "verdade",
          "universo"
        ],
        "entities": [
          [
            "Descobrir",
            "ORG"
          ],
          [
            "Todos",
            "GPE"
          ],
          [
            "melhor que",
            "GPE"
          ],
          [
            "Temos",
            "PERSON"
          ],
          [
            "motivos erramos",
            "PERSON"
          ],
          [
            "motivos devemos",
            "PERSON"
          ],
          [
            "zona",
            "CARDINAL"
          ],
          [
            "uma zona caótica e problemática",
            "ORG"
          ],
          [
            "qualquer coisa",
            "PERSON"
          ],
          [
            "essa luta precisa ser contra",
            "PERSON"
          ]
        ],
        "readability_score": 90.98811475409836,
        "semantic_density": 0,
        "word_count": 183,
        "unique_words": 119,
        "lexical_diversity": 0.6502732240437158
      },
      "preservation_score": 0.0002502484368917457
    },
    {
      "id": 96,
      "text": "“O erro não está em discutir, brigar, lutar, odiar e sim na mente ao lutar pelo preconceito sendo preconceituoso, e isso, é o extremismo da própria certeza.”\\n\\nA partir do momento que brigamos pelo preconceito sem ter poder ou dinheiro de nada adianta falarmos, até porque, não temos voz ativa na sociedade, logo vejo que o brigar, de nada adianta se não conseguirmos ser superiores aqueles que têm mais poder, e isso, provém da sorte de ter nascido com o cu na Lua, são essas condições que causam a injúria daqueles que acham que estão lutando, brigando, querendo e achando que está certo pela ignorância de não ver o Ibope desnecessário para aqueles que só querem ser reconhecido e não ter reconhecimento!!!\\n\\n“Quando damos tempo ao tempo, nós começamos a perceber que o tempo só avança e só volta em nossas mentes.”\\n\\nQuando deixamos o tempo seguir e seguimos juntos com o tempo, todos aqueles problemas que nós causam ansiedades, deixam de ser problemas e se transformam em estilo de vida. \\n\\n",
      "position": 93594,
      "chapter": 5,
      "page": 59,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 40.43333333333334,
      "complexity_metrics": {
        "word_count": 171,
        "sentence_count": 4,
        "paragraph_count": 4,
        "avg_sentence_length": 42.75,
        "avg_word_length": 4.777777777777778,
        "unique_word_ratio": 0.6432748538011696,
        "avg_paragraph_length": 42.75,
        "punctuation_density": 0.13450292397660818,
        "line_break_count": 8,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "tempo",
          "aqueles",
          "está",
          "brigar",
          "lutar",
          "pelo",
          "preconceito",
          "isso",
          "poder",
          "nada",
          "adianta",
          "causam",
          "quando",
          "problemas",
          "erro",
          "discutir",
          "odiar",
          "mente",
          "sendo",
          "preconceituoso"
        ],
        "entities": [
          [
            "discutir",
            "NORP"
          ],
          [
            "lutar pelo preconceito",
            "PERSON"
          ],
          [
            "extremismo da própria",
            "ORG"
          ],
          [
            "pelo preconceito",
            "PERSON"
          ],
          [
            "não temos voz ativa",
            "PERSON"
          ],
          [
            "vejo",
            "ORG"
          ],
          [
            "brigar, de nada",
            "ORG"
          ],
          [
            "se não conseguirmos",
            "PERSON"
          ],
          [
            "têm mais",
            "ORG"
          ],
          [
            "que",
            "CARDINAL"
          ]
        ],
        "readability_score": 77.19166666666666,
        "semantic_density": 0,
        "word_count": 171,
        "unique_words": 110,
        "lexical_diversity": 0.6432748538011696
      },
      "preservation_score": 2.8874819641355277e-05
    },
    {
      "id": 97,
      "text": "Aqueles que são mais velhos, não são mais inteligentes que os mais novos e sim mais sábios, até porque, até o ignorante fica sábio quando percebe que o tempo não se luta e sim vive.\\n\\nPorquê nossos corpos precisam de açúcar?\\n\\nQuantos tipos de açúcar nós temos?\\n\\nAçúcar = energia para o corpo.\\n\\nExcesso de energia não gasta o que acontece? Acumula. \\n\\nO problema da nossa alimentação não é o açúcar e sim todos aqueles alimentos com excesso de conservantes (a maioria usa sódio e esse absorve líquido).\\n\\nTemos açúcar bom e ruim.\\n\\nPrecisamos saber o quanto podemos consumir, e isso, depende do nosso metabolismo e o quanto gastamos de energia no dia a dia.\\n\\nSemelhante ao açúcar temos a gordura boa e a gordura ruim.\\n\\nGordura ruim – Óleo, margarina e todas aquelas que passaram por industrialização.\\n\\nGordura boa – banha de porco, manteiga e todas aquelas que não passaram por industrialização. \\n\\nAssim como o açúcar a gordura também gera energia e protege os nossos corpos.\\n\\n",
      "position": 94587,
      "chapter": 5,
      "page": 60,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 22.84403500690926,
      "complexity_metrics": {
        "word_count": 167,
        "sentence_count": 13,
        "paragraph_count": 12,
        "avg_sentence_length": 12.846153846153847,
        "avg_word_length": 4.736526946107785,
        "unique_word_ratio": 0.6287425149700598,
        "avg_paragraph_length": 13.916666666666666,
        "punctuation_density": 0.11976047904191617,
        "line_break_count": 24,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "açúcar",
          "gordura",
          "mais",
          "energia",
          "temos",
          "ruim",
          "aqueles",
          "nossos",
          "corpos",
          "excesso",
          "quanto",
          "todas",
          "aquelas",
          "passaram",
          "industrialização",
          "velhos",
          "inteligentes",
          "novos",
          "sábios",
          "porque"
        ],
        "entities": [
          [
            "mais velhos",
            "PERSON"
          ],
          [
            "não são mais",
            "ORG"
          ],
          [
            "fica",
            "GPE"
          ],
          [
            "quando percebe",
            "PERSON"
          ],
          [
            "Porquê",
            "PERSON"
          ],
          [
            "para o corpo",
            "PERSON"
          ],
          [
            "Excesso de energia",
            "ORG"
          ],
          [
            "Acumula",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "excesso de conservantes",
            "PERSON"
          ]
        ],
        "readability_score": 92.15596499309075,
        "semantic_density": 0,
        "word_count": 167,
        "unique_words": 105,
        "lexical_diversity": 0.6287425149700598
      },
      "preservation_score": 0.00021174867736993867
    },
    {
      "id": 98,
      "text": "Não podemos de deixar de consumir aquilo que os nossos corpos precisam, e sim, descobrir como realmente os nossos corpos precisam se adaptar.\\n\\nQuais são os alimentos mais saudáveis, aquelas que fazemos sem produtos industrializados ou aquelas que fazemos com produtos industrializados?\\n\\n“Todos nós queremos soluções depois de ter vívido toda uma vida de excessos.” \\n\\n“Nós somos tão cegos perante as nossas falhas, que a justificativa das mesmas não condiz com as avarias do trajeto.”\\n\\n“Temos que dar valor ao início do trajeto e não no final presente da trajetória.”\\n\\nQuando ficarmos velho, qual velho desejamos ser semelhantes?\\n\\nEu abro o YouTube, televisão, Instagram, Facebook e qualquer meio de comunicação, logo vem: Como ficar rico, ganhe dinheiro, mente milionária, 12 exercícios que todos os ricos fazem.\\n\\nQual é o velho que aparenta estar feliz?\\n\\nNa maioria das vezes são aqueles que vivem na roça com leveza e amor para todos os lados. \\n\\n",
      "position": 95559,
      "chapter": 5,
      "page": 61,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 25.16045321637427,
      "complexity_metrics": {
        "word_count": 152,
        "sentence_count": 9,
        "paragraph_count": 9,
        "avg_sentence_length": 16.88888888888889,
        "avg_word_length": 5.1644736842105265,
        "unique_word_ratio": 0.7828947368421053,
        "avg_paragraph_length": 16.88888888888889,
        "punctuation_density": 0.14473684210526316,
        "line_break_count": 18,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "todos",
          "velho",
          "nossos",
          "corpos",
          "precisam",
          "como",
          "aquelas",
          "fazemos",
          "produtos",
          "industrializados",
          "trajeto",
          "qual",
          "podemos",
          "deixar",
          "consumir",
          "aquilo",
          "descobrir",
          "realmente",
          "adaptar",
          "quais"
        ],
        "entities": [
          [
            "Não podemos de deixar de consumir",
            "ORG"
          ],
          [
            "que",
            "CARDINAL"
          ],
          [
            "fazemos sem",
            "PERSON"
          ],
          [
            "Todos",
            "GPE"
          ],
          [
            "queremos",
            "DATE"
          ],
          [
            "nossas falhas",
            "ORG"
          ],
          [
            "das mesmas",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "Eu",
            "PERSON"
          ],
          [
            "YouTube",
            "GPE"
          ]
        ],
        "readability_score": 90.00621345029239,
        "semantic_density": 0,
        "word_count": 152,
        "unique_words": 119,
        "lexical_diversity": 0.7828947368421053
      },
      "preservation_score": 0.0001515928031171152
    },
    {
      "id": 99,
      "text": "O problema não é o dinheiro e sim o que é necessário ser feito para ter dinheiro.\\n\\nSe conseguir ganhar dinheiro sem prejudicar o sentimento, faça, o olhar em nossa volta não vai nos matar, e sim, ensinar a forma de viver melhor no amanhã.\\n\\n“Todos nós imaginamos e almejamos uma vida boa daquelas do tipo vivida nos contos enganosos que causam esperança depressiva.”\\n\\nImagina Tudo que nossos corpos vivem e viveram durante toda a existência, quantas memórias musculares foram necessárias evoluir e adaptar-se?\\n\\nAtravés dos nossos exageros e necessidades, nossos corpos que demoraram 200 mil anos para adaptar-se a um padrão satisfatório, hoje, temos vários exageros, supérfluos e todas essas extravagâncias corpóreas e mentais nós deixando perdidos tentando adaptar-se, e quando não conseguimos, desistem de produzir recursos para aqueles excessos e deixa nós fazermos o trabalho, até porque, sempre vivemos em excesso seja para uma aparência ou a procura da vida saudável sendo perfeccionista.\\n\\n",
      "position": 96507,
      "chapter": 5,
      "page": 62,
      "segment_type": "preserved_segment",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 32.21612903225807,
      "complexity_metrics": {
        "word_count": 155,
        "sentence_count": 5,
        "paragraph_count": 5,
        "avg_sentence_length": 31.0,
        "avg_word_length": 5.387096774193548,
        "unique_word_ratio": 0.7677419354838709,
        "avg_paragraph_length": 31.0,
        "punctuation_density": 0.11612903225806452,
        "line_break_count": 10,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "dinheiro",
          "nossos",
          "adaptar",
          "vida",
          "corpos",
          "exageros",
          "problema",
          "necessário",
          "feito",
          "conseguir",
          "ganhar",
          "prejudicar",
          "sentimento",
          "faça",
          "olhar",
          "nossa",
          "volta",
          "matar",
          "ensinar",
          "forma"
        ],
        "entities": [
          [
            "necessário ser feito para",
            "ORG"
          ],
          [
            "Se",
            "PERSON"
          ],
          [
            "ganhar dinheiro",
            "PERSON"
          ],
          [
            "Todos",
            "NORP"
          ],
          [
            "causam esperança depressiva",
            "ORG"
          ],
          [
            "Imagina Tudo",
            "PERSON"
          ],
          [
            "necessárias evoluir",
            "ORG"
          ],
          [
            "200",
            "CARDINAL"
          ],
          [
            "temos vários exageros",
            "ORG"
          ],
          [
            "mentais nós deixando",
            "ORG"
          ]
        ],
        "readability_score": 82.88387096774193,
        "semantic_density": 0,
        "word_count": 155,
        "unique_words": 119,
        "lexical_diversity": 0.7677419354838709
      },
      "preservation_score": 3.843291966152611e-05
    },
    {
      "id": 100,
      "text": "O que acontece quando nossos corpos desistem de resolver os problemas que criamos para eles?\\n\\nQuantas religiões politeístas e monoteísta deram certo?\\n\\nDesde quando a política foi de benefício para todos?\\n\\nDesde quando o excesso de regras, são dê benefícios para aqueles que querem quebrar as regras?\\n\\nA felicidade ou a alegria é de benefício ser ou ter?\\n\\nAté que ponto o fazer sexo não é prejudicial para nossas vidas?\\n\\n“Todos nós humanos somos depressivos diante dos próprios pensamentos.”\\n\\nTodos nós olhamos e observamos tanto os nossos benefícios, que esquecemos do benefício de termos um copo para beber água, um cobertor, uma televisão, um arroz, um adubo e tudo aquilo que não sabemos fazer e temos devido alguém no planeta Terra saber fazer.\\n\\n“Todos nós somos um só de pensar e agir para o planeta Terra.”\\n\\n“O nosso fracasso não pode ser vergonhoso quando for para algo maior que a vergonha do fracasso.”\\n\\n",
      "position": 97502,
      "chapter": 5,
      "page": 63,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 23.56149732620321,
      "complexity_metrics": {
        "word_count": 153,
        "sentence_count": 11,
        "paragraph_count": 10,
        "avg_sentence_length": 13.909090909090908,
        "avg_word_length": 4.901960784313726,
        "unique_word_ratio": 0.6797385620915033,
        "avg_paragraph_length": 15.3,
        "punctuation_density": 0.10457516339869281,
        "line_break_count": 20,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "quando",
          "todos",
          "benefício",
          "fazer",
          "nossos",
          "desde",
          "regras",
          "benefícios",
          "somos",
          "planeta",
          "terra",
          "fracasso",
          "acontece",
          "corpos",
          "desistem",
          "resolver",
          "problemas",
          "criamos",
          "eles",
          "quantas"
        ],
        "entities": [
          [
            "quando",
            "PERSON"
          ],
          [
            "Quantas",
            "GPE"
          ],
          [
            "excesso de regras",
            "ORG"
          ],
          [
            "para aqueles",
            "PERSON"
          ],
          [
            "querem quebrar",
            "PERSON"
          ],
          [
            "Todos",
            "NORP"
          ],
          [
            "depressivos diante",
            "PERSON"
          ],
          [
            "Todos",
            "PRODUCT"
          ],
          [
            "benefício de termos",
            "PERSON"
          ],
          [
            "que",
            "CARDINAL"
          ]
        ],
        "readability_score": 91.57486631016043,
        "semantic_density": 0,
        "word_count": 153,
        "unique_words": 104,
        "lexical_diversity": 0.6797385620915033
      },
      "preservation_score": 0.00014704769261801297
    },
    {
      "id": 101,
      "text": "“O nosso maior fracasso é aquele que não reconhecemos como fracasso.”\\n\\n Exemplos: meu filho não é bom jogando futebol, irei apoiar ele jogar futebol? \\n\\nFiz a minha unha em uma manicure amiga e ficou horrível, fala para ela ou não? \\n\\nTenho o dom para jogar tênis de mesa, porém não sei conversar, não respeito, sou melhor, não preciso de ninguém, procrastino e tenho o dom, assim sei que vou ser grande...\\n\\nTodos nós somos falhos diante da vida e nessa mesma vida contém erros e fracassos, ambos também podem conter benefícios. Quais são os benefícios que temos dentro dos nossos erros e Fracassos?\\n\\nNão se julgue como incapaz, até porque, só nos tornamos incapazes quando não reconhecemos onde fracassamos!\\n\\n“Temos que ter muito cuidado em dar amor, até porque, a felicidade conquistada provém da mesma desgraça quando não se têm o valor esperado da gratidão ao ser retribuído.”\\n\\nNessas minhas aventuras entre as classes sociais, percebi uma única coisa padrão para a felicidade de todos aqueles que ",
      "position": 98415,
      "chapter": 5,
      "page": 64,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 25.867332002661342,
      "complexity_metrics": {
        "word_count": 167,
        "sentence_count": 9,
        "paragraph_count": 8,
        "avg_sentence_length": 18.555555555555557,
        "avg_word_length": 4.92814371257485,
        "unique_word_ratio": 0.7604790419161677,
        "avg_paragraph_length": 20.875,
        "punctuation_density": 0.1497005988023952,
        "line_break_count": 14,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "fracasso",
          "reconhecemos",
          "como",
          "futebol",
          "jogar",
          "tenho",
          "todos",
          "vida",
          "mesma",
          "erros",
          "fracassos",
          "benefícios",
          "temos",
          "porque",
          "quando",
          "felicidade",
          "nosso",
          "maior",
          "aquele",
          "exemplos"
        ],
        "entities": [
          [
            "jogando futebol",
            "PERSON"
          ],
          [
            "ela",
            "PERSON"
          ],
          [
            "Tenho",
            "ORG"
          ],
          [
            "jogar tênis de mesa",
            "PERSON"
          ],
          [
            "sou melhor",
            "GPE"
          ],
          [
            "vou",
            "ORG"
          ],
          [
            "ambos também",
            "PERSON"
          ],
          [
            "que temos dentro",
            "PERSON"
          ],
          [
            "Fracassos",
            "ORG"
          ],
          [
            "quando não reconhecemos",
            "PERSON"
          ]
        ],
        "readability_score": 89.24377910844977,
        "semantic_density": 0,
        "word_count": 167,
        "unique_words": 127,
        "lexical_diversity": 0.7604790419161677
      },
      "preservation_score": 0.00010854793309620596
    },
    {
      "id": 102,
      "text": "são humanos, e essa condição: só é vista, através do amor por aqueles que são importantes para nós.\\n\\n“Os que são felizes sem confiança e respeito, esses sim, são miseráveis de espírito e amor.”\\n\\n“O sentimento motivacional do amor, pode ser o mesmo que causa inveja e a ruína de si próprio.”\\n\\nQuantos movimentos interpretamos e agimos junto ao universo? \\n\\nDesde o início nós movimentamos corretamente junto a forma de captarmos a energia?\\n\\nO movimento gerado para se ter o início do universo, quanto tempo leva para o mesmo adaptar-se?\\n\\nTempo é relativo. \\n\\nNós nascemos e temos um padrão de tempo.\\n\\nQual é o tempo que o universo têm e quanto tempo têm o nosso planeta Terra?\\n\\nO nosso planeta Terra está em qual idade para o universo?\\n\\nEle já aprendeu a abrir os olhos, cagar, comer, falar, engatinhar, andar, correr, amar, sentir e movimentar-se com todos no universo?\\n\\n“Deus é perfeito por desistir de amar e direcionar aqueles que não enxergam o próprio destino.”\\n\\n",
      "position": 99415,
      "chapter": 5,
      "page": 65,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 22.892447552447553,
      "complexity_metrics": {
        "word_count": 165,
        "sentence_count": 13,
        "paragraph_count": 12,
        "avg_sentence_length": 12.692307692307692,
        "avg_word_length": 4.7696969696969695,
        "unique_word_ratio": 0.6848484848484848,
        "avg_paragraph_length": 13.75,
        "punctuation_density": 0.16363636363636364,
        "line_break_count": 24,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "universo",
          "tempo",
          "amor",
          "aqueles",
          "mesmo",
          "próprio",
          "junto",
          "início",
          "quanto",
          "qual",
          "nosso",
          "planeta",
          "terra",
          "amar",
          "humanos",
          "essa",
          "condição",
          "vista",
          "através",
          "importantes"
        ],
        "entities": [
          [
            "são humanos",
            "PERSON"
          ],
          [
            "Desde",
            "ORG"
          ],
          [
            "universo",
            "ORG"
          ],
          [
            "quanto tempo",
            "PERSON"
          ],
          [
            "leva",
            "ORG"
          ],
          [
            "mesmo",
            "ORG"
          ],
          [
            "universo têm e quanto",
            "ORG"
          ],
          [
            "têm o",
            "ORG"
          ],
          [
            "Terra",
            "PERSON"
          ],
          [
            "universo",
            "PERSON"
          ]
        ],
        "readability_score": 92.22293706293706,
        "semantic_density": 0,
        "word_count": 165,
        "unique_words": 113,
        "lexical_diversity": 0.6848484848484848
      },
      "preservation_score": 0.00033687289581581145
    },
    {
      "id": 103,
      "text": "“Todos nós nascemos sem saber nada e vamos vivendo com todos aqueles movimentos que só alguns poderiam ser capaz de seguir corretamente.” \\n\\nMuitas vezes o trajeto de trabalhar até tarde e fazer o que não foi combinado, para alguns: não percebem a necessidade de fazer para ser digno de ter um aumento salarial, promoção, indicação para outros trabalhos, melhor cargo e outras formas necessárias que é preciso dedicação em sermos melhores, ao invés de ir em um caminho onde o estudar nunca será o trajeto em conseguir parar de pensar na fome, até porque, quantos conseguem atingir o não pensar nos problemas estudando e trabalhando?\\n\\n“Os idiotas vão tomar conta do mundo; não pela capacidade, mas pela quantidade. Eles são muitos.” Nelson Rodrigues\\n\\nO movimento da própria vida virou uma bola de neve e acúmulo de caos, semelhante a um besouro que carrega a própria casa, construída pelas próprias merdas.\\n\\n",
      "position": 100381,
      "chapter": 5,
      "page": 66,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 31.701999999999998,
      "complexity_metrics": {
        "word_count": 150,
        "sentence_count": 5,
        "paragraph_count": 4,
        "avg_sentence_length": 30.0,
        "avg_word_length": 5.006666666666667,
        "unique_word_ratio": 0.76,
        "avg_paragraph_length": 37.5,
        "punctuation_density": 0.11333333333333333,
        "line_break_count": 8,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "todos",
          "alguns",
          "trajeto",
          "fazer",
          "pensar",
          "pela",
          "própria",
          "nascemos",
          "saber",
          "nada",
          "vamos",
          "vivendo",
          "aqueles",
          "movimentos",
          "poderiam",
          "capaz",
          "seguir",
          "corretamente",
          "muitas",
          "vezes"
        ],
        "entities": [
          [
            "nascemos sem",
            "PERSON"
          ],
          [
            "nada e vamos vivendo",
            "ORG"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "poderiam ser capaz de seguir",
            "PERSON"
          ],
          [
            "de trabalhar",
            "PERSON"
          ],
          [
            "para ser",
            "PERSON"
          ],
          [
            "para outros trabalhos",
            "PERSON"
          ],
          [
            "mas pela",
            "PERSON"
          ],
          [
            "Nelson Rodrigues",
            "PERSON"
          ],
          [
            "da própria",
            "PERSON"
          ]
        ],
        "readability_score": 83.498,
        "semantic_density": 0,
        "word_count": 150,
        "unique_words": 114,
        "lexical_diversity": 0.76
      },
      "preservation_score": 2.2458193054387435e-05
    },
    {
      "id": 104,
      "text": "Todos nós seguimos doutrinas que já foram necessárias quando o movimento precisava ser seguido, assim como: O universo não continha vida e com o tempo obteve, quanto tempo para adaptar-se levou e nós humanos não somos diferentes, porém, nós seguimos nossa própria ordem dentro de um universo com uma ordem superior.\\n\\nTodos nós somos captadores dê energia em conseguir sentir o destino da Terra, seja para o lado do amor ou do caos, tudo vai depender de como é interpretado o que é sentido.\\n\\n Quando a Terra fica doente e fora de equilíbrio com o movimento do universo, o que acontece com as energias que dependem da Terra para se mover?\\n\\nTodos nós somos captadores da energia da Terra junto ao universo, desde: andorinha, Formiga, baleia e qualquer tipo de energia física que necessita viver em singularidade com o universo.\\n\\nSomos feitos de movimentos, evolução, adaptação e singularidade.\\n\\nNão são todos que vão entender os pensamentos daqueles que vieram para regular e direcionar a propagação vív",
      "position": 101287,
      "chapter": 5,
      "page": 67,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 30.33152610441767,
      "complexity_metrics": {
        "word_count": 166,
        "sentence_count": 6,
        "paragraph_count": 6,
        "avg_sentence_length": 27.666666666666668,
        "avg_word_length": 4.993975903614458,
        "unique_word_ratio": 0.6566265060240963,
        "avg_paragraph_length": 27.666666666666668,
        "punctuation_density": 0.1144578313253012,
        "line_break_count": 10,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "universo",
          "todos",
          "somos",
          "terra",
          "energia",
          "seguimos",
          "quando",
          "movimento",
          "como",
          "tempo",
          "ordem",
          "captadores",
          "singularidade",
          "doutrinas",
          "necessárias",
          "precisava",
          "seguido",
          "assim",
          "continha",
          "vida"
        ],
        "entities": [
          [
            "necessárias quando",
            "PERSON"
          ],
          [
            "ser seguido",
            "PERSON"
          ],
          [
            "para adaptar",
            "PERSON"
          ],
          [
            "própria ordem",
            "ORG"
          ],
          [
            "dentro de um universo",
            "ORG"
          ],
          [
            "Todos",
            "CARDINAL"
          ],
          [
            "nós somos captadores dê energia",
            "ORG"
          ],
          [
            "destino da Terra",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "universo, o que acontece",
            "ORG"
          ]
        ],
        "readability_score": 84.66847389558232,
        "semantic_density": 0,
        "word_count": 166,
        "unique_words": 109,
        "lexical_diversity": 0.6566265060240963
      },
      "preservation_score": 4.010391616854898e-05
    },
    {
      "id": 105,
      "text": "ida e interpretada por Nostradamus, Salomão, Sócrates, Platão, Sidarta Gautama, Moisés, Cleópatra, Jesus, Darwin, Leonardo da Vinci, Pitágoras, Tesla, Marie Curie, Einstein, Hitler, Chico Xavier e todos aqueles que captaram a energia de um caos vivido junto a necessidade de adaptar-se.\\n\\nMatemática – ciência que estuda, por método dedutivo, objetos abstratos (números, figuras, funções) e as relações (padrão) existentes entre eles, tendo o zero como regulador dos padrões.\\n\\nOrigem – A Matemática, como a conhecemos hoje, surgiu no Antigo Egito e no Império Babilônico, por volta de 3500 a.C. Porém, na pré-história, os seres humanos já usavam os conceitos de contar e medir. Por isso, a matemática não teve nenhum inventor, mas foi criada a partir da necessidade de os homens das cavernas medir e contar objetos.\\n\\nTudo que contém movimentos, contém matemática, sendo que: qual é a forma certa de correlacionar um padrão matemático?\\n\\n",
      "position": 102287,
      "chapter": 5,
      "page": 68,
      "segment_type": "preserved_segment",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 34.05477832512315,
      "complexity_metrics": {
        "word_count": 145,
        "sentence_count": 7,
        "paragraph_count": 4,
        "avg_sentence_length": 20.714285714285715,
        "avg_word_length": 5.4206896551724135,
        "unique_word_ratio": 0.8,
        "avg_paragraph_length": 36.25,
        "punctuation_density": 0.25517241379310346,
        "line_break_count": 8,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "matemática",
          "necessidade",
          "objetos",
          "padrão",
          "como",
          "contar",
          "medir",
          "contém",
          "interpretada",
          "nostradamus",
          "salomão",
          "sócrates",
          "platão",
          "sidarta",
          "gautama",
          "moisés",
          "cleópatra",
          "jesus",
          "darwin",
          "leonardo"
        ],
        "entities": [
          [
            "ida e",
            "PERSON"
          ],
          [
            "interpretada",
            "NORP"
          ],
          [
            "Nostradamus",
            "NORP"
          ],
          [
            "Sócrates",
            "GPE"
          ],
          [
            "Platão",
            "GPE"
          ],
          [
            "Sidarta Gautama",
            "PERSON"
          ],
          [
            "Cleópatra",
            "PERSON"
          ],
          [
            "Jesus",
            "PERSON"
          ],
          [
            "Darwin",
            "PERSON"
          ],
          [
            "Leonardo da Vinci",
            "PERSON"
          ]
        ],
        "readability_score": 88.01665024630542,
        "semantic_density": 0,
        "word_count": 145,
        "unique_words": 116,
        "lexical_diversity": 0.8
      },
      "preservation_score": 4.5985823873269514e-05
    },
    {
      "id": 106,
      "text": "Como era usado o cálculo no Egito antigo? \\n\\nNo Egito antigo nós usávamos a numerologia para captarmos e adaptarmos o nosso viver com o viver do universo, são esses cálculos usado como base no triângulo da vida, pirâmides e todas as formas de se encontrar os números 3, 6 e 9.\\n\\n3 é considerado como a união entre o corpo, o espírito e a mente, representando, portanto, pessoas que procuram manter o equilíbrio. \\n\\n6 pode ser lido como um número conciliador, relacionado com elementos corretos como a justiça, verdade e honestidade.\\n\\n9 Como se trata de um número de pessoas que conseguem entender ambos os lados, espiritual e material, o 9 representa a realização total do homem em todas as suas aspirações, oferecendo o atendimento de todos os seus desejos.\\n\\nLembrando que: todos os cálculos feitos na Cabala judaica são somados, multiplicados, divididos e reduzidos. Exemplo: 30/08/1986 somamos os números 3+0+0+8+1+9+8+6=35\\n\\n",
      "position": 103222,
      "chapter": 5,
      "page": 69,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 27.307568590350048,
      "complexity_metrics": {
        "word_count": 151,
        "sentence_count": 7,
        "paragraph_count": 6,
        "avg_sentence_length": 21.571428571428573,
        "avg_word_length": 5.072847682119205,
        "unique_word_ratio": 0.6887417218543046,
        "avg_paragraph_length": 25.166666666666668,
        "punctuation_density": 0.1456953642384106,
        "line_break_count": 12,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "como",
          "usado",
          "egito",
          "antigo",
          "viver",
          "cálculos",
          "todas",
          "números",
          "pessoas",
          "número",
          "todos",
          "cálculo",
          "usávamos",
          "numerologia",
          "captarmos",
          "adaptarmos",
          "nosso",
          "universo",
          "esses",
          "base"
        ],
        "entities": [
          [
            "Egito",
            "PERSON"
          ],
          [
            "Egito",
            "PERSON"
          ],
          [
            "numerologia para captarmos e adaptarmos o",
            "ORG"
          ],
          [
            "formas de se",
            "PERSON"
          ],
          [
            "6",
            "CARDINAL"
          ],
          [
            "9",
            "CARDINAL"
          ],
          [
            "3",
            "CARDINAL"
          ],
          [
            "representando",
            "GPE"
          ],
          [
            "portanto",
            "GPE"
          ],
          [
            "6",
            "CARDINAL"
          ]
        ],
        "readability_score": 87.69243140964996,
        "semantic_density": 0,
        "word_count": 151,
        "unique_words": 104,
        "lexical_diversity": 0.6887417218543046
      },
      "preservation_score": 5.293716934248467e-05
    },
    {
      "id": 107,
      "text": "Reduzindo=8\\n\\nTodos nós fomos criados fazendo soma, multiplicação e divisão seja em valores positivos ou valores negativos. \\n\\nTodos nós procuramos padrões matemáticos originários de uma forma de captar e entendermos o padrão, qual caminho está nós levando a qual está indo esse padrão?\\n\\nDesde o início dos tempos, olhamos a matemática de uma forma que aprendemos na escola como padrão para chegarmos a uma exatidão.\\n\\nA partir desse ponto de vista, será que estamos a lhe dar com a matemática de uma forma correta de ser usada ou durante toda a nossa existência esquecemos de compreender a energia e queremos solucionar o que já foi captado?\\n\\nSabe aquele ditado que diz:\\n\\n“Deus não dá asas a cobra.”\\n\\n“Eu vejo o Universo trabalhando certo com Linhas tortas.”\\n\\nTodos nós somos frutos da nossa própria imaginação de como ver a vida. \\n\\nComo nós alimentamos.\\n\\nComo nós enxergamos.\\n\\nComo nós ouvimos.\\n\\nComo falamos. \\n\\n",
      "position": 104147,
      "chapter": 5,
      "page": 70,
      "segment_type": "preserved_segment",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 23.39909090909091,
      "complexity_metrics": {
        "word_count": 150,
        "sentence_count": 11,
        "paragraph_count": 13,
        "avg_sentence_length": 13.636363636363637,
        "avg_word_length": 4.966666666666667,
        "unique_word_ratio": 0.6866666666666666,
        "avg_paragraph_length": 11.538461538461538,
        "punctuation_density": 0.10666666666666667,
        "line_break_count": 26,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "como",
          "todos",
          "forma",
          "padrão",
          "valores",
          "qual",
          "está",
          "matemática",
          "nossa",
          "reduzindo",
          "fomos",
          "criados",
          "fazendo",
          "soma",
          "multiplicação",
          "divisão",
          "seja",
          "positivos",
          "negativos",
          "procuramos"
        ],
        "entities": [
          [
            "Todos",
            "CARDINAL"
          ],
          [
            "multiplicação e divisão",
            "ORG"
          ],
          [
            "Todos",
            "GPE"
          ],
          [
            "padrões matemáticos",
            "PERSON"
          ],
          [
            "de uma forma de captar",
            "PERSON"
          ],
          [
            "padrão",
            "ORG"
          ],
          [
            "Desde",
            "ORG"
          ],
          [
            "para chegarmos",
            "PERSON"
          ],
          [
            "Universo",
            "GPE"
          ],
          [
            "Todos",
            "PRODUCT"
          ]
        ],
        "readability_score": 91.69181818181818,
        "semantic_density": 0,
        "word_count": 150,
        "unique_words": 103,
        "lexical_diversity": 0.6866666666666666
      },
      "preservation_score": 0.0002259187277494927
    },
    {
      "id": 108,
      "text": "Como sentimos.\\n\\nComo nós tocamos.\\n\\nVejo que: grandes humanos que não queriam aquilo que o universo os deu como dom, o mesmo dom foi a destruição para aqueles que não conseguiram administrar o ser grande proporcional a grandeza.\\n\\nVejo que: grandes humanos que queriam aquilo que o universo os deu como dom, o mesmo dom foi a evolução do caos e dá miséria no seu entorno.\\n\\n“O mesmo caráter que nós faz bem é o mesmo que nós faz mal e para conseguir entender, basta olhar de um ângulo diferente.”\\n\\nTodos nós somos frutos de um passado, esse passado leva quanto tempo para adaptar-se?\\n\\nOs países desenvolvidos estão em qual fase de adaptação proporcional ao próprio passado?\\n\\nQual foi o maior tempo em que um humano ficou no comando de um país e quantas pessoas pensam semelhantes?\\n\\nQuando acabou a escravidão, poder para as mulheres, poder para Gays e liberdade de expressão para todos?\\n\\nQual é a melhor forma de consumo e estilo de vida a qual um humano precisa viver?\\n\\n",
      "position": 105058,
      "chapter": 5,
      "page": 71,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 24.892982456140352,
      "complexity_metrics": {
        "word_count": 171,
        "sentence_count": 10,
        "paragraph_count": 10,
        "avg_sentence_length": 17.1,
        "avg_word_length": 4.60233918128655,
        "unique_word_ratio": 0.5964912280701754,
        "avg_paragraph_length": 17.1,
        "punctuation_density": 0.10526315789473684,
        "line_break_count": 20,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "como",
          "mesmo",
          "qual",
          "passado",
          "vejo",
          "grandes",
          "humanos",
          "queriam",
          "aquilo",
          "universo",
          "proporcional",
          "todos",
          "tempo",
          "humano",
          "poder",
          "sentimos",
          "tocamos",
          "destruição",
          "aqueles",
          "conseguiram"
        ],
        "entities": [
          [
            "Vejo",
            "PERSON"
          ],
          [
            "não queriam",
            "PERSON"
          ],
          [
            "Vejo",
            "PERSON"
          ],
          [
            "que queriam",
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
            "faz",
            "ORG"
          ],
          [
            "basta",
            "NORP"
          ],
          [
            "Todos",
            "PRODUCT"
          ],
          [
            "leva quanto",
            "PERSON"
          ]
        ],
        "readability_score": 90.06929824561404,
        "semantic_density": 0,
        "word_count": 171,
        "unique_words": 102,
        "lexical_diversity": 0.5964912280701754
      },
      "preservation_score": 0.00014036370658992146
    },
    {
      "id": 109,
      "text": "Se somos filhos de uma pessoa viciada qual é o caminho até ter uma vida satisfatória?\\n\\nAtravés dessa pergunta, como foi o trajeto para aqueles que têm uma mãe (pai), comida, cama, casa, carro, colégio particular, excessos e tudo aquilo que todos merecem?\\n\\nQuais são os gatilhos emocionais que os trajetos causam?\\n\\nQuando morremos com um raio caindo sobre nossas cabeças é azar, porém, quando ganhamos na Megasena achamos sorte. \\n\\nQuantas formas de se expressar e falar sobre os mesmos assuntos temos?\\n\\nA palavra probabilidade só serve para a matemática ou serve para substituir bom ou ruim?\\n\\nQual é o valor que precisamos ter para viver satisfeito?\\n\\n O empresário de cigarro, cerveja, jogos e todas aquelas coisas que nós vejamos como errado, culpamos outros pela falta de reconhecimento do próprio erro. \\n\\nTemos o pobre que vive reclamando de não ter dinheiro, porém, quer ter dinheiro sem trabalhar.\\n\\n",
      "position": 106026,
      "chapter": 5,
      "page": 72,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 24.685034013605442,
      "complexity_metrics": {
        "word_count": 147,
        "sentence_count": 9,
        "paragraph_count": 9,
        "avg_sentence_length": 16.333333333333332,
        "avg_word_length": 5.061224489795919,
        "unique_word_ratio": 0.7891156462585034,
        "avg_paragraph_length": 16.333333333333332,
        "punctuation_density": 0.1564625850340136,
        "line_break_count": 18,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "qual",
          "como",
          "quando",
          "porém",
          "temos",
          "serve",
          "dinheiro",
          "somos",
          "filhos",
          "pessoa",
          "viciada",
          "caminho",
          "vida",
          "satisfatória",
          "através",
          "dessa",
          "pergunta",
          "trajeto",
          "aqueles",
          "comida"
        ],
        "entities": [
          [
            "Se somos filhos de uma pessoa",
            "PERSON"
          ],
          [
            "têm uma mãe (",
            "ORG"
          ],
          [
            "casa",
            "ORG"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "Quando morremos",
            "PERSON"
          ],
          [
            "caindo",
            "NORP"
          ],
          [
            "quando ganhamos",
            "PERSON"
          ],
          [
            "Megasena",
            "PRODUCT"
          ],
          [
            "Quantas",
            "GPE"
          ],
          [
            "mesmos assuntos temos",
            "PERSON"
          ]
        ],
        "readability_score": 90.31496598639455,
        "semantic_density": 0,
        "word_count": 147,
        "unique_words": 116,
        "lexical_diversity": 0.7891156462585034
      },
      "preservation_score": 0.00013535071706885285
    },
    {
      "id": 110,
      "text": "Ninguém quer catar o lixo, porém todos querem ser bem sucedido e viver confortável.\\n\\nNenhuma política e nenhum método, poderá dar certo se a origem vier provinda e direcionada para alguns beneficiados a uma classe habituada em viver acima da miséria.\\n\\n“Na política não temos como favorecer o pobre sem prejudicar o contexto.”\\n\\nNinguém quer dar emprego para alguém que não tenha estudo, educação, aparência, personalidade, autoestima e todas aquelas coisas que vejamos como necessário ser e ter como abertura em algum trajeto até a confiança.\\n\\nNós somos ciclos de adaptação até chegarmos a singularidade. Esses ciclos adaptáveis variam de acordo com a interferência do dano sofrido e esse dano aumentando, provém de ocorrer com mais intensidade e o tempo de acontecimentos serão menores.\\n\\n“Quando esses acontecimentos acontecem com muita intensidade, os ciclos e os acontecimentos ficam semelhantes a uma lembrança de nossas mentes... parecem estar afunilando na mesma sincronicidade.”\\n\\n",
      "position": 106929,
      "chapter": 5,
      "page": 73,
      "segment_type": "preserved_segment",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 27.104444444444447,
      "complexity_metrics": {
        "word_count": 150,
        "sentence_count": 9,
        "paragraph_count": 6,
        "avg_sentence_length": 16.666666666666668,
        "avg_word_length": 5.533333333333333,
        "unique_word_ratio": 0.7266666666666667,
        "avg_paragraph_length": 25.0,
        "punctuation_density": 0.12,
        "line_break_count": 12,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "como",
          "ciclos",
          "acontecimentos",
          "ninguém",
          "quer",
          "viver",
          "política",
          "esses",
          "dano",
          "intensidade",
          "catar",
          "lixo",
          "porém",
          "todos",
          "querem",
          "sucedido",
          "confortável",
          "nenhuma",
          "nenhum",
          "método"
        ],
        "entities": [
          [
            "Ninguém",
            "ORG"
          ],
          [
            "lixo",
            "ORG"
          ],
          [
            "todos",
            "NORP"
          ],
          [
            "querem ser bem sucedido",
            "PERSON"
          ],
          [
            "Nenhuma",
            "PERSON"
          ],
          [
            "provinda e direcionada para",
            "PERSON"
          ],
          [
            "habituada",
            "PERSON"
          ],
          [
            "viver acima da miséria",
            "PERSON"
          ],
          [
            "Ninguém",
            "ORG"
          ],
          [
            "dar emprego",
            "PERSON"
          ]
        ],
        "readability_score": 90.00666666666666,
        "semantic_density": 0,
        "word_count": 150,
        "unique_words": 109,
        "lexical_diversity": 0.7266666666666667
      },
      "preservation_score": 5.293716934248467e-05
    },
    {
      "id": 111,
      "text": "Sincronicidades em forma de captação extrema período pré idade Média:\\n\\nMatemática, religião, filosofia, arte, política, Cleópatra (besta), Cesar (abertura sexto selo), Alexandre o Grande, peste negra, cataclisma e muita morte e dor. \\n\\n“Na fé se cura a dor e na religião se cura a morte.”\\n\\nPós idade média e formas de captar:\\n\\nPolítica (Nicolau Maquiavel), filósofo (Shakespeare), matemática (Leonardo da Vinci), religião (cura sentimental), psicologia, telefone, luz, revolução industrial, aprofundamento física Quântica, Marilyn Monroe (besta), Hitler (abertura sexto selo), tecnologia, Chico Xavier (falou que Brasil seria o berço do mundo e uma nova ordem mundial).\\n\\nAcontecimentos pré apocalíptico no presente:\\n\\nCatástrofes em escalas maiores que o de costume. Estações do ano e tempo de rotação do planeta Terra alterados, pequenos ciclos evolutivos, revolução tecnológica, Pandemia, descobertas de diamantes com o interior ainda com água.\\n\\n",
      "position": 107915,
      "chapter": 5,
      "page": 74,
      "segment_type": "preserved_segment",
      "themes": {
        "filosofia": 39.473684210526315,
        "ciencia": 34.21052631578947,
        "arte": 13.157894736842104,
        "tecnologia": 13.157894736842104
      },
      "difficulty": 30.3,
      "complexity_metrics": {
        "word_count": 134,
        "sentence_count": 5,
        "paragraph_count": 7,
        "avg_sentence_length": 26.8,
        "avg_word_length": 6.0,
        "unique_word_ratio": 0.7910447761194029,
        "avg_paragraph_length": 19.142857142857142,
        "punctuation_density": 0.2462686567164179,
        "line_break_count": 14,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "religião",
          "cura",
          "idade",
          "média",
          "matemática",
          "política",
          "besta",
          "abertura",
          "sexto",
          "selo",
          "morte",
          "revolução",
          "sincronicidades",
          "forma",
          "captação",
          "extrema",
          "período",
          "filosofia",
          "arte",
          "cleópatra"
        ],
        "entities": [
          [
            "Média",
            "GPE"
          ],
          [
            "Matemática",
            "GPE"
          ],
          [
            "Cleópatra",
            "PERSON"
          ],
          [
            "Cesar",
            "ORG"
          ],
          [
            "selo",
            "PERSON"
          ],
          [
            "Alexandre",
            "PERSON"
          ],
          [
            "formas de captar",
            "ORG"
          ],
          [
            "Shakespeare",
            "PERSON"
          ],
          [
            "matemática",
            "PERSON"
          ],
          [
            "Leonardo da Vinci",
            "PERSON"
          ]
        ],
        "readability_score": 84.8,
        "semantic_density": 0,
        "word_count": 134,
        "unique_words": 106,
        "lexical_diversity": 0.7910447761194029
      },
      "preservation_score": 0.00017358311714953624
    },
    {
      "id": 112,
      "text": "Diamantes são pedras vindas do centro para o extremo, sendo empurrados, fundidos e comprimidos, assim os diamantes mais puros, são aqueles que têm menos imperfeições no núcleo dele. \\n\\nForam encontrados diamantes vindos mais próximo do centro da Terra, esse continham 1,5 por cento d’água no seu interior, logo esse diamante está com mais abertura em sua trajetória, assim, esse fator é determinante em termos noção sobre o quanto o interior da Terra está abalado. \\n\\nEsse diamante foi encontrado na Amazônia brasileira, onde podemos encontrar a ponta de uma placa tectônica, essas colidindo umas com as outras ocorrem pequenas ou grandes trepidações e nessas trepidações aquelas fissuras mais antigas, expelem aquilo que demora muito tempo para ser expelido. \\n\\n“De acordo com Chico Xavier, o Brasil seria o berço do mundo se nós nos matássemos, e se isso não ocorrer, os alienígenas iriam vir do espaço e o planeta Terra faria parte de uma grande ordem interplanetária.”\\n\\n",
      "position": 108861,
      "chapter": 5,
      "page": 75,
      "segment_type": "preserved_segment",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 32.1658064516129,
      "complexity_metrics": {
        "word_count": 155,
        "sentence_count": 5,
        "paragraph_count": 4,
        "avg_sentence_length": 31.0,
        "avg_word_length": 5.219354838709678,
        "unique_word_ratio": 0.7806451612903226,
        "avg_paragraph_length": 38.75,
        "punctuation_density": 0.12258064516129032,
        "line_break_count": 8,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "esse",
          "diamantes",
          "terra",
          "centro",
          "assim",
          "interior",
          "diamante",
          "está",
          "trepidações",
          "pedras",
          "vindas",
          "extremo",
          "sendo",
          "empurrados",
          "fundidos",
          "comprimidos",
          "puros",
          "aqueles",
          "menos"
        ],
        "entities": [
          [
            "pedras",
            "ORG"
          ],
          [
            "para",
            "PRODUCT"
          ],
          [
            "diamantes mais puros",
            "PERSON"
          ],
          [
            "mais próximo",
            "PERSON"
          ],
          [
            "da Terra",
            "PERSON"
          ],
          [
            "1,5",
            "CARDINAL"
          ],
          [
            "mais abertura",
            "PERSON"
          ],
          [
            "Amazônia",
            "GPE"
          ],
          [
            "tectônica",
            "PERSON"
          ],
          [
            "que demora muito",
            "PERSON"
          ]
        ],
        "readability_score": 82.9341935483871,
        "semantic_density": 0,
        "word_count": 155,
        "unique_words": 121,
        "lexical_diversity": 0.7806451612903226
      },
      "preservation_score": 2.352763081888208e-05
    },
    {
      "id": 113,
      "text": "Vamos pegar os fatos que estão acontecendo, tipo assim:\\n\\nSou virginiano e todos sabem que virginianos são metódicos, então essa característica marcante é dominante.\\n\\nVamos visualizar tudo que está acontecendo de longe e em um contexto:\\n\\nTodos os acontecimentos estão no mesmo ciclo dos acontecimentos pré idade média. \\n\\nTodos os indícios de um grande cataclisma estão sendo expostos.\\n\\nGrandes vidências de acontecimentos estão sendo premeditadas.\\n\\nRússia e Ucrânia em uma guerra nuclear onde a Europa será a maior prejudicada. \\n\\nAs pedras da morte voltando a aparecer na Europa.\\n\\nUm cataclisma perto das fronteiras no lado Norte do Brasil para acontecer, têm sinais que Isso possa vir acontecer.\\n\\nO que está acontecendo com o nosso planeta Terra?\\n\\nQual é a melhor forma de conversar, debater, instruir, agregar e aquelas coisas que são necessárias termos?\\n\\nJô Soares – no meu ponto de vista é o melhor entrevistador que eu pude ver. \\n\\n",
      "position": 109832,
      "chapter": 5,
      "page": 76,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 24.002348993288592,
      "complexity_metrics": {
        "word_count": 149,
        "sentence_count": 10,
        "paragraph_count": 12,
        "avg_sentence_length": 14.9,
        "avg_word_length": 5.174496644295302,
        "unique_word_ratio": 0.7449664429530202,
        "avg_paragraph_length": 12.416666666666666,
        "punctuation_density": 0.12080536912751678,
        "line_break_count": 24,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "estão",
          "acontecendo",
          "todos",
          "acontecimentos",
          "vamos",
          "está",
          "cataclisma",
          "sendo",
          "europa",
          "acontecer",
          "melhor",
          "pegar",
          "fatos",
          "tipo",
          "assim",
          "virginiano",
          "sabem",
          "virginianos",
          "metódicos",
          "então"
        ],
        "entities": [
          [
            "Vamos",
            "PERSON"
          ],
          [
            "Sou",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "virginianos são",
            "PERSON"
          ],
          [
            "metódicos",
            "PRODUCT"
          ],
          [
            "essa característica",
            "GPE"
          ],
          [
            "Vamos",
            "PERSON"
          ],
          [
            "Todos",
            "GPE"
          ],
          [
            "Todos",
            "GPE"
          ],
          [
            "Rússia e Ucrânia",
            "GPE"
          ]
        ],
        "readability_score": 90.99765100671141,
        "semantic_density": 0,
        "word_count": 149,
        "unique_words": 111,
        "lexical_diversity": 0.7449664429530202
      },
      "preservation_score": 0.00017324891784813162
    },
    {
      "id": 114,
      "text": "Porque ele era bom? Sabia fazer as perguntas certas, ser dinâmico com o entrevistado e cômico quando era necessário ser. \\n\\nMelhores entrevistados – no meu ponto de vista são aqueles que conseguem concluir o assunto e não ter perguntas, e os questionamentos sempre são agregadores.\\n\\nCoisas que não são legais em uma conversa: \\n\\nViu aquele filme? \\n\\nVi e achei uma merda!!! pois as cenas de ação eram horríveis.\\n\\nDiscordo totalmente de você, achei bom pacaralho... \\n\\nAté que ponto o manter o assunto é saudável? \\n\\nAté que ponto o opinar ou ser opinado é legal? \\n\\n...\\n\\nComprei um carro amarelo e tinha banco de couro!!\\n\\nEle veio com multimídia?\\n\\nVeio sim e além de multimídia, veio com comando no volante!!\\n\\nIrado!! Tá feliz?\\n\\nMinha filha só faz merda, me pediu um dinheiro e\\n\\nGastou tudo com roupa.\\n\\nCaralho, você está feliz com o carro?\\n\\n...\\n\\nTemos várias formas de conversar e falar, porém os erros começam pela boca quando as palavras são ditas, antes disso, ela veio originária do seu próprio padrão de pensar, agir e evoluir a vida!\\n\\n",
      "position": 110767,
      "chapter": 5,
      "page": 77,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 21.582088565763385,
      "complexity_metrics": {
        "word_count": 178,
        "sentence_count": 17,
        "paragraph_count": 18,
        "avg_sentence_length": 10.470588235294118,
        "avg_word_length": 4.685393258426966,
        "unique_word_ratio": 0.7303370786516854,
        "avg_paragraph_length": 9.88888888888889,
        "punctuation_density": 0.2303370786516854,
        "line_break_count": 36,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "veio",
          "ponto",
          "perguntas",
          "quando",
          "assunto",
          "achei",
          "merda",
          "você",
          "carro",
          "multimídia",
          "feliz",
          "porque",
          "sabia",
          "fazer",
          "certas",
          "dinâmico",
          "entrevistado",
          "cômico",
          "necessário",
          "melhores"
        ],
        "entities": [
          [
            "perguntas",
            "ORG"
          ],
          [
            "cômico quando",
            "PERSON"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "Coisas",
            "NORP"
          ],
          [
            "Discordo totalmente de você",
            "PERSON"
          ],
          [
            "amarelo e",
            "PERSON"
          ],
          [
            "banco de couro",
            "ORG"
          ],
          [
            "Ele veio",
            "PERSON"
          ],
          [
            "Veio",
            "PERSON"
          ],
          [
            "Irado",
            "NORP"
          ]
        ],
        "readability_score": 93.35908790482485,
        "semantic_density": 0,
        "word_count": 178,
        "unique_words": 130,
        "lexical_diversity": 0.7303370786516854
      },
      "preservation_score": 0.0008879007039716746
    },
    {
      "id": 115,
      "text": "Alguém faz alguma coisa por mim se eu não fizer?\\n\\n Eu fazendo merda no meu trabalho ou escola, o que acontece comigo? Sou mandado embora, expulsão, suspensão, redução de salário...\\n\\nSe eu fizer merda na vida? Posso ser morto, preso, machucado, fudido...\\n\\nAlguém está se importando com os meus erros? \\n\\nPorque devemos supervisionar aqueles que eram para nós supervisionar?\\n\\nPorque devemos dar palpite no trabalho de outros, se eu não gosto nem de ninguém perto quando estou trabalhando? \\n\\nPorque devo orientar e supervisionar o trabalho de um deputado, vereador, prefeito, governador, senador e presidente?\\n\\nPensa comigo: Eu sou prefeito da cidade e você um cidadão, você votou em mim para não ter roubo, ter comida, água, esgoto, hospital, infraestrutura, lazer, diversão e etecetera, porém, quem está na liderança está preocupado com tudo isso ou está preocupado com uma parte disso só para melhorar a sua própria vida?\\n\\n",
      "position": 111803,
      "chapter": 5,
      "page": 78,
      "segment_type": "preserved_segment",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 25.909183673469386,
      "complexity_metrics": {
        "word_count": 147,
        "sentence_count": 10,
        "paragraph_count": 8,
        "avg_sentence_length": 14.7,
        "avg_word_length": 5.197278911564626,
        "unique_word_ratio": 0.7346938775510204,
        "avg_paragraph_length": 18.375,
        "punctuation_density": 0.25170068027210885,
        "line_break_count": 16,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "está",
          "trabalho",
          "porque",
          "supervisionar",
          "alguém",
          "fizer",
          "merda",
          "comigo",
          "vida",
          "devemos",
          "prefeito",
          "você",
          "preocupado",
          "alguma",
          "coisa",
          "fazendo",
          "escola",
          "acontece",
          "mandado",
          "embora"
        ],
        "entities": [
          [
            "faz",
            "ORG"
          ],
          [
            "mim",
            "PERSON"
          ],
          [
            "se eu",
            "PERSON"
          ],
          [
            "Eu",
            "PERSON"
          ],
          [
            "expulsão",
            "GPE"
          ],
          [
            "suspensão",
            "ORG"
          ],
          [
            "Se eu",
            "PERSON"
          ],
          [
            "Posso ser morto",
            "ORG"
          ],
          [
            "preso",
            "ORG"
          ],
          [
            "machucado",
            "GPE"
          ]
        ],
        "readability_score": 91.09081632653061,
        "semantic_density": 0,
        "word_count": 147,
        "unique_words": 108,
        "lexical_diversity": 0.7346938775510204
      },
      "preservation_score": 0.0001582767891452067
    },
    {
      "id": 116,
      "text": "“Todos que estão no poder são semelhantes àqueles que estão ao nosso lado.”\\n\\nTemos aqueles “amigos” que viraram ladrões, temos aqueles “amigos” que eram ladrões, temos aqueles “amigos” que são corruptos, temos aqueles “amigos” que roubam, temos aqueles “amigos” que se tiverem uma oportunidade em se dar bem vão se dar bem, não adianta reclamar do que é um padrão.\\n\\nNão iremos evoluir e viver em paz e harmonia do dia para noite e o processo de adaptação está em rumo para alguma direção, qual direção está indo? \\n\\n“Tudo depende de cada um por si vivendo para todos!”\\n\\n“Odeio pessoas inteligentes, até porque, aqueles que realmente são inteligentes não estão preocupados em ser.”\\n\\n Estou dentro do meu carro e leio: olimpíadas de matemática. \\n\\nPara que serve a matemática?\\n\\nHoje em dia para que usamos a matemática?\\n\\nQuantas formas usamos a matemática que aprendemos na escola? \\n\\nUma inteligência artificial dê um computador quântico, reduziu 100 mil teorias quânticas em 4, por qual motivo conseguiu chegar a essa redução? \\n\\n",
      "position": 112725,
      "chapter": 5,
      "page": 79,
      "segment_type": "preserved_segment",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 29.01616766467066,
      "complexity_metrics": {
        "word_count": 167,
        "sentence_count": 10,
        "paragraph_count": 10,
        "avg_sentence_length": 16.7,
        "avg_word_length": 5.053892215568863,
        "unique_word_ratio": 0.6526946107784432,
        "avg_paragraph_length": 16.7,
        "punctuation_density": 0.12574850299401197,
        "line_break_count": 20,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "aqueles",
          "temos",
          "amigos",
          "matemática",
          "estão",
          "todos",
          "ladrões",
          "está",
          "direção",
          "qual",
          "inteligentes",
          "usamos",
          "poder",
          "semelhantes",
          "àqueles",
          "nosso",
          "lado",
          "viraram",
          "eram",
          "corruptos"
        ],
        "entities": [
          [
            "Temos",
            "PERSON"
          ],
          [
            "vão se dar bem",
            "PERSON"
          ],
          [
            "dia",
            "ORG"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "Odeio",
            "GPE"
          ],
          [
            "Estou",
            "GPE"
          ],
          [
            "olimpíadas de matemática",
            "ORG"
          ],
          [
            "dia",
            "ORG"
          ],
          [
            "que",
            "CARDINAL"
          ],
          [
            "Quantas",
            "GPE"
          ]
        ],
        "readability_score": 90.13383233532934,
        "semantic_density": 0,
        "word_count": 167,
        "unique_words": 109,
        "lexical_diversity": 0.6526946107784432
      },
      "preservation_score": 0.00024730748303938545
    },
    {
      "id": 117,
      "text": "Uma inteligência artificial aprende a solucionar os erros através do próprio erro.\\n\\nComo assim: nós humanos vivemos e aprendemos a aprimorar através de praticar e alguns já vieram com uma pré disposição para o aprendizado são esses que conseguem ter mais facilidades em se aprimorar, lembrando que: A vida é um tempo contínuo e esse fator é determinante para nós aprimorarmos em algo. Quantas vezes erramos para executar com excelência?\\n\\nA inteligência artificial trabalha da mesma forma no mundo virtual. \\n\\nNós somos semelhante a um processador, alguns contém algumas respostas mais rápida, outros contém soluções mais rápidas e outros correlacionam o sentimento da vida com mais facilidade.\\n\\nTemos situações que se tornam exagerada pelo próprio pânico provinda da procrastinação junto a depressão de ser bom para alguns e ruim para a Terra pelo viver preguiçoso. \\n\\nAqueles que matam e fazem mal para a vida humana, não fazem tudo de mal para o planeta Terra.",
      "position": 113751,
      "chapter": 5,
      "page": 80,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 27.558441558441558,
      "complexity_metrics": {
        "word_count": 154,
        "sentence_count": 7,
        "paragraph_count": 6,
        "avg_sentence_length": 22.0,
        "avg_word_length": 5.194805194805195,
        "unique_word_ratio": 0.6883116883116883,
        "avg_paragraph_length": 25.666666666666668,
        "punctuation_density": 0.08441558441558442,
        "line_break_count": 10,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "mais",
          "alguns",
          "vida",
          "inteligência",
          "artificial",
          "através",
          "próprio",
          "aprimorar",
          "contém",
          "outros",
          "pelo",
          "terra",
          "fazem",
          "aprende",
          "solucionar",
          "erros",
          "erro",
          "como",
          "assim",
          "humanos"
        ],
        "entities": [
          [
            "nós humanos vivemos",
            "ORG"
          ],
          [
            "já vieram",
            "PERSON"
          ],
          [
            "aprendizado",
            "GPE"
          ],
          [
            "para nós aprimorarmos",
            "PERSON"
          ],
          [
            "Quantas",
            "GPE"
          ],
          [
            "vezes erramos",
            "PERSON"
          ],
          [
            "para executar",
            "PERSON"
          ],
          [
            "excelência",
            "PERSON"
          ],
          [
            "processador",
            "GPE"
          ],
          [
            "contém algumas respostas mais rápida",
            "ORG"
          ]
        ],
        "readability_score": 87.44155844155844,
        "semantic_density": 0,
        "word_count": 154,
        "unique_words": 106,
        "lexical_diversity": 0.6883116883116883
      },
      "preservation_score": 2.6067545509556844e-05
    },
    {
      "id": 118,
      "text": " Devido a esse fator ocorrer, só podemos aceitar quando o mesmo vêm provindo de um benefício futuro em que a perda se tornou maior que a vida.\\n\\nExemplos: um processador (mente) ruim com muito espaço para armazenamento, quanto tempo leva para abrir uma foto, música, filme, programas, jogos e etecetera?\\n\\nUm processador bom com pouco espaço para armazenamento, quanto tempo leva para abrir uma foto, música e etecetera?\\n\\nUm processador bom ou ruim, com muito armazenamento, quanto tempo leva para ele abrir uma imagem, música e etecetera? \\n\\nNós humanos não temos manual de instruções, logo o nosso processador não sendo educado, direcionado e ensinado a trabalhar, como ele irá trabalhar com o sentir?\\n\\nDo que adianta sermos inteligentes sem saber a direção?\\n\\nDo que adianta sermos inteligentes se não sabemos viver?\\n\\nDo que adianta sermos inteligentes indo em uma direção errada? \\n\\nDo que adianta sermos inteligentes para cálculo se não somos inteligentes com o nosso sentimento?\\n\\n",
      "position": 114711,
      "chapter": 5,
      "page": 81,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 23.851923076923075,
      "complexity_metrics": {
        "word_count": 156,
        "sentence_count": 9,
        "paragraph_count": 9,
        "avg_sentence_length": 17.333333333333332,
        "avg_word_length": 5.211538461538462,
        "unique_word_ratio": 0.5448717948717948,
        "avg_paragraph_length": 17.333333333333332,
        "punctuation_density": 0.15384615384615385,
        "line_break_count": 18,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "inteligentes",
          "processador",
          "adianta",
          "sermos",
          "armazenamento",
          "quanto",
          "tempo",
          "leva",
          "abrir",
          "música",
          "etecetera",
          "ruim",
          "muito",
          "espaço",
          "foto",
          "nosso",
          "trabalhar",
          "direção",
          "devido",
          "esse"
        ],
        "entities": [
          [
            "Devido",
            "PERSON"
          ],
          [
            "quando o",
            "PERSON"
          ],
          [
            "mesmo",
            "ORG"
          ],
          [
            "Exemplos",
            "PERSON"
          ],
          [
            "muito espaço para armazenamento",
            "PERSON"
          ],
          [
            "quanto tempo",
            "PERSON"
          ],
          [
            "leva para",
            "ORG"
          ],
          [
            "música",
            "GPE"
          ],
          [
            "jogos",
            "GPE"
          ],
          [
            "pouco espaço para armazenamento",
            "PERSON"
          ]
        ],
        "readability_score": 89.76987179487179,
        "semantic_density": 0,
        "word_count": 156,
        "unique_words": 85,
        "lexical_diversity": 0.5448717948717948
      },
      "preservation_score": 0.00014076474575160696
    },
    {
      "id": 119,
      "text": "“Ninguém é melhor que ninguém e para enxergamos essa condição, basta olharmos em outro ângulo.” \\n\\nAssim como o inteligente não têm sagacidade em várias coisas que os menos inteligentes e com menos informações teve sabedoria em ver e viver, por não estar em foco, e essa percepção, o inteligente que aprofundou e se afogou em tanto estudo, ficou muito próximo da inteligência e passou sem ver, sem admirar e sem sentir.\\n\\nPiada de Deus vinda dê um ateu:\\n\\nUm barco afundou no meio do oceano, porém um rapaz de muita fé e incrédulo que o mundo possa lhe trazer coisas boas, está se afogando em alto mar.\\n\\nVarão – Deus me ajude, estou no meio desse oceano e não sei o que fazer, quero ver meus filhos, minha esposa, abraçar, beijar e tudo aquilo que eu esqueci de fazer pois não percebi, estava sempre te pedindo a solução dos meus problemas, sendo direcionado, porém a cegueira causada através das minhas certezas não me deixavam perceber e sentir, mesmo assim, hoje, percebo o meu erro e peço perdão por não ter dado valor. Me salva, por favor!\\n\\n",
      "position": 115692,
      "chapter": 5,
      "page": 82,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 35.07258064516129,
      "complexity_metrics": {
        "word_count": 186,
        "sentence_count": 5,
        "paragraph_count": 5,
        "avg_sentence_length": 37.2,
        "avg_word_length": 4.575268817204301,
        "unique_word_ratio": 0.7311827956989247,
        "avg_paragraph_length": 37.2,
        "punctuation_density": 0.13978494623655913,
        "line_break_count": 10,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "ninguém",
          "essa",
          "assim",
          "inteligente",
          "coisas",
          "menos",
          "sentir",
          "deus",
          "meio",
          "oceano",
          "porém",
          "fazer",
          "meus",
          "melhor",
          "enxergamos",
          "condição",
          "basta",
          "olharmos",
          "outro",
          "ângulo"
        ],
        "entities": [
          [
            "Ninguém",
            "ORG"
          ],
          [
            "para enxergamos",
            "PERSON"
          ],
          [
            "essa condição",
            "PERSON"
          ],
          [
            "basta",
            "NORP"
          ],
          [
            "Assim",
            "NORP"
          ],
          [
            "afogou em",
            "ORG"
          ],
          [
            "tanto",
            "GPE"
          ],
          [
            "muito próximo da inteligência",
            "PERSON"
          ],
          [
            "Piada de Deus",
            "PERSON"
          ],
          [
            "Varão",
            "PERSON"
          ]
        ],
        "readability_score": 80.02741935483871,
        "semantic_density": 0,
        "word_count": 186,
        "unique_words": 136,
        "lexical_diversity": 0.7311827956989247
      },
      "preservation_score": 4.6787902196640486e-05
    },
    {
      "id": 120,
      "text": "Passou um barco perguntando: moço precisa de ajuda?\\n\\nNão preciso, Deus me salvará. A minha fé é forte, sei que ele fará algo maior e melhor.\\n\\nVeio outro barco maior e melhor, porém a mesma resposta foi dada. \\n\\nVeio um iate oferecendo maçã, pão e vinho...\\n\\nVarão – O luxo não entra no reino dos céus.\\n\\nEsse iate foi conquistado através da luxúria e da ganância, imagina quantos lares familiares foram destruídos só pela necessidade de suprir os seus desejos?\\n\\nMorreu!!!\\n\\nChegou ao local onde seria avaliando e com toda a sua fé arrogante e com toda a sua certeza, perguntou para um anjo: \\n\\nDeus vai vir me atender, eu fui um servo de Deus como ele me mandou ser.\\n\\nAnjo – Como Deus pediu para você ser? \\n\\nVarão – Amar ao próximo como a si mesmo. Eu amei. \\n\\nAnjo - Veja só, o que precisamos ser e ter para amar ao próximo? Não devam nada a ninguém, a não ser o amor de uns pelos outros, pois aquele que ama seu próximo tem cumprido a Lei. Cada um de nós deve agradar ao seu próximo para o bem dele, a fim de edificá-lo. Seja constante o amor fraternal. \\n\\n",
      "position": 116735,
      "chapter": 5,
      "page": 83,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 22.47905150753769,
      "complexity_metrics": {
        "word_count": 199,
        "sentence_count": 16,
        "paragraph_count": 12,
        "avg_sentence_length": 12.4375,
        "avg_word_length": 4.201005025125628,
        "unique_word_ratio": 0.6934673366834171,
        "avg_paragraph_length": 16.583333333333332,
        "punctuation_density": 0.1658291457286432,
        "line_break_count": 24,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "deus",
          "próximo",
          "anjo",
          "como",
          "barco",
          "maior",
          "melhor",
          "veio",
          "iate",
          "varão",
          "toda",
          "amar",
          "amor",
          "passou",
          "perguntando",
          "moço",
          "precisa",
          "ajuda",
          "preciso",
          "salvará"
        ],
        "entities": [
          [
            "precisa de ajuda",
            "PERSON"
          ],
          [
            "Deus",
            "PERSON"
          ],
          [
            "Veio",
            "PERSON"
          ],
          [
            "Veio",
            "PERSON"
          ],
          [
            "Varão",
            "PERSON"
          ],
          [
            "imagina quantos",
            "PERSON"
          ],
          [
            "Deus",
            "PERSON"
          ],
          [
            "eu fui",
            "PERSON"
          ],
          [
            "de Deus",
            "PERSON"
          ],
          [
            "Como Deus",
            "PERSON"
          ]
        ],
        "readability_score": 92.52094849246231,
        "semantic_density": 0,
        "word_count": 199,
        "unique_words": 138,
        "lexical_diversity": 0.6934673366834171
      },
      "preservation_score": 0.00033687289581581145
    },
    {
      "id": 121,
      "text": "Como amou ao próximo se mesmo antes de morrer não enxergou o respeito? \\n\\nDentro de todas as leis de Deus o amar ao próximo é sagrado. Abraçar, beijar, educar, direcionar, confiar e tudo aquilo que todos nós somos “Amados, amemos uns aos outros, pois o amor procede de Deus.” Assim como o amor surge de Deus, quem somos nós para julgar quem devemos amar se não enxergamos o que provém das bênçãos do destino?\\n\\nAssim o veredito parou no inferno. \\n\\nNão adianta vivermos e não entendermos os sinais que o universo nós ensina e direciona, até porque, o sentir os nossos erros é contra o instinto humano da própria evolução, pois nós humanos queremos ser ou ter mais que o próximo, e isso, provém em pensar que Deus nós escolheu em ter uma vida melhor que de outros.\\n\\n“Desisto de pegar a onda onde todos estão indo.”\\n\\nTodas as ondas que eu escuto e vejo, são ondas onde a hipocrisia é dominante, essa dominação não provém de outros, e sim, de si próprio.\\n\\n",
      "position": 117787,
      "chapter": 5,
      "page": 84,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 27.271026011560693,
      "complexity_metrics": {
        "word_count": 173,
        "sentence_count": 8,
        "paragraph_count": 6,
        "avg_sentence_length": 21.625,
        "avg_word_length": 4.445086705202312,
        "unique_word_ratio": 0.6647398843930635,
        "avg_paragraph_length": 28.833333333333332,
        "punctuation_density": 0.13872832369942195,
        "line_break_count": 12,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "deus",
          "próximo",
          "outros",
          "provém",
          "como",
          "todas",
          "amar",
          "todos",
          "somos",
          "pois",
          "amor",
          "assim",
          "quem",
          "onde",
          "ondas",
          "amou",
          "mesmo",
          "antes",
          "morrer",
          "enxergou"
        ],
        "entities": [
          [
            "mesmo",
            "ORG"
          ],
          [
            "de morrer não enxergou o respeito",
            "PERSON"
          ],
          [
            "leis de Deus",
            "PERSON"
          ],
          [
            "Abraçar",
            "ORG"
          ],
          [
            "beijar",
            "ORG"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "aos outros",
            "PERSON"
          ],
          [
            "procede de Deus",
            "PERSON"
          ],
          [
            "de Deus",
            "PERSON"
          ],
          [
            "quem somos nós",
            "ORG"
          ]
        ],
        "readability_score": 87.85397398843931,
        "semantic_density": 0,
        "word_count": 173,
        "unique_words": 115,
        "lexical_diversity": 0.6647398843930635
      },
      "preservation_score": 6.73745791631623e-05
    },
    {
      "id": 122,
      "text": "Temos imaginações e soluções criativas em grande escala para soluções que vão nós levar para um labirinto sem saída, nós deixando encurralados por nós mesmos, pois alguns estão indo para uma direção onde todos já estão travado, já outros, preferem burlar o labirinto e cavar em meio ao trajeto e prejudicando alguns que tentam ir pelo mesmo caminho estreito e perigoso, porém, não estão conseguindo enxergar o trajeto anterior, e isso, provém do fluxo ser muito grande para passar por aquele pequeno buraco, com o tempo, vira um rombo sem controle, assim eu vejo que nada adianta falar, discutir, debater, conversar, brigar e tudo que possa ir contra um fluxo de maior gravidade pela bondade ou pela cegueira. Não preciso falar sobre todos esses erros de percursos são cansativos e exaustivos, até porque, estamos brigando contra um sistema que já tiveram muitos rombos no labirinto, e talvez, esses rombos estão tão grande, que criamos barreiras em todo nosso entorno que nós deixaram cegos diante d",
      "position": 118737,
      "chapter": 5,
      "page": 85,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 38.519999999999996,
      "complexity_metrics": {
        "word_count": 165,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 82.5,
        "avg_word_length": 5.066666666666666,
        "unique_word_ratio": 0.7212121212121212,
        "avg_paragraph_length": 165.0,
        "punctuation_density": 0.12727272727272726,
        "line_break_count": 0,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "estão",
          "grande",
          "labirinto",
          "soluções",
          "alguns",
          "todos",
          "trajeto",
          "fluxo",
          "falar",
          "contra",
          "pela",
          "esses",
          "rombos",
          "temos",
          "imaginações",
          "criativas",
          "escala",
          "levar",
          "saída",
          "deixando"
        ],
        "entities": [
          [
            "todos",
            "CARDINAL"
          ],
          [
            "já estão travado",
            "PERSON"
          ],
          [
            "já outros",
            "PERSON"
          ],
          [
            "preferem burlar",
            "PERSON"
          ],
          [
            "que tentam ir pelo mesmo",
            "PERSON"
          ],
          [
            "fluxo",
            "CARDINAL"
          ],
          [
            "buraco",
            "GPE"
          ],
          [
            "assim eu",
            "PERSON"
          ],
          [
            "vejo",
            "GPE"
          ],
          [
            "nada",
            "GPE"
          ]
        ],
        "readability_score": 57.23,
        "semantic_density": 0,
        "word_count": 165,
        "unique_words": 119,
        "lexical_diversity": 0.7212121212121212
      },
      "preservation_score": 0.0
    },
    {
      "id": 123,
      "text": "a nossa própria casinha ilusória, cheias de imaginações férteis e inteligentes para mim, pois para outro não importa, pois é mais fácil construir um castelo que me importar com todos.\\n\\nHoje, vejo que prefiro opinar e falar dando uma solução sem argumentos, até porque, se tiver argumentos a serem gerados, esperamos que o mesmo, faça valer apena eu estar no meu espaço tempo naquele momento.\\n\\nMeus movimentos corpóreos e mentais nem sempre vão ter a mesma paciência e a mesma gentileza com certas situações, logo, o perceber isso, torna-se mais fácil de viver em harmonia, não podendo ser paz, até porque, para se ter paz é necessário todo o nosso mundo próprio, estar em paz!!!\\n\\nA vida é um paradoxo. \\n\\nQueremos a perfeição onde será a nossa destruição!\\n\\n“Tudo deve estar, onde precisa estar, pois independente o tempo vai passar.”\\n\\nAqueles que são contra ideologia de gênero, torço para que tenha um filho(a) gay e que ele seja um humano fora de sério.\\n\\n",
      "position": 119737,
      "chapter": 5,
      "page": 86,
      "segment_type": "preserved_segment",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 28.159070990359332,
      "complexity_metrics": {
        "word_count": 163,
        "sentence_count": 7,
        "paragraph_count": 7,
        "avg_sentence_length": 23.285714285714285,
        "avg_word_length": 4.815950920245399,
        "unique_word_ratio": 0.7239263803680982,
        "avg_paragraph_length": 23.285714285714285,
        "punctuation_density": 0.1656441717791411,
        "line_break_count": 14,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "pois",
          "nossa",
          "mais",
          "fácil",
          "argumentos",
          "porque",
          "tempo",
          "mesma",
          "onde",
          "própria",
          "casinha",
          "ilusória",
          "cheias",
          "imaginações",
          "férteis",
          "inteligentes",
          "outro",
          "importa",
          "construir",
          "castelo"
        ],
        "entities": [
          [
            "para mim",
            "PERSON"
          ],
          [
            "para outro",
            "PERSON"
          ],
          [
            "importa",
            "GPE"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "Hoje",
            "PERSON"
          ],
          [
            "vejo que",
            "GPE"
          ],
          [
            "mesmo",
            "ORG"
          ],
          [
            "valer apena eu estar",
            "PERSON"
          ],
          [
            "Meus",
            "PERSON"
          ],
          [
            "mentais nem sempre",
            "PERSON"
          ]
        ],
        "readability_score": 86.91235758106924,
        "semantic_density": 0,
        "word_count": 163,
        "unique_words": 118,
        "lexical_diversity": 0.7239263803680982
      },
      "preservation_score": 0.00010480490092047472
    },
    {
      "id": 124,
      "text": "Aqueles que são contra aborto, não torço para sua filha(0) sofra estupro e muito menos tenha um filho de 12, 13 anos que tenha um filho. \\n\\nAs mulheres que transaram por diversão e engravidar, torço para que o pai assuma a responsabilidade.\\n\\nAqueles que são contra as drogas, torço para que nunca fique doente, forte, gordo, magro, depressão, ansiedade, vida pacata e todas aquelas fugas necessárias para aqueles que trabalham e usam drogas pela necessidade de ter alegrias e felicidades.\\n\\nTodos que são contra um outro humano sem saber o motivo, torço que viva todas as coisas necessárias para aprender a respeitar, admirar, reconhecer, entender, compreender e não se meter nos erros ou no acerto, tudo é relativo, logo ninguém sabe o que é bom para mim, assim como eu não sei o que possa ser bom para você.\\n\\nO universo faz todo o trabalho difícil e nós só temos que viver em harmonia um para com o outro, e essa situação é tão fácil, que a facilidade não é digna de confiança, ninguém da nada de graça, muito menos um bom conselho.\\n\\n",
      "position": 120693,
      "chapter": 5,
      "page": 87,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 34.68524590163935,
      "complexity_metrics": {
        "word_count": 183,
        "sentence_count": 5,
        "paragraph_count": 5,
        "avg_sentence_length": 36.6,
        "avg_word_length": 4.617486338797814,
        "unique_word_ratio": 0.6557377049180327,
        "avg_paragraph_length": 36.6,
        "punctuation_density": 0.14754098360655737,
        "line_break_count": 10,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "torço",
          "aqueles",
          "contra",
          "muito",
          "menos",
          "tenha",
          "filho",
          "drogas",
          "todas",
          "necessárias",
          "outro",
          "ninguém",
          "aborto",
          "filha",
          "sofra",
          "estupro",
          "anos",
          "mulheres",
          "transaram",
          "diversão"
        ],
        "entities": [
          [
            "não torço para sua filha(0",
            "ORG"
          ],
          [
            "muito menos",
            "PERSON"
          ],
          [
            "12",
            "CARDINAL"
          ],
          [
            "13",
            "CARDINAL"
          ],
          [
            "torço",
            "ORG"
          ],
          [
            "contra",
            "NORP"
          ],
          [
            "drogas",
            "GPE"
          ],
          [
            "torço",
            "ORG"
          ],
          [
            "magro",
            "GPE"
          ],
          [
            "depressão",
            "GPE"
          ]
        ],
        "readability_score": 80.31475409836065,
        "semantic_density": 0,
        "word_count": 183,
        "unique_words": 120,
        "lexical_diversity": 0.6557377049180327
      },
      "preservation_score": 4.845889870366336e-05
    },
    {
      "id": 125,
      "text": "Afinal, nascemos sabendo tudo sobre o certo a se fazer e tudo de errado a se fazer, não por saber e sim por não querer sentir.\\n\\nNós somos tão egoísta um para com o outro que não enxergamos o amor quando contém, com isso o interpretar fica turvo e embasado dando destaque ao ódio, que quando deixamos de ter, “viramos psicopatas pela falta de sentir ou ter empatia pelo sentir o próprio viver, assim, o viver deixou de ser sentindo e sim interpretado as vezes pelo o excesso de estudo, vivência ou os dois, não por ser mais belo e melhor, e sim por ser mais fácil o acesso em estar familiarizado.\\n\\nNão adianta falar, falar, falar e falar, pois aquele que fala é a razão de tudo e de todos, já os que não falam, são errados por não agir, mesmo assim, falamos um para com o outro e de nada importa falar pois o que entra em um ouvido, sai pelo o outro e quando não sai, fica presa aos nossos sentimentos e naquelas histerias que ficam fora de controle, e isso, provém do incomodo causado devido aos exce",
      "position": 121727,
      "chapter": 5,
      "page": 88,
      "segment_type": "preserved_segment",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 36.26910994764398,
      "complexity_metrics": {
        "word_count": 191,
        "sentence_count": 3,
        "paragraph_count": 3,
        "avg_sentence_length": 63.666666666666664,
        "avg_word_length": 4.230366492146596,
        "unique_word_ratio": 0.6020942408376964,
        "avg_paragraph_length": 63.666666666666664,
        "punctuation_density": 0.12041884816753927,
        "line_break_count": 4,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "falar",
          "tudo",
          "sentir",
          "outro",
          "quando",
          "pelo",
          "fazer",
          "isso",
          "fica",
          "viver",
          "assim",
          "mais",
          "pois",
          "afinal",
          "nascemos",
          "sabendo",
          "certo",
          "errado",
          "saber",
          "querer"
        ],
        "entities": [
          [
            "nascemos sabendo",
            "GPE"
          ],
          [
            "Nós",
            "ORG"
          ],
          [
            "tão",
            "ORG"
          ],
          [
            "não enxergamos",
            "ORG"
          ],
          [
            "amor quando contém",
            "PERSON"
          ],
          [
            "interpretar fica",
            "ORG"
          ],
          [
            "que quando deixamos de ter",
            "PERSON"
          ],
          [
            "viramos psicopatas",
            "PERSON"
          ],
          [
            "falta de",
            "ORG"
          ],
          [
            "pelo",
            "PERSON"
          ]
        ],
        "readability_score": 66.89755671902269,
        "semantic_density": 0,
        "word_count": 191,
        "unique_words": 115,
        "lexical_diversity": 0.6020942408376964
      },
      "preservation_score": 9.624939880451758e-06
    },
    {
      "id": 126,
      "text": "ssos de barulhos ou estrondos mentais de quando falamos, até porque, temos tantas pessoas que vivem no pânico sentindo e imaginário que o assimilar qualquer som é sinônimo de histeria e medo.\\n\\n“À própria estrada que construímos é a mesma que iremos passar.”\\n\\nA vida são ciclos ajustáveis e adaptáveis e tudo que coexiste contém caos e amor, ambos em escala necessária de ação e reação proporcional ao valor.\\n\\nToda a nossa estrada colocamos nomes nos buracos, nas curvas, na escuridão semelhante a um buraco negro que regula galáxia, onde o mesmo: o lado mental é o epicentro e os corpos que habitam no entorno é o corpo.  A dificuldade é relativa ao nosso pensar e agir, assim como uns falam pipa e outros papagaio assim funciona para física, química, filosofia, religião, favela, classe social e tudo que contém confiança no meio em que vivemos, só mudando a forma e as palavras usadas, até porque, todos são ciclos e tem formas de interpretações diferentes com um final igual para todos.\\n\\n",
      "position": 122727,
      "chapter": 5,
      "page": 89,
      "segment_type": "preserved_segment",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 33.540000000000006,
      "complexity_metrics": {
        "word_count": 170,
        "sentence_count": 5,
        "paragraph_count": 4,
        "avg_sentence_length": 34.0,
        "avg_word_length": 4.8,
        "unique_word_ratio": 0.711764705882353,
        "avg_paragraph_length": 42.5,
        "punctuation_density": 0.12352941176470589,
        "line_break_count": 8,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "porque",
          "estrada",
          "ciclos",
          "tudo",
          "contém",
          "assim",
          "todos",
          "ssos",
          "barulhos",
          "estrondos",
          "mentais",
          "quando",
          "falamos",
          "temos",
          "tantas",
          "pessoas",
          "vivem",
          "pânico",
          "sentindo",
          "imaginário"
        ],
        "entities": [
          [
            "ssos de barulhos",
            "ORG"
          ],
          [
            "mentais de quando falamos",
            "ORG"
          ],
          [
            "própria estrada que construímos",
            "ORG"
          ],
          [
            "nas curvas",
            "PERSON"
          ],
          [
            "buraco",
            "NORP"
          ],
          [
            "falam",
            "GPE"
          ],
          [
            "outros papagaio",
            "ORG"
          ],
          [
            "funciona",
            "GPE"
          ],
          [
            "para física",
            "PERSON"
          ],
          [
            "química",
            "GPE"
          ]
        ],
        "readability_score": 81.56,
        "semantic_density": 0,
        "word_count": 170,
        "unique_words": 121,
        "lexical_diversity": 0.711764705882353
      },
      "preservation_score": 2.459706858337672e-05
    },
    {
      "id": 127,
      "text": "Nossos preconceitos só existem por nosso pensar ser incoerente com o outro, porém, o viver a vida nos mesmos ciclos e ter sentimentos semelhantes, me fizeram perceber que a maior alteração entre as classes sociais é o conforto do bem estar corpóreo e não mental, e são esses atributos egoístas e medíocres que a grande maioria enxergam a empatia e o amor no outro.\\n\\n“Meu único problema é sobreviver aos meus próprios pensamentos.”\\n\\nCapítulo 9\\n\\nAfinal, somos nós ou eu?\\n\\n  “Sempre pensamos que estamos pensando em coletivo, mas na verdade, o nosso pensamento é só meu.”\\n\\n   Tudo e todos vêm de uma origem de assimilar os traumas e as histerias e o que seriam?\\n\\n   Nossos traumas ou histeria, ambos são relativos e originários de feridas, machucados, pancadas, golpes e deixa cicatrizes ou queloides e por muitas vezes deixam lacunas ou fragmentos vinda com insights do próprio pensamento que nós mesmos criamos rupturas, rompimentos, fraturas, fraturas expostas e tudo que possa vir ser um incômodo qu",
      "position": 123718,
      "chapter": 5,
      "page": 90,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 32.41121212121212,
      "complexity_metrics": {
        "word_count": 165,
        "sentence_count": 6,
        "paragraph_count": 7,
        "avg_sentence_length": 27.5,
        "avg_word_length": 4.9818181818181815,
        "unique_word_ratio": 0.7333333333333333,
        "avg_paragraph_length": 23.571428571428573,
        "punctuation_density": 0.11515151515151516,
        "line_break_count": 12,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "nossos",
          "nosso",
          "outro",
          "mesmos",
          "pensamento",
          "tudo",
          "traumas",
          "fraturas",
          "preconceitos",
          "existem",
          "pensar",
          "incoerente",
          "porém",
          "viver",
          "vida",
          "ciclos",
          "sentimentos",
          "semelhantes",
          "fizeram",
          "perceber"
        ],
        "entities": [
          [
            "mesmos ciclos",
            "PERSON"
          ],
          [
            "fizeram",
            "ORG"
          ],
          [
            "estar",
            "PRODUCT"
          ],
          [
            "Sempre",
            "ORG"
          ],
          [
            "pensando",
            "GPE"
          ],
          [
            "seriam",
            "PERSON"
          ],
          [
            "histeria",
            "GPE"
          ],
          [
            "de feridas",
            "PERSON"
          ],
          [
            "mesmos criamos",
            "PERSON"
          ],
          [
            "fraturas expostas e tudo",
            "ORG"
          ]
        ],
        "readability_score": 84.75545454545454,
        "semantic_density": 0,
        "word_count": 165,
        "unique_words": 121,
        "lexical_diversity": 0.7333333333333333
      },
      "preservation_score": 6.456730503136388e-05
    },
    {
      "id": 128,
      "text": "e possa vir causar felicidades ou tristezas, tudo dependendo de como percebemos o nosso próprio destino e denominamos as palavras e os sentimentos, assim como o universo contém uma ordem e têm um espaço tempo para adaptar-se aos seus próprios problemas, nós somos semelhantes com bem menos problemas que o universo.\\n\\n“Meu único problema é sobreviver aos pensamentos.”\\n\\nO universo faz todo o trabalho que vejamos como impossível ser feito e nós só precisávamos viver em harmonia um para com o outro, talvez essa situação seja tão fácil, que a facilidade e a nossa visão ficam destoadas pela falta de confiança em termos algo de graça e estarmos próximos, até porque, ninguém dá nada de graça muito menos conselhos, amor e notícia ruim chega rápido.\\n\\nOs nossos erros vieram derivados do tédio, logo o nosso tempo é muito curto para ficarmos entediados e querermos chegar à perfeição e o mesmo está no início, meio ou final, não sabemos quanto tempo irá demorar.",
      "position": 124718,
      "chapter": 5,
      "page": 91,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.47222222222222,
      "complexity_metrics": {
        "word_count": 162,
        "sentence_count": 4,
        "paragraph_count": 4,
        "avg_sentence_length": 40.5,
        "avg_word_length": 4.907407407407407,
        "unique_word_ratio": 0.7592592592592593,
        "avg_paragraph_length": 40.5,
        "punctuation_density": 0.09259259259259259,
        "line_break_count": 6,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "como",
          "universo",
          "tempo",
          "nosso",
          "problemas",
          "menos",
          "graça",
          "muito",
          "possa",
          "causar",
          "felicidades",
          "tristezas",
          "tudo",
          "dependendo",
          "percebemos",
          "próprio",
          "destino",
          "denominamos",
          "palavras",
          "sentimentos"
        ],
        "entities": [
          [
            "dependendo de como percebemos",
            "ORG"
          ],
          [
            "universo contém",
            "PERSON"
          ],
          [
            "para adaptar",
            "PERSON"
          ],
          [
            "nós somos",
            "GPE"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "talvez essa situação",
            "ORG"
          ],
          [
            "visão ficam",
            "ORG"
          ],
          [
            "falta de confiança em termos algo de",
            "ORG"
          ],
          [
            "nada de graça",
            "ORG"
          ],
          [
            "muito menos",
            "PERSON"
          ]
        ],
        "readability_score": 78.27777777777777,
        "semantic_density": 0,
        "word_count": 162,
        "unique_words": 123,
        "lexical_diversity": 0.7592592592592593
      },
      "preservation_score": 1.4437409820677639e-05
    },
    {
      "id": 129,
      "text": " O trajeto que achamos tedioso é o mesmo que quando piscamos, dançamos e perdemos o tempo que para nós, passa muito mais rápido se compararmos o nosso tempo de vida com outras vidas, seja ela de uma árvore ou até mesmo de um papagaio e quando abrimos os olhos ao terminar de piscar, já estamos na hora de descansar para sempre e os que percebem o passar rápido, querem dominar o mundo ao decorrer do trajeto sem parar nem para cuspir, e esse passar, nos faz querer viver intensamente sem enxergar o contexto da vida, e o engraçado que essa é a graça da via, até porque, se todos nós fossemos iguais ao universo seríamos felizes e não teríamos remorsos, paixão, sexo, competição, guerras, empatia, brigas e tudo que precisa existir para se ter vida.\\n\\nO que será esse trajeto, quais são as estradas e para onde vão as estradas?\\n\\nComo construímos essas estradas?\\n\\nPegamos algumas estradas com várias paisagens, algumas bonitas e outras feias, àquela que nós acolhe e aquelas que nós dá medo, e isso, depende da nossa própria tensão em traçar a rota, porém qual seria essa rota?\\n\\n",
      "position": 125677,
      "chapter": 5,
      "page": 92,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.38219895287958,
      "complexity_metrics": {
        "word_count": 191,
        "sentence_count": 4,
        "paragraph_count": 4,
        "avg_sentence_length": 47.75,
        "avg_word_length": 4.607329842931938,
        "unique_word_ratio": 0.6963350785340314,
        "avg_paragraph_length": 47.75,
        "punctuation_density": 0.13612565445026178,
        "line_break_count": 8,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "estradas",
          "trajeto",
          "vida",
          "mesmo",
          "quando",
          "tempo",
          "rápido",
          "outras",
          "passar",
          "esse",
          "essa",
          "algumas",
          "rota",
          "achamos",
          "tedioso",
          "piscamos",
          "dançamos",
          "perdemos",
          "passa",
          "muito"
        ],
        "entities": [
          [
            "mesmo",
            "ORG"
          ],
          [
            "quando piscamos",
            "PERSON"
          ],
          [
            "dançamos e perdemos",
            "PERSON"
          ],
          [
            "passa muito mais",
            "PERSON"
          ],
          [
            "se compararmos o",
            "PERSON"
          ],
          [
            "outras vidas",
            "PERSON"
          ],
          [
            "ela de uma árvore",
            "PERSON"
          ],
          [
            "quando abrimos",
            "PERSON"
          ],
          [
            "já estamos",
            "PERSON"
          ],
          [
            "hora de descansar para sempre e os",
            "PERSON"
          ]
        ],
        "readability_score": 74.74280104712042,
        "semantic_density": 0,
        "word_count": 191,
        "unique_words": 133,
        "lexical_diversity": 0.6963350785340314
      },
      "preservation_score": 2.780538187686064e-05
    },
    {
      "id": 130,
      "text": "Inicialmente pegamos em tudo que vemos e quando conseguimos alcançar e pegar, por instinto, tudo que pegamos pensamos que são alimentos para os nossos corpos que precisam sobreviver ao tempo, até porque, o espaço que está sendo comandado por outros espaços e tempo, são o mesmo espaço, e essa condição, torna-se relativo ao próprio espaço tempo vivido. Ao crescer, começamos a ter mais energia e aprender a movimentar-se melhor ou pior e quando começamos a perceber, já estamos em várias bifurcações de vários trajetos, e são esses, que nós direcionam a entender quais são os melhores espaços e tempo. Ao movimentar-se com mais agilidade e volume criamos mais combustíveis e energia para aprender a movimentar-se melhor ou pior, até porque, já tínhamos começado a viver em várias bifurcações de trajetos, e são esses, que nós direcionam quando precisamos entender o que é melhor para o meu espaço e tempo. \\n\\n",
      "position": 126753,
      "chapter": 5,
      "page": 93,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 35.11476510067114,
      "complexity_metrics": {
        "word_count": 149,
        "sentence_count": 3,
        "paragraph_count": 1,
        "avg_sentence_length": 49.666666666666664,
        "avg_word_length": 5.080536912751678,
        "unique_word_ratio": 0.5436241610738255,
        "avg_paragraph_length": 149.0,
        "punctuation_density": 0.12080536912751678,
        "line_break_count": 2,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "tempo",
          "espaço",
          "quando",
          "mais",
          "movimentar",
          "melhor",
          "pegamos",
          "tudo",
          "porque",
          "espaços",
          "começamos",
          "energia",
          "aprender",
          "pior",
          "várias",
          "bifurcações",
          "trajetos",
          "esses",
          "direcionam",
          "entender"
        ],
        "entities": [
          [
            "quando",
            "ORG"
          ],
          [
            "quando começamos",
            "PERSON"
          ],
          [
            "perceber",
            "GPE"
          ],
          [
            "já estamos",
            "PERSON"
          ],
          [
            "várias bifurcações de vários trajetos",
            "PERSON"
          ],
          [
            "para aprender",
            "PERSON"
          ],
          [
            "já tínhamos",
            "PERSON"
          ],
          [
            "quando precisamos",
            "PERSON"
          ]
        ],
        "readability_score": 73.64250559284116,
        "semantic_density": 0,
        "word_count": 149,
        "unique_words": 81,
        "lexical_diversity": 0.5436241610738255
      },
      "preservation_score": 1.47047692618013e-06
    },
    {
      "id": 131,
      "text": "Os nossos primeiros movimentos sem ninguém para nos direcionar são todos desastrados, honestos e engraçados, somos todos bonitinhos mesmo sendo feios e nessa “dificuldade” hipócrita e necessária, começamos a entender um mundo cheios de pensamentos relativos e com muitas incoerências comportamentais.\\n\\n“O ruim da vida não são as incoerências, e sim, como são direcionadas.”\\n\\n“Todos somos um vácuo até nascermos e após esse nascimento, o mesmo precisa ser direcionado para algum trajeto, até porque, não temos culpa de nascer e sim culpa ao viver. “\\n\\n“Quando começamos a nos acostumar com as rotatórias, começamos a entender a hora certa de entrar e sair.”\\n\\nAqueles pequenos desastres podem torna-se grande, ninguém nasce sabendo dirigir se nunca dirigiu um carro, barco, avião, nave, vida logo a prevenção de uma boa estrada é saber reparar ou observar onde estão os defeitos e os buracos, logo a prevenção dê uma boa dirigibilidade é se atentar aos padrões do trajeto e por muitas vezes esses desast",
      "position": 127661,
      "chapter": 5,
      "page": 94,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 32.85776397515528,
      "complexity_metrics": {
        "word_count": 161,
        "sentence_count": 5,
        "paragraph_count": 5,
        "avg_sentence_length": 32.2,
        "avg_word_length": 5.192546583850931,
        "unique_word_ratio": 0.7267080745341615,
        "avg_paragraph_length": 32.2,
        "punctuation_density": 0.11801242236024845,
        "line_break_count": 8,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "todos",
          "começamos",
          "ninguém",
          "somos",
          "mesmo",
          "entender",
          "muitas",
          "incoerências",
          "vida",
          "trajeto",
          "culpa",
          "logo",
          "prevenção",
          "nossos",
          "primeiros",
          "movimentos",
          "direcionar",
          "desastrados",
          "honestos",
          "engraçados"
        ],
        "entities": [
          [
            "todos",
            "NORP"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "vácuo até nascermos",
            "ORG"
          ],
          [
            "mesmo",
            "ORG"
          ],
          [
            "precisa ser",
            "PRODUCT"
          ],
          [
            "direcionado para algum",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "hora certa de entrar",
            "PERSON"
          ],
          [
            "sabendo",
            "GPE"
          ],
          [
            "barco",
            "ORG"
          ]
        ],
        "readability_score": 82.34223602484472,
        "semantic_density": 0,
        "word_count": 161,
        "unique_words": 117,
        "lexical_diversity": 0.7267080745341615
      },
      "preservation_score": 3.7430321757312396e-05
    },
    {
      "id": 132,
      "text": "res torna-se uma aventura prazerosa e com muita adrenalina, e o viver com essas emoções, são cansativas e exaustivas, até porque, necessitam de muita energia e não são todos os corpos que conseguem ter uma boa direção com muitas energias a serem controladas e com recursos necessários em seguir sem esforço e sem problemas, devido a esses pequenos desastres virarem necessidade para a vida.\\n\\nComeçamos a crescer dê uma forma ordenada e desordenada com muitas memórias e lembranças de todos os tipos, padrões e com muito sentimento sem ser seguido por não ser ensinado, retribuído e muito menos direcionados, assim ao começar a entendermos as palavras faladas e escutadas, começamos a ver estradas diferentes... Algumas parecendo um conto de fadas  em pele de cordeiro sendo lobo e outros entre sujos como porcos em lama e são lindos como flores, tudo sendo ouvido e absorvido de acordo com a minha própria histeria.\\n\\n",
      "position": 128661,
      "chapter": 5,
      "page": 95,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.5158940397351,
      "complexity_metrics": {
        "word_count": 151,
        "sentence_count": 3,
        "paragraph_count": 2,
        "avg_sentence_length": 50.333333333333336,
        "avg_word_length": 5.052980132450331,
        "unique_word_ratio": 0.695364238410596,
        "avg_paragraph_length": 75.5,
        "punctuation_density": 0.09933774834437085,
        "line_break_count": 4,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "muita",
          "todos",
          "muitas",
          "começamos",
          "muito",
          "sendo",
          "como",
          "torna",
          "aventura",
          "prazerosa",
          "adrenalina",
          "viver",
          "essas",
          "emoções",
          "cansativas",
          "exaustivas",
          "porque",
          "necessitam",
          "energia",
          "corpos"
        ],
        "entities": [
          [
            "uma aventura prazerosa e com",
            "ORG"
          ],
          [
            "muita adrenalina",
            "PERSON"
          ],
          [
            "necessitam de muita",
            "ORG"
          ],
          [
            "virarem necessidade",
            "PERSON"
          ],
          [
            "Começamos",
            "PERSON"
          ],
          [
            "desordenada",
            "GPE"
          ],
          [
            "muito sentimento sem",
            "PERSON"
          ],
          [
            "retribuído e muito menos",
            "ORG"
          ],
          [
            "faladas e escutadas",
            "ORG"
          ],
          [
            "Algumas",
            "PERSON"
          ]
        ],
        "readability_score": 73.31743929359823,
        "semantic_density": 0,
        "word_count": 151,
        "unique_words": 105,
        "lexical_diversity": 0.695364238410596
      },
      "preservation_score": 4.27775105797856e-06
    },
    {
      "id": 133,
      "text": "Essas palavras escritas até agora, vieram com um peso proporcional a minha própria criação, e isso, veio dê um próprio pesar do trajeto, como podemos usar palavras que fomos criados e ouvimos de uma forma sentimental a qual não é a certa para uma totalidade e sim territorial?\\n\\n“Quando começamos a admirar o ouvir, todas os sons torna-se interessante e logo ficamos atentos, porém ficamos confortáveis ao escutar o que nós dão aconchego.”\\n\\nQuando sentimos afinidades por uma voz ficamos confortáveis por quais motivos?\\n\\nUma voz com sotaque arretado da peste e outros abrindo a porteira para entrarmos com o galo cantando ao passar e perguntar onde estamos e escutamos um logo ali... Já outros pela beleza e a calmaria que para outros é chato de tão calmo e prefere os estrondos da vida nas metrópoles cheias de prazeres, adrenalina e vícios para sairmos de um tédio sem fim, e quando estamos chegando próximo do fim o tom de uma voz alta nós incômoda, uma música alta, nem se fala, ainda mais quando ",
      "position": 129578,
      "chapter": 5,
      "page": 96,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 33.82890173410404,
      "complexity_metrics": {
        "word_count": 173,
        "sentence_count": 5,
        "paragraph_count": 4,
        "avg_sentence_length": 34.6,
        "avg_word_length": 4.763005780346821,
        "unique_word_ratio": 0.6878612716763006,
        "avg_paragraph_length": 43.25,
        "punctuation_density": 0.09826589595375723,
        "line_break_count": 6,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "quando",
          "ficamos",
          "outros",
          "palavras",
          "logo",
          "confortáveis",
          "estamos",
          "alta",
          "essas",
          "escritas",
          "agora",
          "vieram",
          "peso",
          "proporcional",
          "minha",
          "própria",
          "criação",
          "isso",
          "veio",
          "próprio"
        ],
        "entities": [
          [
            "Essas",
            "GPE"
          ],
          [
            "escritas até agora",
            "ORG"
          ],
          [
            "como podemos usar",
            "ORG"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "porém ficamos confortáveis",
            "ORG"
          ],
          [
            "dão aconchego",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "voz ficamos confortáveis",
            "PERSON"
          ],
          [
            "motivos",
            "PERSON"
          ],
          [
            "Uma voz",
            "PERSON"
          ]
        ],
        "readability_score": 81.27109826589596,
        "semantic_density": 0,
        "word_count": 173,
        "unique_words": 119,
        "lexical_diversity": 0.6878612716763006
      },
      "preservation_score": 1.6041566467419597e-05
    },
    {
      "id": 134,
      "text": "não é da minha época onde as músicas realmente eram boas, continham muito sentimento e muitas formas de assimilar o ódio e amor na mesma relevância não importando a forma, e sim, como saber usar na hora e no momento certo que precisará e será de utilidade para a vida.\\n\\nNão sabendo usar as palavras com clareza, preguiça, não gostar, melhor ficar quieto, “do que” responder com frequência e quando responder, saiba usar dê uma forma mais sábia, até porque, uma boa conversa têm um final conclusivo e sem questionamentos dando continuidade apenas em evoluir, lembrando que só podemos da certeza aos nossos questionamentos correlacionando com outras certezas.\\n\\nNinguém sabe de tudo porém todos sabem sobre alguma coisa, até porque, o nada é alguma coisa, assim todos nós temos algo melhor ou pior proporcionalmente ao nosso destino, esforço, dedicação, vontade, amor e tudo que almejamos como grandeza para um contexto, onde os mesmos não conseguem ter a menor ideia onde são os meus momentos de felici",
      "position": 130578,
      "chapter": 5,
      "page": 97,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.505421686746985,
      "complexity_metrics": {
        "word_count": 166,
        "sentence_count": 3,
        "paragraph_count": 3,
        "avg_sentence_length": 55.333333333333336,
        "avg_word_length": 5.018072289156627,
        "unique_word_ratio": 0.7469879518072289,
        "avg_paragraph_length": 55.333333333333336,
        "punctuation_density": 0.12650602409638553,
        "line_break_count": 4,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "onde",
          "usar",
          "amor",
          "forma",
          "como",
          "melhor",
          "responder",
          "porque",
          "questionamentos",
          "tudo",
          "todos",
          "alguma",
          "coisa",
          "minha",
          "época",
          "músicas",
          "realmente",
          "eram",
          "boas",
          "continham"
        ],
        "entities": [
          [
            "continham muito",
            "PERSON"
          ],
          [
            "melhor",
            "GPE"
          ],
          [
            "frequência e quando responder",
            "ORG"
          ],
          [
            "sábia",
            "GPE"
          ],
          [
            "Ninguém",
            "ORG"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "nada",
            "ORG"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "nós temos algo melhor",
            "FAC"
          ],
          [
            "nosso destino",
            "PERSON"
          ]
        ],
        "readability_score": 70.82791164658634,
        "semantic_density": 0,
        "word_count": 166,
        "unique_words": 124,
        "lexical_diversity": 0.7469879518072289
      },
      "preservation_score": 9.223900718766269e-06
    },
    {
      "id": 135,
      "text": "dades e tristezas, julgando que o meu agir tá errado, diante de uma origem do certo sendo todo errado sem saber qual é o certo, até porque, todas as regras vieram dê um acerto que possa vir ser errado e vice versa e tudo depende do território e tempo em que foi vivenciado, sentido e testemunhados por aqueles que continham uma visão sobre o viver ao sentir um perfume que nós causa uma cicatriz de tão forte e marcante, que nos deixa uma lembrança. Quando tocamos e fazemos nossa comida, e ao comer, chegamos a ter um orgasmo de tão prazeroso que nós dá vontade de deitar e dormir ouvindo aquela música bem baixa que tocou em nossos corações pelos ouvidos, afinal, temos duas orelhas e uma boca, assim o ouvir torna-se mais fácil e acessível em termos uma maior percepção de espaço, sem essa função trabalhando corretamente ficamos tontos, enjoados, desorientado, labirintite, instável e fora de eixo, até porque, são duas para nós manter equilibrados e quando começamos a perder a paciência ganhamo",
      "position": 131578,
      "chapter": 5,
      "page": 98,
      "segment_type": "preserved_segment",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 36.425862068965515,
      "complexity_metrics": {
        "word_count": 174,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 87.0,
        "avg_word_length": 4.752873563218391,
        "unique_word_ratio": 0.7241379310344828,
        "avg_paragraph_length": 174.0,
        "punctuation_density": 0.10919540229885058,
        "line_break_count": 0,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "errado",
          "certo",
          "porque",
          "quando",
          "duas",
          "dades",
          "tristezas",
          "julgando",
          "agir",
          "diante",
          "origem",
          "sendo",
          "todo",
          "saber",
          "qual",
          "todas",
          "regras",
          "vieram",
          "acerto",
          "possa"
        ],
        "entities": [
          [
            "meu agir tá errado",
            "ORG"
          ],
          [
            "diante de uma",
            "PERSON"
          ],
          [
            "certo",
            "NORP"
          ],
          [
            "ser errado e",
            "ORG"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "fazemos nossa comida",
            "PERSON"
          ],
          [
            "orgasmo de tão",
            "ORG"
          ],
          [
            "vontade de deitar",
            "ORG"
          ],
          [
            "aquela música bem baixa",
            "PERSON"
          ],
          [
            "pelos ouvidos",
            "PERSON"
          ]
        ],
        "readability_score": 55.074137931034485,
        "semantic_density": 0,
        "word_count": 174,
        "unique_words": 126,
        "lexical_diversity": 0.7241379310344828
      },
      "preservation_score": 0.0
    },
    {
      "id": 136,
      "text": "s histeria dos estrondos de uma guerra, batida de um carro, sirene, fogos de artifícios, unha no vidro, voz irritante, sorriso irritante, conversa irritante e qualquer barulho que eu não estou mais afim e ter paciência, incômodo, pânico, fobia e tudo que for necessário viver em ser feliz e eufórico, já para outros desnecessário e estrondoso para aqueles que já viveram esses momentos e deixaram de gostar dos mesmos.\\n\\nOs movimentos que nós transformam em pessoas mais sábias e inteligentes são os mesmos que sofrem com o preconceito, e isso, provém devido aos momentos caóticos e perigosos que não queremos deixar os nossos filhos viverem, pelo medo de acontecer o pior nesses momentos perigosos cheios de adrenalina e prazeres sexuais “ruins” de serem feitos e vividos” que por muitas vezes terminam em momentos de amor para toda a vida.\\n\\n“O trajeto caótico do amor é necessário ser compreendido e direcionado.”\\n\\n",
      "position": 132578,
      "chapter": 5,
      "page": 99,
      "segment_type": "preserved_segment",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 37.400999999999996,
      "complexity_metrics": {
        "word_count": 150,
        "sentence_count": 4,
        "paragraph_count": 3,
        "avg_sentence_length": 37.5,
        "avg_word_length": 5.086666666666667,
        "unique_word_ratio": 0.72,
        "avg_paragraph_length": 50.0,
        "punctuation_density": 0.11333333333333333,
        "line_break_count": 6,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "momentos",
          "irritante",
          "mais",
          "necessário",
          "mesmos",
          "perigosos",
          "amor",
          "histeria",
          "estrondos",
          "guerra",
          "batida",
          "carro",
          "sirene",
          "fogos",
          "artifícios",
          "unha",
          "vidro",
          "sorriso",
          "conversa",
          "qualquer"
        ],
        "entities": [
          [
            "s histeria",
            "ORG"
          ],
          [
            "fogos de artifícios",
            "ORG"
          ],
          [
            "voz irritante",
            "PERSON"
          ],
          [
            "qualquer barulho",
            "PERSON"
          ],
          [
            "eu não estou mais",
            "PERSON"
          ],
          [
            "eufórico",
            "GPE"
          ],
          [
            "já para outros desnecessário",
            "PERSON"
          ],
          [
            "mesmos",
            "PERSON"
          ],
          [
            "mesmos que sofrem",
            "PERSON"
          ],
          [
            "devido aos momentos caóticos",
            "PERSON"
          ]
        ],
        "readability_score": 79.724,
        "semantic_density": 0,
        "word_count": 150,
        "unique_words": 108,
        "lexical_diversity": 0.72
      },
      "preservation_score": 1.3234292335621167e-05
    },
    {
      "id": 137,
      "text": "  “Sabemos que o mundo não irá adaptar-se a uma pessoa, e para tirar a Terra do eixo, precisamos de um valor quântico.”\\n\\n   Ao chegar na idade de começar a ingerir alimentos além de colostro e leite materno, descobrimos o quanto a Terra pode nos dar de sabor, porém o viver nesse paradoxo não nós permite termos equilíbrio entre nós mesmos para com os recursos que podemos retirar, assim, alimentar-se corretamente é relativo a um costume territorial onde nossos corpos vieram mais adaptados com certos tipos de alimentos e costumes que transformaram os nossos corpos em uma máquina que funciona a base de combustíveis fósseis ou combustíveis orgânicos, ambos necessitam ser consumidos para o próprio corpo e mente proporcional ao próprio gasto energético originário dê um costume territorial e o costume familiar, até porque, nosso segundo cérebro faz o trabalho de destruir toda a energia para o corpo inclusive para o primeiro cérebro, assim percebemos que a falta de equilíbrio em alimentar-se, c",
      "position": 133494,
      "chapter": 5,
      "page": 100,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.54259259259259,
      "complexity_metrics": {
        "word_count": 162,
        "sentence_count": 2,
        "paragraph_count": 2,
        "avg_sentence_length": 81.0,
        "avg_word_length": 5.1419753086419755,
        "unique_word_ratio": 0.6790123456790124,
        "avg_paragraph_length": 81.0,
        "punctuation_density": 0.07407407407407407,
        "line_break_count": 2,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "costume",
          "terra",
          "alimentos",
          "equilíbrio",
          "assim",
          "alimentar",
          "territorial",
          "nossos",
          "corpos",
          "combustíveis",
          "próprio",
          "corpo",
          "cérebro",
          "sabemos",
          "mundo",
          "adaptar",
          "pessoa",
          "tirar",
          "eixo",
          "precisamos"
        ],
        "entities": [
          [
            "Terra",
            "ORG"
          ],
          [
            "descobrimos",
            "PERSON"
          ],
          [
            "nós mesmos",
            "ORG"
          ],
          [
            "vieram mais",
            "PERSON"
          ],
          [
            "funciona",
            "GPE"
          ],
          [
            "ambos necessitam",
            "PERSON"
          ],
          [
            "faz",
            "ORG"
          ],
          [
            "primeiro cérebro",
            "ORG"
          ],
          [
            "assim percebemos",
            "PERSON"
          ]
        ],
        "readability_score": 57.95740740740741,
        "semantic_density": 0,
        "word_count": 162,
        "unique_words": 110,
        "lexical_diversity": 0.6790123456790124
      },
      "preservation_score": 2.2725552495511095e-06
    },
    {
      "id": 138,
      "text": "ausam danos irreversíveis e permanentes tendo sempre a necessidade de tratar o transtorno que por muitas vezes são causada pela fome vívida sem querer ser vívida, ou por vezes, não conseguia controlar os próprios pensamentos e usando o comer como fuga, e talvez, possa ter sido um transtorno hormonal que por muitas vezes veio derivado de um passado que ninguém queria viver e teve que viver.\\n\\n“Todo padrão têm como ser alterado o próprio padrão, basta ter foco, paciência, dedicação e vontade pois sem esforço, não têm ganho.”\\n\\n  Começamos a engatinhar e ter uma nova percepção, já a curiosidade, torna-se viciosa e evoluída ao ponto colocarmos na boca devido a uma ironia da vida e o tocar, sentir, conectar, sujar, doenças, células, nervosismo, adrenalina, prazer e equilíbrio entre causa e efeito de felicidade e tristezas, alegria e dor, aprendizado e frustração, expectativa e depressão, histeria e as loucuras que imaginamos ser mais loucas que realmente são, vieram fundidas com gritos de des",
      "position": 134494,
      "chapter": 5,
      "page": 101,
      "segment_type": "preserved_segment",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 36.5462962962963,
      "complexity_metrics": {
        "word_count": 162,
        "sentence_count": 3,
        "paragraph_count": 3,
        "avg_sentence_length": 54.0,
        "avg_word_length": 5.154320987654321,
        "unique_word_ratio": 0.7345679012345679,
        "avg_paragraph_length": 54.0,
        "punctuation_density": 0.15432098765432098,
        "line_break_count": 4,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "vezes",
          "transtorno",
          "muitas",
          "vívida",
          "como",
          "viver",
          "padrão",
          "ausam",
          "danos",
          "irreversíveis",
          "permanentes",
          "tendo",
          "sempre",
          "necessidade",
          "tratar",
          "causada",
          "pela",
          "fome",
          "querer",
          "conseguia"
        ],
        "entities": [
          [
            "ausam danos irreversíveis",
            "PERSON"
          ],
          [
            "causada",
            "NORP"
          ],
          [
            "vívida sem querer ser vívida",
            "FAC"
          ],
          [
            "talvez",
            "GPE"
          ],
          [
            "têm como ser alterado",
            "ORG"
          ],
          [
            "próprio padrão",
            "GPE"
          ],
          [
            "basta",
            "NORP"
          ],
          [
            "Começamos",
            "PERSON"
          ],
          [
            "nova",
            "LOC"
          ],
          [
            "boca devido",
            "PERSON"
          ]
        ],
        "readability_score": 71.4537037037037,
        "semantic_density": 0,
        "word_count": 162,
        "unique_words": 119,
        "lexical_diversity": 0.7345679012345679
      },
      "preservation_score": 1.1229096527193718e-05
    },
    {
      "id": 139,
      "text": "espero daqueles que nos ama e cuida, e esse cuidar, vira uma loucura sentimental e material, até porque, cada vez que a “euforia da curiosidade foram acima do saber movimentar-se, merdas cagadas não voltam ao rabo.” \\n\\n“Assim como o rio corre para baixo a cachoeira não sobe para cima.”\\n\\nPara entender melhor esse pleonasmo necessário ser dito, irei usar uma das melhores metáfora com muita analogia que eu posso descrever que o impossível se torna possível com amor, esforço e dedicação. \\n\\nMestre ancião ou cavaleiro de ouro da casa de Libra -  ficava sentado na frente de sua cachoeira sem pensar no tédio e devido a essa postura se transformou em um homem sábio, poderoso, puro (matou muitas pessoas), calmo, focado e um ótimo mestre e o melhor discípulo era incrédulo em si próprio, olhava para o seu mestre com admiração pela serenidade que ele passava mesmo com tudo que ele já tinha presenciado e vívido, e isso, o Shiryu levava como motivo em suas batalhas em ver o lado de fazer o necessário para um bem maior.",
      "position": 135494,
      "chapter": 5,
      "page": 102,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.407303370786515,
      "complexity_metrics": {
        "word_count": 178,
        "sentence_count": 4,
        "paragraph_count": 4,
        "avg_sentence_length": 44.5,
        "avg_word_length": 4.691011235955056,
        "unique_word_ratio": 0.7415730337078652,
        "avg_paragraph_length": 44.5,
        "punctuation_density": 0.10112359550561797,
        "line_break_count": 6,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "mestre",
          "esse",
          "como",
          "cachoeira",
          "melhor",
          "necessário",
          "espero",
          "daqueles",
          "cuida",
          "cuidar",
          "vira",
          "loucura",
          "sentimental",
          "material",
          "porque",
          "cada",
          "euforia",
          "curiosidade",
          "acima",
          "saber"
        ],
        "entities": [
          [
            "espero daqueles que",
            "PERSON"
          ],
          [
            "vira uma loucura",
            "PERSON"
          ],
          [
            "cada vez",
            "ORG"
          ],
          [
            "acima",
            "ORG"
          ],
          [
            "merdas cagadas",
            "ORG"
          ],
          [
            "corre",
            "NORP"
          ],
          [
            "para cima",
            "PERSON"
          ],
          [
            "Para",
            "PRODUCT"
          ],
          [
            "necessário ser dito",
            "ORG"
          ],
          [
            "muita analogia",
            "PERSON"
          ]
        ],
        "readability_score": 76.34269662921349,
        "semantic_density": 0,
        "word_count": 178,
        "unique_words": 132,
        "lexical_diversity": 0.7415730337078652
      },
      "preservation_score": 2.085403640764548e-05
    },
    {
      "id": 140,
      "text": " Voltemos para o mestre, até porque, o estar sentado na frente de sua cachoeira, pensando o mínimo possível e se mexendo só o necessário para economizar toda a sua energia e conseguir viver até alguém ser digno de seguir seu legado em momentos necessário em ter um bom guerreiro em meio a guerra ao lado do amor.\\n\\nShiryu ou cavaleiro de bronze (dragão) – Incrédulo com tantas perdas diante de nunca ter feito o mal, não conseguia encontrar forças e motivação para um bem maior, por mais que fosse predestinado, esforçado, focado, ele não tinha vivido todas as linhas tortas necessárias a serem redirecionadas para o seu próprio destino ser digno de fazer o impossível acontecer, quando se a morte está próxima do nosso sentir, fazer o impossível torna-se possível ao fazer a cachoeira correr para cima apenas com um chute do dragão, a mesma arte que ele nasceu com um o Dom, o mestre só teve o trabalho de agregar e direcionar em outro destino.\\n\\n",
      "position": 136512,
      "chapter": 5,
      "page": 103,
      "segment_type": "preserved_segment",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 36.404216867469884,
      "complexity_metrics": {
        "word_count": 166,
        "sentence_count": 2,
        "paragraph_count": 2,
        "avg_sentence_length": 83.0,
        "avg_word_length": 4.680722891566265,
        "unique_word_ratio": 0.6746987951807228,
        "avg_paragraph_length": 83.0,
        "punctuation_density": 0.08433734939759036,
        "line_break_count": 4,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "fazer",
          "mestre",
          "cachoeira",
          "possível",
          "necessário",
          "digno",
          "dragão",
          "destino",
          "impossível",
          "voltemos",
          "porque",
          "sentado",
          "frente",
          "pensando",
          "mínimo",
          "mexendo",
          "economizar",
          "toda",
          "energia",
          "conseguir"
        ],
        "entities": [
          [
            "Voltemos",
            "ORG"
          ],
          [
            "estar",
            "PRODUCT"
          ],
          [
            "na frente de sua cachoeira",
            "PERSON"
          ],
          [
            "pensando",
            "GPE"
          ],
          [
            "mexendo só",
            "ORG"
          ],
          [
            "necessário",
            "GPE"
          ],
          [
            "digno de seguir",
            "ORG"
          ],
          [
            "seu legado",
            "FAC"
          ],
          [
            "Shiryu",
            "ORG"
          ],
          [
            "cavaleiro de bronze",
            "ORG"
          ]
        ],
        "readability_score": 57.09578313253012,
        "semantic_density": 0,
        "word_count": 166,
        "unique_words": 112,
        "lexical_diversity": 0.6746987951807228
      },
      "preservation_score": 4.545110499102219e-06
    },
    {
      "id": 141,
      "text": "“Impossível é uma palavra referente à uma situação, e por acaso se alguma situação obtiver perda ou ganho, felicidade ou tristeza têm como equilibrar. Assim o possível precisa existir para coexistir com o impossível.”\\n\\nQuando começamos a correlacionar o sentimento de tocar e sentir, despertamos curiosidades sentimentais do próprio aprender e interpretar sem cálculo de erros ou acertos e sim momentos engraçados, cômicos, interessantes, intrigantes, pensativos, revolucionário, agressivo, explosivo semelhante aqueles desenhos animados que a cabeça fica avermelhada e saindo fumaça pelos ouvidos, esses que causam histeria são os mesmos que causam uma sensação de paz ao ouvir um passarinho cantando, cigarra agradecendo pelo entardecer de um novo ciclo diário da vida.\\n\\n“Ao começar a andar, parecemos um saco vazio que só fica de pé, se alguém segurar.”\\n\\nNas caminhadas dessas vidas tropeçamos, caímos e levantamos semelhantes a um descer de um tobogã de 90°, montanha russa com giros, loops e mui",
      "position": 137458,
      "chapter": 5,
      "page": 104,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 32.069736842105264,
      "complexity_metrics": {
        "word_count": 152,
        "sentence_count": 5,
        "paragraph_count": 4,
        "avg_sentence_length": 30.4,
        "avg_word_length": 5.565789473684211,
        "unique_word_ratio": 0.7894736842105263,
        "avg_paragraph_length": 38.0,
        "punctuation_density": 0.13815789473684212,
        "line_break_count": 6,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "impossível",
          "situação",
          "fica",
          "causam",
          "palavra",
          "referente",
          "acaso",
          "alguma",
          "obtiver",
          "perda",
          "ganho",
          "felicidade",
          "tristeza",
          "como",
          "equilibrar",
          "assim",
          "possível",
          "precisa",
          "existir",
          "coexistir"
        ],
        "entities": [
          [
            "para coexistir",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "despertamos",
            "PERSON"
          ],
          [
            "cômicos",
            "ORG"
          ],
          [
            "pelos ouvidos",
            "PERSON"
          ],
          [
            "mesmos que",
            "PERSON"
          ],
          [
            "pelo entardecer de um novo",
            "PERSON"
          ],
          [
            "fica de pé",
            "PERSON"
          ],
          [
            "Nas",
            "PERSON"
          ],
          [
            "vidas tropeçamos",
            "PERSON"
          ]
        ],
        "readability_score": 83.13026315789475,
        "semantic_density": 0,
        "word_count": 152,
        "unique_words": 120,
        "lexical_diversity": 0.7894736842105263
      },
      "preservation_score": 2.00519580842745e-05
    },
    {
      "id": 142,
      "text": "tas emoções depressivas e expressivas de um pensar relativo ao momento e a idade. Por muitas vezes o caminhar não dá tempo e precisamos correr em uma direção a uma bola para chutar antes do amiguinho, e é esse amiguinho que não vai em direção a bola para você chegar antes por te amar mais que a si mesmo, até porque, o eu de cada um, são muitos “eus” relativos ao sentir e cada momento vivido junto com outros “eus” vinda junta com o meu eu, são os melhores brinquedos que um parque de diversões, mesmo com todas as ofertas e demandas dos nossos picos de felicidades junta a luxúria da diversão, onde a confiança é conquistada pela fome ou pelos prazeres do momento da companhia, essa não percebendo os nossos malefícios e os nossos benefícios corretamente, origina pequenos momentos de interpretações que vão nós moldando e nós transformando em pessoas com vontades e desejos “próprios”, vinda de um vício mal interpretado de outras vidas que deram certo em outras más interpretações com benefícios",
      "position": 138458,
      "chapter": 5,
      "page": 105,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.425862068965515,
      "complexity_metrics": {
        "word_count": 174,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 87.0,
        "avg_word_length": 4.752873563218391,
        "unique_word_ratio": 0.6551724137931034,
        "avg_paragraph_length": 174.0,
        "punctuation_density": 0.06321839080459771,
        "line_break_count": 0,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "momento",
          "nossos",
          "direção",
          "bola",
          "antes",
          "amiguinho",
          "mesmo",
          "cada",
          "vinda",
          "junta",
          "benefícios",
          "interpretações",
          "outras",
          "emoções",
          "depressivas",
          "expressivas",
          "pensar",
          "relativo",
          "idade",
          "muitas"
        ],
        "entities": [
          [
            "bola",
            "ORG"
          ],
          [
            "eu de cada",
            "PERSON"
          ],
          [
            "vinda",
            "PERSON"
          ],
          [
            "meu eu",
            "PERSON"
          ],
          [
            "picos de felicidades",
            "PERSON"
          ],
          [
            "conquistada",
            "ORG"
          ],
          [
            "essa não percebendo os nossos",
            "ORG"
          ],
          [
            "outras más interpretações",
            "PERSON"
          ]
        ],
        "readability_score": 55.074137931034485,
        "semantic_density": 0,
        "word_count": 174,
        "unique_words": 114,
        "lexical_diversity": 0.6551724137931034
      },
      "preservation_score": 0.0
    },
    {
      "id": 143,
      "text": ", assim começamos a viver uma direção correta de erros não vistos e menos ensinado a ser direcionado o nosso caminhar ou o nosso correr.\\n\\n“Piscou dançou e já estamos cheios de obrigações e metas para uma vida que a miséria tem um eleitorado de ignorantes que ficam cego pela fome ou pela ganância.”\\n\\nQuando começamos a nascer pentelhos, são os primeiros sinais dê uma necessidade por uma maior liberdade não podendo ser vivida devido as regras infindáveis e fúteis coletivas, para um viver entediado em ganância para ter mais conforto de dar inveja por ser a oposição da miséria. Servindo como maior e melhor vício de vida a qual se pode viver, onde os recursos se todos pudessem viver dessa forma, não dava para atender ¼ da população mundial pensando nas melhores estimativas, e isso, não é pela falta da sagacidade humana, pois essa, deu e dá nó até no diabo, imagina entre nós?\\n\\n   Essas hipóteses são tão infindáveis quanto a necessidade de ser ou ter mais e mais em uma proporção que esquecemos",
      "position": 139458,
      "chapter": 5,
      "page": 106,
      "segment_type": "preserved_segment",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 34.00571428571429,
      "complexity_metrics": {
        "word_count": 175,
        "sentence_count": 5,
        "paragraph_count": 4,
        "avg_sentence_length": 35.0,
        "avg_word_length": 4.685714285714286,
        "unique_word_ratio": 0.6742857142857143,
        "avg_paragraph_length": 43.75,
        "punctuation_density": 0.08,
        "line_break_count": 6,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "viver",
          "pela",
          "mais",
          "começamos",
          "nosso",
          "vida",
          "miséria",
          "ganância",
          "necessidade",
          "maior",
          "infindáveis",
          "assim",
          "direção",
          "correta",
          "erros",
          "vistos",
          "menos",
          "ensinado",
          "direcionado",
          "caminhar"
        ],
        "entities": [
          [
            "de erros",
            "ORG"
          ],
          [
            "já estamos",
            "PERSON"
          ],
          [
            "de obrigações",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "ganância para",
            "PERSON"
          ],
          [
            "Servindo",
            "PERSON"
          ],
          [
            "melhor vício de",
            "FAC"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "viver dessa forma",
            "PERSON"
          ],
          [
            "não dava",
            "ORG"
          ]
        ],
        "readability_score": 81.09428571428572,
        "semantic_density": 0,
        "word_count": 175,
        "unique_words": 118,
        "lexical_diversity": 0.6742857142857143
      },
      "preservation_score": 1.2833253173935679e-05
    },
    {
      "id": 144,
      "text": " dos momentos que nós motiva e nós fizeram chegar no espaço tempo em que estamos vivendo, pois a luxúria de um estilo de vida é exemplar e muito mais legal e divertido, um mundo sem fronteiras e sem vida para quase todos aqueles que estão cheios de energia, sendo mal gasta e mal direcionada por uma falsa vida exemplar e gostosa de se viver em um extremo pelo prazer e conforto torna-se difícil acompanhar e cansativo viver, porém o tédio, cai no esquecimento pelas fugas constantes mais vantajosas que uma leitura cheias de palavras arcaicas dê um sentimento que ninguém mais vive e ninguém mais irá viver. Semelhantes aqueles filmes “cult”, onde, a maioria que acompanham e gostam são pessoas com traumas ou direcionamentos de vida parecida com aquela música que desperta um sentimento ou uma imagem cheias de lembranças depressivas e muito bem interpretado e explicado para se dar como conselho, até porque, nessa idade e em muitas outras idades não se pode falar sobre sexo, “não podemos falar s",
      "position": 140458,
      "chapter": 5,
      "page": 107,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 36.45438596491228,
      "complexity_metrics": {
        "word_count": 171,
        "sentence_count": 2,
        "paragraph_count": 1,
        "avg_sentence_length": 85.5,
        "avg_word_length": 4.847953216374269,
        "unique_word_ratio": 0.6783625730994152,
        "avg_paragraph_length": 171.0,
        "punctuation_density": 0.06432748538011696,
        "line_break_count": 0,
        "formatting_preservation_score": 65.0
      },
      "analysis": {
        "keywords": [
          "vida",
          "mais",
          "viver",
          "exemplar",
          "muito",
          "aqueles",
          "cheias",
          "sentimento",
          "ninguém",
          "falar",
          "momentos",
          "motiva",
          "fizeram",
          "chegar",
          "espaço",
          "tempo",
          "estamos",
          "vivendo",
          "pois",
          "luxúria"
        ],
        "entities": [
          [
            "estamos vivendo",
            "PERSON"
          ],
          [
            "muito mais",
            "PERSON"
          ],
          [
            "todos",
            "CARDINAL"
          ],
          [
            "mal gasta",
            "PERSON"
          ],
          [
            "mal direcionada",
            "PERSON"
          ],
          [
            "gostosa de se",
            "PERSON"
          ],
          [
            "extremo pelo",
            "PERSON"
          ],
          [
            "de palavras arcaicas",
            "PERSON"
          ],
          [
            "aquela música",
            "PERSON"
          ],
          [
            "depressivas e muito bem",
            "PERSON"
          ]
        ],
        "readability_score": 55.795614035087716,
        "semantic_density": 0,
        "word_count": 171,
        "unique_words": 116,
        "lexical_diversity": 0.6783625730994152
      },
      "preservation_score": 0.0
    },
    {
      "id": 145,
      "text": "obre o que nós gera, o falar, cria desejos sombrios e obscuros naqueles que podem vir ser um estuprador bem informado, assim aqueles estuprados e mal informado, com famílias e lares destruídos e construídos através de um ato sexual gerado pela falta de informações não informada, pelo  preconceito necessário em um passado muito distante e longe de se ter necessidade de existir novamente.\\n\\nComo iremos nós manter saudáveis e felizes sem direcionamentos em saber ter prazer em um tocar E entender que podemos conhecer aqueles que poderá ser a única pessoa a qual deseja ter os maiores sexo, foda, fetiches, trepada, rapidinha e todos aqueles momentos prazerosos e cheios de preconceitos com tanto Amor, que chega a dar inveja na vizinhança que não conseguem ter gratidão pelo amor recebido. \\n\\n   Quando começamos a sentir inveja desses momentos, é a idade e o tempo vivido que estão pesando e nós deixando mais cansados, tão exaustos que dá preguiça de ouvir os mesmos assuntos cansativos e sem senti",
      "position": 141458,
      "chapter": 5,
      "page": 108,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 40.50727272727273,
      "complexity_metrics": {
        "word_count": 165,
        "sentence_count": 3,
        "paragraph_count": 3,
        "avg_sentence_length": 55.0,
        "avg_word_length": 5.024242424242424,
        "unique_word_ratio": 0.7090909090909091,
        "avg_paragraph_length": 55.0,
        "punctuation_density": 0.08484848484848485,
        "line_break_count": 4,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "aqueles",
          "informado",
          "pelo",
          "momentos",
          "amor",
          "inveja",
          "obre",
          "gera",
          "falar",
          "cria",
          "desejos",
          "sombrios",
          "obscuros",
          "naqueles",
          "podem",
          "estuprador",
          "assim",
          "estuprados",
          "famílias",
          "lares"
        ],
        "entities": [
          [
            "cria desejos sombrios",
            "PERSON"
          ],
          [
            "pelo  preconceito",
            "PERSON"
          ],
          [
            "muito distante e longe de se",
            "PERSON"
          ],
          [
            "Amor",
            "PERSON"
          ],
          [
            "pelo amor recebido",
            "PERSON"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "pesando e nós",
            "PERSON"
          ],
          [
            "deixando mais",
            "PERSON"
          ],
          [
            "tão",
            "ORG"
          ],
          [
            "mesmos assuntos",
            "PERSON"
          ]
        ],
        "readability_score": 70.99272727272728,
        "semantic_density": 0,
        "word_count": 165,
        "unique_words": 117,
        "lexical_diversity": 0.7090909090909091
      },
      "preservation_score": 5.614548263596859e-06
    },
    {
      "id": 146,
      "text": "do em concordar e ser obrigado a concordar para não arrumar briga com maluco, pois aquele que revida, está se rebaixando ao mesmo nível e para não chegar a esse ponto, basta usar a sabedoria para revidar em deixar aqueles próximos, sem ações e sim adorações pelas palavras brandas e dignas de serem lembradas e exaltadas quando forem lembradas, até porque, o sentimento ao ser repassado será a propagação do sentir a palavra dita e lembrada como a única em meio a um entrelaçamento caótico.\\n\\n“Após tantas fugas prazerosas, percebemos que o valor gasto para termos certos benefícios, não compensam os desgastes do trajeto.”\\n\\n   Percebemos que vamos em fuga de um movimentar-se mais preguiçoso que possamos obter e conforme vamos atingindo níveis, as necessidades sociais vão intensificando e o nosso tempo vão modificando os nossos valores de acordo com a necessidade de ser o que precisa ter, nós tornando escravos evoluídos dentro de um sistema necessário coexistir dentro de uma única gratidão que necessitamos ter e reconhecer:\\n\\n",
      "position": 142458,
      "chapter": 5,
      "page": 109,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 38.54311377245509,
      "complexity_metrics": {
        "word_count": 167,
        "sentence_count": 3,
        "paragraph_count": 3,
        "avg_sentence_length": 55.666666666666664,
        "avg_word_length": 5.1437125748503,
        "unique_word_ratio": 0.7005988023952096,
        "avg_paragraph_length": 55.666666666666664,
        "punctuation_density": 0.07784431137724551,
        "line_break_count": 6,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "concordar",
          "lembradas",
          "única",
          "percebemos",
          "vamos",
          "dentro",
          "obrigado",
          "arrumar",
          "briga",
          "maluco",
          "pois",
          "aquele",
          "revida",
          "está",
          "rebaixando",
          "mesmo",
          "nível",
          "chegar",
          "esse",
          "ponto"
        ],
        "entities": [
          [
            "basta",
            "NORP"
          ],
          [
            "dignas de serem",
            "PERSON"
          ],
          [
            "quando forem lembradas",
            "PERSON"
          ],
          [
            "lembrada como",
            "ORG"
          ],
          [
            "Após",
            "PERSON"
          ],
          [
            "prazerosas, percebemos que",
            "ORG"
          ],
          [
            "não compensam",
            "PERSON"
          ],
          [
            "Percebemos",
            "PERSON"
          ],
          [
            "vamos atingindo níveis",
            "PERSON"
          ],
          [
            "vão modificando os nossos",
            "PERSON"
          ]
        ],
        "readability_score": 70.62355289421157,
        "semantic_density": 0,
        "word_count": 167,
        "unique_words": 117,
        "lexical_diversity": 0.7005988023952096
      },
      "preservation_score": 9.624939880451756e-06
    },
    {
      "id": 147,
      "text": "“Tudo e todos têm haver com o nosso futuro”\\n\\nQuando nascemos o primeiro valor adquirido se chama destino.\\n\\nDentro dos nossos destinos os valores para conseguir equilibrar é proporcional ao próprio destino, esse mesmo, provém dos valores adquiridos pela interferência quântica durante o trajeto do próprio destino, sabendo que:\\n\\nQual é o peso do nosso destino para com a Terra, continente, país, estado, cidade, bairro, comunidade, agregação, grêmio, família e para si próprio?\\n\\nSó podemos saber sobre o destino vivendo e sobrevivendo aos caminhos, são esses caminhos que nós deixam felizes, alegres, tristes e cansados com vontade de desistir da vida por não ser reconhecido por aqueles que são os motivos dê nossas vidas, esses, são os mesmos reguladores da nossa propagação quântica.\\n\\nO nosso destino vêm com um peso caótico provinda do próprio nascimento, esse peso é a proporção da interferência que necessitamos corrigir em nosso destino. A vida que temos é o trajeto regulador do destino de tod",
      "position": 143490,
      "chapter": 5,
      "page": 110,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 32.567499999999995,
      "complexity_metrics": {
        "word_count": 160,
        "sentence_count": 5,
        "paragraph_count": 6,
        "avg_sentence_length": 32.0,
        "avg_word_length": 5.225,
        "unique_word_ratio": 0.69375,
        "avg_paragraph_length": 26.666666666666668,
        "punctuation_density": 0.14375,
        "line_break_count": 10,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "destino",
          "nosso",
          "próprio",
          "peso",
          "valores",
          "esse",
          "interferência",
          "quântica",
          "trajeto",
          "caminhos",
          "esses",
          "vida",
          "tudo",
          "todos",
          "haver",
          "futuro",
          "quando",
          "nascemos",
          "primeiro",
          "valor"
        ],
        "entities": [
          [
            "Quando nascemos",
            "PERSON"
          ],
          [
            "primeiro valor",
            "ORG"
          ],
          [
            "chama destino",
            "ORG"
          ],
          [
            "Dentro",
            "LOC"
          ],
          [
            "para conseguir",
            "PERSON"
          ],
          [
            "interferência quântica",
            "PERSON"
          ],
          [
            "nosso destino",
            "PERSON"
          ],
          [
            "Terra",
            "ORG"
          ],
          [
            "grêmio",
            "ORG"
          ],
          [
            "destino vivendo",
            "FAC"
          ]
        ],
        "readability_score": 82.4325,
        "semantic_density": 0,
        "word_count": 160,
        "unique_words": 111,
        "lexical_diversity": 0.69375
      },
      "preservation_score": 5.0129895210686234e-05
    },
    {
      "id": 148,
      "text": "os aqueles que estão ao nosso lado, sabendo que: Cada um têm a sua quantidade de energia que possa vir armazenar, sentir, absorver, analisar e interpretar proporcional ao peso e em qual lado da moeda está vivendo a lembrança ou a memória.\\n\\n   Sempre que vivemos algo de bom na vida ou ruim “questão de observação” em escala de ser lembrança é o destino regulando a nossa propagação quântica.\\n\\n“Vivemos com livre arbítrio preso a um destino.”\\n\\nO que nós convém em equilibrar o próprio destino:\\n\\nObservar, sentir o destino e aprender, até porque, nada adianta brigar.\\n\\nBrigar contra o destino e causando interferências onde o equilibrar a ação e a reação torna-se exaustivos e depressivos, seja para o lado do amor ou do ódio.\\n\\nEducar, direcionar, sentir e deixar acontecer o viver a razão do destino com muito mais facilidades quando aprende a sentir e a aceitar o que foi nós dado como único.\\n\\n“Quando tudo parecer perdido é quando aprendemos o valor de renascer e surgir mais sábios, inteligentes e belos semelhantes a uma fênix que acaba de ressurgir das cinzas.”\\n\\n",
      "position": 144490,
      "chapter": 5,
      "page": 111,
      "segment_type": "preserved_segment",
      "themes": {
        "filosofia": 100.0
      },
      "difficulty": 27.94065934065934,
      "complexity_metrics": {
        "word_count": 182,
        "sentence_count": 8,
        "paragraph_count": 8,
        "avg_sentence_length": 22.75,
        "avg_word_length": 4.802197802197802,
        "unique_word_ratio": 0.6813186813186813,
        "avg_paragraph_length": 22.75,
        "punctuation_density": 0.10989010989010989,
        "line_break_count": 16,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "destino",
          "sentir",
          "lado",
          "quando",
          "lembrança",
          "vivemos",
          "equilibrar",
          "brigar",
          "mais",
          "aqueles",
          "estão",
          "nosso",
          "sabendo",
          "cada",
          "quantidade",
          "energia",
          "possa",
          "armazenar",
          "absorver",
          "analisar"
        ],
        "entities": [
          [
            "lado",
            "GPE"
          ],
          [
            "Vivemos",
            "PERSON"
          ],
          [
            "Observar",
            "PERSON"
          ],
          [
            "nada",
            "ORG"
          ],
          [
            "muito mais",
            "PERSON"
          ],
          [
            "dado",
            "GPE"
          ],
          [
            "único",
            "GPE"
          ],
          [
            "Quando",
            "PERSON"
          ],
          [
            "quando aprendemos",
            "PERSON"
          ],
          [
            "valor de renascer",
            "ORG"
          ]
        ],
        "readability_score": 87.18434065934066,
        "semantic_density": 0,
        "word_count": 182,
        "unique_words": 124,
        "lexical_diversity": 0.6813186813186813
      },
      "preservation_score": 0.00011549927856542111
    },
    {
      "id": 149,
      "text": "“O sentido da vida é escrever certo com linhas tortas, até porque, todos os momentos que provém dê uma experiência lendária, épica, prazerosa, dopamina, adrenalina pode ser a que causa em nós um instinto de sobrevivência gostoso junto ao sentir e perceber, que o destino só é possível devido ao impossível coexistir nesses movimentos em paradoxo que se chama, Vida!!”\\n\\nGratidão por existir!\\n\\nCaverna do Marcelo\\n\\nAo fechar os olhos entro em um mundo pessoal cheio de falhas, lacunas, ausências, conflitos, desejos, sonhos, imaginação, imagens, sentimentos, angustia, duvidas, forma como viu, como interpretou, qual é o tamanho do próprio sentir e tudo que provem de conseguir aceitar a própria mente e o corpo. \\n\\n“Independentemente do próprio viver e o que viveu, já foi vívido e o tempo vai passar.”\\n\\nChegar nesse estágio de não ter incomodo, gatilhos, histeria e qualquer desconforto que me faça pensar em algo sem eu querer pensar e pensar pela própria tensão ou ansiedade, O tempo vai passar.\\n\\n",
      "position": 145557,
      "chapter": 5,
      "page": 112,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 32.93333333333333,
      "complexity_metrics": {
        "word_count": 162,
        "sentence_count": 5,
        "paragraph_count": 6,
        "avg_sentence_length": 32.4,
        "avg_word_length": 5.111111111111111,
        "unique_word_ratio": 0.7654320987654321,
        "avg_paragraph_length": 27.0,
        "punctuation_density": 0.19135802469135801,
        "line_break_count": 12,
        "formatting_preservation_score": 100.0
      },
      "analysis": {
        "keywords": [
          "pensar",
          "vida",
          "sentir",
          "como",
          "próprio",
          "própria",
          "tempo",
          "passar",
          "sentido",
          "escrever",
          "certo",
          "linhas",
          "tortas",
          "porque",
          "todos",
          "momentos",
          "provém",
          "experiência",
          "lendária",
          "épica"
        ],
        "entities": [
          [
            "todos",
            "CARDINAL"
          ],
          [
            "lendária",
            "GPE"
          ],
          [
            "épica",
            "GPE"
          ],
          [
            "prazerosa, dopamina",
            "GPE"
          ],
          [
            "adrenalina pode ser",
            "FAC"
          ],
          [
            "perceber",
            "GPE"
          ],
          [
            "Gratidão",
            "PERSON"
          ],
          [
            "Caverna",
            "GPE"
          ],
          [
            "Marcelo",
            "ORG"
          ],
          [
            "lacunas",
            "PERSON"
          ]
        ],
        "readability_score": 82.26666666666667,
        "semantic_density": 0,
        "word_count": 162,
        "unique_words": 124,
        "lexical_diversity": 0.7654320987654321
      },
      "preservation_score": 8.421822395395286e-05
    },
    {
      "id": 150,
      "text": "Todas as nossas formas de pensar tem um lado bom ou ruim, não precisamos ter incomodo com o ruim e com o bom, até porque, ambas as palavras são relativas ao próprio pensar e agir, assim, o meu pensar é o meu próprio incomodo e quando não contém pendências consigo mesmo, o pensar torna-se relativo a duas formas de correlacionar a nossa própria caverna, onde uma é cheia de imagens sem sentido e a outra cheio de sentimentos sem sentido. Todas as memorias ou lembranças deixadas de ter amor ou importância, entram nas memorias interpretativas e no intuito de agregar em não querer viver ou aprender a controlar o sentir, não importa qual seja, ambas são relativa a cada caverna.\\n\\nQuando percebemos e analisamos a nossa caverna, percebemos que os nossos gatilhos de lembranças ou memorias são necessárias acontecerem para iluminar a parte escura e pouca acessada no meu próprio universo imaginário, ate porque ao chegar nesse estágio mental a minha percepção de caverna, torna-se um ponto em meio a um",
      "position": 146554,
      "chapter": 5,
      "page": 113,
      "segment_type": "preserved_segment",
      "themes": {
        "arte": 100.0
      },
      "difficulty": 36.45438596491228,
      "complexity_metrics": {
        "word_count": 171,
        "sentence_count": 3,
        "paragraph_count": 2,
        "avg_sentence_length": 57.0,
        "avg_word_length": 4.847953216374269,
        "unique_word_ratio": 0.6198830409356725,
        "avg_paragraph_length": 85.5,
        "punctuation_density": 0.08771929824561403,
        "line_break_count": 2,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "pensar",
          "caverna",
          "próprio",
          "memorias",
          "todas",
          "formas",
          "ruim",
          "incomodo",
          "porque",
          "ambas",
          "quando",
          "torna",
          "nossa",
          "sentido",
          "lembranças",
          "percebemos",
          "nossas",
          "lado",
          "precisamos",
          "palavras"
        ],
        "entities": [
          [
            "Todas",
            "PERSON"
          ],
          [
            "nossas formas de pensar",
            "PERSON"
          ],
          [
            "palavras são",
            "PERSON"
          ],
          [
            "quando não contém pendências",
            "ORG"
          ],
          [
            "outra",
            "NORP"
          ],
          [
            "Todas",
            "PERSON"
          ],
          [
            "importa",
            "NORP"
          ],
          [
            "relativa",
            "ORG"
          ],
          [
            "cada caverna",
            "ORG"
          ],
          [
            "Quando",
            "PERSON"
          ]
        ],
        "readability_score": 70.04561403508772,
        "semantic_density": 0,
        "word_count": 171,
        "unique_words": 106,
        "lexical_diversity": 0.6198830409356725
      },
      "preservation_score": 2.2725552495511095e-06
    },
    {
      "id": 151,
      "text": "a imensa escuridão onde a imagem lembra uma luz no fim do túnel, onde estou parado sem sair  do local e aquele ponto estagnado expele um raio em minha direção com o movimento a ser pensado e analisado e quando não executo esse processo, merdas cagadas não voltam ao rabo.\\n\\nMinha caverna  é um parque de diversão temático relativo ao momento ou ao pensamento, sabendo que as aventuras vívidas são muito mais aproveitadas que as ensinadas percebi que a minha caverna demorando a ser explorada da medo, fica obscura, cheias de espíritos vagando, teias de aranha, floresta sombria e todos aqueles medos as quais provém do meu próprio eu.\\n\\nO viver explorando a minha própria caverna é cansativo proporcional ao tempo e a quantidade que cavei para chegar onde quero ir e quanto mais cavamos, maior é a quantidade de obstáculos e resíduos deixados para trás que por muitas vezes ficamos com preguiça e cansados em organizar a bagunça que o cavar vai deixando, para organizar a bagunça deixada quando voltamo",
      "position": 147554,
      "chapter": 5,
      "page": 114,
      "segment_type": "preserved_segment",
      "themes": {},
      "difficulty": 38.449122807017545,
      "complexity_metrics": {
        "word_count": 171,
        "sentence_count": 3,
        "paragraph_count": 3,
        "avg_sentence_length": 57.0,
        "avg_word_length": 4.830409356725146,
        "unique_word_ratio": 0.695906432748538,
        "avg_paragraph_length": 57.0,
        "punctuation_density": 0.06432748538011696,
        "line_break_count": 4,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "minha",
          "onde",
          "caverna",
          "quando",
          "mais",
          "quantidade",
          "organizar",
          "bagunça",
          "imensa",
          "escuridão",
          "imagem",
          "lembra",
          "túnel",
          "estou",
          "parado",
          "sair",
          "local",
          "aquele",
          "ponto",
          "estagnado"
        ],
        "entities": [
          [
            "quando não executo esse",
            "ORG"
          ],
          [
            "merdas cagadas não voltam",
            "ORG"
          ],
          [
            "parque de diversão temático relativo",
            "ORG"
          ],
          [
            "pensamento",
            "GPE"
          ],
          [
            "sabendo",
            "GPE"
          ],
          [
            "muito mais aproveitadas",
            "PERSON"
          ],
          [
            "ensinadas percebi",
            "ORG"
          ],
          [
            "fica obscura",
            "PERSON"
          ],
          [
            "floresta sombria",
            "ORG"
          ],
          [
            "próprio eu",
            "PERSON"
          ]
        ],
        "readability_score": 70.05087719298245,
        "semantic_density": 0,
        "word_count": 171,
        "unique_words": 119,
        "lexical_diversity": 0.695906432748538
      },
      "preservation_score": 4.411430778540389e-06
    },
    {
      "id": 152,
      "text": "s, torna-se mais difícil descobrir por onde posso começar a arrumar a bagunça deixada, até porque, não lembramos onde foi o inicio da bagunça deixada. \\n\\nTambém temos aquelas pequenas bagunças que nada irá me afetar, assim o ter paciência com o tempo passando, será a minha melhor forma de percepção em organizar que o tempo vai passar.\\n\\nTenho tantas lembranças em minha caverna que algumas tem o seu próprio espaço e forma de agir, muitas vezes o acesso a esse lado obscuro da lua é nadar em águas sombrias e pouco conhecida, navegar sem saber o que possa vir, causa histeria e alucinação quando não se têm lucidez, em outros casos, me perco na minha própria caverna, assim o agir e falar ficam travados no automático pela própria proteção em não querer entender ou ver pela própria histeria ou captação causada, são esses fatores, que transformam a loucura em genialidade ou a genialidade em loucura, ambos os casos dependem da minha própria histeria em aceitar a minha própria caverna.",
      "position": 148554,
      "chapter": 5,
      "page": 115,
      "segment_type": "preserved_segment",
      "themes": {
        "ciencia": 100.0
      },
      "difficulty": 36.44852071005917,
      "complexity_metrics": {
        "word_count": 169,
        "sentence_count": 3,
        "paragraph_count": 3,
        "avg_sentence_length": 56.333333333333336,
        "avg_word_length": 4.828402366863905,
        "unique_word_ratio": 0.6923076923076923,
        "avg_paragraph_length": 56.333333333333336,
        "punctuation_density": 0.10059171597633136,
        "line_break_count": 4,
        "formatting_preservation_score": 85.0
      },
      "analysis": {
        "keywords": [
          "minha",
          "própria",
          "caverna",
          "histeria",
          "onde",
          "bagunça",
          "deixada",
          "assim",
          "tempo",
          "forma",
          "agir",
          "casos",
          "pela",
          "loucura",
          "genialidade",
          "torna",
          "mais",
          "difícil",
          "descobrir",
          "posso"
        ],
        "entities": [
          [
            "posso",
            "PERSON"
          ],
          [
            "Também",
            "LOC"
          ],
          [
            "nada irá me afetar",
            "PERSON"
          ],
          [
            "Tenho",
            "ORG"
          ],
          [
            "forma de agir",
            "ORG"
          ],
          [
            "pouco conhecida",
            "PERSON"
          ],
          [
            "navegar sem",
            "PERSON"
          ],
          [
            "histeria e alucinação",
            "ORG"
          ],
          [
            "quando",
            "PERSON"
          ],
          [
            "outros casos",
            "PERSON"
          ]
        ],
        "readability_score": 70.38481262327416,
        "semantic_density": 0,
        "word_count": 169,
        "unique_words": 117,
        "lexical_diversity": 0.6923076923076923
      },
      "preservation_score": 7.218704910338818e-06
    }
  ],
  "book_name": "paradoxo dos movimentos concluído.docx",
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