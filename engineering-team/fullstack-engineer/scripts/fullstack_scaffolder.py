#!/usr/bin/env python3
"""
Fullstack Feature Scaffolder
Generates complete frontend and backend code for features
"""

import os
import json
from pathlib import Path
from typing import Dict, List

class FullstackScaffolder:
    """Generate full-stack feature boilerplate"""
    
    def __init__(self):
        self.templates = {
            'react': self._get_react_templates(),
            'nextjs': self._get_nextjs_templates(),
            'express': self._get_express_templates(),
            'graphql': self._get_graphql_templates()
        }
    
    def scaffold_feature(self, feature_name: str, options: Dict) -> Dict:
        """Scaffold a complete full-stack feature"""
        
        feature = {
            'name': feature_name,
            'frontend': {},
            'backend': {},
            'database': {},
            'tests': {},
            'documentation': {}
        }
        
        # Generate based on stack
        stack = options.get('stack', 'react-express')
        
        if 'react' in stack or 'next' in stack:
            feature['frontend'] = self._generate_frontend(feature_name, options)
        
        if 'express' in stack or 'node' in stack:
            feature['backend'] = self._generate_backend(feature_name, options)
        
        if 'graphql' in stack:
            feature['backend']['graphql'] = self._generate_graphql(feature_name, options)
        
        feature['database'] = self._generate_database(feature_name, options)
        feature['tests'] = self._generate_tests(feature_name, options)
        feature['documentation'] = self._generate_docs(feature_name, options)
        
        return feature
    
    def _generate_frontend(self, name: str, options: Dict) -> Dict:
        """Generate frontend components"""
        
        framework = options.get('frontend_framework', 'react')
        use_typescript = options.get('typescript', True)
        ext = '.tsx' if use_typescript else '.jsx'
        
        frontend = {
            'component': self._create_react_component(name, use_typescript),
            'styles': self._create_styles(name, options.get('css_approach', 'modules')),
            'hooks': self._create_custom_hook(name, use_typescript),
            'api_client': self._create_api_client(name, use_typescript),
            'state': self._create_state_management(name, options.get('state_lib', 'context')),
            'types': self._create_types(name) if use_typescript else None
        }
        
        return frontend
    
    def _generate_backend(self, name: str, options: Dict) -> Dict:
        """Generate backend API code"""
        
        framework = options.get('backend_framework', 'express')
        use_typescript = options.get('typescript', True)
        
        backend = {
            'controller': self._create_controller(name, framework, use_typescript),
            'service': self._create_service(name, use_typescript),
            'repository': self._create_repository(name, use_typescript),
            'routes': self._create_routes(name, framework),
            'middleware': self._create_middleware(name),
            'validation': self._create_validation(name)
        }
        
        return backend
    
    def _generate_graphql(self, name: str, options: Dict) -> Dict:
        """Generate GraphQL schema and resolvers"""
        
        return {
            'schema': self._create_graphql_schema(name),
            'resolvers': self._create_graphql_resolvers(name),
            'dataloaders': self._create_dataloaders(name)
        }
    
    def _generate_database(self, name: str, options: Dict) -> Dict:
        """Generate database schemas and migrations"""
        
        db_type = options.get('database', 'postgresql')
        
        return {
            'migration': self._create_migration(name, db_type),
            'model': self._create_model(name, options.get('orm', 'prisma')),
            'seed': self._create_seed_data(name)
        }
    
    def _generate_tests(self, name: str, options: Dict) -> Dict:
        """Generate test files"""
        
        return {
            'unit_tests': {
                'frontend': self._create_component_tests(name),
                'backend': self._create_service_tests(name)
            },
            'integration_tests': self._create_integration_tests(name),
            'e2e_tests': self._create_e2e_tests(name)
        }
    
    def _generate_docs(self, name: str, options: Dict) -> Dict:
        """Generate documentation"""
        
        return {
            'api_docs': self._create_api_documentation(name),
            'component_docs': self._create_component_documentation(name),
            'readme': self._create_feature_readme(name)
        }
    
    def _create_react_component(self, name: str, typescript: bool) -> str:
        """Create React component"""
        
        pascal_name = self._to_pascal_case(name)
        
        if typescript:
            return f"""import React, {{ useState, useEffect }} from 'react';
import {{ use{pascal_name} }} from './hooks/use{pascal_name}';
import styles from './{pascal_name}.module.css';

interface {pascal_name}Props {{
  id?: string;
  onSuccess?: (data: any) => void;
  onError?: (error: Error) => void;
}}

export const {pascal_name}: React.FC<{pascal_name}Props> = ({{ id, onSuccess, onError }}) => {{
  const {{ data, loading, error, refetch }} = use{pascal_name}(id);
  
  if (loading) return <div className={{styles.loading}}>Loading...</div>;
  if (error) return <div className={{styles.error}}>Error: {{error.message}}</div>;
  
  return (
    <div className={{styles.container}}>
      <h2>{pascal_name}</h2>
      {{/* Component content */}}
    </div>
  );
}};

export default {pascal_name};"""
        else:
            return f"""import React, {{ useState, useEffect }} from 'react';
import {{ use{pascal_name} }} from './hooks/use{pascal_name}';
import styles from './{pascal_name}.module.css';

export const {pascal_name} = ({{ id, onSuccess, onError }}) => {{
  const {{ data, loading, error, refetch }} = use{pascal_name}(id);
  
  if (loading) return <div className={{styles.loading}}>Loading...</div>;
  if (error) return <div className={{styles.error}}>Error: {{error.message}}</div>;
  
  return (
    <div className={{styles.container}}>
      <h2>{pascal_name}</h2>
      {{/* Component content */}}
    </div>
  );
}};

export default {pascal_name};"""
    
    def _create_custom_hook(self, name: str, typescript: bool) -> str:
        """Create custom React hook"""
        
        pascal_name = self._to_pascal_case(name)
        camel_name = self._to_camel_case(name)
        
        if typescript:
            return f"""import {{ useState, useEffect }} from 'react';
import {{ fetch{pascal_name} }} from '../api/{camel_name}Api';

interface Use{pascal_name}Result {{
  data: any | null;
  loading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
}}

export const use{pascal_name} = (id?: string): Use{pascal_name}Result => {{
  const [data, setData] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchData = async () => {{
    try {{
      setLoading(true);
      const result = await fetch{pascal_name}(id);
      setData(result);
      setError(null);
    }} catch (err) {{
      setError(err as Error);
    }} finally {{
      setLoading(false);
    }}
  }};

  useEffect(() => {{
    fetchData();
  }}, [id]);

  return {{ data, loading, error, refetch: fetchData }};
}};"""
        else:
            return f"""import {{ useState, useEffect }} from 'react';
import {{ fetch{pascal_name} }} from '../api/{camel_name}Api';

export const use{pascal_name} = (id) => {{
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = async () => {{
    try {{
      setLoading(true);
      const result = await fetch{pascal_name}(id);
      setData(result);
      setError(null);
    }} catch (err) {{
      setError(err);
    }} finally {{
      setLoading(false);
    }}
  }};

  useEffect(() => {{
    fetchData();
  }}, [id]);

  return {{ data, loading, error, refetch: fetchData }};
}};"""
    
    def _create_api_client(self, name: str, typescript: bool) -> str:
        """Create API client"""
        
        pascal_name = self._to_pascal_case(name)
        camel_name = self._to_camel_case(name)
        
        if typescript:
            return f"""import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001';

export interface {pascal_name}Data {{
  id: string;
  // Add fields
}}

export const fetch{pascal_name} = async (id?: string): Promise<{pascal_name}Data> => {{
  const url = id ? `${{API_BASE_URL}}/{camel_name}/${{id}}` : `${{API_BASE_URL}}/{camel_name}`;
  const response = await axios.get(url);
  return response.data;
}};

export const create{pascal_name} = async (data: Partial<{pascal_name}Data>): Promise<{pascal_name}Data> => {{
  const response = await axios.post(`${{API_BASE_URL}}/{camel_name}`, data);
  return response.data;
}};

export const update{pascal_name} = async (id: string, data: Partial<{pascal_name}Data>): Promise<{pascal_name}Data> => {{
  const response = await axios.put(`${{API_BASE_URL}}/{camel_name}/${{id}}`, data);
  return response.data;
}};

export const delete{pascal_name} = async (id: string): Promise<void> => {{
  await axios.delete(`${{API_BASE_URL}}/{camel_name}/${{id}}`);
}};"""
        else:
            return f"""import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001';

export const fetch{pascal_name} = async (id) => {{
  const url = id ? `${{API_BASE_URL}}/{camel_name}/${{id}}` : `${{API_BASE_URL}}/{camel_name}`;
  const response = await axios.get(url);
  return response.data;
}};

export const create{pascal_name} = async (data) => {{
  const response = await axios.post(`${{API_BASE_URL}}/{camel_name}`, data);
  return response.data;
}};

export const update{pascal_name} = async (id, data) => {{
  const response = await axios.put(`${{API_BASE_URL}}/{camel_name}/${{id}}`, data);
  return response.data;
}};

export const delete{pascal_name} = async (id) => {{
  await axios.delete(`${{API_BASE_URL}}/{camel_name}/${{id}}`);
}};"""
    
    def _create_controller(self, name: str, framework: str, typescript: bool) -> str:
        """Create backend controller"""
        
        pascal_name = self._to_pascal_case(name)
        camel_name = self._to_camel_case(name)
        
        if typescript:
            return f"""import {{ Request, Response, NextFunction }} from 'express';
import {{ {pascal_name}Service }} from '../services/{camel_name}Service';

export class {pascal_name}Controller {{
  private {camel_name}Service: {pascal_name}Service;

  constructor() {{
    this.{camel_name}Service = new {pascal_name}Service();
  }}

  async getAll(req: Request, res: Response, next: NextFunction) {{
    try {{
      const data = await this.{camel_name}Service.findAll(req.query);
      res.json({{ success: true, data }});
    }} catch (error) {{
      next(error);
    }}
  }}

  async getById(req: Request, res: Response, next: NextFunction) {{
    try {{
      const data = await this.{camel_name}Service.findById(req.params.id);
      if (!data) {{
        return res.status(404).json({{ success: false, message: 'Not found' }});
      }}
      res.json({{ success: true, data }});
    }} catch (error) {{
      next(error);
    }}
  }}

  async create(req: Request, res: Response, next: NextFunction) {{
    try {{
      const data = await this.{camel_name}Service.create(req.body);
      res.status(201).json({{ success: true, data }});
    }} catch (error) {{
      next(error);
    }}
  }}

  async update(req: Request, res: Response, next: NextFunction) {{
    try {{
      const data = await this.{camel_name}Service.update(req.params.id, req.body);
      res.json({{ success: true, data }});
    }} catch (error) {{
      next(error);
    }}
  }}

  async delete(req: Request, res: Response, next: NextFunction) {{
    try {{
      await this.{camel_name}Service.delete(req.params.id);
      res.status(204).send();
    }} catch (error) {{
      next(error);
    }}
  }}
}}

export default new {pascal_name}Controller();"""
        else:
            return f"""const {pascal_name}Service = require('../services/{camel_name}Service');

class {pascal_name}Controller {{
  constructor() {{
    this.{camel_name}Service = new {pascal_name}Service();
  }}

  async getAll(req, res, next) {{
    try {{
      const data = await this.{camel_name}Service.findAll(req.query);
      res.json({{ success: true, data }});
    }} catch (error) {{
      next(error);
    }}
  }}

  async getById(req, res, next) {{
    try {{
      const data = await this.{camel_name}Service.findById(req.params.id);
      if (!data) {{
        return res.status(404).json({{ success: false, message: 'Not found' }});
      }}
      res.json({{ success: true, data }});
    }} catch (error) {{
      next(error);
    }}
  }}

  async create(req, res, next) {{
    try {{
      const data = await this.{camel_name}Service.create(req.body);
      res.status(201).json({{ success: true, data }});
    }} catch (error) {{
      next(error);
    }}
  }}

  async update(req, res, next) {{
    try {{
      const data = await this.{camel_name}Service.update(req.params.id, req.body);
      res.json({{ success: true, data }});
    }} catch (error) {{
      next(error);
    }}
  }}

  async delete(req, res, next) {{
    try {{
      await this.{camel_name}Service.delete(req.params.id);
      res.status(204).send();
    }} catch (error) {{
      next(error);
    }}
  }}
}}

module.exports = new {pascal_name}Controller();"""
    
    def _create_service(self, name: str, typescript: bool) -> str:
        """Create service layer"""
        
        pascal_name = self._to_pascal_case(name)
        camel_name = self._to_camel_case(name)
        
        if typescript:
            return f"""import {{ {pascal_name}Repository }} from '../repositories/{camel_name}Repository';

export class {pascal_name}Service {{
  private repository: {pascal_name}Repository;

  constructor() {{
    this.repository = new {pascal_name}Repository();
  }}

  async findAll(filters: any = {{}}) {{
    // Add business logic here
    return await this.repository.findAll(filters);
  }}

  async findById(id: string) {{
    // Add business logic here
    return await this.repository.findById(id);
  }}

  async create(data: any) {{
    // Add validation and business logic
    return await this.repository.create(data);
  }}

  async update(id: string, data: any) {{
    // Add validation and business logic
    return await this.repository.update(id, data);
  }}

  async delete(id: string) {{
    // Add business logic here
    return await this.repository.delete(id);
  }}
}}

export default {pascal_name}Service;"""
        else:
            return f"""const {pascal_name}Repository = require('../repositories/{camel_name}Repository');

class {pascal_name}Service {{
  constructor() {{
    this.repository = new {pascal_name}Repository();
  }}

  async findAll(filters = {{}}) {{
    // Add business logic here
    return await this.repository.findAll(filters);
  }}

  async findById(id) {{
    // Add business logic here
    return await this.repository.findById(id);
  }}

  async create(data) {{
    // Add validation and business logic
    return await this.repository.create(data);
  }}

  async update(id, data) {{
    // Add validation and business logic
    return await this.repository.update(id, data);
  }}

  async delete(id) {{
    // Add business logic here
    return await this.repository.delete(id);
  }}
}}

module.exports = {pascal_name}Service;"""
    
    def _create_repository(self, name: str, typescript: bool) -> str:
        """Create repository layer"""
        
        pascal_name = self._to_pascal_case(name)
        snake_name = self._to_snake_case(name)
        
        if typescript:
            return f"""import {{ PrismaClient }} from '@prisma/client';

export class {pascal_name}Repository {{
  private prisma: PrismaClient;

  constructor() {{
    this.prisma = new PrismaClient();
  }}

  async findAll(filters: any = {{}}) {{
    return await this.prisma.{snake_name}.findMany({{
      where: filters
    }});
  }}

  async findById(id: string) {{
    return await this.prisma.{snake_name}.findUnique({{
      where: {{ id }}
    }});
  }}

  async create(data: any) {{
    return await this.prisma.{snake_name}.create({{
      data
    }});
  }}

  async update(id: string, data: any) {{
    return await this.prisma.{snake_name}.update({{
      where: {{ id }},
      data
    }});
  }}

  async delete(id: string) {{
    return await this.prisma.{snake_name}.delete({{
      where: {{ id }}
    }});
  }}
}}

export default {pascal_name}Repository;"""
        else:
            return f"""const {{ PrismaClient }} = require('@prisma/client');

class {pascal_name}Repository {{
  constructor() {{
    this.prisma = new PrismaClient();
  }}

  async findAll(filters = {{}}) {{
    return await this.prisma.{snake_name}.findMany({{
      where: filters
    }});
  }}

  async findById(id) {{
    return await this.prisma.{snake_name}.findUnique({{
      where: {{ id }}
    }});
  }}

  async create(data) {{
    return await this.prisma.{snake_name}.create({{
      data
    }});
  }}

  async update(id, data) {{
    return await this.prisma.{snake_name}.update({{
      where: {{ id }},
      data
    }});
  }}

  async delete(id) {{
    return await this.prisma.{snake_name}.delete({{
      where: {{ id }}
    }});
  }}
}}

module.exports = {pascal_name}Repository;"""
    
    def _create_routes(self, name: str, framework: str) -> str:
        """Create API routes"""
        
        pascal_name = self._to_pascal_case(name)
        camel_name = self._to_camel_case(name)
        
        return f"""import {{ Router }} from 'express';
import {camel_name}Controller from '../controllers/{camel_name}Controller';
import {{ validate }} from '../middleware/validation';
import {{ authenticate }} from '../middleware/auth';
import {{ {camel_name}Schema }} from '../validations/{camel_name}Validation';

const router = Router();

router.get('/', authenticate, {camel_name}Controller.getAll);
router.get('/:id', authenticate, {camel_name}Controller.getById);
router.post('/', authenticate, validate({camel_name}Schema), {camel_name}Controller.create);
router.put('/:id', authenticate, validate({camel_name}Schema), {camel_name}Controller.update);
router.delete('/:id', authenticate, {camel_name}Controller.delete);

export default router;"""
    
    def _create_middleware(self, name: str) -> str:
        """Create middleware"""
        
        return f"""export const {name}Middleware = (req, res, next) => {{
  // Add middleware logic
  console.log('{name} middleware');
  next();
}};"""
    
    def _create_validation(self, name: str) -> str:
        """Create validation schema"""
        
        pascal_name = self._to_pascal_case(name)
        camel_name = self._to_camel_case(name)
        
        return f"""import Joi from 'joi';

export const {camel_name}Schema = Joi.object({{
  name: Joi.string().required().min(3).max(100),
  description: Joi.string().optional().max(500),
  status: Joi.string().valid('active', 'inactive').default('active'),
  // Add more fields as needed
}});

export const update{pascal_name}Schema = Joi.object({{
  name: Joi.string().optional().min(3).max(100),
  description: Joi.string().optional().max(500),
  status: Joi.string().valid('active', 'inactive').optional(),
}});"""
    
    def _create_graphql_schema(self, name: str) -> str:
        """Create GraphQL schema"""
        
        pascal_name = self._to_pascal_case(name)
        
        return f"""type {pascal_name} {{
  id: ID!
  name: String!
  description: String
  status: Status!
  createdAt: DateTime!
  updatedAt: DateTime!
}}

enum Status {{
  ACTIVE
  INACTIVE
}}

input {pascal_name}Input {{
  name: String!
  description: String
  status: Status
}}

input {pascal_name}UpdateInput {{
  name: String
  description: String
  status: Status
}}

type Query {{
  {name}(id: ID!): {pascal_name}
  all{pascal_name}s(limit: Int, offset: Int): [{pascal_name}!]!
}}

type Mutation {{
  create{pascal_name}(input: {pascal_name}Input!): {pascal_name}!
  update{pascal_name}(id: ID!, input: {pascal_name}UpdateInput!): {pascal_name}!
  delete{pascal_name}(id: ID!): Boolean!
}}"""
    
    def _create_graphql_resolvers(self, name: str) -> str:
        """Create GraphQL resolvers"""
        
        pascal_name = self._to_pascal_case(name)
        camel_name = self._to_camel_case(name)
        
        return f"""import {{ {pascal_name}Service }} from '../services/{camel_name}Service';

const {camel_name}Service = new {pascal_name}Service();

export const {camel_name}Resolvers = {{
  Query: {{
    {name}: async (_, {{ id }}) => {{
      return await {camel_name}Service.findById(id);
    }},
    all{pascal_name}s: async (_, {{ limit = 10, offset = 0 }}) => {{
      return await {camel_name}Service.findAll({{ limit, offset }});
    }}
  }},
  
  Mutation: {{
    create{pascal_name}: async (_, {{ input }}) => {{
      return await {camel_name}Service.create(input);
    }},
    update{pascal_name}: async (_, {{ id, input }}) => {{
      return await {camel_name}Service.update(id, input);
    }},
    delete{pascal_name}: async (_, {{ id }}) => {{
      await {camel_name}Service.delete(id);
      return true;
    }}
  }}
}};"""
    
    def _create_dataloaders(self, name: str) -> str:
        """Create DataLoader for N+1 query prevention"""
        
        pascal_name = self._to_pascal_case(name)
        camel_name = self._to_camel_case(name)
        
        return f"""import DataLoader from 'dataloader';
import {{ {pascal_name}Repository }} from '../repositories/{camel_name}Repository';

const repository = new {pascal_name}Repository();

export const create{pascal_name}Loader = () => {{
  return new DataLoader(async (ids) => {{
    const items = await repository.findByIds(ids);
    const itemMap = {{}};
    items.forEach(item => {{
      itemMap[item.id] = item;
    }});
    return ids.map(id => itemMap[id]);
  }});
}};"""
    
    def _create_migration(self, name: str, db_type: str) -> str:
        """Create database migration"""
        
        snake_name = self._to_snake_case(name)
        table_name = f"{snake_name}s"
        
        if db_type == 'postgresql':
            return f"""-- Migration: Create {table_name} table
-- Timestamp: {{new Date().toISOString()}}

CREATE TABLE IF NOT EXISTS {table_name} (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  description TEXT,
  status VARCHAR(50) DEFAULT 'active',
  created_by UUID REFERENCES users(id),
  updated_by UUID REFERENCES users(id),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_{table_name}_status ON {table_name}(status);
CREATE INDEX idx_{table_name}_created_at ON {table_name}(created_at DESC);

-- Trigger for updated_at
CREATE TRIGGER update_{table_name}_updated_at
  BEFORE UPDATE ON {table_name}
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();"""
        else:
            return f"""-- Migration for {table_name}
CREATE TABLE {table_name} (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  status VARCHAR(50) DEFAULT 'active',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);"""
    
    def _create_model(self, name: str, orm: str) -> str:
        """Create ORM model"""
        
        pascal_name = self._to_pascal_case(name)
        snake_name = self._to_snake_case(name)
        
        if orm == 'prisma':
            return f"""model {pascal_name} {{
  id          String   @id @default(uuid())
  name        String
  description String?
  status      Status   @default(ACTIVE)
  createdBy   String?
  updatedBy   String?
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
  
  @@map("{snake_name}s")
}}

enum Status {{
  ACTIVE
  INACTIVE
}}"""
        else:
            return f"""// Sequelize model
const {{ Model, DataTypes }} = require('sequelize');

class {pascal_name} extends Model {{
  static init(sequelize) {{
    super.init({{
      name: {{
        type: DataTypes.STRING,
        allowNull: false
      }},
      description: {{
        type: DataTypes.TEXT,
        allowNull: true
      }},
      status: {{
        type: DataTypes.ENUM('active', 'inactive'),
        defaultValue: 'active'
      }}
    }}, {{
      sequelize,
      modelName: '{pascal_name}',
      tableName: '{snake_name}s'
    }});
  }}
}}

module.exports = {pascal_name};"""
    
    def _create_seed_data(self, name: str) -> str:
        """Create seed data"""
        
        pascal_name = self._to_pascal_case(name)
        
        return f"""// Seed data for {pascal_name}
export const {name}Seeds = [
  {{
    name: 'Sample {pascal_name} 1',
    description: 'This is a sample {name}',
    status: 'active'
  }},
  {{
    name: 'Sample {pascal_name} 2',
    description: 'Another sample {name}',
    status: 'active'
  }},
  {{
    name: 'Sample {pascal_name} 3',
    description: 'Inactive sample {name}',
    status: 'inactive'
  }}
];"""
    
    def _create_component_tests(self, name: str) -> str:
        """Create component tests"""
        
        pascal_name = self._to_pascal_case(name)
        
        return f"""import {{ render, screen, waitFor, fireEvent }} from '@testing-library/react';
import {{ {pascal_name} }} from '../{pascal_name}';

describe('{pascal_name}', () => {{
  it('renders without crashing', () => {{
    render(<{pascal_name} />);
    expect(screen.getByText('{pascal_name}')).toBeInTheDocument();
  }});

  it('shows loading state', () => {{
    render(<{pascal_name} />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  }});

  it('displays error state', async () => {{
    // Mock error scenario
    render(<{pascal_name} />);
    await waitFor(() => {{
      expect(screen.getByText(/Error:/)).toBeInTheDocument();
    }});
  }});

  it('handles user interaction', async () => {{
    render(<{pascal_name} />);
    // Add interaction tests
  }});
}});"""
    
    def _create_service_tests(self, name: str) -> str:
        """Create service tests"""
        
        pascal_name = self._to_pascal_case(name)
        camel_name = self._to_camel_case(name)
        
        return f"""import {{ {pascal_name}Service }} from '../services/{camel_name}Service';

describe('{pascal_name}Service', () => {{
  let service;

  beforeEach(() => {{
    service = new {pascal_name}Service();
  }});

  describe('findAll', () => {{
    it('returns all items', async () => {{
      const result = await service.findAll();
      expect(Array.isArray(result)).toBe(true);
    }});
  }});

  describe('findById', () => {{
    it('returns single item', async () => {{
      const result = await service.findById('test-id');
      expect(result).toBeDefined();
    }});
  }});

  describe('create', () => {{
    it('creates new item', async () => {{
      const data = {{ name: 'Test' }};
      const result = await service.create(data);
      expect(result.name).toBe('Test');
    }});
  }});
}});"""
    
    def _create_integration_tests(self, name: str) -> str:
        """Create integration tests"""
        
        camel_name = self._to_camel_case(name)
        
        return f"""import request from 'supertest';
import app from '../app';

describe('/{camel_name} endpoints', () => {{
  describe('GET /{camel_name}', () => {{
    it('returns list of items', async () => {{
      const res = await request(app)
        .get('/{camel_name}')
        .expect(200);
      
      expect(res.body.success).toBe(true);
      expect(Array.isArray(res.body.data)).toBe(true);
    }});
  }});

  describe('POST /{camel_name}', () => {{
    it('creates new item', async () => {{
      const res = await request(app)
        .post('/{camel_name}')
        .send({{ name: 'Test Item' }})
        .expect(201);
      
      expect(res.body.success).toBe(true);
      expect(res.body.data.name).toBe('Test Item');
    }});
  }});
}});"""
    
    def _create_e2e_tests(self, name: str) -> str:
        """Create E2E tests"""
        
        pascal_name = self._to_pascal_case(name)
        
        return f"""import {{ test, expect }} from '@playwright/test';

test.describe('{pascal_name} Feature', () => {{
  test.beforeEach(async ({{ page }}) => {{
    await page.goto('http://localhost:3000/{name}');
  }});

  test('displays {name} page', async ({{ page }}) => {{
    await expect(page.locator('h2')).toContainText('{pascal_name}');
  }});

  test('creates new {name}', async ({{ page }}) => {{
    await page.click('button:has-text("New")');
    await page.fill('input[name="name"]', 'Test {pascal_name}');
    await page.click('button:has-text("Save")');
    
    await expect(page.locator('.success')).toBeVisible();
  }});

  test('edits existing {name}', async ({{ page }}) => {{
    await page.click('.edit-button:first-child');
    await page.fill('input[name="name"]', 'Updated {pascal_name}');
    await page.click('button:has-text("Update")');
    
    await expect(page.locator('.success')).toBeVisible();
  }});
}});"""
    
    def _create_api_documentation(self, name: str) -> str:
        """Create API documentation"""
        
        camel_name = self._to_camel_case(name)
        pascal_name = self._to_pascal_case(name)
        
        return f"""# {pascal_name} API Documentation

## Endpoints

### GET /{camel_name}
Retrieve all {name} items.

**Response:**
```json
{{
  "success": true,
  "data": [
    {{
      "id": "uuid",
      "name": "string",
      "description": "string",
      "status": "active|inactive",
      "createdAt": "2024-01-01T00:00:00Z",
      "updatedAt": "2024-01-01T00:00:00Z"
    }}
  ]
}}
```

### GET /{camel_name}/:id
Retrieve single {name} by ID.

### POST /{camel_name}
Create new {name}.

**Request Body:**
```json
{{
  "name": "string",
  "description": "string",
  "status": "active|inactive"
}}
```

### PUT /{camel_name}/:id
Update existing {name}.

### DELETE /{camel_name}/:id
Delete {name} by ID.

## Error Responses

- 400: Bad Request - Invalid input data
- 401: Unauthorized - Missing or invalid authentication
- 404: Not Found - Resource does not exist
- 500: Internal Server Error
"""
    
    def _create_component_documentation(self, name: str) -> str:
        """Create component documentation"""
        
        pascal_name = self._to_pascal_case(name)
        
        return f"""# {pascal_name} Component

## Usage

```jsx
import {{ {pascal_name} }} from './components/{pascal_name}';

function App() {{
  return (
    <{pascal_name}
      id="optional-id"
      onSuccess={{handleSuccess}}
      onError={{handleError}}
    />
  );
}}
```

## Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| id | string | No | ID of item to display |
| onSuccess | function | No | Callback on successful operation |
| onError | function | No | Callback on error |

## Hooks

### use{pascal_name}

Custom hook for {name} data management.

```jsx
const {{ data, loading, error, refetch }} = use{pascal_name}(id);
```
"""
    
    def _create_feature_readme(self, name: str) -> str:
        """Create feature README"""
        
        pascal_name = self._to_pascal_case(name)
        
        return f"""# {pascal_name} Feature

## Overview
Full-stack implementation of {pascal_name} functionality.

## Structure
```
{name}/
├── frontend/
│   ├── components/
│   ├── hooks/
│   ├── api/
│   └── tests/
├── backend/
│   ├── controllers/
│   ├── services/
│   ├── repositories/
│   ├── routes/
│   └── tests/
├── database/
│   ├── migrations/
│   └── seeds/
└── docs/
```

## Setup

1. Install dependencies:
```bash
npm install
```

2. Run migrations:
```bash
npm run migrate
```

3. Seed database:
```bash
npm run seed
```

4. Start development:
```bash
npm run dev
```

## Testing

```bash
# Unit tests
npm run test:unit

# Integration tests
npm run test:integration

# E2E tests
npm run test:e2e
```

## API Documentation
See [API.md](./docs/API.md)

## Component Documentation
See [COMPONENT.md](./docs/COMPONENT.md)
"""
    
    def _create_styles(self, name: str, approach: str) -> str:
        """Create styles based on approach"""
        
        pascal_name = self._to_pascal_case(name)
        
        if approach == 'modules':
            return f""".container {{
  padding: 1rem;
  border-radius: 8px;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}}

.loading {{
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
  color: #666;
}}

.error {{
  padding: 1rem;
  background: #fee;
  color: #c00;
  border-radius: 4px;
  margin: 1rem 0;
}}"""
        else:
            return f"""import styled from 'styled-components';

export const Container = styled.div`
  padding: 1rem;
  border-radius: 8px;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

export const Loading = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
  color: #666;
`;

export const Error = styled.div`
  padding: 1rem;
  background: #fee;
  color: #c00;
  border-radius: 4px;
  margin: 1rem 0;
`;"""
    
    def _create_state_management(self, name: str, lib: str) -> str:
        """Create state management"""
        
        pascal_name = self._to_pascal_case(name)
        camel_name = self._to_camel_case(name)
        
        if lib == 'redux':
            return f"""import {{ createSlice, createAsyncThunk }} from '@reduxjs/toolkit';
import {{ fetch{pascal_name} }} from '../api/{camel_name}Api';

export const get{pascal_name} = createAsyncThunk(
  '{camel_name}/fetch',
  async (id) => {{
    const response = await fetch{pascal_name}(id);
    return response;
  }}
);

const {camel_name}Slice = createSlice({{
  name: '{camel_name}',
  initialState: {{
    data: null,
    loading: false,
    error: null
  }},
  reducers: {{}},
  extraReducers: (builder) => {{
    builder
      .addCase(get{pascal_name}.pending, (state) => {{
        state.loading = true;
        state.error = null;
      }})
      .addCase(get{pascal_name}.fulfilled, (state, action) => {{
        state.loading = false;
        state.data = action.payload;
      }})
      .addCase(get{pascal_name}.rejected, (state, action) => {{
        state.loading = false;
        state.error = action.error.message;
      }});
  }}
}});

export default {camel_name}Slice.reducer;"""
        else:
            return f"""import React, {{ createContext, useContext, useReducer }} from 'react';

const {pascal_name}Context = createContext();

const initialState = {{
  data: null,
  loading: false,
  error: null
}};

function {camel_name}Reducer(state, action) {{
  switch (action.type) {{
    case 'FETCH_START':
      return {{ ...state, loading: true, error: null }};
    case 'FETCH_SUCCESS':
      return {{ ...state, loading: false, data: action.payload }};
    case 'FETCH_ERROR':
      return {{ ...state, loading: false, error: action.payload }};
    default:
      return state;
  }}
}}

export function {pascal_name}Provider({{ children }}) {{
  const [state, dispatch] = useReducer({camel_name}Reducer, initialState);

  return (
    <{pascal_name}Context.Provider value={{ state, dispatch }}>
      {{children}}
    </{pascal_name}Context.Provider>
  );
}}

export const use{pascal_name}Context = () => useContext({pascal_name}Context);"""
    
    def _create_types(self, name: str) -> str:
        """Create TypeScript types"""
        
        pascal_name = self._to_pascal_case(name)
        
        return f"""export interface {pascal_name} {{
  id: string;
  name: string;
  description?: string;
  status: 'active' | 'inactive';
  createdAt: Date;
  updatedAt: Date;
  createdBy?: string;
  updatedBy?: string;
}}

export interface {pascal_name}Input {{
  name: string;
  description?: string;
  status?: 'active' | 'inactive';
}}

export interface {pascal_name}Filter {{
  status?: 'active' | 'inactive';
  search?: string;
  limit?: number;
  offset?: number;
}}

export interface {pascal_name}Response {{
  success: boolean;
  data: {pascal_name} | {pascal_name}[];
  message?: string;
  error?: string;
}}"""
    
    def _get_react_templates(self) -> Dict:
        """Get React templates"""
        return {}
    
    def _get_nextjs_templates(self) -> Dict:
        """Get Next.js templates"""
        return {}
    
    def _get_express_templates(self) -> Dict:
        """Get Express templates"""
        return {}
    
    def _get_graphql_templates(self) -> Dict:
        """Get GraphQL templates"""
        return {}
    
    def _to_pascal_case(self, name: str) -> str:
        """Convert to PascalCase"""
        return ''.join(word.capitalize() for word in name.split('_'))
    
    def _to_camel_case(self, name: str) -> str:
        """Convert to camelCase"""
        pascal = self._to_pascal_case(name)
        return pascal[0].lower() + pascal[1:] if pascal else ''
    
    def _to_snake_case(self, name: str) -> str:
        """Convert to snake_case"""
        return name.lower().replace(' ', '_').replace('-', '_')
    
    def write_files(self, feature: Dict, output_dir: str = '.') -> List[str]:
        """Write generated files to disk"""
        
        created_files = []
        base_path = Path(output_dir)
        
        # Create directory structure
        feature_name = feature['name']
        feature_path = base_path / feature_name
        
        # Frontend files
        if feature['frontend']:
            frontend_path = feature_path / 'frontend'
            
            # Component
            if feature['frontend'].get('component'):
                comp_file = frontend_path / 'components' / f"{self._to_pascal_case(feature_name)}.tsx"
                comp_file.parent.mkdir(parents=True, exist_ok=True)
                comp_file.write_text(feature['frontend']['component'])
                created_files.append(str(comp_file))
            
            # Styles
            if feature['frontend'].get('styles'):
                style_file = frontend_path / 'components' / f"{self._to_pascal_case(feature_name)}.module.css"
                style_file.parent.mkdir(parents=True, exist_ok=True)
                style_file.write_text(feature['frontend']['styles'])
                created_files.append(str(style_file))
            
            # Hooks
            if feature['frontend'].get('hooks'):
                hook_file = frontend_path / 'hooks' / f"use{self._to_pascal_case(feature_name)}.ts"
                hook_file.parent.mkdir(parents=True, exist_ok=True)
                hook_file.write_text(feature['frontend']['hooks'])
                created_files.append(str(hook_file))
        
        # Backend files
        if feature['backend']:
            backend_path = feature_path / 'backend'
            
            # Controller
            if feature['backend'].get('controller'):
                ctrl_file = backend_path / 'controllers' / f"{self._to_camel_case(feature_name)}Controller.ts"
                ctrl_file.parent.mkdir(parents=True, exist_ok=True)
                ctrl_file.write_text(feature['backend']['controller'])
                created_files.append(str(ctrl_file))
            
            # Service
            if feature['backend'].get('service'):
                svc_file = backend_path / 'services' / f"{self._to_camel_case(feature_name)}Service.ts"
                svc_file.parent.mkdir(parents=True, exist_ok=True)
                svc_file.write_text(feature['backend']['service'])
                created_files.append(str(svc_file))
            
            # Repository
            if feature['backend'].get('repository'):
                repo_file = backend_path / 'repositories' / f"{self._to_camel_case(feature_name)}Repository.ts"
                repo_file.parent.mkdir(parents=True, exist_ok=True)
                repo_file.write_text(feature['backend']['repository'])
                created_files.append(str(repo_file))
        
        # Database files
        if feature['database']:
            db_path = feature_path / 'database'
            
            # Migration
            if feature['database'].get('migration'):
                mig_file = db_path / 'migrations' / f"001_create_{self._to_snake_case(feature_name)}.sql"
                mig_file.parent.mkdir(parents=True, exist_ok=True)
                mig_file.write_text(feature['database']['migration'])
                created_files.append(str(mig_file))
        
        # Documentation
        if feature['documentation']:
            docs_path = feature_path / 'docs'
            docs_path.mkdir(parents=True, exist_ok=True)
            
            if feature['documentation'].get('readme'):
                readme_file = feature_path / 'README.md'
                readme_file.write_text(feature['documentation']['readme'])
                created_files.append(str(readme_file))
        
        return created_files

def main():
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='Scaffold full-stack features')
    parser.add_argument('feature_name', help='Name of the feature')
    parser.add_argument('--stack', default='react-express', help='Tech stack')
    parser.add_argument('--typescript', action='store_true', help='Use TypeScript')
    parser.add_argument('--graphql', action='store_true', help='Include GraphQL')
    parser.add_argument('--output', default='.', help='Output directory')
    parser.add_argument('--write', action='store_true', help='Write files to disk')
    
    args = parser.parse_args()
    
    scaffolder = FullstackScaffolder()
    
    options = {
        'stack': args.stack,
        'typescript': args.typescript,
        'frontend_framework': 'react',
        'backend_framework': 'express',
        'database': 'postgresql',
        'orm': 'prisma'
    }
    
    if args.graphql:
        options['stack'] += '-graphql'
    
    feature = scaffolder.scaffold_feature(args.feature_name, options)
    
    if args.write:
        files = scaffolder.write_files(feature, args.output)
        print(f"✅ Created {len(files)} files for {args.feature_name} feature")
        for f in files[:10]:  # Show first 10
            print(f"  📁 {f}")
    else:
        # Display summary
        print("=" * 60)
        print(f"FULLSTACK FEATURE: {args.feature_name}")
        print("=" * 60)
        
        print("\n📦 GENERATED STRUCTURE:")
        
        if feature['frontend']:
            print("\nFrontend:")
            for key in feature['frontend']:
                if feature['frontend'][key]:
                    print(f"  ✓ {key}")
        
        if feature['backend']:
            print("\nBackend:")
            for key in feature['backend']:
                if feature['backend'][key]:
                    print(f"  ✓ {key}")
        
        if feature['database']:
            print("\nDatabase:")
            for key in feature['database']:
                if feature['database'][key]:
                    print(f"  ✓ {key}")
        
        print(f"\nTo write files: python {sys.argv[0]} {args.feature_name} --write")

if __name__ == "__main__":
    main()
