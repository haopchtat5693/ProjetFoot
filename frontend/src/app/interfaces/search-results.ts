export type SearchResultKind = 'team' | 'player' | 'coach' | 'stadium' | 'league';
export type SearchScope = 'all' | SearchResultKind;

export interface SearchResult {
  kind: SearchResultKind;
  id: number;
  title: string;
  subtitle: string;
  route: string;
}
